"""Build servisi — DOCX build."""

from __future__ import annotations

from pathlib import Path

from bookmaker.build.pipeline import build_chapter


def build_docx(project_root: str | Path, chapter_id: str,
               source_path: str | None = None) -> dict:
    """Bölümü DOCX olarak build eder."""
    root = Path(project_root).resolve()
    if source_path:
        p = root / source_path
    else:
        base = root / "chapters" / chapter_id / "approved"
        candidates = [base / f"{chapter_id}_v001.md",
                      base / f"{chapter_id}_v002.md", base / "v001.md"]
        p = next((c for c in candidates if c.exists()), None)
    if not p or not p.exists():
        return {"error": f"Kaynak bulunamadi: {chapter_id}"}
    try:
        result = build_chapter(p)
        return {"chapter_id": chapter_id,
                "compiled": result.get("compiled", 0),
                "extracted": result.get("extracted", 0),
                "total": result.get("total_code_blocks", 0)}
    except Exception as e:
        return {"error": f"Build hatasi: {str(e)[:300]}"}
