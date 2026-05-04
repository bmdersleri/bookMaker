"""Proje kok ve chapter yol yardimcilari.

bookMaker'da iki ayri kok vardir:
1. Otomasyon koku (automation_root) - pyproject.toml'in bulundugu yer, src/bookmaker/
2. Kitap proje koku (project_root)  - book_profile.yaml'in bulundugu yer, book_projects/<book_name>/

CLI komutlari genelde kitap proje koku uzerinde calisir.
"""

from __future__ import annotations

from pathlib import Path

_DEFAULT_BOOK = "java-temelleri"


def find_automation_root(start: Path | None = None) -> Path | None:
    """Otomasyon kkunu bulur (pyproject.toml veya src/bookmaker/ ile)."""
    current = (start or Path.cwd()).resolve()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
        if (parent / "src" / "bookmaker").is_dir():
            return parent
    return None


def find_project_root(start: Path | None = None, book_name: str = _DEFAULT_BOOK) -> Path | None:
    """Kitap proje kokunu bulur.

    - Once mevcut dizinden yukari dogru book_profile.yaml ara
    - Bulamazsa automation_root/book_projects/<book_name>/ dene
    """
    current = (start or Path.cwd()).resolve()

    # 1. Mevcut dizin ve ust dizinlerde book_profile.yaml ara
    for parent in [current, *current.parents]:
        if (parent / "book_profile.yaml").exists():
            return parent

    # 2. Otomasyon kokunde book_projects/<book_name>/ dene
    auto_root = find_automation_root(start)
    if auto_root:
        book_path = auto_root / "book_projects" / book_name
        if (book_path / "book_profile.yaml").exists():
            return book_path

    return None


def chapter_dir(project_root: Path, chapter_id: str) -> Path:
    """Bolum dizinini dondurur: <project_root>/chapters/<chapter_id>/"""
    return project_root / "chapters" / chapter_id


def approved_path(project_root: Path, chapter_id: str) -> Path:
    """Onayli bolum dosyasi yolu."""
    return chapter_dir(project_root, chapter_id) / "approved" / f"{chapter_id}.md"


def version_log_path(project_root: Path, chapter_id: str) -> Path:
    return chapter_dir(project_root, chapter_id) / "version_log.jsonl"


def active_version_path(project_root: Path, chapter_id: str) -> Path:
    return chapter_dir(project_root, chapter_id) / "active_version.yaml"
