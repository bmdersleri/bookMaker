"""CLI build komutu testleri."""

from pathlib import Path

from typer.testing import CliRunner

from bookmaker.cli import app

runner = CliRunner()


def test_build_sample_chapter(sample_chapter: Path) -> None:
    result = runner.invoke(app, ["build", "chapter", str(sample_chapter)])
    assert result.exit_code == 0
    assert "Build Raporu" in result.output
    assert "Derlenen" in result.output


def test_build_nonexistent_file() -> None:
    result = runner.invoke(app, ["build", "chapter", "yok.md"])
    assert result.exit_code == 1
    assert "bulunamad" in result.output


def test_build_with_json_flag(sample_chapter: Path, tmp_path: Path) -> None:
    import os
    original = Path.cwd()
    os.chdir(str(tmp_path))
    try:
        (tmp_path / "build" / "reports").mkdir(parents=True, exist_ok=True)
        result = runner.invoke(app, ["build", "chapter", str(sample_chapter), "--json"])
        assert result.exit_code == 0
        reports = list((tmp_path / "build" / "reports").glob("*build_report.json"))
        assert len(reports) > 0
    finally:
        os.chdir(str(original))
