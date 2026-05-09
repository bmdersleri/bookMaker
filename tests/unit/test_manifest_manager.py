"""Manifest manager testleri."""

from pathlib import Path

from bookmaker.manifest.manager import ManifestManager


def test_manager_nonexistent(tmp_path: Path) -> None:
    mgr = ManifestManager(tmp_path)
    assert not mgr.exists()
    m = mgr.load()
    assert m.book.title == ""


def test_manager_load_or_generate_empty(tmp_path: Path) -> None:
    mgr = ManifestManager(tmp_path)
    m = mgr.load_or_generate()
    assert m.book.title == ""
    assert m.chapters == []


def test_validate_empty_project(tmp_path: Path) -> None:
    mgr = ManifestManager(tmp_path)
    issues = mgr.validate()
    assert len(issues) > 0


def test_validate_valid_manifest(tmp_path: Path) -> None:
    p = tmp_path / "book_manifest.yaml"
    content = (
        "book:\n  title: Test\nchapters:\n"
        "  - order: 1\n    chapter_id: ch1\n"
        "    title: Ch1\n    source: ch1.md\n"
        "    github_slug: ch1\n"
    )
    p.write_text(content, encoding="utf-8")
    mgr = ManifestManager(tmp_path)
    issues = mgr.validate()
    assert len(issues) == 0
