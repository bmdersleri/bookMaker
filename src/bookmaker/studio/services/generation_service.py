"""Generation service for Studio."""

from __future__ import annotations

import time
from pathlib import Path

from bookmaker.generation.pipeline import ChapterGenerator
from bookmaker.llm.config import LLMConfig


def get_generator(project_root: str | Path) -> ChapterGenerator | None:
    """Create a ChapterGenerator when LLM is configured."""
    root = Path(project_root).resolve()
    cfg = LLMConfig(root)
    if not cfg.is_configured():
        return None
    generator = ChapterGenerator(root)
    return generator if generator.is_ready() else None


def run_generation(
    project_root: str | Path,
    chapter_id: str,
    title: str,
    concepts: list[str] | None = None,
    enrich_types: list[str] | None = None,
    chapter_no: int | None = None,
) -> dict:
    """Run the synchronous generation pipeline."""
    generator = get_generator(project_root)
    if not generator:
        return {"error": "LLM yapilandirilmamis"}

    root = Path(project_root).resolve()
    started = time.time()
    try:
        result = generator.generate_chapter_with_spec(
            chapter_id=chapter_id,
            title=title,
            concepts=concepts or [f"{title} ana kavramlari"],
            chapter_no=chapter_no,
            enrich_types=enrich_types or ["ozet", "sozluk", "soru", "alistirma", "hata", "kopru"],
        )
        final_path = root / "build" / "generation" / "step4_final.md"
        response = {
            "chapter_id": chapter_id,
            "title": title,
            "elapsed_s": round(time.time() - started, 1),
            "spec_words": len(result.get("spec", "").split()),
            "seed_words": len(result.get("seed", "").split()),
            "enriched_count": len(result.get("enriched", {})),
            "final_words": 0,
            "path": None,
        }
        if final_path.exists():
            final_text = final_path.read_text(encoding="utf-8")
            response["final_words"] = len(final_text.split())
            response["path"] = str(final_path.relative_to(root))
        return response
    except RuntimeError as exc:
        return {"error": f"Pipeline hatasi: {str(exc)[:300]}"}
