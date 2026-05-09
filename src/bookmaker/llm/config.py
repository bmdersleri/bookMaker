"""LLM API yapilandirma yonetimi.
Tek model: DeepSeek v4 Flash (deepseek-chat).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

# .env dosyasini modul yuklenirken oku
try:
    from dotenv import load_dotenv

    _cwd = Path.cwd().resolve()
    for _parent in [_cwd, *_cwd.parents]:
        _env = _parent / ".env"
        if _env.exists():
            load_dotenv(_env, override=False)
            break
except ImportError:
    pass

_CONFIG_FILE = "llm_config.json"


class LLMConfig:
    """LLM API anahtarlari ve model tercihlerini yonetir.

    Tek model destegi: tum API cagrilari ayni modeli kullanir.
    Mevcut model: deepseek-chat (DeepSeek v4 Flash).
    """

    PROVIDERS = {
        "deepseek": {
            "base_url": "https://api.deepseek.com/v1",
            "models": ["deepseek-chat", "deepseek-reasoner"],
        },
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "models": ["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"],
        },
        "anthropic": {
            "base_url": "https://api.anthropic.com/v1",
            "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
        },
    }

    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = project_root or Path.cwd()
        self._data: dict = self._load()

    def _config_path(self) -> Path:
        return self.project_root / _CONFIG_FILE

    def _load(self) -> dict:
        p = self._config_path()
        if p.exists():
            try:
                raw = json.loads(p.read_text(encoding="utf-8"))
                # Eski format destegi: [{"model":"..."}] veya {"model":"..."}
                if isinstance(raw, list):
                    raw = raw[0] if raw else {}
                if isinstance(raw, dict):
                    # Geriye uyum: eski seed_model/enrich_model varsa model'den oku
                    if "model" not in raw:
                        raw["model"] = raw.get("seed_model", "deepseek-chat")
                    return raw
            except (json.JSONDecodeError, OSError):
                pass
        return {"provider": "", "api_key": "", "model": ""}

    def save(self) -> None:
        self._config_path().write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # ----------------------------------------------------------
    # TEMEL BILGILER
    # ----------------------------------------------------------

    @property
    def provider(self) -> str:
        return self._data.get("provider", "")

    @provider.setter
    def provider(self, value: str) -> None:
        self._data["provider"] = value
        self.save()

    @property
    def api_key(self) -> str:
        # Oncelik sirasi:
        # 1. BOOKMAKER_LLM_API_KEY env var (en guvenli)
        # 2. Provider-spesifik env var (LLM_API_KEY_DEEPSEEK)
        # 3. Generic env var (LLM_API_KEY)
        # 4. llm_config.json dosyasindaki deger (geriye uyumlu)
        key = os.environ.get("BOOKMAKER_LLM_API_KEY", "")
        if not key:
            key = os.environ.get(f"LLM_API_KEY_{self.provider.upper()}", "")
            key = key or os.environ.get("LLM_API_KEY", "")
        if not key:
            key = self._data.get("api_key", "")
        return key

    @api_key.setter
    def api_key(self, value: str) -> None:
        self._data["api_key"] = value
        self.save()

    @property
    def base_url(self) -> str:
        p = self.provider
        return self.PROVIDERS.get(p, {}).get("base_url", "")

    def is_configured(self) -> bool:
        return bool(self.provider and self.api_key)

    # ----------------------------------------------------------
    # MODEL ADI (Tek model)
    # ----------------------------------------------------------
    #
    # Ayarlanmazsa varsayilan: deepseek-chat (DeepSeek v4 Flash)
    # Ornek llm_config.json:
    #   { "provider": "deepseek", "api_key": "...", "model": "deepseek-chat" }
    # ----------------------------------------------------------

    @property
    def model(self) -> str:
        """Kullanilacak model adi."""
        return self._data.get("model", "deepseek-chat")

    @model.setter
    def model(self, value: str) -> None:
        self._data["model"] = value
        self.save()

    # ----------------------------------------------------------
    # YARDIMCILAR
    # ----------------------------------------------------------

    def available_providers(self) -> list[str]:
        return list(self.PROVIDERS.keys())

    def available_models(self, provider: str | None = None) -> list[str]:
        p = provider or self.provider
        return self.PROVIDERS.get(p, {}).get("models", [])

    @property
    def ambos_configured(self) -> bool:
        """Backward-compatible alias for the old dual-model check."""
        return self.is_configured()
