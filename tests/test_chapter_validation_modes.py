from bookmaker.chapter.validation_modes import (
    get_allowed_test_modes,
    is_allowed_test_mode_for_profile,
    is_known_code_test_mode,
    normalize_profile,
    resolve_validation_profile_from_manifest,
)


def test_normalize_profile_known_aliases() -> None:
    assert normalize_profile("java") == "java"
    assert normalize_profile("java-temelleri") == "java"
    assert normalize_profile("flutter") == "flutter"
    assert normalize_profile("flutter-mobil") == "flutter"
    assert normalize_profile("dart") == "flutter"
    assert normalize_profile("javanin-temelleri") == "java"


def test_normalize_profile_unknown_or_empty_defaults_to_generic() -> None:
    assert normalize_profile(None) == "generic"
    assert normalize_profile("") == "generic"
    assert normalize_profile("unknown-profile") == "generic"


def test_flutter_profile_allows_flutter_and_non_execution_modes() -> None:
    allowed = get_allowed_test_modes("flutter")

    assert "flutter_analyze" in allowed
    assert "dart_test" in allowed
    assert "widget_test" in allowed
    assert "review_only" in allowed
    assert "skip" in allowed
    assert "none" in allowed


def test_flutter_profile_does_not_allow_java_execution_modes() -> None:
    assert not is_allowed_test_mode_for_profile("compile_run_assert", "flutter")
    assert not is_allowed_test_mode_for_profile("run", "flutter")


def test_java_profile_allows_java_and_non_execution_modes() -> None:
    allowed = get_allowed_test_modes("java")

    assert "compile" in allowed
    assert "run_assert" in allowed
    assert "compile_run_assert" in allowed
    assert "review_only" in allowed
    assert "skip" in allowed
    assert "none" in allowed


def test_java_profile_does_not_allow_flutter_modes() -> None:
    assert not is_allowed_test_mode_for_profile("flutter_test", "java")
    assert not is_allowed_test_mode_for_profile("dart_analyze", "java")


def test_generic_profile_only_allows_non_execution_modes() -> None:
    allowed = get_allowed_test_modes("generic")

    assert allowed == frozenset({"screenshot_only", "review_only", "skip", "none"})


def test_known_code_test_modes_still_include_all_supported_modes() -> None:
    assert is_known_code_test_mode("compile")
    assert is_known_code_test_mode("flutter_test")
    assert is_known_code_test_mode("screenshot_only")
    assert is_known_code_test_mode("none")
    assert not is_known_code_test_mode("invalid_mode")


def test_manifest_resolver_detects_flutter_from_book_alias() -> None:
    manifest = {"book": {"alias": "flutter-ile-mobil-uygulama-gelistirme"}}

    assert resolve_validation_profile_from_manifest(manifest) == "flutter"


def test_manifest_resolver_detects_framework_alias() -> None:
    manifest = {"style": {"framework": "flutter"}}

    assert resolve_validation_profile_from_manifest(manifest) == "flutter"


def test_manifest_resolver_handles_unknown_manifest_safely() -> None:
    manifest = {"book": {"alias": "react-web"}, "style": {"framework": "react"}}

    assert resolve_validation_profile_from_manifest(manifest) is None
