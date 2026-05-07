"""Merkezi uygulama konfigurasyonu — .env ve environment variable tabanli.

Tum magic number'lar, varsayilan degerler ve uygulama geneli ayarlar burada toplanir.

Kullanim:
    from bookmaker.core.app_config import config

    print(config.llm_timeout)      # 300
    print(config.studio_port)      # 8765
    print(config.log_level)        # "INFO"

Environment Variables (BOOKMAKER_ prefix):
    BOOKMAKER_LLM_API_KEY         — DeepSeek API anahtari (.env'den okunur)
    BOOKMAKER_LLM_MODEL           — Model adi (varsayilan: deepseek-chat)
    BOOKMAKER_LLM_BASE_URL        — API base URL (varsayilan: https://api.deepseek.com/v1)
    BOOKMAKER_LLM_TIMEOUT         — API timeout saniye (varsayilan: 300)
    BOOKMAKER_LLM_MAX_RETRIES     — max retry sayisi (varsayilan: 3)
    BOOKMAKER_LOG_LEVEL           — DEBUG, INFO, WARNING, ERROR (varsayilan: INFO)
    BOOKMAKER_STUDIO_PORT         — Studio GUI port (varsayilan: 8765)
    BOOKMAKER_STUDIO_HOST         — Studio GUI host (varsayilan: 127.0.0.1)
    BOOKMAKER_STUDIO_TOKEN        — Studio API token (bos = devre disi)
    BOOKMAKER_MAX_WORKERS         — Paralel islem worker sayisi (varsayilan: 4)
    BOOKMAKER_OUTPUT_DIR          — Varsayilan cikti dizini
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _load_dotenv() -> None:
    """Proje kokundeki .env dosyasini yukler."""
    try:
        from dotenv import load_dotenv as _load

        # Proje kokunu bul: src/bookmaker/core/app_config.py -> proje koku
        current = Path(__file__).resolve().parent.parent.parent.parent
        env_path = current / ".env"
        if env_path.exists():
            _load(env_path, override=False)  # override=False: env var .env'den once gelir
    except ImportError:
        pass


def _env(key: str, default: str = "") -> str:
    """BOOKMAKER_ prefixli environment variable okur."""
    return os.environ.get(f"BOOKMAKER_{key}", default)


def _env_int(key: str, default: int) -> int:
    val = _env(key, str(default))
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _env_bool(key: str, default: bool) -> bool:
    val = _env(key, "").lower()
    if val in ("1", "true", "yes", "on"):
        return True
    if val in ("0", "false", "no", "off"):
        return False
    return default


@dataclass
class AppConfig:
    """Merkezi uygulama konfigurasyonu.

    .env dosyasindan ve environment variable'lardan okur.
    Singleton pattern: modul duzeyinde tek bir `config` instance'i kullanilir.
    """

    # ----------------------------------------------------------
    # LLM / API
    # ----------------------------------------------------------
    llm_api_key: str = field(default_factory=lambda: _env("LLM_API_KEY", ""))
    llm_model: str = field(default_factory=lambda: _env("LLM_MODEL", "deepseek-chat"))
    llm_base_url: str = field(
        default_factory=lambda: _env("LLM_BASE_URL", "https://api.deepseek.com/v1")
    )
    llm_timeout: int = field(default_factory=lambda: _env_int("LLM_TIMEOUT", 300))
    llm_max_retries: int = field(default_factory=lambda: _env_int("LLM_MAX_RETRIES", 3))
    llm_max_tokens: int = field(default_factory=lambda: _env_int("LLM_MAX_TOKENS", 8192))
    llm_temperature: float = field(
        default_factory=lambda: float(_env("LLM_TEMPERATURE", "0.7"))
    )

    # ----------------------------------------------------------
    # Studio GUI
    # ----------------------------------------------------------
    studio_port: int = field(default_factory=lambda: _env_int("STUDIO_PORT", 8765))
    studio_host: str = field(default_factory=lambda: _env("STUDIO_HOST", "127.0.0.1"))
    studio_token: str = field(default_factory=lambda: _env("STUDIO_TOKEN", ""))

    # ----------------------------------------------------------
    # Logging
    # ----------------------------------------------------------
    log_level: str = field(default_factory=lambda: _env("LOG_LEVEL", "INFO"))

    # ----------------------------------------------------------
    # Pipeline / Islem
    # ----------------------------------------------------------
    max_workers: int = field(default_factory=lambda: _env_int("MAX_WORKERS", 4))
    output_dir: str = field(default_factory=lambda: _env("OUTPUT_DIR", ""))

    # ----------------------------------------------------------
    # Kod uretimi
    # ----------------------------------------------------------
    code_timeout: int = field(default_factory=lambda: _env_int("CODE_TIMEOUT", 30))
    code_max_lines: int = field(default_factory=lambda: _env_int("CODE_MAX_LINES", 1000))

    # ----------------------------------------------------------
    # Mermaid
    # ----------------------------------------------------------
    mermaid_timeout: int = field(default_factory=lambda: _env_int("MERMAID_TIMEOUT", 30))

    def __post_init__(self) -> None:
        _load_dotenv()
        # .env yuklendikten sonra tekrar oku (.env override etmesin diye)
        # burada sadece .env'de olup env var'da olmayanlari al

    @property
    def is_configured(self) -> bool:
        """LLM API yapilandirmasi tamam mi?"""
        return bool(self.llm_api_key)


# Singleton instance
config = AppConfig()
