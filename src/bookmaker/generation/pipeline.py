"""2 asamali bolum uretim pipeline'i.
Cift model destegi: Seed (Pro) + Enrich (Flash).

Asama 1 — SEEDING:    LLM (Pro) serbest bolum icerigi uretir
Asama 2 — NORMALIZATION: Python kodu (0 token)
Asama 3 — ENRICHMENT:  LLM (Flash, paralel) eksik bolumleri doldurur
Asama 4 — ASSEMBLY:    Python kodu (0 token)
"""

from __future__ import annotations

import concurrent.futures
import time
from pathlib import Path
from typing import Any, Optional

from bookmaker.authoring.pipeline import AuthoringPipeline
from bookmaker.core.config import load_config
from bookmaker.generation.postprocess import (
    detect_missing_sections,
    extract_sections,
    insert_section,
    normalize,
)
from bookmaker.generation.spec import (
    build_seed_from_spec_prompt,
    build_spec_prompt,
    build_spec_validation_prompt,
    generate_spec,
    validate_spec,
)
from bookmaker.generation.prompts import (
    SYSTEM_AUTHOR,
    build_enrich_bridge_prompt,
    build_enrich_errors_prompt,
    build_enrich_exercises_prompt,
    build_enrich_glossary_prompt,
    build_enrich_questions_prompt,
    build_enrich_summary_prompt,
    build_seed_prompt,
)
from bookmaker.llm.config import LLMConfig
from bookmaker.llm.openai import OpenAICompatibleClient


