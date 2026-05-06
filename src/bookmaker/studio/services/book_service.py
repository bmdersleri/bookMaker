"""Book manifest service for Studio."""

from __future__ import annotations

from pathlib import Path

from bookmaker.chapter.validation_modes import resolve_validation_profile_from_manifest
from bookmaker.manifest.manager import ManifestManager
from bookmaker.manifest.models import BookManifest, ChapterPipelineEntry, ChapterState
from bookmaker.manifest.pipeline import PipelineManager


def load_manifest(project_root: str | Path) -> BookManifest:
    """Load or generate book_manifest.yaml."""
    return ManifestManager(Path(project_root).resolve()).load_or_generate()


def _chapter_states(pipeline_state) -> list[str]:
    chapters = pipeline_state.chapters
    if isinstance(chapters, dict):
        return [
            state.current_step
            for state in chapters.values()
            if isinstance(state, ChapterState)
        ]
    return [
        entry.status.state
        for entry in chapters
        if isinstance(entry, ChapterPipelineEntry)
    ]


def get_project_info(project_root: str | Path) -> dict:
    """Return high-level book and pipeline summary."""
    root = Path(project_root).resolve()
    manifest = ManifestManager(root).load_or_generate()
    pipeline_state = PipelineManager(root).load()

    stages = {"planned": 0, "approved": 0, "full_text_pasted": 0}
    for stage in _chapter_states(pipeline_state):
        if stage in stages:
            stages[stage] += 1

    return {
        "title": manifest.book.title or "(isimsiz)",
        "alias": manifest.book.alias or root.name,
        "chapters": len(manifest.chapters),
        "author": manifest.book.author or "-",
        "profile": resolve_validation_profile_from_manifest(manifest),
        "framework": manifest.style.framework or "",
        "code_language": manifest.style.code_language or "",
        "screenshot_required": manifest.automation.screenshot_required,
        "qr_policy": manifest.automation.qr_policy,
        "stage": pipeline_state.current_stage or pipeline_state.pipeline.global_state,
        "stage_counts": stages,
    }
