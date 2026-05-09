#!/usr/bin/env python3
"""
book_pdf_v3.py — bookMaker PDF Uretim (pandoc + xelatex)
1. Placeholder'lari temizle
2. Mermaid -> PNG
3. LaTeX icin agresif karakter temizligi
4. Pandoc + xelatex ile PDF
"""

import os
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BOOK_PROJECT = ROOT / "book_projects" / "java-temelleri"
INPUT_MD = BOOK_PROJECT / "build" / "output" / "java-programlamaya-giris.md"
IMAGES_DIR = BOOK_PROJECT / "build" / "output" / "images"
OUTPUT_DIR = BOOK_PROJECT / "build" / "output"
TEMP_MD = OUTPUT_DIR / "java-programlamaya-giris-latex-ready.md"
OUTPUT_PDF = OUTPUT_DIR / "java-programlamaya-giris.pdf"


def log(msg, color="green"):
    colors = {"green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m", "cyan": "\033[96m", "reset": "\033[0m"}
    c = colors.get(color, colors["green"])
    print(f"{c}==> {msg}{colors['reset']}", flush=True)


def sanitize_for_latex(content):
    """Markdown icinde LaTeX'te sorun cikaracak karakterleri temizle."""
    lines = content.split('\n')
    new_lines = []
    in_code_block = False
    in_code_fence = False

    for line in lines:
        stripped = line.strip()

        # Kod blogu kontrolu
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block:
            # Kod blogu icinde sadece \n karakterlerini temizle
            # LaTeX: \n -> kontrol dizisi olarak algilanir
            # Guvenli: n (metin olarak)
            new_lines.append(line)
            continue

        # Kod bloklari DISINDA:
        # Inline code icindekileri koru, disindakileri temizle
        parts = re.split(r'(?s)(`[^`]*`)', line)
        cleaned_parts = []
        for part in parts:
            if part.startswith('`') and part.endswith('`'):
                cleaned_parts.append(part)
            else:
                # \n -> \\textbackslash n  (guvenli)
                part = part.replace('\\n', '\\textbackslash{}n')
                # \t -> bosluk
                part = part.replace('\\t', '\\textbackslash{}t')
                # \r -> sil
                part = part.replace('\\r', '')
                cleaned_parts.append(part)

        new_lines.append(''.join(cleaned_parts))

    return '\n'.join(new_lines)


def preprocess(content):
    """Ana on isleme."""
    # 1. Placeholder temizle
    count = 0
    for pattern in [
        r'!\[.*?\]\(https?://[^)]*placeholder[^)]*\)',
        r'!\[.*?\]\(https?://[^)]*via\.placeholder[^)]*\)',
    ]:
        content, n = re.subn(pattern, '', content)
        count += n
    if count:
        log(f"Temizlendi: {count} placeholder resim", "yellow")

    # 2. Mermaid -> PNG
    lines = content.split('\n')
    new_lines = []
    i = 0
    mermaid_count = 0
    converted_count = 0
    block_num = 0

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith('```') and 'mermaid' in line.strip().lower():
            mermaid_count += 1
            block_num += 1
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                i += 1

            png_file = f"mermaid-{block_num:03d}.png"
            png_path = IMAGES_DIR / png_file

            if png_path.exists():
                abs_path = str(png_path.resolve())
                # Pandoc markdown image syntax
                new_lines.append(f'![Mermaid Diyagrami {block_num}]({abs_path})')
                new_lines.append('')
                converted_count += 1
                log(f"Mermaid #{block_num} -> PNG", "cyan")
            else:
                # Blok olarak birak ama mermaid isaretini kaldir
                new_lines.append('```')
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    new_lines.append(lines[i])
                    i += 1
                new_lines.append('```')
                log(f"Mermaid #{block_num} -> BLOK (PNG yok)", "yellow")

            i += 1
        else:
            new_lines.append(line)
            i += 1

    log(f"Mermaid: {converted_count}/{mermaid_count} PNG'ye donustu",
        "green" if converted_count == mermaid_count else "yellow")

    content = '\n'.join(new_lines)

    # 3. LaTeX guvenli hale getir
    content = sanitize_for_latex(content)

    return content


def generate_pdf(content):
    """Pandoc + xelatex ile PDF uret."""
    # Gecici MD dosyasina yaz
    with open(TEMP_MD, 'w', encoding='utf-8') as f:
        f.write(content)

    log(f"Gecici MD yazildi: {TEMP_MD.stat().st_size:,} bytes", "green")

    # Pandoc komutu
    cmd = [
        "pandoc", str(TEMP_MD),
        "-o", str(OUTPUT_PDF),
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=2cm",
        "-V", "geometry:top=2.5cm",
        "-V", "geometry:bottom=2.5cm",
        "-V", "mainfont=Arial",
        "-V", "fontsize=11pt",
        "--toc",
        "--toc-depth=2",
        "--metadata", "title=Java Programlamaya Giris",
        "-f", "markdown",
    ]

    log(f"Pandoc + xelatex ile PDF uretiliyor...", "cyan")
    log(f"  Bu islem 2-5 dakika surebilir...", "yellow")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600,
        cwd=str(OUTPUT_DIR),
    )

    # Stderr'deki onemli hatalari goster
    if result.stderr:
        for line in result.stderr.split('\n'):
            line = line.strip()
            if line:
                is_error = any(w in line.lower() for w in ['error', 'fail', 'undefined', 'fatal'])
                log(line, "red" if is_error else "yellow")

    if OUTPUT_PDF.exists() and OUTPUT_PDF.stat().st_size > 0:
        size = OUTPUT_PDF.stat().st_size
        log(f"BASARILI: {OUTPUT_PDF} ({size:,} bytes)", "green")
        return True
    else:
        log(f"HATA: PDF olusturulamadi. Pandoc kodu: {result.returncode}", "red")
        if result.stderr:
            log("Son hatalar:", "red")
            for line in result.stderr.split('\n')[-10:]:
                log(line.strip(), "red")
        return False


def cleanup():
    if TEMP_MD.exists():
        os.remove(TEMP_MD)
        log(f"Temizlendi: {TEMP_MD.name}", "yellow")


def main():
    log("=" * 60, "cyan")
    log("bookMaker PDF Uretici v3 (pandoc + xelatex)", "cyan")
    log("=" * 60, "cyan")

    if not INPUT_MD.exists():
        log(f"HATA: {INPUT_MD} bulunamadi!", "red")
        return 1

    with open(INPUT_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    log(f"Okundu: {len(content):,} karakter", "green")

    # On isleme
    content = preprocess(content)

    # PDF uret
    success = generate_pdf(content)

    # Temizlik
    if success:
        cleanup()

    print()
    log("=" * 60, "cyan")
    if success:
        size = OUTPUT_PDF.stat().st_size
        log(f"PDF hazir: {OUTPUT_PDF}", "green")
        log(f"Boyut: {size:,} bytes ({size/1024:.0f} KB, {size/1024/1024:.1f} MB)", "green")
    else:
        log(f"PDF URETILEMEDI. Debug icin: {TEMP_MD}", "red")
    log("=" * 60, "cyan")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

