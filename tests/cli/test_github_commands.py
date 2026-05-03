"""CLI github komut testleri."""

from pathlib import Path

from typer.testing import CliRunner

from bookmaker.cli import app

runner = CliRunner()


def test_github_status(tmp_path: Path) -> None:
    result = runner.invoke(app, ["github", "status", "--path", str(tmp_path)])
    # tmp_path repo icinde olabilir; exit_code 0 veya 1 olabilir
    assert result.exit_code in (0, 1)


def test_github_sync_nonexistent(tmp_path: Path) -> None:
    result = runner.invoke(app, ["github", "sync-code", "yok", "--path", str(tmp_path)])
    assert result.exit_code == 1
