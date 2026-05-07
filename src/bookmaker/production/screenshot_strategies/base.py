"""
bookmaker.production.screenshot_strategies.base
=================================================
Screenshot stratejilerinin ortak arayüzü ve veri modelleri.
"""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ScreenshotResult:
    """Tek bir kod bloğunun screenshot sonucu."""
    index: int
    hint: str                  # "plot" | "console" | "screenshot"
    output_path: Path
    was_cached: bool = False
    error: str | None = None
    caption: str = ""          # Markdown'a eklenecek alt yazı

    @property
    def success(self) -> bool:
        return self.error is None


@dataclass
class ScreenshotConfig:
    """
    book_manifest.yaml → production.screenshots bölümünden yüklenir.

    Örnek manifest:
        production:
          screenshots:
            enabled: true
            python_timeout: 15
            react_timeout: 10
            viewport_width: 1280
            viewport_height: 720
            scale: 2
            terminal_theme: dark
    """
    enabled: bool = True
    python_timeout: int = 15
    react_timeout: int = 10
    viewport_width: int = 1280
    viewport_height: int = 720
    scale: int = 2
    terminal_theme: str = "dark"   # "dark" | "light"

    @classmethod
    def from_manifest(cls, data: dict | None) -> ScreenshotConfig:
        if not data:
            return cls()
        return cls(
            enabled=data.get("enabled", True),
            python_timeout=data.get("python_timeout", 15),
            react_timeout=data.get("react_timeout", 10),
            viewport_width=data.get("viewport_width", 1280),
            viewport_height=data.get("viewport_height", 720),
            scale=data.get("scale", 2),
            terminal_theme=data.get("terminal_theme", "dark"),
        )


class ScreenshotStrategy(ABC):
    """Tüm screenshot stratejilerinin uygulaması gereken arayüz."""

    def __init__(self, config: ScreenshotConfig) -> None:
        self.config = config

    @property
    @abstractmethod
    def hint(self) -> str:
        """Bu stratejinin işlediği fence hint'i: 'plot', 'console', 'screenshot'"""

    @abstractmethod
    def capture(
        self,
        code: str,
        output_path: Path,
        index: int,
    ) -> ScreenshotResult:
        """
        Kodu çalıştır ve output_path'e PNG yaz.
        Hata olursa result.error doldurulur, exception fırlatılmaz.
        """

    @staticmethod
    def cache_key(code: str, hint: str) -> str:
        """Kod + hint'ten idempotent hash üretir."""
        return hashlib.md5(f"{hint}::{code.strip()}".encode()).hexdigest()
