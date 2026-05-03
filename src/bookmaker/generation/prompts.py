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
Verilen outline ve seed bilgisine göre CHAPTER_SPEC.md uyumlu
eksiksiz bir bölüm Markdown metni üreteceksin.

Kurallar:
1. YAML front matter ile başla.
2. Başlıklar elle numaralandırılmasın.
3. Her kod bloğundan önce CODE_META bloğu olsun.
4. Kod örnekleri Java olsun, dosya adı public class adıyla uyumlu olsun.
5. Pedagojik kutular için blockquote kullan.
6. Bölüm sonunda özet, terim sözlüğü, sorular ve alıştırmalar olsun.
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
