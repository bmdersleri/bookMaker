"""book_manifest.yaml yükleyici — kitap anayasasını okur ve tüm araçlara sunar.

Kullanim:
    config = BookConfig(project_root)
    config.title                 # "Java'nin Temelleri"
    config.reference_docx_path   # PosixPath('.../referenceV17_java_temelleri.docx')
    config.chapter_ids           # ['bolum-01', 'bolum-02', ..., 'ek-d']
    config.pandoc_cmd("input.md", "output.docx")  # -> list[str]
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from bookmaker.core.errors import ConfigError

# ============================================================
# VARSAYILAN DEGERLER
# ============================================================

_DEFAULTS: dict = {
    "pandoc": {
        "from_format": "markdown+tex_math_single_backslash",
        "filter": "build/styles_revised_v17.lua",
        "reference_doc": "build/referenceV17_java_temelleri.docx",
        "toc": True,
        "toc_depth": 2,
        "toc_title": "Icindekiler",
        "mermaid_image_dir": "build/mermaid_images",
        "mermaid_naming": "diagram_%03d.png",
        "callout_icon_dir": "build/callout_icons",
        "pagebreak_marker": "\\newpage",
    },
    "mermaid": {
        "renderer": "mmdc",
        "shell": "pwsh",
        "shell_path": "C:\\Program Files\\PowerShell\\7\\pwsh.exe",
        "background": "white",
        "output_format": "png",
        "timeout_seconds": 30,
    },
    "outputs": {
        "docx": True,
        "pdf": False,
        "epub": False,
        "html_site": False,
    },
    "ci": {
        "enabled": True,
        "fail_on_code_error": True,
        "fail_on_missing_screenshot": False,
        "fail_on_mermaid_error": True,
    },
    "code": {
        "extract": True,
        "test": False,
        "github_sync": False,
        "qr_generation": False,
    },
}

# Varsayilan bolum sirasi (ekler dahil)
_DEFAULT_CHAPTER_ORDER = (
    [f"bolum-{i:02d}" for i in range(1, 24)]
    + [f"ek-{c}" for c in ["a", "b", "c", "d"]]
)


# ============================================================
# YARDIMCILAR
# ============================================================

def _deep_get(d: dict, *keys: str, default: Any = None) -> Any:
    """İç içe dict'lerde guvenli anahtar erisimi."""
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, {})
    return d if d != {} else default


def _resolve(path: str | Path, anchor: Path) -> Path:
    """Yolu proje kokune gore cozumler.
    - Mutlak yolsa oldugu gibi don
    - Goreceli yolsa anchor'a gore ekle
    """
    p = Path(path)
    if p.is_absolute():
        return p
    return (anchor / p).resolve()


def _resolve_optional(path: str | Path | None, anchor: Path) -> Path | None:
    """Opsiyonel yol cozumleme — None veya mevcut olmayan dosya None doner."""
    if path is None:
        return None
    resolved = _resolve(str(path), anchor)
    return resolved if resolved.exists() else None


# ============================================================
# ANA SINIF
# ============================================================

