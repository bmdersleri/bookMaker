"""OpenAI/DeepSeek uyumlu API istemcisi."""

from __future__ import annotations

import json
from typing import Any

from bookmaker.llm.base import LLMClient

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore


class OpenAICompatibleClient(LLMClient):
    """OpenAI ve DeepSeek API'leri ile uyumlu istemci."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 120,
    ) -> None:
        super().__init__(api_key, model, base_url)
        self.timeout = timeout

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(self, messages: list[dict], **kwargs: Any) -> dict:
        """Sohbet tamamlama API'sini çağırır."""
        if httpx is None:
            return {"error": "httpx not installed", "content": ""}

        payload = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 4096),
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._headers(),
                    json=payload,
                )
                if resp.status_code != 200:
                    return {
                        "error": f"API error {resp.status_code}: {resp.text}",
                        "content": "",
                    }
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                return {"content": content, "model": data.get("model", ""), "usage": data.get("usage", {})}
        except Exception as e:
            return {"error": str(e), "content": ""}

    def test_connection(self) -> dict:
        """API bağlantısını test eder (minimal bir istek gönderir)."""
        messages = [
            {"role": "user", "content": "Reply with only the word OK."}
        ]
        result = self.chat(messages, max_tokens=10)
        if result.get("error"):
            return {"status": "error", "message": result["error"]}
        return {"status": "ok", "model": result.get("model", ""), "response": result.get("content", "")}

    def generate_text(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:
        """Basit metin üretimi. content veya error döndürür."""
        messages = self.make_prompt_messages(system_prompt, user_prompt)
        result = self.chat(messages, **kwargs)
        if result.get("error"):
            raise RuntimeError(result["error"])
        return result.get("content", "")
