#!/usr/bin/env python3
"""Mermaid bloklarini PNG yollariyla degistir + DOCX olustur"""
import re, os, subprocess, sys

OUTPUT_DIR = r"D:\bookMaker_Deepseek\build\output"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
MERGED_MD = os.path.join(OUTPUT_DIR, "java-programlamaya-giris.md")
TEMP_MD = os.path.join(OUTPUT_DIR, "temp_docx_ready.md")
DOCX_OUT = os.path.join(OUTPUT_DIR, "java-programlamaya-giris.docx")

# 1. Merged markdown oku
with open(MERGED_MD, "r", encoding="utf-8") as f:
    content = f.read()

# 2. Mermaid bloklarini bul ve degistir
pattern = re.compile(r"```mermaid\s*.*?\s*```", re.DOTALL)
block_num = [0]

def replace_fn(match):
    block_num[0] += 1
    n = block_num[0]
    png_path = os.path.join(IMAGES_DIR, f"mermaid-{n:03d}.png")
    sys.stdout.write(f"  Blok #{n} -> {os.path.basename(png_path)}")
    if os.path.exists(png_path):
        abs_path = os.path.abspath(png_path)
        sys.stdout.write(f" ({os.path.getsize(png_path)} bytes)\n")
        return f"![Mermaid Diyagrami {n}]({abs_path})"
    else:
        sys.stdout.write(" [BULUNAMADI!]\n")
        return match.group(0)

new_content = pattern.sub(replace_fn, content)

# 3. Gecici MD yaz
with open(TEMP_MD, "w", encoding="utf-8") as f:
    f.write(new_content)
print(f"\nTemp MD yazildi: {len(new_content):,} bytes")
print(f"Toplam Mermaid: {block_num[0]}")

# 4. Pandoc ile DOCX
pandoc_path = r"C:\Program Files\Pandoc\pandoc.exe"
cmd = [pandoc_path, TEMP_MD, "-o", DOCX_OUT,
       "--from", "markdown", "--toc", "--toc-depth=2",
       "--wrap", "none"]

print(f"\nPandoc baslatiliyor: {' '.join(cmd)}")
sys.stdout.flush()

# capture_output=True hata veriyor (cp1254), o yuzden bayrak kullanalim
result = subprocess.run(cmd, capture_output=True, text=False)

if result.returncode == 0:
    size = os.path.getsize(DOCX_OUT)
    print(f"\n[OK] DOCX hazir: {size:,} bytes")
else:
    print(f"\n[HATA] Kod: {result.returncode}")
    stderr = result.stderr[:500].decode("utf-8", errors="replace")
    print(f"STDERR: {stderr}")

# 5. Temizlik
if os.path.exists(TEMP_MD):
    os.remove(TEMP_MD)
    print("Temp MD temizlendi")
