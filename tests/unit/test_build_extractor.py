"""Build extractor testleri."""

from pathlib import Path

from bookmaker.build.extractor import extract_code
from bookmaker.chapter.parser import parse


def test_extract_sample_chapter_code(sample_chapter: Path) -> None:
    chapter = parse(sample_chapter)
    results = extract_code(chapter, Path("build/code"))
    assert len(results) == 9  # 9 CODE_META in sample
    extracted = [r for r in results if r["status"] == "extracted"]
    skipped = [r for r in results if r["status"] == "skipped"]
    assert len(extracted) == 6  # 6 runnable/compile_only
    assert len(skipped) == 3  # 3 broken_example (skip)


def test_extract_writes_files(sample_chapter: Path, tmp_path: Path) -> None:
    chapter = parse(sample_chapter)
    results = extract_code(chapter, tmp_path)
    for r in results:
        if r["status"] == "extracted" and r["path"]:
            assert Path(r["path"]).exists()


def test_skipped_code_not_written(sample_chapter: Path, tmp_path: Path) -> None:
    chapter = parse(sample_chapter)
    results = extract_code(chapter, tmp_path)
    broken = [r for r in results if r["kind"] == "broken_example"]
    for r in broken:
        assert r["status"] == "skipped"


def test_empty_chapter_no_code(tmp_path: Path) -> None:
    f = tmp_path / "empty.md"
    f.write_text("---\ntitle: Empty\n---\n# Empty\n", encoding="utf-8")
    chapter = parse(f)
    results = extract_code(chapter, tmp_path)
    assert results == []
