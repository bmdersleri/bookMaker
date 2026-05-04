#!/usr/bin/env python3
"""Check heading structure of all chapters."""
import os, re

CHAPTERS_DIR = 'chapters'
order = [
    'bolum-01','bolum-02','bolum-03','bolum-04','bolum-05','bolum-06',
    'bolum-07','bolum-08','bolum-09','bolum-10','bolum-11',
    'bolum-12','bolum-13','bolum-14','bolum-15','bolum-16',
    'bolum-17','bolum-18','bolum-19','bolum-20','bolum-21',
    'bolum-22','bolum-23',
    'ek-a','ek-b','ek-c','ek-d'
]

print("=" * 80)
print("MEVCUT BASLIK YAPISI")
print("=" * 80)

for idx, ch in enumerate(order, 1):
    path = os.path.join(CHAPTERS_DIR, ch, 'draft_versions', 'v001.md')
    if not os.path.exists(path):
        print(f"{idx:2d}. {ch}: DOSYA YOK!")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    content = ''.join(lines)
    
    # Find first H1 after front matter
    in_fm = False
    first_h1 = None
    h1_line_num = None
    h2_list = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '---':
            in_fm = not in_fm
            continue
        if in_fm:
            continue
        
        if stripped.startswith('# ') and not stripped.startswith('## '):
            if first_h1 is None:
                first_h1 = stripped[2:].strip()
                h1_line_num = i + 1
        elif stripped.startswith('## ') and not stripped.startswith('### '):
            h2_list.append((i + 1, stripped[3:].strip()))
    
    if first_h1:
        print(f"\n{idx:2d}. {ch} (satir {h1_line_num}):")
        print(f"     H1: {first_h1[:80]}")
        h2_preview = h2_list[:3]
        for ln, h2 in h2_preview:
            print(f"     H2 @{ln}: {h2[:70]}")
        if len(h2_list) > 3:
            print(f"     ... +{len(h2_list)-3} more H2")
    else:
        # Try to find any heading at all
        print(f"\n{idx:2d}. {ch}: H1 YOK!")
        # Find first heading
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('#') and not stripped.startswith('## '):
                print(f"     Bulunan: satir {i+1}: {stripped[:80]}")
                break
        else:
            print(f"     Hic baslik bulunamadi!")
            # Show first non-empty, non-front-matter line
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and stripped != '---':
                    print(f"     Ilk icerik @{i+1}: {stripped[:80]}")
                    break
