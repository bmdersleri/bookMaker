"""Merkezi logging sistemi.

Kullanim:
    from bookmaker.utils.logging import setup_logging, get_logger

    setup_logging(level="INFO")  # app baslangicinda bir kere
    logger = get_logger(__name__)
    logger.info("Mesaj")
    logger.warning("Uyari")
    logger.error("Hata", exc_info=True)

Konsol ciktisi: Rich formatli, renkli
Dosya ciktisi: logs/bookmaker.log (rotating, max 10MB, 5 backup)
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def _get_default_log_dir() -> Path:
    return Path.cwd() / "logs"


def setup_logging(
    level: str = "INFO",
    log_dir: str | Path | None = None,
    *,
    console: bool = True,
    file: bool = True,
) -> None:
    """Tum uygulama icin merkezi logging konfigurasyonu.

    Args:
        level: Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               BOOKMAKER_LOG_LEVEL env var ile override edilir.
        log_dir: Log dosyalarinin yazilacagi dizin. None = ./logs
        console: Konsola renkli cikti acik/kapali
        file: Dosyaya yazma acik/kapali
    """
    import os

    level = os.environ.get("BOOKMAKER_LOG_LEVEL", level).upper()
    root = logging.getLogger()
    root.setLevel(getattr(logging, level, logging.INFO))

    # Onceki handler'lari temizle (cift cagri durumunda)
    root.handlers.clear()

    # Formatter: [ZAMAN] SEVIYE MODUL: mesaj
    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    if console:
        try:
            from rich.logging import RichHandler

            rh = RichHandler(
                rich_tracebacks=True,
                markup=True,
                show_time=True,
                show_path=False,
            )
            rh.setLevel(logging.DEBUG)
            root.addHandler(rh)
        except ImportError:
            ch = logging.StreamHandler(sys.stderr)
            ch.setFormatter(fmt)
            root.addHandler(ch)

    if file:
        log_path = Path(log_dir) if log_dir else _get_default_log_dir()
        log_path.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(
            log_path / "bookmaker.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8",
        )
        fh.setFormatter(fmt)
        root.addHandler(fh)

    # Ucuncu parti kutuphaneleri sustur
    for lib in ("httpx", "urllib3", "websockets", "playwright", "asyncio"):
        logging.getLogger(lib).setLevel(logging.WARNING)

    root.debug("Logging baslatildi (level=%s)", level)


def get_logger(name: str) -> logging.Logger:
    """Modul adina gore logger dondurur.

    Args:
        name: Genellikle __name__ ile cagrilir.

    Returns:
        Configure edilmis Logger instance.
    """
    return logging.getLogger(name)
