#!/usr/bin/env python3
"""Tum bolumlerdeki CODE_META bloklarini tara ve gosterim sorunlarini bul"""
import re, os

chapters_dir = r"D:\bookMaker_Deepseek\chapters"
order = [f"bolum-{i:02d}" for i in range(1, 24)] + [f"ek-{c}" for c in "abcd"]

print("=== CODE_META GORUNUMLULUK ANALIZI ===")
print()

for ch in order:
    path = os.path.join(chapters_dir, ch, "draft_versions", "v001.md")
    if not os.path.exists(path):
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 1. Kod blogu icindeki // CODE_META satirlari (gorunur)
    visible_code_meta_lines = []
    # 2. HTML yorumundaki <!-- CODE_META bloklari (gizli)
    hidden_code_meta_lines = []
    # 3. Baslik olarak CODE_META (gorunur)
    heading_code_meta = []
    
    in_code_block = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Kod blogu baslangic/bitis
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        
        if "CODE_META" in stripped:
            if in_code_block:
                visible_code_meta_lines.append((i+1, stripped))
            elif stripped.startswith("<!--"):
                hidden_code_meta_lines.append((i+1, stripped))
            elif stripped.startswith("#"):
                heading_code_meta.append((i+1, stripped))
            else:
                visible_code_meta_lines.append((i+1, stripped))
    
    if visible_code_meta_lines or heading_code_meta:
        print(f"\n>>> {ch}")
        if visible_code_meta_lines:
            print(f"  [GORUNUR] Kod icinde // CODE_META ({len(visible_code_meta_lines)} satir):")
            for ln, txt in visible_code_meta_lines:
                print(f"    Satir {ln}: {txt[:80]}")
        if heading_code_meta:
            print(f"  [BASLIK] Baslik olarak CODE_META ({len(heading_code_meta)} satir):")
            for ln, txt in heading_code_meta:
                print(f"    Satir {ln}: {txt[:80]}")
        if hidden_code_meta_lines:
            print(f"  [GIZLI] HTML yorumu ({len(hidden_code_meta_lines)} satir) - OK")
    
    if hidden_code_meta_lines:
        print(f"  [GIZLI] HTML yorumu ({len(hidden_code_meta_lines)} satir) - OK")

print()
print("=== COZUM ONERILERI ===")
print("1. Kod icindeki // CODE_META satirlari: KALDIRILMALI")
print("2. Basliklardaki CODE_META: KALDIRILMALI")
print("3. HTML yorumu <!-- CODE_META ... -->: DOGRU FORMAT (sadece bu kalmali)")
