"""Prompt file service for Studio."""

from __future__ import annotations

from pathlib import Path


def _root(project_root: str | Path) -> Path:
    return Path(project_root).resolve()


def get_default_prompt(project_root: str | Path, prompt_type: str = "chapter") -> dict:
    """Read prompts/default_chapter.md or prompts/default_review.md."""
    filename = "default_review.md" if prompt_type == "review" else "default_chapter.md"
    path = _root(project_root) / "prompts" / filename
    if not path.exists():
        return {"error": f"Prompt bulunamadi: {filename}"}
    text = path.read_text(encoding="utf-8")
    return {
        "type": prompt_type,
        "path": str(path.relative_to(_root(project_root))),
        "content": text,
    }


def save_default_prompt(
    project_root: str | Path,
    content: str,
    prompt_type: str = "chapter",
) -> dict:
    """Write prompts/default_chapter.md or prompts/default_review.md."""
    filename = "default_review.md" if prompt_type == "review" else "default_chapter.md"
    root = _root(project_root)
    path = root / "prompts" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {"status": "ok", "type": prompt_type, "path": str(path.relative_to(root))}


def get_chapter_prompt(project_root: str | Path, chapter_id: str) -> dict:
    """Read chapters/<alias>/prompt.md."""
    root = _root(project_root)
    path = root / "chapters" / chapter_id / "prompt.md"
    if not path.exists():
        return {"error": f"Prompt bulunamadi: {chapter_id}"}
    return {
        "chapter_id": chapter_id,
        "path": str(path.relative_to(root)),
        "content": path.read_text(encoding="utf-8"),
    }


def save_chapter_prompt(project_root: str | Path, chapter_id: str, content: str) -> dict:
    """Write chapters/<alias>/prompt.md."""
    root = _root(project_root)
    path = root / "chapters" / chapter_id / "prompt.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {"status": "ok", "chapter_id": chapter_id, "path": str(path.relative_to(root))}
