"""Retry decorator — gecici hatalarda otomatik tekrar.

Kullanim:
    from bookmaker.utils.retry import retry_on_transient_error

    @retry_on_transient_error(max_retries=3, backoff=2.0)
    def api_call():
        ...

    # Veya context manager olarak:
    with RetryContext(max_retries=3) as retry:
        for attempt in retry:
            try:
                result = api_call()
                break
            except TransientError:
                retry.wait(attempt)
"""

from __future__ import annotations

import functools
import random
import time
from collections.abc import Callable, Iterator
from typing import Any

# Retry yapilacak hata siniflari (varsayilan)
DEFAULT_RETRYABLE = (
    TimeoutError,
    ConnectionError,
    OSError,
)

# Minimum backoff bekleme suresi (saniye)
MIN_BACKOFF_DELAY: float = 0.5

# Jitter orani (±%25)
JITTER_RATIO: float = 0.25


def _backoff_delay(attempt: int, base: float = 2.0) -> float:
    """Exponential backoff + jitter hesapla."""
    delay = base * (2 ** attempt)
    jitter = delay * random.uniform(-JITTER_RATIO, JITTER_RATIO)
    return max(MIN_BACKOFF_DELAY, delay + jitter)


def retry_on_transient_error(
    max_retries: int = 3,
    backoff: float = 2.0,
    retryable: tuple[type[BaseException], ...] = DEFAULT_RETRYABLE,
    on_retry: Callable[[Exception, int, float], None] | None = None,
) -> Callable:
    """Gecici hatalarda exponential backoff ile otomatik retry decorator.

    Args:
        max_retries: Maksimum tekrar sayisi (toplam deneme = max_retries + 1)
        backoff: Ilk bekleme suresi (saniye), her denemede 2x katlanir
        retryable: Retry yapilacak hata tipleri
        on_retry: Her retry oncesi cagrilan callback (exception, attempt, delay)

    Returns:
        Decorated function wrapper.

    Raises:
        Son denemede de basarisiz olursa orijinal hatayi yeniden firlatir.

    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable as e:
                    last_error = e
                    if attempt < max_retries:
                        delay = _backoff_delay(attempt, backoff)
                        if on_retry:
                            on_retry(e, attempt + 1, delay)
                        time.sleep(delay)
            raise last_error  # type: ignore[misc]

        return wrapper

    return decorator


class RetryContext:
    """Context manager tabanli retry.

    Kullanim:
        with RetryContext(max_retries=3) as retry:
            for attempt in retry:
                try:
                    result = api_call()
                    break
                except ConnectionError as e:
                    retry.wait_or_raise(attempt, e)
    """

    def __init__(
        self,
        max_retries: int = 3,
        backoff: float = 2.0,
        retryable: tuple[type[BaseException], ...] = DEFAULT_RETRYABLE,
    ) -> None:
        self.max_retries = max_retries
        self.backoff = backoff
        self.retryable = retryable
        self._last_error: Exception | None = None

    def __enter__(self) -> RetryContext:
        """Context manager'e giris."""
        return self

    def __exit__(self, *_: Any) -> bool:
        """Context manager'den cikis. Istisnalari bastirmaz."""
        return False

    def __iter__(self) -> Iterator[int]:
        """Retry denemeleri icin iterator dondurur."""
        return iter(range(self.max_retries + 1))

    def wait(self, attempt: int) -> None:
        """Attempt denemesi icin backoff beklemesi yapar."""
        if attempt < self.max_retries:
            delay = _backoff_delay(attempt, self.backoff)
            time.sleep(delay)

    def wait_or_raise(self, attempt: int, error: Exception) -> None:
        """Hatayi kontrol eder: retry yapilabilirse bekler, yoksa firlatir."""
        if not isinstance(error, self.retryable):
            raise error
        self._last_error = error
        if attempt >= self.max_retries:
            raise error
        delay = _backoff_delay(attempt, self.backoff)
        time.sleep(delay)
