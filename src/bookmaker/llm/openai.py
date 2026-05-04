"""OpenAI/DeepSeek uyumlu API istemcisi.
requests kutuphanesi kullanir (httpx yerine).

Retry + exponential backoff + jitter ile timeout/dayaniklilik stratejisi:
- Timeout: 120s (tek çağrı)
- Max retry: 3 (toplam 4 deneme)
- Backoff: 2s → 4s → 8s (+ random jitter %25)
- Retry sebepleri: Timeout, ConnectionError, 5xx, 429
- Retry YAPILMAZ: 4xx (auth hatası, bad request vs.)
"""

from __future__ import annotations

import random
import time
from typing import Any

import requests

from bookmaker.llm.base import LLMClient


class OpenAICompatibleClient(LLMClient):
    """OpenAI ve DeepSeek API'leri ile uyumlu istemci.

    Retry stratejisi:
        - Her başarısız çağrıda exponential backoff
        - Jitter ile thundering herd önleme
        - Sadece geçici hatalarda retry (timeout, 5xx, 429)

    Kullanim:
        client = OpenAICompatibleClient(api_key="...", model="deepseek-chat")
        text = client.generate_text("system prompt", "user prompt")
    """

    # Retry yapilacak HTTP status kodlari (sunucu/gecici hatalar)
    RETRYABLE_STATUSES: set[int] = {429, 500, 502, 503, 504}

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com/v1",
        timeout: int = 120,
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ) -> None:
        super().__init__(api_key, model, base_url)
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(self, messages: list[dict], **kwargs: Any) -> dict:
        """Sohbet tamamlama API'sini cagirir. Retry + backoff ile.

        Retry stratejisi:
            - Timeout, ConnectionError, 5xx, 429 → retry (exponential backoff)
            - 4xx (auth, bad request) → retry YAPILMAZ, hemen hata döner
            - Jitter: backoff süresine ±%25 rastgele ekleme

        Args:
            messages: OpenAI formatinda mesaj listesi
            **kwargs: model, temperature, max_tokens vb.

        Returns:
            {"content": "...", "model": "...", "usage": {...}, "retries": N}
            veya {"error": "...", "retries": N}
        """
        payload = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 4096),
        }

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._headers(),
                    json=payload,
                    timeout=self.timeout,
                )

                # 4xx hatalari → retry YAPILMAZ (auth, bad request vs.)
                if 400 <= resp.status_code < 500 and resp.status_code != 429:
                    return {
                        "error": f"API client error {resp.status_code}: {resp.text[:300]}",
                        "content": "",
                        "retries": attempt,
                    }

                # 5xx / 429 → retry yapilabilir
                if resp.status_code in self.RETRYABLE_STATUSES:
                    last_error = f"API server error {resp.status_code}"
                    if attempt < self.max_retries:
                        delay = self._backoff_delay(attempt)
                        print(f"  [RETRY {attempt+1}/{self.max_retries}] "
                              f"{last_error} — {delay:.1f}s sonra tekrar...",
                              flush=True)
                        time.sleep(delay)
                        continue
                    return {
                        "error": f"{last_error}: {resp.text[:200]}",
                        "content": "",
                        "retries": attempt,
                    }

                # 200 OK
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                return {
                    "content": content,
                    "model": data.get("model", ""),
                    "usage": data.get("usage", {}),
                    "retries": attempt,
                }

            except requests.exceptions.Timeout:
                last_error = f"API timeout ({self.timeout}s)"
            except requests.exceptions.ConnectionError:
                last_error = f"API baglanti hatasi: {self.base_url}"
            except Exception as e:
                last_error = str(e)

            if attempt < self.max_retries:
                delay = self._backoff_delay(attempt)
                print(f"  [RETRY {attempt+1}/{self.max_retries}] "
                      f"{last_error} — {delay:.1f}s sonra tekrar...",
                      flush=True)
                time.sleep(delay)
            else:
                return {
                    "error": f"{last_error} ({self.max_retries} retry denendi)",
                    "content": "",
                    "retries": attempt,
                }

        # Buraya gelinmemeli (safe guard)
        return {
            "error": f"Beklenmeyen hata: {last_error}",
            "content": "",
            "retries": self.max_retries,
        }

    def _backoff_delay(self, attempt: int) -> float:
        """Exponential backoff + jitter hesapla.

        Formül: base_delay * 2^attempt * (0.75 ~ 1.25 jitter)
        Örnek: 2.0 * 2^0 = 2.0s → 2.0 * 2^1 = 4.0s → 2.0 * 2^2 = 8.0s
        """
        base = self.retry_delay * (2 ** attempt)
        jitter = base * random.uniform(-0.25, 0.25)  # ±%25
        return max(0.5, base + jitter)  # minimum 0.5s

    def test_connection(self) -> dict:
        """API baglantisini test eder (minimal bir istek gonderir)."""
        messages = [
            {"role": "user", "content": "Reply with only the word OK."}
        ]
        result = self.chat(messages, max_tokens=10)
        if result.get("error"):
            return {"status": "error", "message": result["error"]}
        return {
            "status": "ok",
            "model": result.get("model", ""),
            "response": result.get("content", ""),
        }

    def generate_text(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> str:
        """Basit metin uretimi. content veya error dondurur."""
        messages = self.make_prompt_messages(system_prompt, user_prompt)
        result = self.chat(messages, **kwargs)
        if result.get("error"):
            raise RuntimeError(result["error"])
        return result.get("content", "")
