"""Shared chapter source resolution for export/readiness flows."""

from __future__ import annotations

from pathlib import Path


def chapter_alias(chapter) -> str:
    return chapter.chapter_id or chapter.alias or ""


def chapter_matches(chapter, chapter_id: str) -> bool:
    return chapter_id in {chapter.chapter_id, chapter.alias}


def default_chapter_source(chapter) -> str:
    alias = chapter_alias(chapter)
    return chapter.source or f"chapters/{alias}/content/final.md"


def _classify_path_kind(path: Path) -> str:
    normalized_parts = [part.lower() for part in path.parts]
    name = path.name.lower()
    if name == "final.md":
        return "final"
    if name == "draft.md":
        return "draft"
    if "approved" in normalized_parts:
        return "legacy"
    return "manifest"


def chapter_source_candidates(root: Path, chapter) -> list[tuple[Path, str]]:
    """Return candidate source paths in precedence order."""
    alias = chapter_alias(chapter)
    candidates: list[tuple[Path, str]] = []
    seen: set[Path] = set()

    def add(path: Path, kind: str) -> None:
        resolved = path.resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        candidates.append((resolved, kind))

    if chapter.source:
        manifest_path = root / chapter.source
        add(manifest_path, _classify_path_kind(manifest_path))

    base = root / "chapters" / alias
    add(base / "content" / "final.md", "final")
    add(base / "content" / "draft.md", "draft")
    add(base / "approved" / f"{alias}_v001.md", "legacy")
    add(base / "approved" / f"{alias}_v002.md", "legacy")
    add(base / "approved" / "v001.md", "legacy")
    return candidates


def resolve_chapter_source(root: Path, chapter) -> dict | None:
    """Resolve first readable source path for a chapter."""
    for candidate, kind in chapter_source_candidates(root, chapter):
        if candidate.exists():
            return {
                "path": candidate,
                "source": str(candidate.relative_to(root)),
                "source_kind": kind,
            }
    return None

