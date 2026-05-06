"""Manifest pipeline testleri."""

from pathlib import Path

from bookmaker.manifest.models import PipelineState
from bookmaker.manifest.pipeline import PipelineManager


def test_pipeline_save_load(tmp_path: Path) -> None:
    mgr = PipelineManager(tmp_path)
    ps = PipelineState(book_id="test", current_stage="authoring")
    mgr.save(ps)
    assert mgr.exists()
    loaded = mgr.load()
    assert loaded.book_id == "test"


def test_pipeline_update_chapter(tmp_path: Path) -> None:
    mgr = PipelineManager(tmp_path)
    cs = mgr.update_chapter("bolum-1", current_step="seeded", score=85)
    assert cs.current_step == "seeded"
    assert cs.score == 85

    loaded = mgr.load()
    assert "bolum-1" in loaded.chapters
    assert loaded.chapters["bolum-1"].current_step == "seeded"
