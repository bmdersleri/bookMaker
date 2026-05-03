"""Manifest model testleri."""

from pathlib import Path

from bookmaker.manifest.models import BookManifest, ManifestChapter, PipelineState


def test_empty_manifest(tmp_path: Path) -> None:
    m = BookManifest()
    assert m.book.title == ""
    assert m.chapters == []


def test_manifest_save_roundtrip(tmp_path: Path) -> None:
    m = BookManifest()
    m.book.title = "Test Kitap"
    m.book.author = "Yazar"
    m.chapters.append(ManifestChapter(
        order=1, chapter_id="bolum-1", title="Bolum 1",
        source="bolum-1.md", github_slug="bolum-1",
    ))
    p = tmp_path / "book_manifest.yaml"
    m.save(p)
    assert p.exists()
    loaded = BookManifest.load(p)
    assert loaded.book.title == "Test Kitap"
    assert len(loaded.chapters) == 1
    assert loaded.chapters[0].chapter_id == "bolum-1"
    assert loaded.chapters[0].order == 1


def test_pipeline_state(tmp_path: Path) -> None:
    ps = PipelineState(book_id="test-book", current_stage="authoring")
    p = tmp_path / "pipeline_state.yaml"
    ps.save(p)
    loaded = PipelineState.load(p)
    assert loaded.book_id == "test-book"
    assert loaded.current_stage == "authoring"
