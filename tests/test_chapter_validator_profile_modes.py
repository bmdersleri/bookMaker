from bookmaker.chapter.book_validator import validate_book
from bookmaker.chapter.parser import MetaBlock
from bookmaker.chapter.validator import _validate_code_meta


def _issue_category(issue) -> str:
    return getattr(issue, "category", getattr(issue, "code", ""))


def _chapter_text(test_mode: str = "compile_run_assert") -> tuple[str, MetaBlock]:
    meta = "```CODE_META\n"
    meta += "code_id: demo_001\n"
    meta += "file: lib/main.dart\n"
    meta += "validation_mode: runnable\n"
    meta += "language: dart\n"
    meta += f"test: {test_mode}\n"
    meta += "```\n"
    text = meta + "```dart\nvoid main() {}\n```\n"
    block = MetaBlock(
        kind="CODE_META",
        data={
            "code_id": "demo_001",
            "file": "lib/main.dart",
            "validation_mode": "runnable",
            "language": "dart",
            "test": test_mode,
        },
        line=1,
        end=len(meta),
    )
    return text, block


def test_flutter_profile_rejects_java_execution_test_mode() -> None:
    text, block = _chapter_text("compile_run_assert")
    issues = []

    _validate_code_meta(
        text,
        [block],
        issues,
        "book_projects/flutter-ile-mobil-uygulama-gelistirme/chapters/giris/final.md",
    )

    assert any(_issue_category(issue) == "code.test_not_allowed_for_profile" for issue in issues)


def test_explicit_flutter_profile_rejects_java_execution_test_mode() -> None:
    text, block = _chapter_text("compile_run_assert")
    issues = []

    _validate_code_meta(
        text,
        [block],
        issues,
        "book_projects/unknown/chapters/giris/final.md",
        profile="flutter",
    )

    assert any(_issue_category(issue) == "code.test_not_allowed_for_profile" for issue in issues)


def test_explicit_java_profile_rejects_flutter_test_mode() -> None:
    text, block = _chapter_text("flutter_test")
    issues = []

    _validate_code_meta(
        text,
        [block],
        issues,
        "book_projects/unknown/chapters/giris/final.md",
        profile="java",
    )

    assert any(_issue_category(issue) == "code.test_not_allowed_for_profile" for issue in issues)


def test_explicit_profile_overrides_path_fallback() -> None:
    text, block = _chapter_text("compile_run_assert")
    issues = []

    _validate_code_meta(
        text,
        [block],
        issues,
        "book_projects/flutter-ile-mobil-uygulama-gelistirme/chapters/giris/final.md",
        profile="java",
    )

    assert not any(
        _issue_category(issue) == "code.test_not_allowed_for_profile"
        for issue in issues
    )


def test_flutter_profile_accepts_flutter_test_mode() -> None:
    text, block = _chapter_text("flutter_test")
    issues = []

    _validate_code_meta(
        text,
        [block],
        issues,
        "book_projects/flutter-ile-mobil-uygulama-gelistirme/chapters/giris/final.md",
    )

    assert not any(
        _issue_category(issue) == "code.test_not_allowed_for_profile"
        for issue in issues
    )
    assert not any(_issue_category(issue) == "code.test_unknown" for issue in issues)


def test_unknown_profile_preserves_legacy_known_mode_behavior() -> None:
    text, block = _chapter_text("compile_run_assert")
    issues = []

    _validate_code_meta(
        text,
        [block],
        issues,
        "book_projects/react-web/chapters/giris/final.md",
    )

    assert not any(
        _issue_category(issue) == "code.test_not_allowed_for_profile"
        for issue in issues
    )
    assert not any(_issue_category(issue) == "code.test_unknown" for issue in issues)


def test_none_profile_preserves_path_fallback_behavior() -> None:
    text, block = _chapter_text("compile_run_assert")
    issues = []

    _validate_code_meta(
        text,
        [block],
        issues,
        "book_projects/flutter-ile-mobil-uygulama-gelistirme/chapters/giris/final.md",
        profile=None,
    )

    assert any(_issue_category(issue) == "code.test_not_allowed_for_profile" for issue in issues)


def test_book_validation_uses_manifest_profile(tmp_path) -> None:
    project = tmp_path / "sample-book"
    chapter = project / "chapters" / "giris"
    content = chapter / "content"
    for path in [
        project / "prompts",
        project / "exports" / "docx",
        project / "exports" / "pdf",
        project / "exports" / "md",
        project / "logs" / "production",
        project / "logs" / "errors",
        project / "logs" / "reviews",
        content / "revisions",
    ]:
        path.mkdir(parents=True, exist_ok=True)

    (project / "prompts" / "default_chapter.md").write_text(
        "default chapter prompt content",
        encoding="utf-8",
    )
    (project / "prompts" / "default_review.md").write_text(
        "default review prompt content",
        encoding="utf-8",
    )
    (project / "book_manifest.yaml").write_text(
        "book:\n"
        "  alias: flutter-ile-mobil-uygulama-gelistirme\n"
        "production: {}\n"
        "style: {}\n"
        "chapters:\n"
        "- alias: giris\n",
        encoding="utf-8",
    )
    (chapter / "chapter_manifest.yaml").write_text(
        "chapter:\n"
        "  title: Giriş\n"
        "  alias: giris\n"
        "  order: 1\n"
        "scope: {}\n"
        "structure: {}\n"
        "automation: {}\n",
        encoding="utf-8",
    )
    (chapter / "prompt.md").write_text("chapter prompt content", encoding="utf-8")
    (content / "draft.md").write_text("henüz taslak yok", encoding="utf-8")
    (content / "final.md").write_text(
        "# Giriş\n\n"
        "Bu bölüm manifest tabanlı profil doğrulamasını sınar.\n\n"
        "<!-- CODE_META\n"
        "code_id: demo_001\n"
        "file: lib/main.dart\n"
        "validation_mode: runnable\n"
        "language: dart\n"
        "test: compile_run_assert\n"
        "-->\n"
        "```dart\n"
        "void main() { print('ok'); }\n"
        "```\n",
        encoding="utf-8",
    )

    result = validate_book(project)
    issues = result.chapter_reports["giris"].issues

    assert any(_issue_category(issue) == "code.test_not_allowed_for_profile" for issue in issues)
