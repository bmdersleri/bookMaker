"""Observer/review service for Studio."""

from __future__ import annotations

from pathlib import Path

from bookmaker.studio.services import prompt_service


def get_review_prompt(project_root: str | Path) -> dict:
    """Return the default observer prompt."""
    return prompt_service.get_default_prompt(project_root, "review")


def save_review_prompt(project_root: str | Path, content: str) -> dict:
    """Save the default observer prompt."""
    return prompt_service.save_default_prompt(project_root, content, "review")
