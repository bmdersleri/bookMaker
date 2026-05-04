"""Üretim prompt şablonları."""

from __future__ import annotations

SYSTEM_PROMPT_OUTLINE = """Sen deneyimli bir teknik kitap editörüsün.
Verilen konu ve amaç doğrultusunda ayrıntılı bir bölüm outline'ı hazırlayacaksın.

Outline:
- Tek H1 başlık
- En az 5 H2 alt bölüm
- Her H2 altında gerekirse H3 detayları
- Kod örneklerinin yer alacağı bölümleri işaretle
- Pedagojik akış: kavram → örnek → uygulama → değerlendirme
"""

SYSTEM_PROMPT_CHAPTER = """Sen deneyimli bir teknik kitap yazarı ve pedagojik içerik uzmanısın.
Verilen outline ve seed bilgisine gore CHAPTER_SPEC.md uyumlu
eksiksiz bir bolum Markdown metni ureteceksin.

YAML FRONT MATTER (mutlaka dosyanin en basinda olmali):
---
title: "[Bolum basligi]"
subtitle: "Java'nin Temelleri"
author: "Ismail Kirbas"
date: "2026"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
repo: bmdersleri
project-alias: javanintemelleri
chapter-alias: [chapter_id]
chapter_id: [chapter_id]
chapter_type: core
automation_profile: academic_technical_book_v1
numbering: auto
github_slug: [chapter_id]
qr_policy: dual_for_code_examples
asset_policy: manual_override
---

Kurallar:
1. YAML front matter ILE BASLA (yukaridaki gibi).
2. Basliklar elle numaralandirilmasin.
3. Her kod blogundan once CODE_META blogu olsun.
4. Kod ornekleri Java olsun, dosya adi public class adiyla uyumlu olsun.
5. Pedagojik kutular icin blockquote kullan.
6. Bolum sonunda ozet, terim sozlugu, sorular ve alistirmalar olsun.
"""

SYSTEM_PROMPT_BOOK = """Sen deneyimli bir teknik kitap yazarısın.
Verilen konu başlığı için eksiksiz bir kitap outline'ı hazırlayacaksın.

Kitap yapısı:
- Kısımlara ayrılmış bölümler
- Her bölüm için amaç, öğrenme çıktıları ve zorunlu kavramlar
- Bölüm başına 2-3 kod örneği planı
- Her bölüm için mini uygulama fikri
"""


def outline_prompt(topic: str, purpose: str = "") -> tuple[str, str]:
    """Outline üretimi için prompt çifti döndürür."""
    user = (
        f"Konu: {topic}\nAmaç: {purpose or 'Temel kavramları öğretmek'}\n"
        "Ayrıntılı bir outline hazırla."
    )
    return SYSTEM_PROMPT_OUTLINE, user


def chapter_prompt(
    chapter_title: str,
    outline_text: str,
    purpose: str = "",
    concepts: list[str] | None = None,
) -> tuple[str, str]:
    """Bölüm üretimi için prompt çifti."""
    concepts_str = "\n".join(f"- {c}" for c in (concepts or []))
    user = (
        f"Bölüm: {chapter_title}\n\n"
        f"Amaç: {purpose or 'Temel kavramları öğretmek'}\n\n"
        f"Outline:\n{outline_text}\n\n"
    )
    if concepts_str:
        user += f"Zorunlu kavramlar:\n{concepts_str}\n\n"
    user += "Yukarıdaki outline'a göre eksiksiz bölüm metnini üret."
    return SYSTEM_PROMPT_CHAPTER, user


def book_prompt(topic: str, language: str = "tr-TR", audience: str = "") -> tuple[str, str]:
    """Kitap outline'ı üretimi için prompt çifti."""
    user = (
        f"Kitap konusu: {topic}\nDil: {language}\n"
        f"Hedef kitle: {audience or 'Başlangıç düzeyi programcılar'}\n\n"
        "Kısımlara ayrılmış, amaç ve öğrenme çıktılarıyla kitap outline'ı hazırla."
    )
    return SYSTEM_PROMPT_BOOK, user
