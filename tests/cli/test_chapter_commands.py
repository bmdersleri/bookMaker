"""CLI chapter komut testleri."""

from pathlib import Path

from typer.testing import CliRunner

from bookmaker.cli import app

runner = CliRunner()


def test_chapter_seed(tmp_path: Path) -> None:
    result = runner.invoke(app, [
        "chapter", "seed", "bolum-1",
        "--purpose", "Test",
        "--path", str(tmp_path),
    ])
    assert result.exit_code == 0
    assert "Seed olusturuldu" in result.output


def test_chapter_outline_prompt(tmp_path: Path) -> None:
    # once seed
    runner.invoke(app, ["chapter", "seed", "bolum-1", "--purpose", "Test",
                        "--path", str(tmp_path)])
    result = runner.invoke(app, ["chapter", "outline", "bolum-1", "prompt",
                                 "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "bolum-1" in result.output


def test_chapter_outline_paste(tmp_path: Path) -> None:
    runner.invoke(app, ["chapter", "seed", "bolum-1", "--purpose", "Test", "--path", str(tmp_path)])
    result = runner.invoke(app, [
        "chapter", "outline", "bolum-1", "paste",
        "--text", "# Outline\n## G\n## G2\n## G3\n",
        "--path", str(tmp_path),
    ])
    assert result.exit_code == 0
    assert "Outline kaydedildi" in result.output


def test_chapter_draft_prompt(tmp_path: Path) -> None:
    runner.invoke(app, ["chapter", "seed", "bolum-1", "--purpose", "T", "--path", str(tmp_path)])
    runner.invoke(app, ["chapter", "outline", "bolum-1", "paste",
                        "--text", "# Outline\n## G\n## G2\n## G3\n",
                        "--path", str(tmp_path)])
    result = runner.invoke(app, ["chapter", "draft", "bolum-1", "prompt", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "bolum-1" in result.output
