#!/usr/bin/env python3
"""Mermaid bloklarini kontrol et ve bozuk olanlari duzelt"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
merged_path = str(ROOT / "book_projects" / "java-temelleri" / "build" / "output" / "java-programlamaya-giris.md")
with open(merged_path, "r", encoding="utf-8") as f:
    content = f.read()

# Tüm Mermaid bloklarını bul
pattern = re.compile(r'```mermaid\s*(.*?)\s*```', re.DOTALL)
matches = pattern.findall(content)

print(f"Toplam Mermaid bloğu: {len(matches)}")

# Problemli bloklar (8, 21, 26, 31)
problem_ids = [8, 21, 26, 31]

for idx in problem_ids:
    i = idx - 1
    if i < len(matches):
        print(f"\n{'='*60}")
        print(f"BLOK #{idx} (index {i})")
        print(f"{'='*60}")
        print(repr(matches[i]))
        print(f"\nHam içerik:")
        print(matches[i])

# Şimdi .mmd dosyalarını kontrol et
import os
mmd_dir = r"D:\bookMaker_Deepseek\build\output\images"
for idx in problem_ids:
    mmd_path = os.path.join(mmd_dir, f"mermaid-{idx:03d}.mmd")
    if os.path.exists(mmd_path):
        with open(mmd_path, "r", encoding="utf-8", errors="replace") as f:
            data = f.read()
        print(f"\n{'='*60}")
        print(f"MMD DOSYASI #mermaid-{idx:03d}.mmd ({len(data)} bytes)")
        print(f"{'='*60}")
        print(repr(data[:500]))
