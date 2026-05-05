"""Normalizasyon — LLM çıktısını yapılandırılmış bölüm dosyasına dönüştürür.
Hiçbir meta etiketi (CODE_META, SECTION_META) kullanılmaz.
Tüm format işlemleri Python kodu ile yapılır."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from bookmaker.core.config import BookConfig
from bookmaker.generation.clean_text import TextCleaner


# ============================================================
# HEADING NORMALIZASYONU
# ============================================================

def normalize_headings(text: str) -> str:
    """Heading seviyelerini düzeltir:
    - İlk # H1 olarak kalır, sonraki tüm #'lar ## olur (H2)
    - H1 başlığından "Bölüm N:", "Chapter N:" öneki temizlenir
    - H3 ve H4 seviyeleri korunur
    - Front matter (---) atlanır
    - Kod blokları içi atlanır
    """
    lines = text.splitlines()
    result = []
    in_front_matter = text.lstrip().startswith("---")
    in_code_block = False
    found_h1 = False

    for line in lines:
        stripped = line.rstrip()

        # Front matter geçişi
        if in_front_matter and stripped == "---":
            in_front_matter = False
            result.append(line)
            continue

        # Kod blokları
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_front_matter or in_code_block:
            result.append(line)
            continue

        # Heading düzeltme
        match = re.match(r"^(#{1,6})\s+", stripped)
        if match:
            level = len(match.group(1))
            if level == 1:
                if not found_h1:
                    found_h1 = True
                    # H1 başlığından "Bölüm N:", "Chapter N:" önekini temizle
                    heading_text = stripped[match.end():]
                    cleaned = re.sub(
                        r'^(Bölüm|Chapter|Bolum)\s+\d+[:\-.]\s*',
                        '', heading_text, flags=re.IGNORECASE
                    ).strip()
                    if cleaned:
                        line = "# " + cleaned
                else:
                    # İkinci H1 → H2'ye düşür
                    line = "##" + line[line.index("#") + 1:]
            elif level > 4:
                # H5/H6 → H4'e yükselt
                line = "####" + line[line.index("#") + len(match.group(1)):]

        result.append(line)

    return "\n".join(result)


# ============================================================
# FRONT MATTER
# ============================================================

def build_front_matter(chapter_id: str, title: str, config: Optional[BookConfig] = None) -> str:
    """book_profile.yaml'daki bilgileri kullanarak YAML front matter olusturur.

    Args:
        chapter_id: Bolum kimligi (orn. bolum-16)
        title: Bolum basligi
        config: Kitap config (None = varsayilan degerler, str = uyari + varsayilan)

    Returns:
        YAML front matter blogu (--- ile cevrili)

    Not: config yanlislikla string gecilirse uyari verir, varsayilan degerlerle
    devam eder (cokmez). normalize() fonksiyonu icinden dogru cagrilir:
        ensure_front_matter(text, chapter_id, title, config)
        -> build_front_matter(chapter_id, title, config)
    """
    # Saglamlik: yanlislikla string gecilmisse uyar
    if isinstance(config, str):
        import warnings
        warnings.warn(
            f"build_front_matter: 'config' parametresine BookConfig yerine "
            f"string gecildi ('{config[:50]}...'). Varsayilan degerler kullaniliyor. "
            f"Dogru kullanim: build_front_matter(chapter_id, title, config)",
            UserWarning, stacklevel=2,
        )
        config = None

    # Config'ten degerleri al (yoksa varsayilan)
    author = config.author if config else "Ismail Kirbas"
    year = config.year if config else 2026
    subtitle = f'"{config.title}"' if config else "\"Java'nin Temelleri\""
    repo = config.github_slug if config else "javanintemelleri"

    return f"""---
