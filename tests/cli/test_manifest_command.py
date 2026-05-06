"""CLI manifest komut testleri."""

from pathlib import Path

from typer.testing import CliRunner

from bookmaker.cli import app

runner = CliRunner()


def test_manifest_view(tmp_path: Path) -> None:
    result = runner.invoke(app, ["manifest", "view", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "Kitap" in result.output


def test_manifest_list_empty(tmp_path: Path) -> None:
    result = runner.invoke(app, ["manifest", "list-chapters", "--path", str(tmp_path)])
    assert "Bolum" in result.output


def test_manifest_validate_missing(tmp_path: Path) -> None:
    result = runner.invoke(app, ["manifest", "validate", "--path", str(tmp_path)])
    assert result.exit_code == 1
    assert "sorun" in result.output or "bulunamadi" in result.output


def test_manifest_validate_valid(tmp_path: Path) -> None:
    p = tmp_path / "book_manifest.yaml"
    p.write_text("book:\n  title: Test\nchapters: []\n", encoding="utf-8")
    result = runner.invoke(app, ["manifest", "validate", "--path", str(tmp_path)])
    # empty chapters will produce issues
    assert result.exit_code == 1


def test_manifest_pipeline_empty(tmp_path: Path) -> None:
    result = runner.invoke(app, ["manifest", "pipeline", "--path", str(tmp_path)])
    assert result.exit_code == 0
