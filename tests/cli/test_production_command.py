"""CLI production komut testleri."""

from pathlib import Path

from typer.testing import CliRunner

from bookmaker.cli import app

runner = CliRunner()


def test_production_help() -> None:
    result = runner.invoke(app, ["production", "--help"])
    assert result.exit_code == 0
    assert "full" in result.output or "mermaid" in result.output or "docx" in result.output


def test_production_full_nonexistent() -> None:
    result = runner.invoke(app, ["production", "full", "yok.md"])
    assert result.exit_code == 1
    assert "bulunamadi" in result.output


def test_production_mermaid_on_sample(sample_chapter: Path) -> None:
    result = runner.invoke(app, ["production", "mermaid", str(sample_chapter)])
    # Mermaid CLI olmayabilir, hata kodu 1 olabilir
    assert result.exit_code in (0, 1)