title: "{title}"
subtitle: {subtitle}
author: "{author}"
date: "{year}"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
repo: bmdersleri
project-alias: javanintemelleri
chapter-alias: {chapter_id}
chapter_id: {chapter_id}
chapter_type: core
automation_profile: academic_technical_book_v1
numbering: auto
github_slug: {chapter_id}
qr_policy: dual_for_code_examples
asset_policy: manual_override
---"""
def ensure_front_matter(text: str, chapter_id: str, title: str,
                        config: Optional[BookConfig] = None) -> str:
    """Metnin başına front matter ekler (H1 başlığı korur)."""
    if text.lstrip().startswith("---"):
        # Mevcut front matter varsa koru
        end = text.find("---", 3)
        if end != -1:
            return text
    # Front matter yoksa başa ekle, H1'i koru
    fm = build_front_matter(chapter_id, title, config)
    return fm + "\n\n" + text.lstrip("\n")


# ============================================================
# BÖLÜM AYRIŞTIRMA
# ============================================================

def extract_sections(text: str) -> list[dict]:
    """Metni H2 başlıklarına göre bölümlere ayırır.

    Returns:
        [{'heading': 'Bölüm özeti', 'content': '...', 'order': 1}, ...]
    """
    in_front_matter = text.lstrip().startswith("---")
    in_code_block = False
    sections = []
    current_heading = None
    current_lines = []
    order = 0

    for line in text.splitlines():
        stripped = line.rstrip()

        # Front matter geçişi
        if in_front_matter and stripped == "---":
            in_front_matter = False
            continue
        if in_front_matter:
            continue

        # Kod blokları
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if current_heading is not None:
                current_lines.append(line)
            continue

        if in_code_block:
            if current_heading is not None:
                current_lines.append(line)
            continue

        # H1 başlık (front matter'dan hemen sonraki)
        if re.match(r"^#\s+", stripped):
            if current_heading is not None:
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_lines),
                    "order": order,
                })
                order += 1
            current_heading = "__title__"  # Özel: bölüm başlığı
            current_lines = []
            continue

        # H2 başlık
        if re.match(r"^##\s+", stripped):
            if current_heading is not None:
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_lines),
                    "order": order,
                })
                order += 1
            current_heading = stripped.lstrip("# ")
            current_lines = []
            continue

        if current_heading is not None:
            current_lines.append(line)

    # Son bölümü ekle
    if current_heading is not None and current_lines:
        sections.append({
            "heading": current_heading,
            "content": "\n".join(current_lines),
            "order": order,
        })

    return sections


# ============================================================
# EKSİK BÖLÜM TESPİTİ
# ============================================================

_STANDARD_END_SECTIONS = {
    "özet": "Bölüm özeti",
    "sözlük": "Terim sözlüğü",
    "soru": "Kendini değerlendirme soruları",
    "alıştırma": "Programlama alıştırmaları",
    "hata": "Sık yapılan hatalar",
    "köprü": "Bir sonraki bölüme",
    "laboratuvar": "Laboratuvar",
    "proje": "Proje görevi",
    "rubrik": "Değerlendirme rubriği",
    "kaynak": "İleri okuma",
}


def detect_missing_sections(text: str) -> list[dict]:
    """Hangi standart bölüm sonu yapılarının eksik olduğunu tespit eder.

    Returns:
        [{'key': 'özet', 'title': 'Bölüm özeti', 'existing': False}, ...]
    """
    text_lower = text.lower()
    sections = extract_sections(text)
    existing_headings = [s["heading"].lower() for s in sections]

    missing = []
    for key, title in _STANDARD_END_SECTIONS.items():
        # Başlıkta geçiyor mu kontrol et
        found = any(key in h for h in existing_headings)
        missing.append({
            "key": key,
            "title": title,
            "existing": found,
        })

    return missing


# ============================================================
# KOD / MERMAID ÇIKARMA
# ============================================================

def extract_code_blocks(text: str, language: str = "java") -> list[dict]:
    """Belirtilen dildeki kod bloklarını çıkarır.

    Returns:
        [{'index': 0, 'code': '...', 'language': 'java', 'start': 100, 'end': 250}, ...]
    """
    pattern = re.compile(
        r"```" + language + r"\s*\n(.*?)```", re.DOTALL
    )
    return [
        {
            "index": i,
            "code": match.group(1).strip(),
            "language": language,
            "start": match.start(),
            "end": match.end(),
        }
        for i, match in enumerate(pattern.finditer(text))
    ]


def extract_mermaid_blocks(text: str) -> list[dict]:
    """Mermaid bloklarını çıkarır.

    Returns:
        [{'index': 0, 'code': '...', 'start': 100, 'end': 250}, ...]
    """
    pattern = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
    return [
        {
            "index": i,
            "code": match.group(1).strip(),
            "start": match.start(),
            "end": match.end(),
        }
        for i, match in enumerate(pattern.finditer(text))
    ]


# ============================================================
# BİRLEŞTİRME
# ============================================================

def insert_section(text: str, section_title: str, section_content: str,
                  before_heading: Optional[str] = None) -> str:
    """Metne yeni bir H2 bölümü ekler.

    Args:
        text: Mevcut metin
        section_title: Eklenecek bölüm başlığı (sadece metin, ## eklenir)
        section_content: Bölüm içeriği (markdown)
        before_heading: Varsa bu başlıktan önce ekle

    Returns:
        Güncellenmiş metin
    """
    new_section = f"\n\n## {section_title}\n\n{section_content.strip()}\n"

    if before_heading:
        # Belirtilen başlıktan önce ekle
        pattern = rf"(^|\n)(##\s+{re.escape(before_heading)})"
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            pos = match.start(2)
            return text[:pos] + new_section + "\n" + text[pos:]
        # Başlık bulunamazsa sona ekle
        return text.rstrip() + new_section

    # Sona ekle
    return text.rstrip() + new_section


# ============================================================
# ANA NORMALİZASYON FONKSİYONU
# ============================================================

def normalize(
    text: str,
    chapter_id: str,
    title: str,
    config: Optional[BookConfig] = None,
) -> str:
    """LLM çıktısını normalize eder: temizlik + başlıklar + front matter.

    Sıra:
    1. TextCleaner ile tırnak/boşluk/yazım düzelt (0 token)
    2. Heading seviyelerini düzelt
    3. Front matter ekle/koru
    4. Fazla boşlukları temizle

    Args:
        text: Ham LLM çıktısı
        chapter_id: Bölüm kimliği
        title: Bölüm başlığı
        config: Kitap config

    Returns:
        Normalize edilmiş bölüm metni
    """
    text = TextCleaner.clean(text)
    text = normalize_headings(text)
    text = ensure_front_matter(text, chapter_id, title, config)
    return text.strip() + "\n"


# ============================================================
# H2 BÖLÜM AYIKLAMA — Teorik derinleştirme için
# ============================================================

def extract_h2_sections(text: str) -> list[dict[str, str]]:
    """Metni H2 başlıklarına göre bölümlere ayırır.

    Her bölüm: {"heading": "H2 başlığı", "content": "içerik"}
    H1 başlığından önceki kısım "__preamble__" olarak döner.

    Kod blokları içindeki ## işaretleri heading sayılmaz.
    """
    sections = []
    lines = text.splitlines()
    current_heading = "__preamble__"
    current_lines = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        # Kod bloğu geçişi
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            current_lines.append(line)
            continue

        if in_code_block:
            current_lines.append(line)
            continue

        # H2 başlık tespiti
        if re.match(r"^##\s+", stripped) and not re.match(r"^###+\s", stripped):
            # Önceki bölümü kaydet
            if current_lines:
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_lines).strip(),
                })
            current_heading = re.sub(r"^##\s+", "", stripped).strip()
            current_lines = [line]
            continue

        current_lines.append(line)

    # Son bölümü kaydet
    if current_lines:
        sections.append({
            "heading": current_heading,
            "content": "\n".join(current_lines).strip(),
        })

    return sections


def deepen_theory(
    sections: list[dict[str, str]],
    deepen_fn,
    chapter_title: str,
    min_chars: int = 500,
) -> list[dict[str, str]]:
    """Her H2 bölümünü LLM ile teorik olarak derinleştirir.

    Args:
        sections: extract_h2_sections() çıktısı
        deepen_fn: (section_heading, section_content) -> genişletilmiş içerik
                   dönen çağrılabilir (genellikle LLM çağrısı)
        chapter_title: Bölüm başlığı
        min_chars: Bu karakterden kısa bölümler atlanır (ön söz vs.)

    Returns:
        Derinleştirilmiş bölümler listesi (aynı yapıda)
    """
    deepened = []
    for sec in sections:
        if sec["heading"] == "__preamble__":
            deepened.append(sec)
            continue
        if len(sec["content"]) < min_chars:
            deepened.append(sec)
            continue
        try:
            expanded = deepen_fn(
                chapter_title=chapter_title,
                section_heading=sec["heading"],
                section_content=sec["content"],
            )
            if expanded and len(expanded) > len(sec["content"]) * 0.5:
                # Hiçbir zaman içeriği küçültme
                if len(expanded) < len(sec["content"]):
                    deepened.append(sec)
                    print(f"    [deepen] '{sec['heading'][:50]}': "
                          f"küçülme tespit edildi ({len(sec['content'])} → {len(expanded)}), orijinal korundu")
                # Aşırı büyümeyi engelle: 3 kattan fazla büyüdüyse orijinali koru
                elif len(expanded) > len(sec["content"]) * 3:
                    deepened.append(sec)
                    print(f"    [deepen] '{sec['heading'][:50]}': "
                          f"aşırı büyüme ({len(sec['content'])} → {len(expanded)}), orijinal korundu")
                else:
                    deepened.append({"heading": sec["heading"], "content": expanded})
                    print(f"    [deepen] '{sec['heading'][:50]}': "
                          f"{len(sec['content'])} → {len(expanded)} karakter")
            else:
                deepened.append(sec)
                print(f"    [deepen] '{sec['heading'][:50]}': atlandı (yeterli genişleme yok)")
        except Exception as e:
            print(f"    [deepen] '{sec['heading'][:50]}': HATA — {e}")
            deepened.append(sec)
    return deepened


def reassemble_from_sections(sections: list[dict[str, str]]) -> str:
    """Derinleştirilmiş bölümleri tekrar birleştirir."""
    parts = []
    for sec in sections:
        if sec["heading"] == "__preamble__":
            parts.append(sec["content"])
        else:
            # Heading zaten content içinde ilk satır olarak var
            parts.append(sec["content"])
    return "\n\n".join(parts)
