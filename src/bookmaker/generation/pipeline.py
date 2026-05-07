"""Bolum uretim pipeline'i.
Tek model (DeepSeek Chat).

Kanonik akış:
SPEC -> VALIDATE -> SEED -> NORMALIZE -> ENRICH -> ASSEMBLE

Üretim çıktıları proje kökündeki ``chapters/<alias>/content`` altında tutulur.
Ara çıktı günlükleri ``logs/production/`` altına yazılır.
"""

from __future__ import annotations

import concurrent.futures
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from bookmaker.authoring.pipeline import AuthoringPipeline
from bookmaker.core.config import load_config
from bookmaker.core.errors import ConfigError
from bookmaker.generation.postprocess import (
    deepen_theory,
    detect_missing_sections,
    extract_h2_sections,
    extract_sections,
    insert_section,
    normalize,
    reassemble_from_sections,
)
from bookmaker.generation.prompts import (
    SYSTEM_AUTHOR,
    build_enrich_bridge_prompt,
    build_enrich_deepen_prompt,
    build_enrich_errors_prompt,
    build_enrich_exercises_prompt,
    build_enrich_glossary_prompt,
    build_enrich_questions_prompt,
    build_enrich_summary_prompt,
    build_seed_prompt,
    build_system_author,
)
from bookmaker.generation.spec import (
    build_seed_from_spec_prompt,
    build_spec_prompt,
    build_spec_validation_prompt,
    generate_spec,
    validate_spec,
)
from bookmaker.llm.config import LLMConfig
from bookmaker.llm.openai import OpenAICompatibleClient


def _fallback_content(key: str, chapter_title: str) -> str:
    """LLM enrichment çalışmadığında güvenli varsayılan içerik üretir."""
    fallback_map = {
        "ozet": (
            f"{chapter_title} bölümünde işlenen temel kavramlar özetlenir. "
            "Bu bölüm, öğrencinin ana fikirleri tekrar etmesine yardımcı olur."
        ),
        "sozluk": (
            "**Temel Kavram** — Bölümde açıklanan ana teknik terim.\n"
            "**Uygulama** — Kavramın çalışan örneklerle gösterilmesi."
        ),
        "soru": (
            "**Soru 1:** Bu bölümün ana amacı nedir?\n"
            "- Cevap: Bölümdeki temel kavramları anlamak ve uygulamaktır."
        ),
        "alistirma": (
            "**Alıştırma 1: Temel Uygulama**\n"
            "- Amaç: Bölüm kavramlarını pekiştirmek.\n"
            "- Görev: Bölümdeki örneği küçük bir değişiklikle yeniden uygulayın.\n"
            "- İpucu: Önce temel akışı çalıştırın, sonra değişkenleri güncelleyin."
        ),
        "hata": (
            "**Yaygın Hata:** Kavramı ezberleyip uygulama bağlamını kaçırmak.\n"
            "- Çözüm: Kodu küçük örneklerle çalıştırarak sonucu gözlemleyin."
        ),
        "kopru": (
            "Bu bölümde öğrenilen kavramlar, bir sonraki bölümde daha kapsamlı "
            "uygulama örnekleri için temel oluşturur."
        ),
    }
    return fallback_map.get(
        key,
        f"{chapter_title} için {key} başlığı altında tamamlayıcı içerik eklenmelidir.",
    )


