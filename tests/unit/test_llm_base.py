"""LLM modül testleri."""

from pathlib import Path

from bookmaker.llm.config import LLMConfig
from bookmaker.llm.openai import OpenAICompatibleClient


def test_config_defaults(tmp_path: Path) -> None:
    cfg = LLMConfig(tmp_path)
    assert cfg.provider == ""
    assert cfg.model == ""
    assert cfg.api_key == ""


def test_config_save_load(tmp_path: Path) -> None:
    cfg = LLMConfig(tmp_path)
    cfg.provider = "openai"
    cfg.model = "gpt-4o"
    cfg.api_key = "sk-test-key-12345"
    cfg.save()

    cfg2 = LLMConfig(tmp_path)
    assert cfg2.provider == "openai"
    assert cfg2.model == "gpt-4o"
    assert cfg2.api_key == "sk-test-key-12345"


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
