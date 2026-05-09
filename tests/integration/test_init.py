from typer.testing import CliRunner

from bookmaker.cli import app
from bookmaker.manifest.models import BookManifest, PipelineState

runner = CliRunner()


def test_init_java_temelleri(tmp_path):
    target = tmp_path / "my-java-book"
    result = runner.invoke(app, ["init", "--preset", "java-temelleri", "--path", str(target)])
    assert result.exit_code == 0, result.output

    # Temel dosyalar
    assert (target / "book_manifest.yaml").exists()
    assert (target / "pipeline_state.yaml").exists()

    # Dizin yapısı
    assert (target / "prompts" / "default_chapter.md").exists()
    assert (target / "prompts" / "default_review.md").exists()
    assert (target / "chapters").is_dir()
    assert (target / "exports" / "docx").is_dir()
    assert (target / "exports" / "pdf").is_dir()
    assert (target / "exports" / "md").is_dir()
    assert (target / "logs" / "reviews").is_dir()

    # Bölüm workspace
    chapter = target / "chapters" / "giris"
    assert (chapter / "chapter_manifest.yaml").exists()
    assert (chapter / "prompt.md").exists()
    assert (chapter / "content" / "draft.md").exists()
    assert (chapter / "content" / "final.md").exists()
    assert (chapter / "content" / "revisions").is_dir()

    manifest = BookManifest.load(target / "book_manifest.yaml")
    assert manifest.book.title == "Java'nın Temelleri"
    assert manifest.style.code_language == "java"
    assert manifest.chapter_aliases() == [
        "giris",
        "degiskenler",
        "kontrol-yapilari",
        "diziler",
        "metotlar",
    ]

    state = PipelineState.load(target / "pipeline_state.yaml")
    assert state.pipeline.book_alias == target.name
    assert [chapter.alias for chapter in state.chapters] == manifest.chapter_aliases()


def test_init_invalid_preset(tmp_path):
    target = str(tmp_path / "x")
    result = runner.invoke(app, ["init", "--preset", "yanlis-preset", "--path", target])
    assert result.exit_code != 0


def test_init_empty_no_preset(tmp_path):
    target = tmp_path / "empty-book"
    result = runner.invoke(app, ["init", "--path", str(target)])
    assert result.exit_code == 0
    assert (target / "book_manifest.yaml").exists()
    assert (target / "pipeline_state.yaml").exists()
    assert (target / "chapters" / "giris" / "content" / "draft.md").exists()
