"""Chapter manifest service for Studio."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from bookmaker.manifest.manager import ManifestManager
from bookmaker.manifest.models import (
    ChapterPipelineEntry,
    ChapterState,
    ManifestChapter,
    PipelineState,
)
from bookmaker.manifest.pipeline import PipelineManager

_yaml = YAML()
_yaml.default_flow_style = False


def _chapter_id(ch: ManifestChapter) -> str:
    return ch.chapter_id or ch.alias


def _chapter_alias(ch: ManifestChapter) -> str:
    return ch.alias or ch.chapter_id or ""


def _state_lookup(pipeline_state: PipelineState) -> dict[str, Any]:
    chapters = pipeline_state.chapters
    if isinstance(chapters, dict):
        return chapters
    return {entry.alias: entry for entry in chapters}


def _state_values(
    state: ChapterPipelineEntry | ChapterState | None,
) -> tuple[str, float | int, str, int]:
    if isinstance(state, ChapterPipelineEntry):
        return (
            state.status.state,
            state.status.quality_score or 0,
            "approved" if state.status.final_approved else "unknown",
            len(state.status.issues),
        )
    if isinstance(state, ChapterState):
        return (
            state.current_step,
            state.score or 0,
            state.decision or "unknown",
            getattr(state, "error_count", 0),
        )
    return ("planned", 0, "unknown", 0)


def _content_flags(root: Path, chapter_id: str) -> dict[str, bool]:
    content_dir = root / "chapters" / chapter_id / "content"
    return {
        "draft_exists": (content_dir / "draft.md").exists(),
        "final_exists": (content_dir / "final.md").exists(),
        "prompt_exists": (root / "chapters" / chapter_id / "prompt.md").exists(),
    }


def _dump_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        _yaml.dump(data, handle)


def _write_text_if_missing(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def _ensure_chapter_workspace(root: Path, chapter_id: str, title: str, order: int) -> None:
    chapter_root = root / "chapters" / chapter_id
    content_dir = chapter_root / "content"
    (content_dir / "revisions").mkdir(parents=True, exist_ok=True)
    _write_text_if_missing(chapter_root / "prompt.md", f"# {title}\n\n")
    _write_text_if_missing(content_dir / "draft.md", f"# {title}\n\n> Taslak henuz uretilmedi.\n")
    _write_text_if_missing(content_dir / "final.md", f"# {title}\n\n> Final henuz onaylanmadi.\n")
    manifest_path = chapter_root / "chapter_manifest.yaml"
    if not manifest_path.exists():
        _dump_yaml(
            manifest_path,
            {
                "chapter": {
                    "title": title,
                    "alias": chapter_id,
                    "order": order,
                    "references": [],
                },
                "scope": {"topics": [title], "objectives": [], "exclusions": []},
                "structure": {"sections": []},
                "automation": {"validation_modes": ["review_only"]},
            },
        )


def get_chapter_list(project_root: str | Path) -> list[dict]:
    """Return manifest chapters joined with pipeline state."""
    root = Path(project_root).resolve()
    manifest = ManifestManager(root).load_or_generate()
    states = _state_lookup(PipelineManager(root).load())

    result = []
    for ch in manifest.chapters:
        cid = _chapter_id(ch)
        alias = _chapter_alias(ch)
        state = states.get(cid) or states.get(alias)
        current_step, score, decision, errors = _state_values(state)
        content_flags = _content_flags(root, cid)
        result.append(
            {
                "chapter_id": cid,
                "alias": alias,
                "title": ch.title or f"Bolum {ch.order}",
                "order": ch.order,
                "status": ch.status,
                "current_step": current_step,
                "score": score,
                "decision": decision,
                "errors": errors,
                **content_flags,
            }
        )
    return result


def add_chapter(
    project_root: str | Path,
    chapter_id: str,
    title: str,
    order: int | None = None,
) -> dict:
    """Add a chapter manifest entry and create the project-based workspace."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    if any(
        _chapter_id(ch) == chapter_id or _chapter_alias(ch) == chapter_id
        for ch in manifest.chapters
    ):
        return {"error": f"Bolum zaten var: {chapter_id}"}

    order = order or len(manifest.chapters) + 1
    title = title or chapter_id
    manifest.chapters.append(
        ManifestChapter(
            alias=chapter_id,
            chapter_id=chapter_id,
            title=title,
            order=order,
            status="planned",
            source=f"chapters/{chapter_id}/content/final.md",
        )
    )
    manifest.chapters.sort(key=lambda chapter: chapter.order)
    for index, chapter in enumerate(manifest.chapters, start=1):
        chapter.order = index
    mgr.save(manifest)
    actual_order = next(
        chapter.order
        for chapter in manifest.chapters
        if _chapter_id(chapter) == chapter_id or _chapter_alias(chapter) == chapter_id
    )
    _ensure_chapter_workspace(root, chapter_id, title, actual_order)
    return {
        "chapter_id": chapter_id,
        "alias": chapter_id,
        "title": title,
        "order": actual_order,
    }


def remove_chapter(project_root: str | Path, chapter_id: str) -> dict:
    """Remove a chapter manifest entry. Files are left on disk."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    for index, chapter in enumerate(manifest.chapters):
        if _chapter_id(chapter) == chapter_id or _chapter_alias(chapter) == chapter_id:
            manifest.chapters.pop(index)
            for order, item in enumerate(manifest.chapters, start=1):
                item.order = order
            mgr.save(manifest)
            return {"chapter_id": chapter_id, "deleted": True}
    return {"error": f"Bolum bulunamadi: {chapter_id}"}


def reorder_chapters(project_root: str | Path, chapter_ids: list[str]) -> dict:
    """Reorder chapters by id/alias."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    id_map = {_chapter_id(chapter): chapter for chapter in manifest.chapters}
    id_map.update({_chapter_alias(chapter): chapter for chapter in manifest.chapters})

    new_order = []
    seen: set[int] = set()
    for cid in chapter_ids:
        chapter = id_map.get(cid)
        if chapter is not None and id(chapter) not in seen:
            new_order.append(chapter)
            seen.add(id(chapter))
    for chapter in manifest.chapters:
        if id(chapter) not in seen:
            new_order.append(chapter)
    for order, chapter in enumerate(new_order, start=1):
        chapter.order = order
    manifest.chapters = new_order
    mgr.save(manifest)
    return {"reordered": True, "count": len(new_order)}


def update_chapter(project_root: str | Path, chapter_id: str, data: dict) -> dict:
    """Update chapter manifest fields."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    for chapter in manifest.chapters:
        if _chapter_id(chapter) == chapter_id or _chapter_alias(chapter) == chapter_id:
            if "title" in data:
                chapter.title = data["title"]
            if "order" in data:
                chapter.order = data["order"]
            if "status" in data:
                chapter.status = data["status"]
            mgr.save(manifest)
            return {"chapter_id": _chapter_id(chapter), "updated": True}
    return {"error": f"Bolum bulunamadi: {chapter_id}"}


def get_chapter_info(project_root: str | Path, chapter_id: str) -> dict | None:
    """Return one chapter manifest record."""
    for chapter in get_chapter_list(project_root):
        if chapter["chapter_id"] == chapter_id or chapter["alias"] == chapter_id:
            return chapter
    return None
