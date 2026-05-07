from __future__ import annotations

from pathlib import Path


def test_exports_dir_points_to_project_exports(tmp_path: Path) -> None:
    from bookmaker.core.config import BookConfig

    root = tmp_path / "sample-book"
    root.mkdir()
    (root / "book_manifest.yaml").write_text(
        "book:\n"
        "  title: Sample\n"
        "  alias: sample-book\n"
        "  author: Test Yazar\n"
        "chapters: []\n",
        encoding="utf-8",
    )

    config = BookConfig(root)

    assert config.exports_dir == root / "exports"
    assert config.output_docx_path == root / "exports" / "sample-book.docx"

