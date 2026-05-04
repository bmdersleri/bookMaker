#!/usr/bin/env python3
"""GitHub Pages icin kitap HTML'i olusturur.

Kullanim:
    python tools/build/pages_build.py
    python tools/build/pages_build.py --serve    # local test server
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_OUTPUT = PROJECT_ROOT / "build" / "output"
DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"

PANDOC = shutil.which("pandoc") or r"C:\Program Files\Pandoc\pandoc.exe"

HEADER = f"""---
title: "Java Programlamaya Giris"
subtitle: "Temel Kavramlar ve Uygulamali Anlatim"
author: "Ismail Kirbas"
---

"""

FOOTER_HTML = """
<footer>
    <p>Java Programlamaya Giris &mdash; Ismail Kirbas &copy; 2026</p>
    <p>
        <a href="https://github.com/bmdersleri/bookMaker">GitHub</a> |
        <a href="java-programlamaya-giris.docx">DOCX</a> |
        <a href="java-programlamaya-giris.pdf">PDF</a>
    </p>
</footer>
"""


def ensure_dirs() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR).mkdir(parents=True, exist_ok=True)


def copy_assets() -> None:
    """CSS ve diger statik dosyalari kopyala."""
    src_css = PROJECT_ROOT / "docs" / "assets" / "style.css"
    dst_css = ASSETS_DIR / "style.css"
    if src_css.exists():
        shutil.copy2(src_css, dst_css)
        print(f"  CSS: {dst_css}")


def copy_images() -> None:
    """Mermaid PNG'leri docs/assets/images/ altina kopyala."""
    src_dir = BUILD_OUTPUT / "images"
    if not src_dir.exists():
        print(f"  [WARN] Kaynak goruntu dizini yok: {src_dir}")
        return
    count = 0
    for png in sorted(src_dir.glob("*.png")):
        shutil.copy2(png, IMAGES_DIR / png.name)
        count += 1
    print(f"  Gorseller: {count} PNG kopyalandi -> {IMAGES_DIR}")


def build_html() -> bool:
    """Markdown -> HTML donusumu (pandoc ile)."""
    src_md = BUILD_OUTPUT / "java-programlamaya-giris.md"
    dst_html = DOCS_DIR / "index.html"

    if not src_md.exists():
        print(f"[ERROR] Kaynak MD bulunamadi: {src_md}")
        return False

    css_path = ASSETS_DIR / "style.css"

    # Gorsel yollarini duzelt: ./images/*.png -> assets/images/*.png
    print("  Gorsel yollari duzeltiliyor...")
    content = src_md.read_text(encoding="utf-8")
    content = content.replace("](./images/", "](./assets/images/")
    content = content.replace('src="./images/', 'src="./assets/images/')
    
    # Header ekle
    temp_md = BUILD_OUTPUT / "_pages_temp.md"
    content = HEADER + content
    temp_md.write_text(content, encoding="utf-8")

    if not Path(PANDOC).exists():
        print(f"[ERROR] Pandoc bulunamadi: {PANDOC}")
        temp_md.unlink(missing_ok=True)
        return False

    cmd = [
        PANDOC,
        str(temp_md),
        "--from", "markdown+yaml_metadata_block+smart+raw_html",
        "--to", "html5",
        "--standalone",
        "--toc",
        "--toc-depth", "3",
        "--metadata", f"title=Java Programlamaya Giris",
        f"--css={css_path}",
        "--highlight-style", "pygments",
        "--section-divs",
        "--wrap=preserve",
        "-o", str(dst_html),
    ]

    print(f"  Pandoc ile HTML olusturuluyor...")
    print(f"  Kaynak: {temp_md.name} ({temp_md.stat().st_size:,} bytes)")
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
    )

    temp_md.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"[ERROR] Pandoc basarisiz (exit={result.returncode})")
        if result.stderr:
            print(f"  STDERR: {result.stderr[:500]}")
        return False

    if not dst_html.exists():
        print(f"[ERROR] HTML olusturulamadi: {dst_html}")
        return False

    html_size = dst_html.stat().st_size
    print(f"  HTML olusturuldu: {dst_html.name} ({html_size:,} bytes)")

    # Footer ekle
    html = dst_html.read_text(encoding="utf-8")
    html = html.replace("</body>", f"{FOOTER_HTML}\n</body>")
    dst_html.write_text(html, encoding="utf-8")

    return True


def build_bookmark_md() -> None:
    """Ana sayfaya yonlendirme icin bookmark.md olustur."""
    bookmark = DOCS_DIR / "README.md"
    content = """# Java Programlamaya Giris

Ismail Kirbas &copy; 2026

- [Kitabi Oku (index.html)](index.html)
- [DOCX indir](https://github.com/bmdersleri/bookMaker/raw/deepseek/build/output/java-programlamaya-giris.docx)
- [PDF indir](https://github.com/bmdersleri/bookMaker/raw/deepseek/build/output/java-programlamaya-giris.pdf)

---

*Bu site GitHub Pages ile yayinlanmaktadir.*
"""
    bookmark.write_text(content, encoding="utf-8")
    print(f"  README: {bookmark}")


def build() -> bool:
    print("=" * 55)
    print("  bookMaker — GitHub Pages Build")
    print("=" * 55)

    ensure_dirs()
    copy_assets()
    copy_images()

    if not build_html():
        return False

    build_bookmark_md()

    # Boyut raporu
    total = sum(f.stat().st_size for f in DOCS_DIR.rglob("*") if f.is_file())
    print(f"\n  Toplam: {total:,} bytes ({total/1024:.0f} KB)")
    print(f"  Dizin: {DOCS_DIR}")
    print(f"  Site: https://bmdersleri.github.io/bookMaker/")
    print()
    print("  GitHub Pages ayarlari:")
    print("    1. GitHub repo -> Settings -> Pages")
    print("    2. Source: Deploy from a branch")
    print("    3. Branch: deepseek, folder: /docs")
    print("    4. Save")
    print("=" * 55)
    return True


def serve() -> None:
    """Local test server."""
    import http.server
    import socketserver

    port = 8000
    os.chdir(str(DOCS_DIR))
    
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"  Local server: http://localhost:{port}")
        print(f"  Kitap: http://localhost:{port}/index.html")
        print("  Ctrl+C ile durdur.")
        httpd.serve_forever()


if __name__ == "__main__":
    import os

    parser = argparse.ArgumentParser(description="GitHub Pages build")
    parser.add_argument("--serve", action="store_true", help="Local test server")
    args = parser.parse_args()

    if args.serve:
        import os
        serve()
    else:
        success = build()
        sys.exit(0 if success else 1)
