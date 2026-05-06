"""Compatibility facade for Studio manifest services."""

from __future__ import annotations

from pathlib import Path

from bookmaker.studio.services import book_service, chapter_service, pipeline_service


def load_manifest(project_root: str | Path) -> dict:
    """Compatibility wrapper for book_service.load_manifest."""
    return book_service.load_manifest(project_root)


def get_pipeline_state(project_root: str | Path) -> dict:
    """Compatibility wrapper for pipeline_service.get_pipeline_state."""
    return pipeline_service.get_pipeline_state(project_root)


def get_project_info(project_root: str | Path) -> dict:
    """Compatibility wrapper for book_service.get_project_info."""
    return book_service.get_project_info(project_root)


def get_chapter_list(project_root: str | Path) -> list[dict]:
    """Compatibility wrapper for chapter_service.get_chapter_list."""
    return chapter_service.get_chapter_list(project_root)


def add_chapter(
    project_root: str | Path,
    chapter_id: str,
    title: str,
    order: int | None = None,
) -> dict:
    """Compatibility wrapper for chapter_service.add_chapter."""
    return chapter_service.add_chapter(project_root, chapter_id, title, order)


def remove_chapter(project_root: str | Path, chapter_id: str) -> dict:
    """Compatibility wrapper for chapter_service.remove_chapter."""
    return chapter_service.remove_chapter(project_root, chapter_id)


def reorder_chapters(project_root: str | Path, chapter_ids: list[str]) -> dict:
    """Compatibility wrapper for chapter_service.reorder_chapters."""
    return chapter_service.reorder_chapters(project_root, chapter_ids)


def update_chapter(project_root: str | Path, chapter_id: str, data: dict) -> dict:
    """Compatibility wrapper for chapter_service.update_chapter."""
    return chapter_service.update_chapter(project_root, chapter_id, data)
