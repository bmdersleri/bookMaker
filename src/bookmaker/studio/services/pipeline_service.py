"""Pipeline servisi — LLM pipeline başlatma, WebSocket progress."""

from __future__ import annotations

import time
from pathlib import Path

from bookmaker.generation.pipeline import ChapterGenerator
from bookmaker.llm.config import LLMConfig


def get_generator(project_root: str | Path) -> ChapterGenerator | None:
    """ChapterGenerator oluşturur (LLM yoksa None)."""
    cfg = LLMConfig(Path(project_root).resolve())
    if not cfg.is_configured():
        return None
    gen = ChapterGenerator(Path(project_root).resolve())
    return gen if gen.is_ready() else None


def run_generation(project_root: str | Path, chapter_id: str,
                   title: str, concepts: list[str] | None = None,
                   enrich_types: list[str] | None = None,
                   chapter_no: int | None = None) -> dict:
    """Pipeline senkron çalıştırır (REST)."""
    gen = get_generator(project_root)
    if not gen:
        return {"error": "LLM yapılandırılmamış"}

    t0 = time.time()
    try:
        result = gen.generate_chapter_with_spec(
            chapter_id=chapter_id, title=title,
            concepts=concepts or [f"{title} ana kavramları"],
            chapter_no=chapter_no,
            enrich_types=enrich_types or [
                "ozet", "sozluk", "soru", "alistirma", "hata", "kopru"],
        )
        elapsed = time.time() - t0
        gen_dir = Path(project_root).resolve() / "build" / "generation"
        final_path = gen_dir / "step4_final.md"
        resp = {"chapter_id": chapter_id, "title": title,
                "elapsed_s": round(elapsed, 1),
                "spec_words": len(result.get("spec", "").split()),
                "seed_words": len(result.get("seed", "").split()),
                "enriched_count": len(result.get("enriched", {})),
                "final_words": 0, "path": None}
        if final_path.exists():
            final_text = final_path.read_text(encoding="utf-8")
            resp["final_words"] = len(final_text.split())
            resp["path"] = str(final_path.relative_to(Path(project_root).resolve()))
        return resp
    except RuntimeError as e:
        return {"error": f"Pipeline hatasi: {str(e)[:300]}"}


def get_chapter_info(project_root: str | Path, chapter_id: str) -> dict | None:
    """Manifest'ten bölüm bilgisini döndürür."""
    from bookmaker.manifest.manager import ManifestManager
    mgr = ManifestManager(Path(project_root).resolve())
    manifest = mgr.load_or_generate()
    for ch in manifest.chapters:
        if ch.chapter_id == chapter_id:
            return {"chapter_id": ch.chapter_id, "title": ch.title,
                    "order": ch.order, "status": ch.status}
    return None
