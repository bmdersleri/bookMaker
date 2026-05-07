from __future__ import annotations

from bookmaker.chapter.validation_modes import normalize_profile
from bookmaker.code.adapters import (
    CodeAdapter,
    FlutterCodeAdapter,
    JavaCodeAdapter,
    PythonCodeAdapter,
    ReactCodeAdapter,
    ReviewOnlyAdapter,
)

_JS_FAMILY: frozenset[str] = frozenset({
    "javascript", "js", "jsx", "tsx", "typescript", "ts",
})


def _normalize_language(code_language: str | None) -> str:
    return (code_language or "").strip().lower()


def select_code_adapter(
    profile: str | None,
    code_language: str | None = None,
) -> CodeAdapter:
    """Select the appropriate code adapter based on profile or language.

    Args:
        profile: Validation profile name (e.g. java, flutter, python).
        code_language: Fenced code language tag as fallback.

    Returns:
        An appropriate CodeAdapter instance for the given context.

    """
    normalized_profile = normalize_profile(profile)
    normalized_language = _normalize_language(code_language)

    if normalized_profile == "flutter" or normalized_language == "dart":
        return FlutterCodeAdapter()
    if normalized_profile == "java" or normalized_language == "java":
        return JavaCodeAdapter()
    if normalized_profile == "python" or normalized_language == "python":
        return PythonCodeAdapter()
    if normalized_language in _JS_FAMILY:
        return ReactCodeAdapter()
    return ReviewOnlyAdapter()