class ChapterGenerator:
    """Bölüm üreticisi.

    Tek modelli, manifest-tabanlı üretim orkestratörüdür.

    Kanonik akış `generate_chapter_with_spec()` ve Studio pipeline üzerinden
    yürür: `SPEC -> VALIDATE -> SEED -> NORMALIZE -> ENRICH -> ASSEMBLE`.
    Bu 6 adım BookMaker'in referans üretim hattıdır.

    `generate_chapter()` geriye uyumluluk için korunur ve basit/legacy
    4-adımlı akışı izler: `SEED -> NORMALIZE -> ENRICH -> ASSEMBLE`.

    Kullanim:
        gen = ChapterGenerator("book_projects/java-temelleri")
        result = gen.generate_chapter(
            chapter_id="bolum-16",
            title="Dosya Islemleri",
            concepts=["File", "Path", "BufferedReader"],
        )

    Uretim stratejileri:
        generate_chapter()               -> Temel 4-asama (seed/norm/enrich/assemble)
        generate_chapter_with_spec()     -> Spec-gudumlu (+ opsiyonel deepen)
        generate_chapter_with_spec_deep() -> Spec + deepen her zaman
        generate_chapter_sectioned()     -> Parça bazlı, bölüm bölüm üretim
        generate_chapter_two_pass()      -> Iki-gecisli (taslak + deepen)
    """

    def __init__(self, project_root: str | Path) -> None:
        self.root = Path(project_root).resolve()
        try:
            self.config = load_config(start=self.root)
        except ConfigError:
            self.config = None
        self.llm_config = LLMConfig(self.root)
        self.client: OpenAICompatibleClient | None = None
        self._init_clients()

    def _init_clients(self) -> None:
        if not self.llm_config.is_configured():
            return
        base = {"api_key": self.llm_config.api_key,
                "base_url": self.llm_config.base_url,
                "model": self.llm_config.model}
        # API loglarını build/api_logs/ altına kaydet
        api_log_dir = str(self.root / "build")
        self.client = OpenAICompatibleClient(
            **base, timeout=120, api_log_dir=api_log_dir)

    def _production_run_dir(self, chapter_id: str, variant: str | None = None) -> Path:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        suffix = f"_{variant}" if variant else ""
        return self.root / "logs" / "production" / f"{chapter_id}{suffix}_{stamp}"

    @property
    def code_language(self) -> str:
        return self.config.primary_code_language if self.config else "java"

    @property
    def system_prompt(self) -> str:
        lang = self.code_language
        return build_system_author(lang) if lang != "java" else SYSTEM_AUTHOR

    def is_ready(self) -> bool:
        return bool(self.config and self.llm_config.is_configured() and self.client)

    # ----------------------------------------------------------
    # ASAMA 1: SEEDING (Pro model)
    # ----------------------------------------------------------

    def seed(self, chapter_title: str, concepts: list[str],
             outline: str | None = None,
             chapter_no: int | None = None) -> str:
        """LLM ile serbest bolum icerigi uretir."""
        if not self.client:
            raise RuntimeError("LLM API yapilandirilmamis.")
        user_prompt = build_seed_prompt(
            chapter_title=chapter_title, concepts=concepts,
            outline=outline, chapter_no=chapter_no)
        model = self.llm_config.model
        print(f"  [SEED:{model}] {chapter_title}...")
        t0 = time.time()
        raw = self.client.generate_text_with_resume(self.system_prompt, user_prompt)
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
               enrich_types: list[str] | None = None,
               next_chapter: str | None = None,
               concepts: list[str] | None = None,
               save_dir: Path | None = None) -> dict[str, str]:
        """Eksik bolumleri LLM ile paralel doldurur."""
        if not self.client:
            print("  [WARN] Enrich client yok, fallback kullaniliyor.")
            return self._fallback_all(enrich_types, chapter_title)

        missing = self.detect_missing(normalized_text)
        sections = extract_sections(normalized_text)
        headings = [s["heading"] for s in sections
                    if s["heading"] != "__title__"]

        # Tam baglam: ilk 2000 + son 2000 karakter
        clean_text = normalized_text
        if clean_text.startswith("---"):
            idx = clean_text.find("---", 3)
            if idx != -1:
                clean_text = clean_text[idx + 3:]
        head = clean_text[:2000].strip()
        tail = clean_text[-2000:].strip() if len(clean_text) > 4000 else ""
        context = head + ("\n...\n" + tail if tail else "")

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
            "teori_genislet": ("Teorik derinlestirme",
                               build_enrich_deepen_prompt),
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

        model = self.llm_config.model
        print(f"  [ENRICH:{model}] {len(pending)} eksik, paralel...")
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
                                 headings=headings, context=context,
                                 concepts=concepts)
                else:
                    up = builder(chapter_title=chapter_title,
                                 headings=headings, context=context,
                                 concepts=concepts)
                # Gercek prompt'u kaydet
                if save_dir:
                    self._save(save_dir / f"prompt3_enrich_{key}.txt", up)
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
        c = self.client.generate_text(self.system_prompt, user_prompt)
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
        """Tum parcalari birlestirir. Mükerrer başlık kontrolü yapar."""
        text = normalized_text

        # Her enrichment tipi için: (başlık, mükerrerlik kontrol terimleri)
        end_order = [
            ("alistirma", "Programlama alistirmalari",
             ["alıştırma", "alistirma"]),
            ("soru", "Kendini degerlendirme sorulari",
             ["soru", "değerlendirme", "degerlendirme"]),
            ("sozluk", "Terim sozlugu",
             ["sözlük", "sozluk"]),
            ("ozet", "Bolum ozeti",
             ["özet", "ozet"]),
            ("hata", "Sik yapilan hatalar ve yanlis sezgiler",
             ["hata", "yanlış", "yanlis", "yanilgi"]),
        ]
        for key, stitle, terms in reversed(end_order):
            if key in enriched and enriched[key]:
                text = insert_section(text, stitle, enriched[key],
                                     turkish_terms=terms)
        if "kopru" in enriched and enriched["kopru"]:
            text = insert_section(text, "Bir sonraki bolume kopru",
                                  enriched["kopru"],
                                  turkish_terms=["köprü", "kopru"])
        return text

    # ----------------------------------------------------------
    # GENERATE: TUM ASAMALAR
    # ----------------------------------------------------------

    def generate_chapter(
        self, chapter_id: str, title: str, concepts: list[str],
        outline: str | None = None,
        chapter_no: int | None = None,
        enrich_types: list[str] | None = None,
        next_chapter: str | None = None,
        save: bool = True,
    ) -> dict[str, Any]:
        """Bolum uretimini bastan sona calistirir."""
        if not self.is_ready():
            raise RuntimeError("LLM API yapilandirilmamis.")

        result = {
            "chapter_id": chapter_id, "title": title,
            "model": self.llm_config.model,
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
                               next_chapter, concepts=concepts) if result["missing"] else {}
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
              f"\n  Model: {result['model']}"
              f"\n  Eksik: {len(result['missing'])} -> {len(enriched)} dolduruldu")
        return result

    def _save_chapter(self, chapter_id: str, text: str) -> Path:
        content_dir = self.root / "chapters" / chapter_id / "content"
        revisions_dir = content_dir / "revisions"
        content_dir.mkdir(parents=True, exist_ok=True)
        revisions_dir.mkdir(parents=True, exist_ok=True)

        draft_path = content_dir / "draft.md"
        draft_path.write_text(text, encoding="utf-8")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        revision_path = revisions_dir / f"draft_{timestamp}.md"
        revision_path.write_text(text, encoding="utf-8")
        return draft_path



    # ----------------------------------------------------------
    # ORTAK YARDIMCI: spec + validate + seed + normalize
    # ----------------------------------------------------------

    def _spec_seed_normalize(
        self, chapter_id: str, title: str, concepts: list[str],
        chapter_no, gen_dir: Path, result: dict,
    ) -> str:
        """Spec -> Validate -> Seed -> Normalize ortak akisi.

        Tum ara ciktilari gen_dir altina kaydeder, sonuclari result'a yazar.
        Normalize edilmis metni dondurur.
        """
        code_lang = self.code_language

        # STEP 0: SPEC
        print("\n--- ADIM 0: SPEC ---")
        spec = generate_spec(self.client, title, concepts,
                             f"Hedef: {self.config.audience}", chapter_no,
                             code_language=code_lang)
        self._save(gen_dir / "step0_spec.md", spec)
        self._save(gen_dir / "prompt0_spec.txt",
                   build_spec_prompt(title, concepts,
                       f"Hedef: {self.config.audience}", chapter_no,
                       code_language=code_lang))
        result["spec"] = spec

        # STEP 0.5: VALIDATE
        print("\n--- ADIM 0.5: DOGRULAMA ---")
        validation = validate_spec(self.client, spec, title,
                                   code_language=code_lang)
        self._save(gen_dir / "step0_validation.md", validation["notes"])
        self._save(gen_dir / "prompt0_validation.txt",
                   build_spec_validation_prompt(spec, title,
                                               code_language=code_lang))
        result["validation"] = validation

        # STEP 1: SEED
        print("\n--- ADIM 1: SEED ---")
        seed_prompt = build_seed_from_spec_prompt(spec, title,
                                                  code_language=code_lang)
        self._save(gen_dir / "prompt1_seed.txt", seed_prompt)
        seed_start = time.time()
        raw = self.client.generate_text_with_resume(
            self.system_prompt, seed_prompt,
            output_path=str(gen_dir / "step1_seed_stream.md"))
        result["seed_time"] = round(time.time() - seed_start, 1)
        self._save(gen_dir / "step1_seed.md", raw)
        print(f"  [SEED] {len(raw.split())} kelime, {result['seed_time']}s")

        # STEP 2: NORMALIZE
        norm = self.normalize_chapter(raw, chapter_id, title)
        self._save(gen_dir / "step2_normalized.md", norm)
        return norm

    # ----------------------------------------------------------
    # GENERATE WITH SPEC (kapsamli, ara dosya kayitli)
    # ----------------------------------------------------------

    def generate_chapter_with_spec(
        self, chapter_id: str, title: str, concepts: list[str],
        chapter_no=None, enrich_types=None, next_chapter=None, save=True,
        include_deepen: bool = False,
    ):
        """Spec -> Validate -> Seed -> Normalize -> [Deepen] -> Enrich -> Assemble.

        Her asamanin ciktisi logs/production/ altina kaydedilir.
        """
        gen_dir = self._production_run_dir(chapter_id)
        gen_dir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        result = {"chapter_id": chapter_id, "title": title, "steps": {}}

        norm = self._spec_seed_normalize(
            chapter_id, title, concepts, chapter_no, gen_dir, result)

        # STEP 2.5: DEEPEN (istege bagli)
        if include_deepen:
            deepen_start = time.time()
            norm = self._deepen_sections(norm, title, gen_dir)
            norm = self.normalize_chapter(norm, chapter_id, title)
            result["deepen_time"] = round(time.time() - deepen_start, 1)

        # STEP 3: ENRICH
        missing = self.detect_missing(norm)
        enriched = self.enrich(norm, title, enrich_types, next_chapter,
                               concepts=concepts, save_dir=gen_dir) if missing else {}
        for k, v in enriched.items():
            self._save(gen_dir / f"step3_enrich_{k}.md", v)
        result["enriched"] = enriched
        result["missing"] = [m for m in missing if not m["existing"]]

        # STEP 4: ASSEMBLE + FINAL NORMALIZE
        final = self.assemble(norm, enriched, chapter_id, title)
        final = self.normalize_chapter(final, chapter_id, title)
        self._save(gen_dir / "step4_final.md", final)

        if save:
            result["path"] = str(self._save_chapter(chapter_id, final))

        wc = len(final.split())
        tt = round(time.time() - t0, 1)
        self._save(gen_dir / "metrics.json",
                   f'{{"chapter":"{chapter_id}","words":{wc},"time":{tt},'
                   f'"seed_time":{result.get("seed_time",0)},'
                   f'"deepen_time":{result.get("deepen_time",0)},'
                   f'"model":"{self.llm_config.model}"}}')
        print(f"\n  DONE {chapter_id}: {wc} kelime, {tt}s"
              f"\n  Dosyalar: {gen_dir}")
        return result

    def generate_chapter_sectioned(
        self, chapter_id: str, title: str, concepts: list[str],
        chapter_no=None, save=True,
    ) -> dict:
        """Parça bazlı bölüm üretimi — her alt bölüm ayrı API çağrısı.

        Strateji:
        1. Önce spec üretilir (hangi bölümler olacak?)
        2. Spec'teki her ana başlık ayrı ayrı üretilir
        3. Parçalar birleştirilir
        4. Eksik enrichment'ler doldurulur

        Avantajları:
        - Tek bir 50KB+ yanıt beklemek yerine 5-6 küçük yanıt
        - Bir parça başarısız olursa sadece o parça tekrar üretilir
        - Kalite kontrolü parça bazında yapılabilir
        - max_tokens limiti sorunu yok
        """
        gen_dir = self._production_run_dir(chapter_id, "sections")
        gen_dir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        result = {"chapter_id": chapter_id, "title": title, "sections": {}}
        code_lang = self.config.primary_code_language

        # --- STEP 0: SPEC ---
        print("\n--- ADIM 0: SPEC (Parçali) ---")
        spec = generate_spec(self.client, title, concepts,
                             f"Hedef: {self.config.audience}", chapter_no,
                             code_language=code_lang)
        self._save(gen_dir / "step0_spec.md", spec)
        result["spec"] = spec

        # --- STEP 0.5: SPEC'ten bölüm başlıklarını çıkar ---
        import re
        # Spec'teki numaralı başlıkları bul: "1. KAVRAMLAR", "2. KOD ÖRNEKLERİ" vb.
        section_pattern = re.compile(
            r'^\d+\.\s+\*?\*?(.+?)\*?\*?\s*$', re.MULTILINE
        )
        raw_sections = section_pattern.findall(spec)
        # Temizle ve ilk 8 başlığı al (çok fazla olmasın)
        sections = []
        seen = set()
        for s in raw_sections:
            s_clean = s.strip().rstrip(':')
            if s_clean and s_clean.lower() not in seen:
                seen.add(s_clean.lower())
                sections.append(s_clean)
                if len(sections) >= 8:
                    break

        if len(sections) < 2:
            print("  [SECTIONED] Yetersiz bölüm başlığı, normal moda geçiliyor...")
            return self.generate_chapter_with_spec(
                chapter_id, title, concepts, chapter_no, save=save)

        print(f"  [SECTIONED] {len(sections)} parça: {', '.join(sections[:5])}...")

        # --- STEP 1: Her parçayı ayrı üret ---
        all_parts = []
        for i, section_title in enumerate(sections):
            part_id = f"part_{i+1:02d}"
            print(f"\n--- ADIM 1.{i+1}: {part_id} — {section_title} ---")

            # Bu parça için özel prompt (teorik derinlik optimizasyonlu)
            section_prompt = (
                f"## Bölüm: {title}\n"
                f"## Alt Bölüm: {section_title}\n\n"
                f"**Tam spesifikasyon (bağlam için):**\n{spec[:2000]}\n\n"
                f"---\n"
                f"Yalnızca '{section_title}' alt bölümünü üret.\n\n"
                f"İÇERİK DERİNLİĞİ KURALLARI:\n"
                f"- Her kavramı en az 3-5 paragraf ile derinlemesine açıkla\n"
                f"- NEDEN var? → NE işe yarar? → NASIL kullanılır? → "
                f"NE ZAMAN tercih edilir? yapısını kullan\n"
                f"- Günlük hayattan en az 1 analoji ile somutlaştır\n"
                f"- Benzer kavramlarla karşılaştırma yap\n"
                f"- Kod örneklerinden sonra satır satır açıklama ekle\n\n"
                f"YAZIM KURALLARI:\n"
                f"- H2 = '{section_title}' başlığıyla başla\n"
                f"- Gerekli kod örneklerini ```{code_lang} bloklarında ver\n"
                f"- Gerekli diyagramları ```mermaid bloklarında ver\n"
                f"- Sadece bu alt bölümün içeriğini üret, diğer bölümlere girme\n"
                f"- Sadece içeriğe odaklan, meta etiketi ekleme"
            )

            t_part = time.time()
            try:
                part_text = self.client.generate_text_with_resume(
                    self.system_prompt, section_prompt, max_tokens=8192
                )
                elapsed = time.time() - t_part
                wc = len(part_text.split())
                print(f"  [PART {part_id}] {wc} kelime, {elapsed:.1f}s")

                self._save(gen_dir / f"{part_id}_{section_title[:30]}.md", part_text)
                all_parts.append(part_text)
                result["sections"][part_id] = {
                    "title": section_title,
                    "words": wc,
                    "time": round(elapsed, 1),
                }
            except Exception as e:
                print(f"  [PART {part_id}] HATA: {e}")
                result["sections"][part_id] = {"title": section_title, "error": str(e)}

        # --- STEP 2: Parçaları birleştir ---
        print("\n--- ADIM 2: BIRLESTIRME ---")
        combined = f"# {title}\n\n"
        for i, part in enumerate(all_parts):
            # İlk parçada H1 başlığı var, sonrakilerde yoksa ekle
            if i > 0 and not part.strip().startswith("##"):
                combined += f"\n## {sections[i]}\n\n"
            combined += part + "\n\n"

        self._save(gen_dir / "combined_raw.md", combined)

        # --- STEP 3: Normalize ---
        print("\n--- ADIM 3: NORMALIZASYON ---")
        normalized = self.normalize_chapter(combined, chapter_id, title)
        self._save(gen_dir / "combined_normalized.md", normalized)

        # --- STEP 4: ENRICH ---
        print("\n--- ADIM 4: ENRICHMENT ---")
        missing = self.detect_missing(normalized)
        enriched = self.enrich(normalized, title, concepts=concepts) if missing else {}
        for k, v in enriched.items():
            self._save(gen_dir / f"enrich_{k}.md", v)
        result["enriched"] = enriched
        result["missing"] = [m for m in missing if not m["existing"]]

        # --- STEP 5: ASSEMBLE ---
        final = self.assemble(normalized, enriched, chapter_id, title)
        final = self.normalize_chapter(final, chapter_id, title)
        self._save(gen_dir / "final.md", final)
        result["final"] = final

        if save:
            path = self._save_chapter(chapter_id, final)
            result["path"] = str(path)

        wc = len(final.split())
        tt = round(time.time() - t0, 1)
        self._save(gen_dir / "metrics.json",
                   f'{{"chapter":"{chapter_id}","words":{wc},"time":{tt},'
                   f'"sections":{len(all_parts)},'
                   f'"model":"{self.llm_config.model}"}}')
        print(f"\n  DONE {chapter_id}: {wc} kelime, {tt}s ({len(all_parts)} parca)")
        print(f"  Dosyalar: {gen_dir}")
        return result

    def _save(self, path, content):
        """Icerigi dosyaya kaydet. Hata durumunda uyari verir."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(content), encoding="utf-8")
        except Exception as e:
            print(f"  [WARN] [SAVE ERROR] {path}: {e}", flush=True)

    # ----------------------------------------------------------
    # DERINLESTIRME (DEEPEN) PASS — Cozum B
    # ----------------------------------------------------------

    def _call_deepen(
        self, chapter_title: str, section_heading: str, section_content: str
    ) -> str:
        """Tek bir H2 bölümü için derinleştirme LLM çağrısı yapar."""
        prompt = build_enrich_deepen_prompt(
            chapter_title=chapter_title,
            section_heading=section_heading,
            section_content=section_content,
        )
        # Bölüm zaten uzunsa daha fazla token iste
        est_tokens = min(8192, max(4096, len(section_content) // 2))
        return self.client.generate_text_with_resume(
            self.system_prompt, prompt, max_tokens=est_tokens
        )

    def _deepen_sections(
        self, text: str, chapter_title: str, gen_dir
    ) -> str:
        """Normalize edilmiş bölümü H2 bazında teorik olarak derinleştirir.

        Her H2 bölümünü ayrı LLM çağrısıyla genişletir,
        kod bloklarını korur, sadece açıklamaları derinleştirir.
        """
        print("\n--- ADIM 3.5: TEORIK DERINLESTIRME ---")
        t0 = time.time()

        sections = extract_h2_sections(text)
        print(f"  [DEEPEN] {len(sections)} H2 bolumu bulundu")

        deepened = deepen_theory(
            sections=sections,
            deepen_fn=self._call_deepen,
            chapter_title=chapter_title,
            min_chars=300,
        )

        result = reassemble_from_sections(deepened)
        elapsed = time.time() - t0
        old_wc = len(text.split())
        new_wc = len(result.split())
        growth = round((new_wc - old_wc) / max(1, old_wc) * 100)
        print(f"  [DEEPEN] {old_wc} → {new_wc} kelime (+%{growth}), {elapsed:.1f}s")

        self._save(gen_dir / "step3_5_deepened.md", result)
        return result

    # ----------------------------------------------------------
    # IKI-GECISLI URETIM (TWO-PASS) — Cozum D
    # ----------------------------------------------------------

    def generate_chapter_two_pass(
        self, chapter_id: str, title: str, concepts: list[str],
        chapter_no=None, enrich_types=None, next_chapter=None, save=True,
    ) -> dict:
        """İki geçişli bölüm üretimi: önce hızlı taslak, sonra bölüm bölüm genişlet.

        Strateji:
        1. Geçiş: Hızlı taslak (düşük max_tokens, tüm bölüm tek seferde)
        2. Geçiş: Her H2 bölümü deepen pass ile genişletilir
        3. Normal enrichment'ler (özet, sözlük, soru vs.) eklenir

        Bu yöntem en yüksek kaliteyi üretir, ancak en çok token harcar.
        """
        gen_dir = self._production_run_dir(chapter_id, "twopass")
        gen_dir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        result = {"chapter_id": chapter_id, "title": title, "mode": "two_pass"}
        code_lang = self.config.primary_code_language

        # --- GECIS 1: HIZLI TASLAK ---
        print("\n=== GECIS 1: HIZLI TASLAK ===")
        # Spec ile outline al
        spec = generate_spec(self.client, title, concepts,
                             f"Hedef: {self.config.audience}", chapter_no,
                             code_language=code_lang)
        self._save(gen_dir / "pass1_spec.md", spec)

        seed_prompt = build_seed_from_spec_prompt(spec, title,
                                                  code_language=code_lang)
        self._save(gen_dir / "pass1_prompt.txt", seed_prompt)

        t_draft = time.time()
        # İlk geçiş: hızlı, kısa taslak
        draft = self.client.generate_text_with_resume(
            self.system_prompt, seed_prompt,
            max_tokens=4096,  # Kısa taslak için düşük limit
            output_path=str(gen_dir / "pass1_draft_stream.md"),
        )
        result["draft_time"] = round(time.time() - t_draft, 1)
        wc_draft = len(draft.split())
        print(f"  [TASLAK] {wc_draft} kelime, {result['draft_time']}s")
        self._save(gen_dir / "pass1_draft.md", draft)

        # --- GECIS 2: DERINLESTIR ---
        print("\n=== GECIS 2: BOLUM BOLUM GENISLET ===")
        # Önce normalize et
        normalized = self.normalize_chapter(draft, chapter_id, title)
        self._save(gen_dir / "pass2_before_deepen.md", normalized)

        # Derinleştir
        t_deepen = time.time()
        deepened = self._deepen_sections(normalized, title, gen_dir)
        result["deepen_time"] = round(time.time() - t_deepen, 1)

        # Tekrar normalize et (heading'ler bozulmuş olabilir)
        deepened = self.normalize_chapter(deepened, chapter_id, title)
        self._save(gen_dir / "pass2_deepened.md", deepened)

        # --- ENRICHMENT ---
        print("\n--- ENRICHMENT ---")
        missing = self.detect_missing(deepened)
        enriched = {}
        if missing:
            enriched = self.enrich(deepened, title, enrich_types, next_chapter,
                                   concepts=concepts)
            for k, v in enriched.items():
                self._save(gen_dir / f"enrich_{k}.md", v)
        result["enriched"] = enriched
        result["missing"] = [m for m in missing if not m["existing"]]

        # --- ASSEMBLE ---
        final = self.assemble(deepened, enriched, chapter_id, title)
        final = self.normalize_chapter(final, chapter_id, title)
        self._save(gen_dir / "final.md", final)
        result["final"] = final

        if save:
            path = self._save_chapter(chapter_id, final)
            result["path"] = str(path)

        wc_final = len(final.split())
        tt = round(time.time() - t0, 1)
        self._save(gen_dir / "metrics.json",
                   f'{{"chapter":"{chapter_id}","mode":"two_pass",'
                   f'"draft_words":{wc_draft},"final_words":{wc_final},'
                   f'"draft_time":{result.get("draft_time",0)},'
                   f'"deepen_time":{result.get("deepen_time",0)},'
                   f'"total_time":{tt},'
                   f'"model":"{self.llm_config.model}"}}')
        print(f"\n  DONE {chapter_id}: {wc_draft} → {wc_final} kelime, {tt}s")
        print(f"  Dosyalar: {gen_dir}")
        return result

    # ----------------------------------------------------------
    # SPEC + DEEPEN (tek adimda tam pipeline) — Cozum B+D
    # ----------------------------------------------------------

    def generate_chapter_with_spec_deep(
        self, chapter_id: str, title: str, concepts: list[str],
        chapter_no=None, enrich_types=None, next_chapter=None, save=True,
    ) -> dict:
        """Spec -> Validate -> Seed -> Normalize -> Deepen -> Enrich -> Assemble.

        Standart spec pipeline'ina deepen pass eklenmis hali.
        """
        gen_dir = self._production_run_dir(chapter_id, "deep")
        gen_dir.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        result = {"chapter_id": chapter_id, "title": title, "mode": "spec_deep"}

        norm = self._spec_seed_normalize(
            chapter_id, title, concepts, chapter_no, gen_dir, result)

        # STEP 3: DEEPEN
        deepened = self._deepen_sections(norm, title, gen_dir)
        deepened = self.normalize_chapter(deepened, chapter_id, title)

        # STEP 4: ENRICH
        missing = self.detect_missing(deepened)
        enriched = self.enrich(deepened, title, enrich_types, next_chapter,
                               concepts=concepts) if missing else {}
        for k, v in enriched.items():
            self._save(gen_dir / f"step4_enrich_{k}.md", v)
        result["enriched"] = enriched
        result["missing"] = [m for m in missing if not m["existing"]]

        # STEP 5: ASSEMBLE
        final = self.assemble(deepened, enriched, chapter_id, title)
        final = self.normalize_chapter(final, chapter_id, title)
        self._save(gen_dir / "step5_final.md", final)
        result["final"] = final

        if save:
            result["path"] = str(self._save_chapter(chapter_id, final))

        wc = len(final.split())
        tt = round(time.time() - t0, 1)
        self._save(gen_dir / "metrics.json",
                   f'{{"chapter":"{chapter_id}","mode":"spec_deep",'
                   f'"words":{wc},"total_time":{tt},'
                   f'"model":"{self.llm_config.model}"}}')
        print(f"\n  DONE {chapter_id} (deep): {wc} kelime, {tt}s"
              f"\n  Dosyalar: {gen_dir}")
        return result


class GenerationPipeline(ChapterGenerator):
    """Legacy class name kept for older tests and integrations."""

    def generate_outline(self, *_args: Any, **_kwargs: Any) -> str:
        if not self.is_ready():
            raise RuntimeError("LLM API is not configured.")
        raise NotImplementedError(
            "generate_outline legacy API is no longer part of the project pipeline."
        )
