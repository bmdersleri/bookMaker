#!/usr/bin/env python3
"""Kaynak bolum dosyalarindaki Mermaid bloklarini duzelt"""
import re

fixes = {
    # B13: java.util.Date() parantez sorunu
    r"D:\bookMaker_Deepseek\chapters\bolum-13\draft_versions\v001.md": [
        (r'(B1\[)java\.util\.Date bugun = new java\.util\.Date\(\)(\])', 
         r'\1"java.util.Date bugun = new java.util.Date()"\2'),
        (r'(B1 --> F\[)Avantaj: Çakışma Yok(\])', 
         r'\1"Avantaj: Cakisma Yok"\2'),
        (r'(B1 --> G\[)Dezavantaj: Uzun Kod(\])', 
         r'\1"Dezavantaj: Uzun Kod"\2'),
    ],
    
    # B16: exists() createNewFile() vb. parantez sorunu
    r"D:\bookMaker_Deepseek\chapters\bolum-16\draft_versions\v001.md": [
        (r'(E\[)exists\(\) metodu(\])', r'\1"exists() metodu"\2'),
        (r'(F\[)createNewFile\(\) metodu(\])', r'\1"createNewFile() metodu"\2'),
        (r'(G\[)mkdir\(\) metodu(\])', r'\1"mkdir() metodu"\2'),
        (r'(H\[)delete\(\) metodu(\])', r'\1"delete() metodu"\2'),
    ],
    
    # B17: <br/> HTML etiketlerini kaldir
    r"D:\bookMaker_Deepseek\chapters\bolum-17\draft_versions\v001.md": [
        (r'<br/>', r' '),  # Tum br etiketlerini boslukla degistir
    ],
    
    # B18: Cift tirnaklari tek tirnak yap
    r"D:\bookMaker_Deepseek\chapters\bolum-18\draft_versions\v001.md": [
        (r'Gitar: "Ting"', r"Gitar: 'Ting'"),
        (r'Piyano: "Ding"', r"Piyano: 'Ding'"),
        (r'Davul: "Bam"', r"Davul: 'Bam'"),
    ],
    
    # B19: BorderLayout tirnak + parantez
    r"D:\bookMaker_Deepseek\chapters\bolum-19\draft_versions\v001.md": [
        (r'NORTH\("NORTH \(Ust\)"\)', r'NORTH["NORTH (Ust)"]'),
        (r'WEST\("WEST \(Sol\)"\)', r'WEST["WEST (Sol)"]'),
        (r'CENTER\("CENTER \(Merkez\)"\)', r'CENTER["CENTER (Merkez)"]'),
        (r'EAST\("EAST \(Sag\)"\)', r'EAST["EAST (Sag)"]'),
        (r'SOUTH\("SOUTH \(Alt\)"\)', r'SOUTH["SOUTH (Alt)"]'),
    ],
}

for fpath, pattern_list in fixes.items():
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    count = 0
    for old, new in pattern_list:
        new_content, n = re.subn(old, new, content)
        if n > 0:
            print(f"{fpath}: {n} duzeltme ({old[:40]}...)")
            content = new_content
            count += n
    
    if count > 0:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  -> {count} degisiklik kaydedildi")
    else:
        print(f"{fpath}: eslesme bulunamadi")