class BookConfig:
    """Kitap yapilandirmasi — book_manifest.yaml'den okunur
    (book_profile.yaml geriye uyumlu fallback).

    Ornek:
        config = BookConfig(Path("book_projects/java-temelleri"))
        print(config.title)                # "Java'nin Temelleri"
        print(config.author)               # "Ismail KIRBAS"
        print(config.reference_docx_path)  # Path to reference DOCX
        print(config.chapter_ids)          # ['bolum-01', ...]
        print(config.chapter_count)        # 27
    """

    def __init__(self, project_root: str | Path) -> None:
        self._root = Path(project_root).resolve()
        self._raw: dict = {}
        self._load()

    # ----------------------------------------------------------
    # YUKLEME
    # ----------------------------------------------------------

    def _load(self) -> None:
        manifest_path = self._root / "book_manifest.yaml"
        legacy_path = self._root / "book_profile.yaml"

        if manifest_path.exists():
            self._raw = self._manifest_to_raw(manifest_path)
        elif legacy_path.exists():
            with open(legacy_path, encoding="utf-8") as f:
                self._raw = yaml.safe_load(f) or {}
        else:
            raise ConfigError(
                f"Ne book_manifest.yaml ne de book_profile.yaml bulunamadi: "
                f"{self._root}\n"
                f"Proje kokunde book_manifest.yaml olmali."
            )

    @staticmethod
    def _manifest_to_raw(manifest_path: Path) -> dict:
        """book_manifest.yaml'i legacy book_profile.yaml dict formatina donusturur."""
        from bookmaker.manifest.models import BookManifest

        manifest = BookManifest.load(manifest_path)
        book = manifest.book
        style = manifest.style
        chapters = manifest.chapters
        pandoc = manifest.pandoc
        mermaid = manifest.mermaid
        outputs = manifest.outputs

        raw: dict = {}

        # book bolumu
        raw["book"] = {
            "book_id": book.alias or "",
            "title": {"tr": book.title or ""},
            "author": book.author or "",
            "primary_code_language": style.code_language or "java",
            "level": "beginner",
            "domain": "programming",
            "edition": str(book.edition or "1"),
            "year": str(book.year or "2026"),
        }

        # language bolumu
        raw["language"] = {
            "primary_language": book.language or "tr",
        }

        # chapters bolumu
        raw["chapters"] = [
            {
                "chapter_id": ch.effective_alias(),
                "title": ch.title or ch.effective_alias(),
                "file": ch.source or f"chapters/{ch.effective_alias()}/content/draft.md",
                "status": ch.status or "planned",
            }
            for ch in chapters
        ]

        # pandoc bolumu (manifest veya defaults)
        if pandoc:
            raw["pandoc"] = {
                "from_format": pandoc.from_format,
                "filter": pandoc.filter,
                "reference_doc": pandoc.reference_doc,
                "toc": pandoc.toc,
                "toc_depth": pandoc.toc_depth,
                "toc_title": pandoc.toc_title,
                "mermaid_image_dir": pandoc.mermaid_image_dir,
                "mermaid_naming": pandoc.mermaid_naming,
                "callout_icon_dir": pandoc.callout_icon_dir,
                "pagebreak_marker": pandoc.pagebreak_marker,
            }

        # mermaid bolumu (manifest veya defaults)
        if mermaid:
            raw["mermaid"] = {
                "renderer": mermaid.renderer,
                "shell": mermaid.shell,
                "shell_path": mermaid.shell_path,
                "background": mermaid.background,
                "output_format": mermaid.output_format,
                "timeout_seconds": mermaid.timeout_seconds,
            }

        # outputs bolumu (manifest veya defaults)
        if outputs:
            raw["outputs"] = {
                "docx": outputs.docx,
                "pdf": outputs.pdf,
                "epub": outputs.epub,
                "html_site": outputs.html_site,
            }

        return raw

    def reload(self) -> None:
        """Dosyayi yeniden yukler (disardan degisiklik sonrasi)."""
        self._load()

    # ----------------------------------------------------------
    # TEMEL BILGILER
    # ----------------------------------------------------------

    @property
    def project_root(self) -> Path:
        return self._root

    @property
    def book_id(self) -> str:
        return _deep_get(self._raw, "book", "book_id", default="bilinmeyen")

    @property
    def title(self) -> str:
        return _deep_get(self._raw, "book", "title", "tr",
                         default=self.book_id.capitalize())

    @property
    def subtitle(self) -> str:
        return _deep_get(self._raw, "book", "subtitle", "tr", default="")

    @property
    def author(self) -> str:
        return _deep_get(self._raw, "book", "author", default="")

    @property
    def edition(self) -> str:
        return _deep_get(self._raw, "book", "edition", default="1")

    @property
    def year(self) -> str:
        return _deep_get(self._raw, "book", "year", default="2026")

    @property
    def description(self) -> str:
        return _deep_get(self._raw, "book", "description", "tr", default="")

    @property
    def audience(self) -> str:
        return _deep_get(self._raw, "book", "audience", "tr", default="")

    @property
    def level(self) -> str:
        return _deep_get(self._raw, "book", "level", default="beginner")

    @property
    def domain(self) -> str:
        return _deep_get(self._raw, "book", "domain", default="programming")

    @property
    def primary_code_language(self) -> str:
        return _deep_get(self._raw, "book", "primary_code_language",
                         default="java")

    @property
    def repo(self) -> str:
        return _deep_get(self._raw, "book", "repo", default="")

    @property
    def github_slug(self) -> str:
        return _deep_get(self._raw, "book", "github_slug", default="")

    # ----------------------------------------------------------
    # DIL AYARLARI
    # ----------------------------------------------------------

    @property
    def primary_language(self) -> str:
        return _deep_get(self._raw, "language", "primary_language",
                         default="tr")

    @property
    def output_languages(self) -> list[str]:
        return _deep_get(self._raw, "language", "output_languages",
                         default=["tr"])

    # ----------------------------------------------------------
    # BOLUMLER
    # ----------------------------------------------------------

    @property
    def chapters(self) -> list[dict]:
        """Her bolum icin [{'chapter_id': ..., 'title': {...}, 'file': ..., 'status': ...}]"""
        return self._raw.get("chapters", [])

    @property
    def chapter_ids(self) -> list[str]:
        """Sirali bolum kimlikleri: ['bolum-01', ..., 'ek-d']"""
        return [c["chapter_id"] for c in self.chapters if "chapter_id" in c]

    @property
    def chapter_count(self) -> int:
        return len(self.chapters)

    @property
    def approved_chapters(self) -> list[dict]:
        """Sadece status 'approved' olan bolumler."""
        return [c for c in self.chapters if c.get("status") == "approved"]

    @property
    def chapter_order(self) -> list[str]:
        """Oncelikle manifest'teki siralamayi dene,
        bulamazsa varsayilan 23+4 sirasini kullan."""
        ids = self.chapter_ids
        return ids if ids else list(_DEFAULT_CHAPTER_ORDER)

    def chapter_title(self, chapter_id: str, lang: str = "tr") -> str:
        """Bolumun verilen dildeki basligini doner."""
        for c in self.chapters:
            if c.get("chapter_id") == chapter_id:
                titles = c.get("title", {})
                if isinstance(titles, dict):
                    return titles.get(lang, titles.get("tr", chapter_id))
                return str(titles)
        return chapter_id

    def chapter_path(self, chapter_id: str) -> Path | None:
        """Approved .md dosyasinin mutlak yolunu doner.
        Yoksa None doner."""
        for c in self.chapters:
            if c.get("chapter_id") == chapter_id:
                rel = c.get("file")
                if rel:
                    resolved = self._root / rel
                    if resolved.exists():
                        return resolved.resolve()
        # Fallback: chapters/<id>/approved/<id>_v001.md
        fallback = (
            self._root / "chapters" / chapter_id / "approved"
        )
        if fallback.is_dir():
            files = sorted(fallback.glob("*.md"))
            if files:
                return files[0].resolve()
        return None

    def chapter_status(self, chapter_id: str) -> str:
        for c in self.chapters:
            if c.get("chapter_id") == chapter_id:
                return c.get("status", "planned")
        return "planned"

    # ----------------------------------------------------------
    # CIKTI DIZINLERI
    # ----------------------------------------------------------

    @property
    def build_dir(self) -> Path:
        return self._root / "build"

    @property
    def exports_dir(self) -> Path:
        return self.build_dir / "exports"

    @property
    def merged_path(self) -> Path:
        return self.build_dir / ".merged_book.md"

    @property
    def mermaid_dir(self) -> Path:
        """Mermaid PNG'lerin oldugu dizin (Lua filter'in bekledigi yer)."""
        rel = _deep_get(self._raw, "pandoc", "mermaid_image_dir",
                        default="build/mermaid_images")
        return _resolve(rel, self._root)

    @property
    def callout_icon_dir(self) -> Path:
        rel = _deep_get(self._raw, "pandoc", "callout_icon_dir",
                        default="build/callout_icons")
        return _resolve(rel, self._root)

    @property
    def output_docx_path(self) -> Path:
        """Birlestirilmis DOCX ciktisi yolu."""
        return self.exports_dir / f"{self.book_id}.docx"

    # ----------------------------------------------------------
    # PANDOC YAPILANDIRMASI
    # ----------------------------------------------------------

    @property
    def pandoc_from_format(self) -> str:
        return _deep_get(self._raw, "pandoc", "from_format",
                         default=_DEFAULTS["pandoc"]["from_format"])

    @property
    def reference_docx_path(self) -> Path | None:
        """Referans DOCX dosyasi — yoksa None."""
        rel = _deep_get(self._raw, "pandoc", "reference_doc",
                        default=_DEFAULTS["pandoc"]["reference_doc"])
        return _resolve_optional(rel, self._root)

    @property
    def lua_filter_path(self) -> Path | None:
        """Lua filter dosyasi — yoksa None."""
        rel = _deep_get(self._raw, "pandoc", "filter",
                        default=_DEFAULTS["pandoc"]["filter"])
        return _resolve_optional(rel, self._root)

    @property
    def toc_enabled(self) -> bool:
        return _deep_get(self._raw, "pandoc", "toc",
                         default=_DEFAULTS["pandoc"]["toc"])

    @property
    def toc_depth(self) -> int:
        return _deep_get(self._raw, "pandoc", "toc_depth",
                         default=_DEFAULTS["pandoc"]["toc_depth"])

    @property
    def toc_title(self) -> str:
        return _deep_get(self._raw, "pandoc", "toc_title",
                         default=_DEFAULTS["pandoc"]["toc_title"])

    @property
    def mermaid_naming(self) -> str:
        """Mermaid PNG adlandirma sablonu: orn 'diagram_%03d.png'."""
        return _deep_get(self._raw, "pandoc", "mermaid_naming",
                         default=_DEFAULTS["pandoc"]["mermaid_naming"])

    @property
    def pagebreak_marker(self) -> str:
        return _deep_get(self._raw, "pandoc", "pagebreak_marker",
                         default=_DEFAULTS["pandoc"]["pagebreak_marker"])

    # ----------------------------------------------------------
    # MERMAID YAPILANDIRMASI
    # ----------------------------------------------------------

    @property
    def mermaid_shell_path(self) -> str:
        return _deep_get(self._raw, "mermaid", "shell_path",
                         default=_DEFAULTS["mermaid"]["shell_path"])

    @property
    def mermaid_background(self) -> str:
        return _deep_get(self._raw, "mermaid", "background",
                         default=_DEFAULTS["mermaid"]["background"])

    @property
    def mermaid_timeout(self) -> int:
        return _deep_get(self._raw, "mermaid", "timeout_seconds",
                         default=_DEFAULTS["mermaid"]["timeout_seconds"])

    @property
    def mermaid_mmdc_cmd(self) -> list[str]:
        """mmdc'yi PowerShell uzerinden cagiran komut listesi."""
        return [
            self.mermaid_shell_path,
            "-NoProfile",
            "-Command",
            _deep_get(self._raw, "mermaid", "renderer",
                      default=_DEFAULTS["mermaid"]["renderer"]),
        ]

    # ----------------------------------------------------------
    # KALITE KAPILARI
    # ----------------------------------------------------------

    @property
    def require_code_meta(self) -> bool:
        return _deep_get(self._raw, "quality_gates", "require_code_meta",
                         default=True)

    @property
    def min_chapter_words(self) -> int:
        return _deep_get(self._raw, "quality_gates", "min_chapter_word_count",
                         default=1000)

    @property
    def max_chapter_words(self) -> int:
        return _deep_get(self._raw, "quality_gates", "max_chapter_word_count",
                         default=8000)

    # ----------------------------------------------------------
    # CIKTILAR
    # ----------------------------------------------------------

    @property
    def docx_enabled(self) -> bool:
        return _deep_get(self._raw, "outputs", "docx",
                         default=_DEFAULTS["outputs"]["docx"])

    @property
    def pdf_enabled(self) -> bool:
        return _deep_get(self._raw, "outputs", "pdf",
                         default=_DEFAULTS["outputs"]["pdf"])

    # ----------------------------------------------------------
    # ISTATISTIKLER
    # ----------------------------------------------------------

    @property
    def statistics(self) -> dict:
        return self._raw.get("statistics", {})

    @property
    def total_words(self) -> int:
        return _deep_get(self._raw, "statistics", "total_words", default=0)

    @property
    def total_mermaid_diagrams(self) -> int:
        return _deep_get(self._raw, "statistics", "total_mermaid_diagrams",
                         default=0)

    # ----------------------------------------------------------
    # YARDIMCI METODLAR
    # ----------------------------------------------------------

    def pandoc_cmd(
        self,
        input_path: Path,
        output_path: Path,
        *,
        toc: bool | None = None,
        extra_args: list[str] | None = None,
    ) -> list[str]:
        """Pandoc komut satirini olusturur.

        Args:
            input_path: Girdi .md dosyasi
            output_path: Cikti .docx dosyasi
            toc: Icindekiler tablosu (None=config'den oku)
            extra_args: Ek pandoc argumanlari

        Returns:
            orn: ['pandoc', '-f', 'markdown+...', '-o', 'output.docx', ...]
        """
        cmd = [
            "pandoc",
            "-f", self.pandoc_from_format,
            "-o", str(output_path),
            str(input_path),
        ]

        ref = self.reference_docx_path
        if ref and ref.exists():
            cmd.extend(["--reference-doc", str(ref)])

        lua = self.lua_filter_path
        if lua and lua.exists():
            cmd.extend(["--lua-filter", str(lua)])

        use_toc = toc if toc is not None else self.toc_enabled
        if use_toc:
            cmd.append("--toc")
            cmd.extend(["--toc-depth", str(self.toc_depth)])
            cmd.extend(["--metadata", f"toc-title:{self.toc_title}"])

        if extra_args:
            cmd.extend(extra_args)

        return cmd

    def pandoc_cmd_combined(self) -> list[str]:
        """Birlestirilmis .merged_book.md -> final DOCX komutu."""
        return self.pandoc_cmd(
            self.merged_path,
            self.output_docx_path,
        )

    def chapter_order_approved(self) -> list[str]:
        """Sadece onaylanmis bolumlerin sirali listesi."""
        return [cid for cid in self.chapter_order
                if self.chapter_status(cid) == "approved"]

    def summary(self) -> dict:
        """Insan tarafindan okunabilir ozet dict."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "chapters": self.chapter_count,
            "approved": len(self.approved_chapters),
            "total_words": self.total_words,
            "mermaid_diagrams": self.total_mermaid_diagrams,
            "reference_docx": str(self.reference_docx_path) if self.reference_docx_path else None,
            "lua_filter": str(self.lua_filter_path) if self.lua_filter_path else None,
            "docx_enabled": self.docx_enabled,
            "pdf_enabled": self.pdf_enabled,
            "build_dir": str(self.build_dir),
            "exports_dir": str(self.exports_dir),
        }

    def __repr__(self) -> str:
        return (
            f"<BookConfig '{self.book_id}'"
            f" {self.chapter_count} chapters"
            f" @ {self._root}>"
        )


# ============================================================
# KOLAYLIK FONKSIYONU
# ============================================================

def load_config(
    start: str | Path | None = None,
    book_name: str | None = None,
) -> BookConfig:
    """book_manifest.yaml'i bulur ve BookConfig dondurur.

    Sirasiyla:
    1. Verilen start dizininden itibaren book_manifest.yaml ara
    2. book_name belirtilmisse automation_root/book_projects/<name>/ dene
    3. Hala bulunamazsa ConfigError firlat

    Args:
        start: Baslangic dizini (None = cwd)
        book_name: Kitap adi (ornek: 'java-temelleri')

    Returns:
        BookConfig instance

    Raises:
        ConfigError: Dosya bulunamazsa
    """
    from bookmaker.core.paths import find_project_root

    root = find_project_root(start, book_name or "java-temelleri")
    if root is None:
        raise ConfigError(
            "book_manifest.yaml bulunamadi. Bir kitap projesinde "
            "oldugunuzdan emin olun veya --path ile belirtin."
        )
    return BookConfig(root)
