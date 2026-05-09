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

JAVA_TEST_MODES: frozenset[str] = frozenset(
    {
        "compile",
        "run",
        "run_assert",
        "compile_run",
        "compile_run_assert",
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

NON_EXECUTION_TEST_MODES: frozenset[str] = frozenset(
    {
        "screenshot_only",
        "review_only",
        "skip",
        "none",
    }
)

CODE_TEST_MODES: frozenset[str] = frozenset(
    JAVA_TEST_MODES | DART_FLUTTER_TEST_MODES | NON_EXECUTION_TEST_MODES
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

PROFILE_ALIASES: dict[str, str] = {
    "java": "java",
    "java-temelleri": "java",
    "java_fundamentals": "java",
    "javanin-temelleri": "java",
    "flutter": "flutter",
    "flutter-mobil": "flutter",
    "flutter_mobile": "flutter",
    "flutter-ile-mobil-uygulama-gelistirme": "flutter",
    "dart": "flutter",
    "python": "python",
    "python-programlama-giris": "python",
    "react": "react",
    "react-native": "react",
    "javascript": "react",
    "generic": "generic",
    "default": "generic",
}

PROFILE_TEST_MODES: dict[str, frozenset[str]] = {
    "java": JAVA_TEST_MODES | NON_EXECUTION_TEST_MODES,
    "flutter": DART_FLUTTER_TEST_MODES | NON_EXECUTION_TEST_MODES,
    "python": NON_EXECUTION_TEST_MODES,
    "react": NON_EXECUTION_TEST_MODES,
    "generic": NON_EXECUTION_TEST_MODES,
}

# Profile → beklenen kod dili eşlemeleri (CODE_META language/profile uyumu için)
PROFILE_LANGUAGES: dict[str, frozenset[str]] = {
    "java": frozenset({"java"}),
    "flutter": frozenset({"dart", "kotlin", "swift", "java", "objective-c"}),
    "python": frozenset({"python"}),
    "react": frozenset({"javascript", "js", "jsx", "tsx", "typescript", "ts"}),
    "generic": frozenset(),
}


def normalize_profile(profile: str | None) -> str:
    """Profil adını dahili kanonik profile dönüştürür.

    Bilinmeyen veya boş profiller ``generic`` kabul edilir. Böylece validator
    profil bilgisiz durumda yalnızca güvenli, çalıştırma gerektirmeyen test
    modlarını varsayılan olarak kullanabilir.
    """
    if not profile:
        return "generic"

    normalized = profile.strip().lower().replace(" ", "-")
    return PROFILE_ALIASES.get(normalized, "generic")


def _get_manifest_value(manifest: object, path: tuple[str, ...]) -> object | None:
    current: object = manifest
    for key in path:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            current = getattr(current, key, None)
        if current is None:
            return None
    return current


def _profile_from_candidate(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = normalize_profile(value)
    if normalized != "generic":
        return normalized
    if value.strip().lower().replace(" ", "-") in {"generic", "default"}:
        return normalized
    return None


def resolve_validation_profile_from_manifest(manifest: object | dict | None) -> str | None:
    """Manifest benzeri nesneden doğrulama profilini çözer.

    Bilinen alias'lar kanonik profile normalize edilir. Bilinmeyen veya boş
    manifest değerleri None döndürür; böylece validator explicit profil
    taşınmadığında eski path fallback davranışını koruyabilir.
    """
    if manifest is None:
        return None

    candidate_paths = (
        ("book", "profile"),
        ("book", "type"),
        ("book", "alias"),
        ("book", "preset"),
        ("technical_profile",),
        ("framework",),
        ("preset",),
        ("language", "primary_language"),
        ("language",),
        ("style", "framework"),
        ("style", "code_language"),
    )
    for path in candidate_paths:
        value = _get_manifest_value(manifest, path)
        profile = _profile_from_candidate(value)
        if profile:
            return profile

    return None


def get_allowed_test_modes(profile: str | None) -> frozenset[str]:
    """Verilen profile göre izin verilen test modlarını döndürür."""
    normalized = normalize_profile(profile)
    return PROFILE_TEST_MODES.get(normalized, PROFILE_TEST_MODES["generic"])


def is_allowed_test_mode_for_profile(test_mode: str | None, profile: str | None) -> bool:
    """Test modunun verilen profile göre izinli olup olmadığını döndürür."""
    if not test_mode:
        return True

    return test_mode in get_allowed_test_modes(profile)


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


def is_language_compatible_with_profile(language: str | None, profile: str | None) -> bool:
    """Check if CODE_META language is compatible with the given profile.

    Profil None veya generic ise her dil kabul edilir.
    Profil java ise yalnızca java kabul edilir.
    Profil flutter ise mobil diller (dart, kotlin, swift, java, objective-c) kabul edilir.
    PROFILE_LANGUAGES içinde boş küme (generic) → kısıtlama yok.
    """
    if not language or not profile:
        return True
    normalized = normalize_profile(profile)
    allowed = PROFILE_LANGUAGES.get(normalized)
    if allowed is None or len(allowed) == 0:
        return True  # kısıtlama yok
    return language.strip().lower() in allowed
