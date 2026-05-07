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

import logging
import random
import time
from collections.abc import Generator
from typing import Any

import requests

from bookmaker.llm.base import LLMClient

logger = logging.getLogger(__name__)

# Varsayilan yapilandirma sabitleri
_DEFAULT_TEMPERATURE: float = 0.7
_DEFAULT_MAX_TOKENS: int = 8192
_MIN_BACKOFF_DELAY: float = 0.5
_JITTER_RATIO: float = 0.25

# Devam (resume) mekanizmasi sabitleri
_CONTEXT_TAIL_SIZE: int = 1500
_CONTEXT_HISTORY_SIZE: int = 3000
_MAX_CONTINUES: int = 5


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
        timeout: int = 300,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        api_log_dir: str = "",
    ) -> None:
        super().__init__(api_key, model, base_url)
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        # API yanıt log dizini (boş ise loglama kapalı)
        self._api_log_dir = api_log_dir
        self._api_call_counter = 0

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _save_api_response(
        self, call_name: str, payload: dict, response: dict | None,
        error: str | None, attempt: int
    ) -> None:
        """API çağrısını ve yanıtını JSON dosyasına kaydeder.

        Bu sayede DeepSeek API'dan gelen ham yanıt incelenebilir,
        uzun yanıt kesintileri, token kullanımı gibi sorunlar tespit edilir.
        """
        if not self._api_log_dir:
            return
        import json
        import os
        from datetime import datetime
        log_dir = os.path.join(self._api_log_dir, "api_logs")
        os.makedirs(log_dir, exist_ok=True)
        self._api_call_counter += 1
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"{ts}_{self._api_call_counter:03d}_{call_name}.json"
        log = {
            "timestamp": ts,
            "call": call_name,
            "model": payload.get("model", ""),
            "max_tokens": payload.get("max_tokens", 0),
            "temperature": payload.get("temperature", 0),
            "attempt": attempt + 1,
            "total_attempts": self.max_retries + 1,
            "payload": {
                "model": payload.get("model", ""),
                "max_tokens": payload.get("max_tokens", 0),
                "temperature": payload.get("temperature", 0),
                "messages_count": len(payload.get("messages", [])),
                "system_prompt_preview": "",
                "user_prompt_preview": "",
            },
            "response": response,
            "error": error,
        }
        # Prompt önizlemesi (ilk 500 karakter)
        for msg in payload.get("messages", []):
            if msg.get("role") == "system":
                log["payload"]["system_prompt_preview"] = msg.get("content", "")[:500]
            elif msg.get("role") == "user":
                log["payload"]["user_prompt_preview"] = msg.get("content", "")[:500]
        path = os.path.join(log_dir, fname)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(log, f, indent=2, ensure_ascii=False)
            logger.debug("API-LOG: %s kaydedildi", fname)
        except Exception:
            pass

    def chat(self, messages: list[dict], **kwargs: Any) -> dict[str, Any]:
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
            "temperature": kwargs.get("temperature", _DEFAULT_TEMPERATURE),
            "max_tokens": kwargs.get("max_tokens", _DEFAULT_MAX_TOKENS),
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
                    err_msg = f"API client error {resp.status_code}: {resp.text[:300]}"
                    self._save_api_response("error_4xx", payload, None, err_msg, attempt)
                    return {
                        "error": err_msg,
                        "content": "",
                        "retries": attempt,
                    }

                # 5xx / 429 → retry yapilabilir
                if resp.status_code in self.RETRYABLE_STATUSES:
                    last_error = f"API server error {resp.status_code}"
                    if attempt < self.max_retries:
                        delay = self._backoff_delay(attempt)
                        logger.warning(
                            "RETRY %s/%s: %s — %.1fs sonra tekrar...",
                            attempt + 1, self.max_retries, last_error, delay
                        )
                        time.sleep(delay)
                        continue
                    self._save_api_response("error_5xx", payload, None, last_error, attempt)
                    return {
                        "error": f"{last_error}: {resp.text[:200]}",
                        "content": "",
                        "retries": attempt,
                    }

                # 200 OK
                data = resp.json()
                choice = data["choices"][0]
                content = choice["message"]["content"]
                finish_reason = choice.get("finish_reason", "unknown")
                usage = data.get("usage", {})

                # Yanıt kesilmiş mi kontrol et
                if finish_reason == "length":
                    completion_tokens = usage.get("completion_tokens", 0)
                    logger.warning(
                        "TRUNCATION: API response max_tokens (%s) limitinde kesildi! "
                        "finish_reason=%s, completion_tokens=%s",
                        payload["max_tokens"], finish_reason, completion_tokens
                    )

                response_info = {
                    "content": content,
                    "model": data.get("model", ""),
                    "usage": usage,
                    "finish_reason": finish_reason,
                    "retries": attempt,
                }
                self._save_api_response(
                    f"ok_finish_{finish_reason}", payload, response_info, None, attempt
                )
                return response_info

            except requests.exceptions.Timeout:
                last_error = f"API timeout ({self.timeout}s)"
            except requests.exceptions.ConnectionError:
                last_error = f"API baglanti hatasi: {self.base_url}"
            except Exception as e:
                last_error = str(e)

            if attempt < self.max_retries:
                delay = self._backoff_delay(attempt)
                logger.warning(
                    "RETRY %s/%s: %s — %.1fs sonra tekrar...",
                    attempt + 1, self.max_retries, last_error, delay
                )
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

        Formül: base_delay * 2^attempt * (1 ± jitter)
        Örnek: 2.0 * 2^0 = 2.0s → 2.0 * 2^1 = 4.0s → 2.0 * 2^2 = 8.0s
        """
        base = self.retry_delay * (2 ** attempt)
        jitter = base * random.uniform(-_JITTER_RATIO, _JITTER_RATIO)
        return max(_MIN_BACKOFF_DELAY, base + jitter)

    def chat_stream(
        self, messages: list[dict], **kwargs: Any
    ) -> Generator[dict[str, Any], None, None]:
        """Streaming modunda API cagrisi. SSE chunk'larini yield eder.

        DeepSeek SSE (Server-Sent Events) formati:
            data: {"choices":[{"delta":{"content":"..."},"finish_reason":null}]}
            data: {"choices":[{"delta":{},"finish_reason":"stop"}]}
            data: [DONE]

        Baglanti koparsa son alinan chunk'a kadar olan icerik kaybolmaz
        (caller tarafinda dosyaya yazilir).

        Yields:
            {"content": "...", "finish_reason": "...", "usage": {...}}
            Her chunk'ta delta content birikir. Son chunk'ta finish_reason ve usage gelir.

        """
        import json

        payload = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", _DEFAULT_TEMPERATURE),
            "max_tokens": kwargs.get("max_tokens", _DEFAULT_MAX_TOKENS),
            "stream": True,
        }

        accumulated = ""
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                resp = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._headers(),
                    json=payload,
                    timeout=(30, self.timeout),  # (connect, read)
                    stream=True,
                )

                if resp.status_code == 200:
                    for line in resp.iter_lines(decode_unicode=True):
                        if not line or not line.startswith("data: "):
                            continue
                        data_str = line[6:]  # "data: " önekini kaldır
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            choice = chunk.get("choices", [{}])[0]
                            delta = choice.get("delta", {})
                            content = delta.get("content", "")
                            finish_reason = choice.get("finish_reason", "")
                            if content:
                                accumulated += content
                            yield {
                                "content": content,
                                "accumulated": accumulated,
                                "finish_reason": finish_reason,
                                "usage": chunk.get("usage", {}),
                                "model": chunk.get("model", ""),
                            }
                            if finish_reason:
                                return  # Stream tamamlandı
                        except json.JSONDecodeError:
                            continue  # Bozuk chunk'ı atla

                    return  # Normal tamamlanma

                elif 400 <= resp.status_code < 500 and resp.status_code != 429:
                    yield {
                        "content": "",
                        "accumulated": accumulated,
                        "finish_reason": "error",
                        "error": f"API client error {resp.status_code}",
                        "usage": {},
                        "model": "",
                    }
                    return

                elif resp.status_code in self.RETRYABLE_STATUSES:
                    last_error = f"API server error {resp.status_code}"
                    if attempt < self.max_retries:
                        delay = self._backoff_delay(attempt)
                        logger.warning(
                            "STREAM RETRY %s/%s: %s — %.1fs sonra...",
                            attempt + 1, self.max_retries, last_error, delay
                        )
                        time.sleep(delay)
                        continue
                    yield {
                        "content": "",
                        "accumulated": accumulated,
                        "finish_reason": "error",
                        "error": last_error,
                        "usage": {},
                        "model": "",
                    }
                    return

            except requests.exceptions.Timeout:
                last_error = f"Stream timeout ({self.timeout}s)"
            except requests.exceptions.ConnectionError:
                last_error = f"Stream baglanti hatasi: {self.base_url}"
            except Exception as e:
                last_error = str(e)

            if attempt < self.max_retries:
                delay = self._backoff_delay(attempt)
                logger.warning(
                    "STREAM RETRY %s/%s: %s — %.1fs sonra...",
                    attempt + 1, self.max_retries, last_error, delay
                )
                time.sleep(delay)
            else:
                yield {
                    "content": "",
                    "accumulated": accumulated,
                    "finish_reason": "error",
                    "error": f"{last_error} ({self.max_retries} retry)",
                    "usage": {},
                    "model": "",
                }
                return

    def generate_text_stream(
        self, system_prompt: str, user_prompt: str, output_path: str = "", **kwargs: Any
    ) -> str:
        """Streaming ile metin uretir. Her chunk'i dosyaya yazar.

        Baglanti kopsa bile o ana kadar gelen icerik kaybolmaz.
        DeepSeek'in 10 dakikaya varan uzun yanitlari icin guvenli yontem.

        Args:
            system_prompt: Sistem prompt'u
            user_prompt: Kullanici prompt'u
            output_path: Cikti dosya yolu (bos ise sadece RAM'de birikir)
            **kwargs: model, temperature, max_tokens vb.

        Returns:
            Tam metin (string)

        """
        messages = self.make_prompt_messages(system_prompt, user_prompt)
        accumulated = ""
        file_handle = None

        if output_path:
            from pathlib import Path
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            file_handle = open(output_path, "w", encoding="utf-8")

        try:
            for chunk in self.chat_stream(messages, **kwargs):
                if chunk.get("error"):
                    raise RuntimeError(chunk["error"])
                accumulated = chunk["accumulated"]
                if file_handle and chunk["content"]:
                    file_handle.write(chunk["content"])
                    file_handle.flush()

                finish = chunk.get("finish_reason", "")
                if finish == "length":
                    logger.warning(
                        "STREAM TRUNCATION: %s karakterde kesildi",
                        len(accumulated)
                    )
        finally:
            if file_handle:
                file_handle.close()

        if accumulated:
            logger.info(
                "STREAM: %s kelime, %s karakter",
                len(accumulated.split()), len(accumulated)
            )
        return accumulated

    def test_connection(self) -> dict[str, Any]:
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
        """Basit metin uretimi. content veya error dondurur.

        Not: finish_reason='length' ise yanıt max_tokens limitinde
        kesilmiş demektir. Daha fazla token için max_tokens artırılmalı.
        """
        messages = self.make_prompt_messages(system_prompt, user_prompt)
        result = self.chat(messages, **kwargs)
        if result.get("error"):
            raise RuntimeError(result["error"])

        # Truncation kontrolü
        finish_reason = result.get("finish_reason", "")
        if finish_reason == "length":
            logger.warning(
                "GENERATE_TEXT TRUNCATION: Yanıt kesildi! "
                "Daha yüksek max_tokens değeri gerekebilir. "
                "Mevcut content uzunluğu: %s karakter",
                len(result.get("content", ""))
            )

        return result.get("content", "")

    def generate_text_with_resume(
        self, system_prompt: str, user_prompt: str, **kwargs: Any
    ) -> str:
        """Kesilme durumunda otomatik devam ederek metin uretir.

        DeepSeek API max_tokens limitine ulasinca finish_reason='length' doner.
        Bu metod, yaniti otomatik olarak devam ettirir:
        1. Ilk cagriyi yapar
        2. Kesilme varsa son 1500 karakteri context olarak alir
        3. "Kaldigin yerden devam et" promptuyla yeni cagri yapar
        4. Tum parcalari birlestirir
        5. Maksimum 5 devam (sonsuz donguye karsi koruma)

        Args:
            system_prompt: Sistem prompt'u
            user_prompt: Kullanici prompt'u
            **kwargs: model, temperature, max_tokens vb.

        Returns:
            Birlestirilmis tam metin

        """
        messages = self.make_prompt_messages(system_prompt, user_prompt)
        all_parts = []
        total_continues = 0
        max_continues = _MAX_CONTINUES

        # Ilk cagri
        result = self.chat(messages, **kwargs)
        if result.get("error"):
            raise RuntimeError(result["error"])

        content = result.get("content", "")
        all_parts.append(content)
        finish_reason = result.get("finish_reason", "")

        while finish_reason == "length" and total_continues < max_continues:
            total_continues += 1
            logger.info(
                "RESUME %s/%s: Yanit %s karakterde kesildi, devam ediliyor...",
                total_continues, max_continues, len(content)
            )

            # Son _CONTEXT_TAIL_SIZE karakteri context olarak al
            tail = content[-_CONTEXT_TAIL_SIZE:] if len(content) > _CONTEXT_TAIL_SIZE else content

            # Gelişmiş devam prompt'u — 7 kesin kural ile
            continue_user = (
                f"!! KESİNTİ DEVAM TALİMATI !!\n\n"
                f"Yukarıdaki metin, teknik bir sınır (max_tokens) nedeniyle "
                f"tam ortasında kesildi. Sen bir kitap bölümü yazıyordun ve "
                f"tam şu noktada kaldın:\n\n"
                f"--- SON ÜRETİLEN KESİT ---\n"
                f"{tail}\n"
                f"--- KESİT SONU ---\n\n"
                f"AŞAĞIDAKİ 7 KURALLARA KESİNLİKLE UY:\n\n"
                f"1. [TEKRAR YASAK] Önceki içeriği ASLA tekrar etme, "
                f"özetleme, yeniden yazma. Okuyucu zaten okudu.\n\n"
                f"2. [BAŞLIK YASAK] Yeni # veya ## başlığı EKLEME. "
                f"Sen zaten bir bölümün ORTASINDASIN, baştan başlamıyorsun.\n\n"
                f"3. [DOĞRUDAN DEVAM] Son cümlenin/paragrafın bittiği "
                f"yerden, bir sonraki kelimeyle başla. Okuyucu aradaki "
                f"kesintiyi fark etmemeli.\n\n"
                f"4. [STİL KORU] Aynı yazım stilini, akademik-sade üslubu, "
                f"Türkçe'yi ve Markdown formatını aynen koru.\n\n"
                f"5. [BLOK TAMAMLA] Eğer bir kod bloğu (```), tablo (|), "
                f"liste (-) veya Mermaid diyagramı (```mermaid) ortasında "
                f"kesildiysen, o bloğu ÖNCE tamamla, sonra devam et.\n\n"
                f"6. [META YORUM YASAK] 'Devam ediyorum', 'Kaldığımız "
                f"yerden...', 'Şimdi...' gibi meta açıklamalar YAZMA. "
                f"Sanki hiç kesinti olmamış gibi yaz.\n\n"
                f"7. [SADECE İÇERİK] Çıktı olarak SADECE devam metnini "
                f"üret. Ne bir giriş cümlesi, ne bir açıklama, ne de "
                f"bir özet ekle.\n\n"
                f"Şimdi, yukarıdaki 7 kurala uyarak, tam olarak kaldığın "
                f"yerden devam et:"
            )

            continue_messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
                {
                    "role": "assistant",
                    "content": (
                        content[-_CONTEXT_HISTORY_SIZE:]
                        if len(content) > _CONTEXT_HISTORY_SIZE
                        else content
                    ),
                },
                {"role": "user", "content": continue_user},
            ]

            result = self.chat(continue_messages, **kwargs)
            if result.get("error"):
                logger.error("RESUME: Hata: %s", result["error"])
                break

            continuation = result.get("content", "")
            finish_reason = result.get("finish_reason", "")

            if continuation:
                all_parts.append(continuation)
                content = content + "\n\n" + continuation

        if total_continues > 0:
            logger.info(
                "RESUME: %s devam ile tamamlandi. Toplam: %s karakter",
                total_continues, len(content)
            )

        return content
