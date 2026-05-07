from typer.testing import CliRunner

from bookmaker.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "0.2.0" in result.output


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "chapter" in result.output
    assert "build" in result.output
    assert "check" in result.output


def test_chapter_help():
    result = runner.invoke(app, ["chapter", "--help"])
    assert result.exit_code == 0


def test_check_help():
    result = runner.invoke(app, ["check", "--help"])
    assert result.exit_code == 0
