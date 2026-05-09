#!/usr/bin/env python3
"""CODE_META gorunurluluk sorunlarini duzelt:
1. Kod blogu icindeki // CODE_META satirlarini kaldir
2. Baslik olarak CODE_META iceren satirlari kaldir
3. Kod blogu icindeki <!-- CODE_META --> HTML yorumlarini kaldir
"""
import re, os

chapters_dir = r"D:\bookMaker_Deepseek\chapters"
order = [f"bolum-{i:02d}" for i in range(1, 24)] + [f"ek-{c}" for c in "abcd"]

total_removed = 0

for ch in order:
    path = os.path.join(chapters_dir, ch, "draft_versions", "v001.md")
    if not os.path.exists(path):
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.split("\n")
    new_lines = []
    
    in_code_block = False
    skip_line = False
    changed = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Kod blogu baslangic/bitis takibi
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
        
        # Kod blogu ICINDEKI CODE_META satirlarini kaldir
        if in_code_block:
            # // CODE_META, // - Purpose:, // - Usage:, // - Note: gibi metadata satirlari
            if re.match(r'^\s*//\s*(CODE_META|- )', stripped):
                changed = True
                continue
            # <!-- CODE_META ... --> HTML yorumu kod blogu icinde (gorunur)
            if stripped.startswith("<!--") and "CODE_META" in stripped:
                changed = True
                continue
        
        # Kod blogu DISINDAKILER
        if not in_code_block:
            # Baslik olarak CODE_META (## 1.12 CODE_META gibi)
            if stripped.startswith("#") and "CODE_META" in stripped:
                changed = True
                continue
            # Bos satirdaki // CODE_META
            if re.match(r'^\s*//\s*CODE_META', stripped):
                changed = True
                continue
        
        new_lines.append(line)
    
    if changed:
        new_content = "\n".join(new_lines)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        removed_count = len(lines) - len(new_lines)
        total_removed += removed_count
        print(f"[DUZELTILDI] {ch}: {removed_count} satir kaldirildi")
    else:
        print(f"[TEMIZ]     {ch}: CODE_META sorunu yok")

print(f"\nToplam: {total_removed} satir CODE_META kaldirildi")
