"""Pipeline state service for Studio."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from bookmaker.generation.pipeline import ChapterGenerator
from bookmaker.manifest.models import ChapterPipelineEntry, ChapterState
from bookmaker.manifest.pipeline import PipelineManager
from bookmaker.studio.services import chapter_service, generation_service


def _chapter_state_dict(
    state: ChapterPipelineEntry | ChapterState | None,
) -> dict:
    if isinstance(state, ChapterPipelineEntry):
        return {
            "current_step": state.status.state,
            "score": state.status.quality_score or 0,
            "decision": "approved" if state.status.final_approved else "unknown",
            "error_count": len(state.status.issues),
            "warning_count": 0,
        }
    if isinstance(state, ChapterState):
        return {
            "current_step": state.current_step,
            "score": state.score,
            "decision": state.decision,
            "error_count": getattr(state, "error_count", 0),
            "warning_count": getattr(state, "warning_count", 0),
        }
    return {
        "current_step": "planned",
        "score": 0,
        "decision": "unknown",
        "error_count": 0,
        "warning_count": 0,
    }


def get_pipeline_state(project_root: str | Path) -> dict:
    """Return pipeline_state.yaml as the Studio API shape."""
    state = PipelineManager(Path(project_root).resolve()).load()
    chapters = state.chapters
    if isinstance(chapters, dict):
        chapter_data = {
            chapter_id: _chapter_state_dict(chapter_state)
            for chapter_id, chapter_state in chapters.items()
        }
    else:
        chapter_data = {entry.alias: _chapter_state_dict(entry) for entry in chapters}
    return {
        "pipeline_id": getattr(state, "pipeline_id", state.pipeline.book_alias),
        "current_stage": state.current_stage or state.pipeline.global_state,
        "chapters": chapter_data,
    }


def update_chapter_state(project_root: str | Path, chapter_id: str, **kwargs: Any) -> dict:
    """Update one chapter state using the manifest pipeline manager."""
    manager = PipelineManager(Path(project_root).resolve())
    state = manager.update_chapter(chapter_id, **kwargs)
    return {"chapter_id": chapter_id, **_chapter_state_dict(state)}


def get_generator(
    project_root: str | Path,
) -> ChapterGenerator | None:
    """Compatibility wrapper for generation_service.get_generator."""
    return generation_service.get_generator(project_root)


def run_generation(
    project_root: str | Path,
    chapter_id: str,
    title: str,
    concepts: list[str] | None = None,
    enrich_types: list[str] | None = None,
    chapter_no: int | None = None,
) -> dict:
    """Compatibility wrapper for generation_service.run_generation."""
    return generation_service.run_generation(
        project_root,
        chapter_id,
        title,
        concepts=concepts,
        enrich_types=enrich_types,
        chapter_no=chapter_no,
    )


def get_chapter_info(project_root: str | Path, chapter_id: str) -> dict | None:
    """Compatibility wrapper for chapter_service.get_chapter_info."""
    return chapter_service.get_chapter_info(project_root, chapter_id)
