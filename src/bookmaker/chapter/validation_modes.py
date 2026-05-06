"""Chapter validation mode definitions.

Bu modül, bölüm içeriği doğrulamasında kullanılan validation/test mode
değerlerini merkezi olarak tutar. Amaç, validator.py dosyasını Java veya
tek bir kitap türüne bağlı sabitlerden arındırarak ileride profile-aware
doğrulamaya geçişi kolaylaştırmaktır.
"""

from __future__ import annotations

VALIDATION_MODES: frozenset[str] = frozenset(
    {
        "runnable",
        "compile_only",
        "analyze_only",
        "test_only",
        "review_only",
        "skip",
        "render",
        "capture",
        "screenshot_only",
    }
)

CODE_TEST_MODES: frozenset[str] = frozenset(
    {
        "compile",
        "run",
        "run_assert",
        "compile_run",
        "compile_run_assert",
        "dart_analyze",
        "dart_test",
        "dart_format_check",
        "flutter_analyze",
        "flutter_test",
        "widget_test",
        "integration_test",
        "screenshot_only",
        "review_only",
        "skip",
        "none",
    }
)

DART_FLUTTER_TEST_MODES: frozenset[str] = frozenset(
    {
        "dart_analyze",
        "dart_test",
        "dart_format_check",
        "flutter_analyze",
        "flutter_test",
        "widget_test",
        "integration_test",
    }
)

JAVA_TEST_MODES: frozenset[str] = frozenset(
    {
        "compile",
        "run",
        "run_assert",
        "compile_run",
        "compile_run_assert",
    }
)

NON_EXECUTION_TEST_MODES: frozenset[str] = frozenset(
    {
        "screenshot_only",
        "review_only",
        "skip",
        "none",
    }
)

QR_POLICIES: frozenset[str] = frozenset(
    {
        "none",
        "source",
        "page",
        "single",
        "dual",
    }
)

CODE_KINDS: frozenset[str] = frozenset(
    {
        "example",
        "application",
        "snippet",
        "broken_example",
        "fixed_example",
    }
)


def is_known_validation_mode(value: str | None) -> bool:
    """validation_mode değerinin bilinen bir mod olup olmadığını döndürür."""
    return not value or value in VALIDATION_MODES


def is_known_code_test_mode(value: str | None) -> bool:
    """CODE_META test değerinin bilinen bir mod olup olmadığını döndürür."""
    return not value or value in CODE_TEST_MODES


def is_known_qr_policy(value: str | None) -> bool:
    """qr_policy değerinin bilinen bir politika olup olmadığını döndürür."""
    return not value or value in QR_POLICIES


def is_known_code_kind(value: str | None) -> bool:
    """CODE_META kind değerinin bilinen bir tür olup olmadığını döndürür."""
    return not value or value in CODE_KINDS
