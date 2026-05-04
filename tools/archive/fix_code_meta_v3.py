#!/usr/bin/env python3
"""Kod blogu icindeki tum metadata satirlarini temizle (v3)"""
import re, pathlib

chapters_dir = pathlib.Path(r"D:\bookMaker_Deepseek\chapters")
order = [f"bolum-{i:02d}" for i in range(1, 24)] + [f"ek-{c}" for c in "abcd"]
removed_total = 0

# Kod blogu icinde temizlenecek desenler
# // CODE_META, // - Purpose:, // - Usage:, ## N.N CODE_META, ## N.N Purpose:, ## N.N Usage:
# <!-- CODE_META: ... -->
patterns_in_block = [
    re.compile(r'^\s*//\s*(CODE_META|- )'),           # // CODE_META, // - Purpose
    re.compile(r'^\s*#+\s*\d+\.\d+\s+CODE_META'),     # ## 1.12 CODE_META
    re.compile(r'^\s*#+\s*\d+\.\d+\s+(Purpose|Usage|Note):'),  # ## 1.13 Purpose:
    re.compile(r'^\s*<!--\s*CODE_META'),               # <!-- CODE_META ...
]

# Kod blogu disinda temizlenecek desenler
patterns_outside = [
    re.compile(r'^#+\s*\d+\.\d+\s+CODE_META'),        # ## 1.12 CODE_META baslik
]

for ch in order:
    p = chapters_dir / ch / "draft_versions" / "v001.md"
    if not p.exists():
        continue
    
    text = p.read_text("utf-8-sig")
    lines = text.split("\n")
    new_lines = []
    in_block = False
    changed = False
    
    for line in lines:
        stripped = line.strip()
        
        # Kod blogu baslangic/bitis
        if stripped.startswith("```"):
            in_block = not in_block
            new_lines.append(line)
            continue
        
        # Kod blogu ICINDE
        if in_block:
            matched = any(pat.search(stripped) for pat in patterns_in_block)
            if matched:
                changed = True
                continue
        # Kod blogu DISINDA
        else:
            matched = any(pat.search(stripped) for pat in patterns_outside)
            if matched:
                changed = True
                continue
        
        new_lines.append(line)
    
    if changed:
        p.write_text("\n".join(new_lines), "utf-8")
        r = len(lines) - len(new_lines)
        removed_total += r
        print(f"[DUZELTILDI] {ch}: -{r} satir")
    else:
        print(f"[TEMIZ]     {ch}")

print(f"\nToplam: {removed_total} satir CODE_META kaldirildi")
