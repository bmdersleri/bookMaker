#!/usr/bin/env python3
"""
fix_numbering.py v2 — Bölüm başlıklarını numaralandır
==================================================
1. H1 başlıklarına "Bölüm N: " veya "Ek X: " ekle
2. H2 alt başlıklarına "N.M" numarası ver (kitap boyunca sürekli)
3. Eksik H1 başlıklarını otomatik oluştur
4. Front matter'daki title alanını da güncelle (eksikse)
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT / "chapters"

CHAPTER_ORDER = [
    ("bolum-01", "Bölüm 1"),
    ("bolum-02", "Bölüm 2"),
    ("bolum-03", "Bölüm 3"),
    ("bolum-04", "Bölüm 4"),
    ("bolum-05", "Bölüm 5"),
    ("bolum-06", "Bölüm 6"),
    ("bolum-07", "Bölüm 7"),
    ("bolum-08", "Bölüm 8"),
    ("bolum-09", "Bölüm 9"),
    ("bolum-10", "Bölüm 10"),
    ("bolum-11", "Bölüm 11"),
    ("bolum-12", "Bölüm 12"),
    ("bolum-13", "Bölüm 13"),
    ("bolum-14", "Bölüm 14"),
    ("bolum-15", "Bölüm 15"),
    ("bolum-16", "Bölüm 16"),
    ("bolum-17", "Bölüm 17"),
    ("bolum-18", "Bölüm 18"),
    ("bolum-19", "Bölüm 19"),
    ("bolum-20", "Bölüm 20"),
    ("bolum-21", "Bölüm 21"),
    ("bolum-22", "Bölüm 22"),
    ("bolum-23", "Bölüm 23"),
    ("ek-a", "Ek A"),
    ("ek-b", "Ek B"),
    ("ek-c", "Ek C"),
    ("ek-d", "Ek D"),
]


def get_chapter_index(chapter_id):
    """Bölümün kitap içindeki sıra numarasını döndür (1-27)."""
    for idx, (cid, _) in enumerate(CHAPTER_ORDER, 1):
        if cid == chapter_id:
            return idx
    return 0


def parse_front_matter(lines):
    """Front matter'ı parse et ve (fm_lines, content_start, content_lines) döndür."""
    in_fm = False
    fm_lines = []
    content_start = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '---':
            if not in_fm:
                in_fm = True
                fm_lines.append(i)
            else:
                content_start = i + 1
                break
    
    return fm_lines, content_start


def extract_title_from_h1(lines, content_start):
    """H1 başlığından title çıkar."""
    for i in range(content_start, len(lines)):
        stripped = lines[i].strip()
        m = re.match(r'^#\s+(.+)$', stripped)
        if m:
            return m.group(1).strip()
    return None


