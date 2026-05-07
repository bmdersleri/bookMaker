"""LLM modül testleri."""

import os
from pathlib import Path

from bookmaker.llm.config import LLMConfig
from bookmaker.llm.openai import OpenAICompatibleClient


def test_config_defaults(tmp_path: Path) -> None:
    cfg = LLMConfig(tmp_path)
    assert cfg.provider == ""
    assert cfg.model == ""
    # api_key .env'den gelebilir (BOOKMAKER_LLM_API_KEY), bos olmayabilir
    assert isinstance(cfg.api_key, str)


def test_config_save_load(tmp_path: Path) -> None:
    cfg = LLMConfig(tmp_path)
    cfg.provider = "openai"
    cfg.model = "gpt-4o"
    cfg.api_key = "sk-test-key-12345"
    cfg.save()

    # _data seviyesinde kayit/yukleme dogrulamasi
    cfg2 = LLMConfig(tmp_path)
    assert cfg2.provider == "openai"
    assert cfg2.model == "gpt-4o"
    assert cfg2._data.get("api_key") == "sk-test-key-12345"
    # api_key property'si env var onceliklidir;
    # BOOKMAKER_LLM_API_KEY setli ise onu dondurur


def test_config_api_key_env_priority(tmp_path: Path, monkeypatch) -> None:
    """Env var varsa _data'daki deger yerine env var kullanilir."""
    monkeypatch.setenv("BOOKMAKER_LLM_API_KEY", "sk-env-priority-test")
    cfg = LLMConfig(tmp_path)
    cfg.api_key = "sk-from-file"
    cfg.save()

    assert cfg.api_key == "sk-env-priority-test"

    # Env var kaldirilinca _data'daki deger kullanilir
    monkeypatch.delenv("BOOKMAKER_LLM_API_KEY")
    assert cfg.api_key == "sk-from-file"


def test_config_providers() -> None:
    cfg = LLMConfig(Path("."))
    providers = cfg.available_providers()
    assert "openai" in providers
    assert "deepseek" in providers
    assert "anthropic" in providers


def test_client_creation() -> None:
    client = OpenAICompatibleClient(
        api_key="sk-test",
        model="gpt-4o",
        base_url="https://api.openai.com/v1",
    )
    assert client.model == "gpt-4o"
    assert client.base_url == "https://api.openai.com/v1"


def test_make_prompt_messages() -> None:
    client = OpenAICompatibleClient(api_key="sk-test")
    msgs = client.make_prompt_messages("System prompt", "User message")
    assert len(msgs) == 2
    assert msgs[0]["role"] == "system"
    assert msgs[1]["role"] == "user"
    assert msgs[0]["content"] == "System prompt"
    assert msgs[1]["content"] == "User message"
