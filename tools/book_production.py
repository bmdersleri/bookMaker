r"""
book_production.py — Kitap Production Pipeline (Mermaid -> PNG -> DOCX)

Kullanim:
  .venv\Scripts\python.exe tools/book_production.py
"""

import base64, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "output"
MD_PATH = BUILD / "java-programlamaya-giris.md"
IMG_DIR = BUILD / "images"


def log(msg, tag="[OK]"):
    print(f"  {tag} {msg}")


def ensure_dirs():
    IMG_DIR.mkdir(parents=True, exist_ok=True)


MMDC_PATH = os.path.expandvars(r"%APPDATA%\npm\mmdc.cmd")


def render_one_mermaid(content, png_path):
    """mmdc ile Mermaid -> PNG (yerel npm paketi)."""
    try:
        mmd_path = png_path.with_suffix(".mmd")
        mmd_path.write_text(content, encoding="utf-8")
        r = subprocess.run(
            [MMDC_PATH, "-i", str(mmd_path), "-o", str(png_path),
             "-w", "800", "-H", "600", "--backgroundColor", "white"],
            capture_output=True, text=True, timeout=30, shell=False,
        )
        if r.returncode == 0 and png_path.exists() and png_path.stat().st_size > 100:
            return True, None
        return False, r.stderr[:200] or "Bilinmeyen hata"
    except Exception as e:
        return False, str(e)[:200]


def process_mermaid(text):
    """Mermaid bloklarini PNG'ye cevir, referanslari guncelle."""
    blocks = list(re.finditer(r"```mermaid\n(.*?)```", text, re.DOTALL))
    log(f"{len(blocks)} Mermaid blogu bulundu", "[INFO]")

    replacements = []
    for i, m in enumerate(blocks):
        png_name = f"mermaid-{i+1:03d}.png"
        png_path = IMG_DIR / png_name
        content = m.group(1).strip()

        print(f"  [{i+1}/{len(blocks)}] Rendering... ", end="")
        sys.stdout.flush()
        t0 = time.time()
        ok, err = render_one_mermaid(content, png_path)
        secs = time.time() - t0

        if ok:
            sz = png_path.stat().st_size
            print(f"OK ({sz:,} bytes, {secs:.1f}s)")
            link = f"![Mermaid Diyagram {i+1}](images/{png_name})"
            replacements.append((m.start(), m.end(), link))
        else:
            print(f"HATA: {err}")

    # Tersten isle
    for start, end, repl in sorted(replacements, key=lambda x: x[0], reverse=True):
        text = text[:start] + repl + text[end:]

    return text


def convert_docx(md_text, out_path):
    """Pandoc ile DOCX (TOC dahil)."""
    tmp_md = BUILD / "_book_temp.md"
    tmp_md.write_text(md_text, encoding="utf-8")

    log("Pandoc ile DOCX donusturuluyor (TOC)...", "[INFO]")
    r = subprocess.run(
        ["pandoc", str(tmp_md), "-o", str(out_path),
         "--toc", "--toc-depth=2",
         "--from=markdown+raw_tex+pipe_tables+fenced_code_blocks",
         "--to=docx", "--wrap=preserve",
         "--metadata", "title=Java Programlamaya Giris",
         "--metadata", "author=bookMaker",
         "--resource-path", str(BUILD)],
        capture_output=True, text=True, timeout=120,
    )
    if r.returncode != 0:
        log(f"Pandoc HATA: {r.stderr[:400]}", "[HATA]")
        return False
    log(f"DOCX: {out_path} ({out_path.stat().st_size:,} bytes)", "[OK]")
    return True


def main():
    if not MD_PATH.exists():
        log(f"Kaynak yok: {MD_PATH}", "[HATA]")
        sys.exit(1)

    ensure_dirs()
    text = MD_PATH.read_text(encoding="utf-8")
    log(f"Kaynak: {MD_PATH} ({len(text):,} chars)")

    # 1. Mermaid -> PNG
    print("\n=== 1. Mermaid Diyagramlari ===")
    text = process_mermaid(text)

    # 2. DOCX
    print("\n=== 2. DOCX (Pandoc + TOC) ===")
    docx_path = BUILD / "java-programlamaya-giris.docx"
    ok = convert_docx(text, docx_path)

    if ok:
        print(f"\n[OK] Kitap hazir: {docx_path}")
        # Temizlik
        tmp = BUILD / "_book_temp.md"
        if tmp.exists():
            tmp.unlink()
    else:
        print("\n[HATA] DOCX olusturulamadi.")


if __name__ == "__main__":
    main()
