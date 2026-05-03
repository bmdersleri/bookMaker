"""LLM API temel istemci sınıfı."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class LLMClient(ABC):
    """Soyut LLM istemci sınıfı."""

    def __init__(self, api_key: str, model: str = "", base_url: str = "") -> None:
        self.api_key = api_key
        self.model = model or "gpt-4o"
        self.base_url = base_url or "https://api.openai.com/v1"

    @abstractmethod
    def chat(self, messages: list[dict], **kwargs: Any) -> dict:
        """Sohbet tamamlama API'sini çağırır."""
        ...

    @abstractmethod
    def test_connection(self) -> dict:
        """API bağlantısını test eder."""
        ...

    def make_prompt_messages(self, system_prompt: str, user_prompt: str) -> list[dict]:
        """Sistem + kullanıcı mesajlarından oluşan standart mesaj listesi."""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
