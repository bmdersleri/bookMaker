#!/usr/bin/env python3
"""Tum bolumlerin karakter sayilarini olc ve analiz et"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
chapters_dir = str(ROOT / "book_projects" / "java-temelleri" / "chapters")

# Bolum sirasi
chapter_order = [
    "bolum-01", "bolum-02", "bolum-03", "bolum-04", "bolum-05", "bolum-06",
    "bolum-07", "bolum-08", "bolum-09", "bolum-10", "bolum-11", "bolum-12",
    "bolum-13", "bolum-14", "bolum-15", "bolum-16", "bolum-17", "bolum-18",
    "bolum-19", "bolum-20", "bolum-21", "bolum-22", "bolum-23",
    "ek-a", "ek-b", "ek-c", "ek-d"
]

total_chars = 0
total_mermaid = 0
total_words = 0

print(f"{'Bolum':<25} {'Karakter':>10} {'Kelime':>8} {'Mermaid':>8} {'Kod Blok':>10}")
print("-" * 65)

for name in chapter_order:
    path = os.path.join(chapters_dir, name, "draft_versions", "v001.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        
        # Karakter sayisi (bosluksuz)
        chars = len(content)
        # Kelime sayisi
        words = len(content.split())
        # Mermaid blok sayisi
        mermaid_count = len(re.findall(r'```mermaid', content))
        # Kod blok sayisi
        code_count = len(re.findall(r'```java', content))
        
        chapters[name] = {
            "chars": chars,
            "words": words,
            "mermaid": mermaid_count,
            "code": code_count
        }
        total_chars += chars
        total_words += words
        total_mermaid += mermaid_count
        
        print(f"{name:<25} {chars:>10,} {words:>8,} {mermaid_count:>8} {code_count:>10}")
    else:
        print(f"{name:<25} {'DOSYA YOK':>10}")

print("-" * 65)
print(f"{'TOPLAM':<25} {total_chars:>10,} {total_words:>8,} {total_mermaid:>8}")

# Istatistik
chars_list = [v["chars"] for v in chapters.values()]
avg_chars = sum(chars_list) / len(chars_list)
min_chars = min(chars_list)
max_chars = max(chars_list)

print(f"\n=== ISTATISTIK ===")
print(f"ORTALAMA: {avg_chars:,.0f} karakter")
print(f"EN KISA:  {min_chars:,} karakter ({( [k for k,v in chapters.items() if v['chars']==min_chars][0] )})")
print(f"EN UZUN:  {max_chars:,} karakter ({( [k for k,v in chapters.items() if v['chars']==max_chars][0] )})")
print(f"FARK ORANI: {max_chars/min_chars:.1f}x (en uzun / en kisa)")
print(f"STD SAPMA: {__import__('statistics').stdev(chars_list):,.0f}")

# PDF sayfa tahmini (ortalama ~3500 karakter/sayfa)
print(f"\n=== PDF TAHMINI ===")
for name in chapter_order:
    if name in chapters:
        pages = chapters[name]["chars"] / 3500
        bar_len = int(pages / 0.5)
        print(f"{name:<20} ~{pages:4.1f} sayfa |{'*' * bar_len}")
