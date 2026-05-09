"""SQLite veritabani islemleri."""
from __future__ import annotations

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

_SCHEMA = Path(__file__).parent / "schema.sql"


def get_connection(db_path: Path) -> sqlite3.Connection:
    """SQLite baglantisi olusturur ve pragmalari ayarlar."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def db(db_path: Path) -> Generator[sqlite3.Connection, None, None]:
    """Baglanti yoneticisi — islem sonunda commit veya rollback yapar."""
    conn = get_connection(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def ensure_schema(db_path: Path) -> None:
    """Veritabanı tablolarını oluşturur; zaten varsa dokunmaz."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    sql = _SCHEMA.read_text(encoding="utf-8")
    with db(db_path) as conn:
        conn.executescript(sql)


def table_names(db_path: Path) -> list[str]:
    """Veritabanindaki tablo isimlerini listeler."""
    with db(db_path) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    return [r["name"] for r in rows]
