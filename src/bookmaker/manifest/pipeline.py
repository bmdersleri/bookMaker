"""Pipeline durum yönetimi."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from bookmaker.manifest.models import ChapterState, PipelineState


class PipelineManager:
    """Pipeline durum dosyasini yoneten sinif."""

    def __init__(self, project_root: Path) -> None:
        self.root = project_root.resolve()

    def state_path(self) -> Path:
        """Pipeline durum dosyasinin yolunu dondurur."""
        return self.root / "pipeline_state.yaml"

    def exists(self) -> bool:
        """Pipeline durum dosyasi var mi kontrol eder."""
        return self.state_path().exists()

    def load(self) -> PipelineState:
        """Pipeline durumunu dosyadan yukler, yoksa varsayilan doner."""
        if not self.exists():
            return PipelineState()
        return PipelineState.load(self.state_path())

    def save(self, state: PipelineState) -> None:
        """Pipeline durumunu dosyaya kaydeder."""
        state.save(self.state_path())

    def update_chapter(self, chapter_id: str, **kwargs: Any) -> ChapterState:
        """Bölüm durumunu günceller."""
        state = self.load()
        if not isinstance(state.chapters, dict):
            state.chapters = {
                entry.alias: ChapterState(
                    current_step=entry.status.state,
                    score=entry.status.quality_score,
                )
                for entry in state.chapters
            }
        if chapter_id not in state.chapters:
            state.chapters[chapter_id] = ChapterState()
        cs = state.chapters[chapter_id]
        for k, v in kwargs.items():
            if hasattr(cs, k):
                setattr(cs, k, v)
        self.save(state)
        return cs