class ChapterGenerator:
    """2 asamali bolum uretici. Cift model destegi.

    Kullanim:
        gen = ChapterGenerator("book_projects/java-temelleri")
        result = gen.generate_chapter(
            chapter_id="bolum-16",
            title="Dosya Islemleri",
            concepts=["File", "Path", "BufferedReader"],
        )

    Model stratejisi:
        seed_model   -> Pro (DeepSeek V4 Pro)    -> ana icerik
        enrich_model -> Flash (DeepSeek V4 Flash) -> tamamlama
    """

    def __init__(self, project_root: str | Path) -> None:
        self.root = Path(project_root).resolve()
        self.config = load_config(start=self.root)
        self.llm_config = LLMConfig(self.root)
        self.seed_client: Optional[OpenAICompatibleClient] = None
        self.enrich_client: Optional[OpenAICompatibleClient] = None
        self._init_clients()

    def _init_clients(self) -> None:
        if not self.llm_config.is_configured():
            return
        base = {"api_key": self.llm_config.api_key,
                "base_url": self.llm_config.base_url}
        sm = self.llm_config.seed_model or "deepseek-chat"
        self.seed_client = OpenAICompatibleClient(**base, model=sm, timeout=300)
        em = self.llm_config.enrich_model or sm
        self.enrich_client = OpenAICompatibleClient(**base, model=em, timeout=60)

    def is_ready(self) -> bool:
        return bool(self.llm_config.is_configured() and self.seed_client)

    # ----------------------------------------------------------
    # ASAMA 1: SEEDING (Pro model)
    # ----------------------------------------------------------

    def seed(self, chapter_title: str, concepts: list[str],
             outline: Optional[str] = None,
             chapter_no: Optional[int] = None) -> str:
        """LLM Pro ile serbest bolum icerigi uretir."""
        if not self.seed_client:
            raise RuntimeError("LLM API yapilandirilmamis.")
        user_prompt = build_seed_prompt(
            chapter_title=chapter_title, concepts=concepts,
            outline=outline, chapter_no=chapter_no)
        model_name = self.llm_config.seed_model or "varsayilan"
        print(f"  [SEED:{model_name}] {chapter_title}...")
        t0 = time.time()
        raw = self.seed_client.generate_text(SYSTEM_AUTHOR, user_prompt)
        elapsed = time.time() - t0
        print(f"  [SEED] {len(raw.split())} kelime, {elapsed:.1f}s")
        return raw

    # ----------------------------------------------------------
    # ASAMA 2: NORMALIZATION (Python, 0 token)
    # ----------------------------------------------------------

    def normalize_chapter(self, raw_text: str, chapter_id: str,
                          title: str) -> str:
        """Ham LLM ciktisini normalize eder."""
        return normalize(raw_text, chapter_id, title, self.config)

    # ----------------------------------------------------------
    # ASAMA 3: ENRICHMENT (Flash model, paralel)
    # ----------------------------------------------------------

    def detect_missing(self, normalized_text: str) -> list[dict]:
        return detect_missing_sections(normalized_text)

    def enrich(self, normalized_text: str, chapter_title: str,
               enrich_types: Optional[list[str]] = None,
               next_chapter: Optional[str] = None) -> dict[str, str]:
        """Eksik bolumleri LLM Flash ile paralel doldurur."""
        if not self.enrich_client:
            print("  [WARN] Enrich client yok, fallback kullaniliyor.")
            return self._fallback_all(enrich_types, chapter_title)

        missing = self.detect_missing(normalized_text)
        sections = extract_sections(normalized_text)
        headings = [s["heading"] for s in sections
                    if s["heading"] != "__title__"]
        first_lines = normalized_text.splitlines()
        ctx_lines = [l for l in first_lines if not l.startswith("---")]
        context = "\n".join(ctx_lines[:20])

        type_map = {
            "ozet": ("Bolum ozeti", build_enrich_summary_prompt),
            "sozluk": ("Terim sozlugu", build_enrich_glossary_prompt),
            "soru": ("Kendini degerlendirme sorulari",
                     build_enrich_questions_prompt),
            "alistirma": ("Programlama alistirmalari",
                          build_enrich_exercises_prompt),
            "hata": ("Sik yapilan hatalar", build_enrich_errors_prompt),
            "kopru": ("Bir sonraki bolume kopru",
                      build_enrich_bridge_prompt),
        }
        if enrich_types is None:
            enrich_types = list(type_map.keys())

        pending = [m["key"] for m in missing
                   if not m["existing"]
                   and m["key"] in enrich_types
                   and m["key"] in type_map]
        if not pending:
            print("  [ENRICH] Eksik yok, atlaniyor.")
            return {}

        model_name = self.llm_config.enrich_model or "varsayilan"
        print(f"  [ENRICH:{model_name}] {len(pending)} eksik, paralel...")
        enriched, start = {}, time.time()

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(len(pending), 4)
        ) as pool:
            fmap = {}
            for key in pending:
                stitle, builder = type_map[key]
                if key == "kopru":
                    up = builder(chapter_title=chapter_title,
                                 next_chapter=next_chapter,
                                 headings=headings, context=context)
                else:
                    up = builder(chapter_title=chapter_title,
                                 headings=headings, context=context)
                fut = pool.submit(self._call_enrich, up)
                fmap[fut] = key
            for fut in concurrent.futures.as_completed(fmap):
                key = fmap[fut]
                try:
                    c, e = fut.result()
                    enriched[key] = c
                    print(f"    [{key}] {len(c.split())} kel, {e:.1f}s")
                except Exception as ex:
                    print(f"    [{key}] HATA: {ex}")
                    enriched[key] = _fallback_content(key, chapter_title)

        print(f"  [ENRICH] {len(enriched)} bolum, {time.time()-start:.1f}s")
        return enriched

    def _call_enrich(self, user_prompt: str) -> tuple[str, float]:
        t0 = time.time()
        c = self.enrich_client.generate_text(SYSTEM_AUTHOR, user_prompt)
        return c.strip(), time.time() - t0

    def _fallback_all(self, enrich_types, chapter_title):
        types = enrich_types or ["ozet", "sozluk", "soru",
                                 "alistirma", "hata", "kopru"]
        return {k: _fallback_content(k, chapter_title) for k in types}

    # ----------------------------------------------------------
    # ASAMA 4: ASSEMBLY (Python, 0 token)
    # ----------------------------------------------------------

    def assemble(self, normalized_text: str, enriched: dict[str, str],
                 chapter_id: str, chapter_title: str) -> str:
        """Tum parcalari birlestirir."""
        text = normalized_text
        end_order = [
            ("alistirma", "Programlama alistirmalari"),
            ("soru", "Kendini degerlendirme sorulari"),
            ("sozluk", "Terim sozlugu"),
            ("ozet", "Bolum ozeti"),
            ("hata", "Sik yapilan hatalar ve yanlis sezgiler"),
        ]
        for key, stitle in reversed(end_order):
            if key in enriched and enriched[key]:
                text = insert_section(text, stitle, enriched[key])
        if "kopru" in enriched and enriched["kopru"]:
            text = insert_section(text, "Bir sonraki bolume kopru",
                                  enriched["kopru"])
        return text

    # ----------------------------------------------------------
    # GENERATE: TUM ASAMALAR
    # ----------------------------------------------------------

    def generate_chapter(
        self, chapter_id: str, title: str, concepts: list[str],
        outline: Optional[str] = None,
        chapter_no: Optional[int] = None,
        enrich_types: Optional[list[str]] = None,
        next_chapter: Optional[str] = None,
        save: bool = True,
    ) -> dict[str, Any]:
        """Bolum uretimini bastan sona calistirir."""
        if not self.is_ready():
            raise RuntimeError("LLM API yapilandirilmamis.")

        result = {
            "chapter_id": chapter_id, "title": title,
            "model_seed": self.llm_config.seed_model or "varsayilan",
            "model_enrich": self.llm_config.enrich_model or "varsayilan",
            "timings": {},
        }

        # Asama 1: Seed
        t0 = time.time()
        raw = self.seed(title, concepts, outline, chapter_no)
        result["seed"] = raw
        result["timings"]["seed"] = round(time.time() - t0, 1)

        # Asama 2: Normalize
        t0 = time.time()
        normalized = self.normalize_chapter(raw, chapter_id, title)
        result["timings"]["normalize"] = round(time.time() - t0, 1)

        # Eksik tespiti
        missing = self.detect_missing(normalized)
        result["missing"] = [m for m in missing if not m["existing"]]

        # Asama 3: Enrich
        t0 = time.time()
        enriched = self.enrich(normalized, title, enrich_types,
                               next_chapter) if result["missing"] else {}
        result["enriched"] = enriched
        result["timings"]["enrich"] = round(time.time() - t0, 1)

        # Asama 4: Assemble + son normalize pasosu
        t0 = time.time()
        final = self.assemble(normalized, enriched, chapter_id, title)
        final = self.normalize_chapter(final, chapter_id, title)
        result["timings"]["assemble"] = round(time.time() - t0, 1)

        if save:
            path = self._save_chapter(chapter_id, final)
            result["path"] = str(path)
            try:
                pipe = AuthoringPipeline(self.root)
                pipe.paste_draft(chapter_id, final)
                pipe.advance(chapter_id, "full_text_pasted")
            except Exception as e:
                print(f"  [WARN] Pipeline kaydi: {e}")

        result["total_time"] = round(sum(result["timings"].values()), 1)
        wc = len(final.split())
        print(f"\n  {chapter_id}: {wc} kel, {result['total_time']}s"
              f"\n  Seed: {result['model_seed']} | Enrich: {result['model_enrich']}"
              f"\n  Eksik: {len(result['missing'])} -> {len(enriched)} dolduruldu")
        return result

    def _save_chapter(self, chapter_id: str, text: str) -> Path:
        d = self.root / "chapters" / chapter_id / "approved"
        d.mkdir(parents=True, exist_ok=True)
        p = d / f"{chapter_id}_v001.md"
        p.write_text(text, encoding="utf-8")
        return p



    # ----------------------------------------------------------
    # GENERATE WITH SPEC (kapsamli, ara dosya kayitli)
    # ----------------------------------------------------------

    def generate_chapter_with_spec(
        self, chapter_id: str, title: str, concepts: list[str],
        chapter_no=None, enrich_types=None, next_chapter=None, save=True,
    ):
        """Spec -> Validate -> Seed -> Normalize -> Enrich -> Assemble.
        Her asamanin ciktisi build/generation/ altina kaydedilir."""
        gen_dir = self.root / "build" / "generation"
        gen_dir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        result = {"chapter_id": chapter_id, "title": title, "steps": {}}

        # --- STEP 0: SPEC ---
        print(f"\n--- ADIM 0: SPEC ---")
        spec = generate_spec(self.seed_client, title, concepts,
                             f"Hedef: {self.config.audience}", chapter_no)
        self._save_gen(gen_dir / "step0_spec.md", spec)
        self._save_gen(gen_dir / "prompt0_spec.txt",
            build_spec_prompt(title, concepts,
                f"Hedef: {self.config.audience}", chapter_no))
        result["spec"] = spec

        # --- STEP 0.5: VALIDATE ---
        print(f"\n--- ADIM 0.5: DOGRULAMA ---")
        validation = validate_spec(self.enrich_client, spec, title)
        self._save_gen(gen_dir / "step0_validation.md", validation["notes"])
        self._save_gen(gen_dir / "prompt0_validation.txt",
            build_spec_validation_prompt(spec, title))
        result["validation"] = validation

        # --- STEP 1: SEED ---
        print(f"\n--- ADIM 1: SEED ---")
        seed_prompt = build_seed_from_spec_prompt(spec, title)
        self._save_gen(gen_dir / "prompt1_seed.txt", seed_prompt)
        seed_start = time.time()
        raw = self.seed_client.generate_text(SYSTEM_AUTHOR, seed_prompt)
        result["seed_time"] = round(time.time() - seed_start, 1)
        self._save_gen(gen_dir / "step1_seed.md", raw)
        print(f"  [SEED] {len(raw.split())} kelime, {result['seed_time']}s")

        # --- STEP 2: NORMALIZE ---
        norm = self.normalize_chapter(raw, chapter_id, title)
        self._save_gen(gen_dir / "step2_normalized.md", norm)

        # --- STEP 3: ENRICH ---
        missing = self.detect_missing(norm)
        enriched = self.enrich(norm, title, enrich_types, next_chapter) if missing else {}
        for k, v in enriched.items():
            self._save_gen(gen_dir / f"prompt3_enrich_{k}.txt",
                f"Enrichment: {k}, Chapter: {title}")
        result["enriched"] = enriched
        result["missing"] = [m for m in missing if not m["existing"]]

        # --- STEP 4: ASSEMBLE + FINAL NORMALIZE ---
        final = self.assemble(norm, enriched, chapter_id, title)
        final = self.normalize_chapter(final, chapter_id, title)
        self._save_gen(gen_dir / "step4_final.md", final)

        if save:
            path = self._save_chapter(chapter_id, final)
            result["path"] = str(path)

        wc = len(final.split())
        tt = round(time.time() - t0, 1)
        print(f"\n  DONE {chapter_id}: {wc} kelime, {tt}s")
        print(f"  Dosyalar: {gen_dir}")
        return result

    def _save_gen(self, path, content):
        """Icerigi generation dizinine kaydet."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(content), encoding="utf-8")
        except Exception:
            pass



def _fallback_content(key: str, chapter_title: str) -> str:
    fb = {
        "ozet": f"Bu bolumde {chapter_title} konusu ele alindi.",
        "sozluk": "**API hatasi** — Sozluk olusturulamadi.",
        "soru": "**API hatasi** — Sorular olusturulamadi.",
        "alistirma": "**API hatasi** — Alistirmalar olusturulamadi.",
        "hata": "**API hatasi** — Hatalar olusturulamadi.",
        "kopru": "Bir sonraki bolumde yeni kavramlar ele alinacak.",
    }
    return fb.get(key, "")

    # ----------------------------------------------------------
    # GENERATE WITH SPEC (kapsamli, ara dosya kayitli)
    # ----------------------------------------------------------


def _fallback_content(key: str, chapter_title: str) -> str:
    fb = {
        "ozet": f"Bu bolumde {chapter_title} konusu ele alindi.",
        "sozluk": "**API hatasi** — Sozluk olusturulamadi.",
        "soru": "**API hatasi** — Sorular olusturulamadi.",
        "alistirma": "**API hatasi** — Alistirmalar olusturulamadi.",
        "hata": "**API hatasi** — Hatalar olusturulamadi.",
        "kopru": "Bir sonraki bolumde yeni kavramlar ele alinacak.",
    }
    return fb.get(key, "")

    # ----------------------------------------------------------
    # GENERATE WITH SPEC (kapsamli, ara dosya kayitli)
    # ----------------------------------------------------------

    def generate_chapter_with_spec(
        self, chapter_id: str, title: str, concepts: list[str],
        chapter_no=None, enrich_types=None, next_chapter=None, save=True,
    ):
        """Spec -> Validate -> Seed -> Normalize -> Enrich -> Assemble.
        Her a�aman�n ��kt�s� build/generation/ alt�na kaydedilir."""
        gen_dir = self.root / "build" / "generation"
        gen_dir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        result = {"chapter_id": chapter_id, "title": title, "steps": {}}

        # --- STEP 0: SPEC ---
        print(f"\\n--- ADIM 0: SPEC ---")
        spec = generate_spec(self.seed_client, title, concepts,
                             f"Hedef: {self.config.audience}", chapter_no)
        self._save(gen_dir / "step0_spec.md", spec)
        self._save(gen_dir / "prompt0_spec.txt",
                   build_spec_prompt(title, concepts, f"Hedef: {self.config.audience}", chapter_no))
        result["spec"] = spec

        # --- STEP 0.5: VALIDATE ---
        print(f"\\n--- ADIM 0.5: DOGRULAMA ---")
        validation = validate_spec(self.enrich_client, spec, title)
        self._save(gen_dir / "step0_validation.md", validation["notes"])
        self._save(gen_dir / "prompt0_validation.txt",
                   build_spec_validation_prompt(spec, title))
        result["validation"] = validation

        # --- STEP 1: SEED ---
        print(f"\\n--- ADIM 1: SEED ---")
        seed_prompt = build_seed_from_spec_prompt(spec, title)
        self._save(gen_dir / "prompt1_seed.txt", seed_prompt)
        seed_start = time.time()
        raw = self.seed_client.generate_text(SYSTEM_AUTHOR, seed_prompt)
        result["seed_time"] = round(time.time() - seed_start, 1)
        self._save(gen_dir / "step1_seed.md", raw)
        print(f"  [SEED] {len(raw.split())} kelime, {result['seed_time']}s")
        result["seed_raw"] = raw

        # --- STEP 2: NORMALIZE ---
        norm = self.normalize_chapter(raw, chapter_id, title)
        self._save(gen_dir / "step2_normalized.md", norm)
        result["normalized"] = norm

        # --- STEP 3: ENRICH ---
        missing = self.detect_missing(norm)
        enriched = self.enrich(norm, title, enrich_types, next_chapter) if missing else {}
        for k, v in enriched.items():
            self._save(gen_dir / f"prompt3_enrich_{k}.txt",
                       f"Enrichment: {k}, Chapter: {title}")
        result["enriched"] = enriched
        result["missing"] = [m for m in missing if not m["existing"]]

        # --- STEP 4: ASSEMBLE ---
        final = self.assemble(norm, enriched, chapter_id, title)
        final = self.normalize_chapter(final, chapter_id, title)
        self._save(gen_dir / "step4_final.md", final)
        result["final"] = final

        if save:
            path = self._save_chapter(chapter_id, final)
            result["path"] = str(path)

        wc = len(final.split())
        tt = round(time.time() - t0, 1)
        self._save(gen_dir / "metrics.json",
                   f'{{"chapter":"{chapter_id}","words":{wc},"time":{tt},'
                   f'"seed_time":{result.get("seed_time",0)},'
                   f'"model":"{self.llm_config.seed_model}"}}')
        print(f"\\n  DONE {chapter_id}: {wc} kelime, {tt}s")
        print(f"  Dosyalar: {gen_dir}")
        return result

    def _save(self, path, content):
        """��eri�i dosyaya kaydet."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(content), encoding="utf-8")
        except Exception:
            pass

