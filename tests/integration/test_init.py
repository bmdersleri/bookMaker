
from typer.testing import CliRunner

from bookmaker.cli import app
from bookmaker.storage.sqlite import table_names

runner = CliRunner()


def test_init_java_temelleri(tmp_path):
    target = tmp_path / "my-java-book"
    result = runner.invoke(app, ["init", "--preset", "java-temelleri", "--path", str(target)])
    assert result.exit_code == 0, result.output

    # Temel dosyalar
    assert (target / "book_profile.yaml").exists()
    assert (target / "book_architecture.yaml").exists()
    assert (target / "bookmaker.sqlite").exists()
    assert (target / "pipeline_state.yaml").exists()

    # Dizin yapısı
    assert (target / "chapters").is_dir()
    assert (target / "assets" / "qr").is_dir()
    assert (target / "exports" / "docx").is_dir()

    # Bölüm workspace
    assert (target / "chapters" / "chapter_01" / "seed").is_dir()
    assert (target / "chapters" / "chapter_01" / "active_version.yaml").exists()
    assert (target / "chapters" / "chapter_01" / "version_log.jsonl").exists()

    # SQLite tabloları
    tables = table_names(target / "bookmaker.sqlite")
    assert "projects" in tables
    assert "chapters" in tables

    # book_profile içeriği
    from bookmaker.models.book import BookProfile
    profile = BookProfile.from_yaml(target / "book_profile.yaml")
    assert profile.title == "Java Temelleri"
    assert profile.primary_code_language == "java"

    # book_architecture içeriği
    from bookmaker.models.book import BookArchitecture
    arch = BookArchitecture.from_yaml(target / "book_architecture.yaml")
    assert len(arch.chapters) == 27
    assert arch.chapters[0].chapter_id == "chapter_01"


def test_init_invalid_preset(tmp_path):
    target = str(tmp_path / "x")
    result = runner.invoke(app, ["init", "--preset", "yanlis-preset", "--path", target])
    assert result.exit_code != 0


def test_init_empty_no_preset(tmp_path):
    target = tmp_path / "empty-book"
    result = runner.invoke(app, ["init", "--path", str(target)])
    assert result.exit_code == 0
    assert (target / "book_profile.yaml").exists()
    assert (target / "bookmaker.sqlite").exists()
