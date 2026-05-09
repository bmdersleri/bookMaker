"""Production pipeline testleri."""

from pathlib import Path

from bookmaker.production.pipeline import run


def test_run_pipeline(sample_chapter: Path, tmp_path: Path) -> None:
    result = run(sample_chapter, tmp_path)
    assert result["chapter"] == "sample_chapter"
    assert "build" in result
    assert "mermaid" in result
    assert "qrcode" in result
    assert "docx" in result
    assert result["build"] is not None
