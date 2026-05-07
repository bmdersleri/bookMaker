from __future__ import annotations

from pathlib import Path


def test_save_chapter_writes_content_draft_and_revision(tmp_path: Path) -> None:
    from bookmaker.generation.pipeline import ChapterGenerator

    generator = ChapterGenerator(tmp_path)
    draft_path = generator._save_chapter("giris", "# Giriş\n\nİçerik.")

    assert draft_path == tmp_path / "chapters" / "giris" / "content" / "draft.md"
    assert draft_path.read_text(encoding="utf-8").startswith("# Giriş")

    revisions = list(
        (tmp_path / "chapters" / "giris" / "content" / "revisions").glob("draft_*.md")
    )
    assert len(revisions) == 1
    assert revisions[0].read_text(encoding="utf-8").startswith("# Giriş")

