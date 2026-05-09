#!/usr/bin/env python3
"""Kod blogu icinde gorunur CODE_META kaldi mi kontrol et"""
import re, pathlib

d = pathlib.Path(r"D:\bookMaker_Deepseek\chapters")
total_visible = 0
total_hidden = 0

for ch in sorted(d.iterdir()):
    if not ch.is_dir() or not (ch.name.startswith("bolum") or ch.name.startswith("ek-")):
        continue
    f = ch / "draft_versions" / "v001.md"
    if not f.exists():
        continue
    
    text = f.read_text("utf-8-sig")
    lines = text.split("\n")
    in_block = False
    visible = 0
    hidden = 0
    
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            in_block = not in_block
            continue
        if "CODE_META" not in s:
            continue
        
        # Kod blogu icinde -> gorunur
        if in_block:
            visible += 1
        # Kod blogu disinda HTML yorumu -> gizli (dogru format)
        elif s.startswith("<!--"):
            hidden += 1
        else:
            visible += 1
    
    if visible:
        print(f"  [GORUNUR] {ch}: {visible} satir")
    total_visible += visible
    total_hidden += hidden

print(f"\nGorunur CODE_META: {total_visible}")
print(f"Gizli (dogru format): {total_hidden}")
print("OK" if total_visible == 0 else "HALA SORUN VAR")
