#!/usr/bin/env python3
"""Kod blogu icindeki ## CODE_META satirlarini da temizle (v2)"""
import re, pathlib

chapters_dir = pathlib.Path(r"D:\bookMaker_Deepseek\chapters")
order = [f"bolum-{i:02d}" for i in range(1, 24)] + [f"ek-{c}" for c in "abcd"]
removed_total = 0

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
        
        if in_block:
            # Kod blogu icindeki metadata: // CODE_META, // - Purpose:, ## N.N CODE_META, ## N.N Purpose:
            if re.match(r'^\s*(//|[#]+)\s*(CODE_META|- )', stripped):
                changed = True
                continue
            # Kod blogu icindeki <!-- CODE_META -->
            if "CODE_META" in stripped and stripped.startswith("<!--"):
                changed = True
                continue
        else:
            # Kod blogu disindaki CODE_META basliklari
            if stripped.startswith("#") and "CODE_META" in stripped:
                changed = True
                continue
        
        new_lines.append(line)
    
    if changed:
        p.write_text("\n".join(new_lines), "utf-8")
        r = len(lines) - len(new_lines)
        removed_total += r
        print(f"[DUZELTILDI] {ch}: {r} satir")
    else:
        print(f"[TEMIZ]     {ch}")

print(f"\nToplam: {removed_total} satir CODE_META kaldirildi")