def get_fm_field(fm_text, field):
    """Front matter'dan bir alanın değerini al."""
    m = re.search(r'^' + field + r':\s*(.+)$', fm_text, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def set_fm_field(fm_text, field, value):
    """Front matter'da bir alanı güncelle veya ekle."""
    pattern = r'^(' + field + r':\s*).*$'
    replacement = r'\1' + value
    if re.search(pattern, fm_text, re.MULTILINE):
        return re.sub(pattern, replacement, fm_text, flags=re.MULTILINE)
    else:
        # title yoksa, ilk satırdan sonra ekle (--- satırından sonra)
        lines = fm_text.split('\n')
        # İlk satır ---, ondan sonra ekle
        insert_pos = 1
        lines.insert(insert_pos, f"{field}: {value}")
        return '\n'.join(lines)


def fix_chapter(chapter_id, chapter_label):
    """Tek bir bölüm dosyasını düzelt."""
    path = CHAPTERS_DIR / chapter_id / "draft_versions" / "v001.md"
    if not path.exists():
        print(f"  ! {chapter_id}: dosya yok")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    lines = content.split('\n')
    
    # Front matter parsing
    fm_line_indices, content_start = parse_front_matter(lines)
    if not fm_line_indices:
        print(f"  ! {chapter_id}: front matter yok")
        return False
    
    fm_text = '\n'.join(lines[:content_start])
    
    # Title al
    title = get_fm_field(fm_text, 'title')
    h1_from_body = extract_title_from_h1(lines, content_start)
    
    # Title yoksa H1'den al
    if not title:
        if h1_from_body:
            title = h1_from_body
            # Front matter'a title ekle
            fm_text = set_fm_field(fm_text, 'title', f'"{title}"')
            print(f"    Front matter: title eklendi: {title[:60]}")
        else:
            print(f"  ! {chapter_id}: title ve H1 yok, atlaniyor")
            return False
    
    ch_num = get_chapter_index(chapter_id)
    
    # Yeni H1 oluştur
    if chapter_id.startswith('bolum-'):
        new_h1 = f"# {chapter_label}: {title}"
    else:
        new_h1 = f"# {chapter_label}: {title}"
    
    # İlk H1'i bul ve değiştir
    h1_found = False
    h1_idx = None
    for i in range(content_start, len(lines)):
        stripped = lines[i].strip()
        if re.match(r'^#\s+\S+', stripped) and not stripped.startswith('## '):
            h1_found = True
            h1_idx = i
            break
    
    if not h1_found:
        # H1 yok — front matter'dan sonra ekle
        print(f"    EKSIK H1: \"{new_h1[2:60]}\" eklendi")
        lines.insert(content_start, '')
        lines.insert(content_start + 1, new_h1)
        lines.insert(content_start + 2, '')
        h1_idx = content_start + 1
    else:
        old_h1 = lines[h1_idx][2:].strip()
        if old_h1 == new_h1[2:]:
            print(f"    H1 zaten dogru: \"{old_h1[:60]}\"")
        else:
            print(f"    H1: \"{old_h1[:60]}\" -> \"{new_h1[2:60]}\"")
            lines[h1_idx] = new_h1
    
    # H2 alt başlıklarını numaralandır
    h2_counter = 0
    modified_h2 = []
    for i in range(max(h1_idx + 1, content_start), len(lines)):
        stripped = lines[i].strip()
        if re.match(r'^##\s+\S+', stripped) and not stripped.startswith('### '):
            h2_text = stripped[3:].strip()
            
            # Mevcut numaralandırmayı temizle
            cleaned = re.sub(r'^[\d]+(?:\.[\d]+)*\.?\s*', '', h2_text)
            # Virgül, nokta gibi kalan ayraçları da temizle
            cleaned = re.sub(r'^[\.\s,\-:;]+', '', cleaned).strip()
            
            h2_counter += 1
            new_h2 = f"## {ch_num}.{h2_counter} {cleaned}"
            
            if lines[i].strip() != new_h2:
                print(f"      H2 @{i+1}: \"{stripped[:50]}\" -> \"{new_h2[:60]}\"")
                lines[i] = new_h2
                modified_h2.append(i)
    
    if h2_counter == 0:
        print(f"    UYARI: H2 basligi bulunamadi!")
    else:
        print(f"    {h2_counter} H2 basligina numara verildi ({ch_num}.1 ... {ch_num}.{h2_counter})")
    
    # Front matter'ı güncelle (title eklenmiş olabilir)
    if fm_text != '\n'.join(lines[:content_start]):
        new_fm_lines = fm_text.split('\n')
        for j in range(min(len(new_fm_lines), content_start)):
            lines[j] = new_fm_lines[j]
    
    # Değişiklik varsa yaz
    new_content = '\n'.join(lines)
    if new_content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fm_updated = " (front matter guncellendi)" if 'title:' in new_content[:content_start] and 'title:' not in original[:content_start] else ""
        print(f"    KAYDEDILDI{fm_updated}")
        return True
    else:
        print(f"    Degisiklik yok")
        return False


def main():
    print("=" * 70)
    print("BOLUM BASLIK NUMARALANDIRMA ARACI v2")
    print("=" * 70)
    
    fixed_count = 0
    for ch_id, ch_label in CHAPTER_ORDER:
        print(f"\n{ch_label} ({ch_id}):")
        if fix_chapter(ch_id, ch_label):
            fixed_count += 1
    
    print(f"\n{'=' * 70}")
    print(f"Toplam {fixed_count}/{len(CHAPTER_ORDER)} dosya duzenlendi")
    print(f"\nMerged markdown'u guncellemek icin:")
    print(f"  python tools/book_build.py --format both")
    print(f"  python tools/book_pdf_v3.py")


if __name__ == "__main__":
    main()
