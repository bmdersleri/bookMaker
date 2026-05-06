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
