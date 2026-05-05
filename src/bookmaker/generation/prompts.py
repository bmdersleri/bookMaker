"""Sade ve işlevsel prompt şablonları.
Strateji: Aşama 1'de LLM serbestçe içerik üretir, Aşama 2'de kod normalleştirir,
Aşama 3'te LLM eksik kısımları doldurur (hedefli, küçük çağrılar).
"""

from __future__ import annotations

# ============================================================
# AŞAMA 0: SISTEM PROMPT — Yazar Personası
# ============================================================
# Çok kısa, çok net. LLM'in nasıl bir yazar olduğunu tanımlar.
# ============================================================

SYSTEM_AUTHOR = """Sen, Türkçe programlama kitabı yazan kıdemli bir teknik yazarsın.

Yazı dilin:
- Akademik ama sade: Karmaşık kavramları basit örneklerle açıklarsın
- Uygulama odaklı: Her kavramın hemen ardından çalışan Java kodu verirsin
- Hedef kitle: Java'ya sıfırdan başlayan, temel programlama mantığını bilen öğrenciler
- Her bölümde mutlaka en az bir Mermaid akış diyagramı kullanırsın
- Derinlemesine açıklama: Her kavramı en az 3-5 paragraf ile açıklar, günlük hayattan analojilerle somutlaştırırsın
- "Neden?" odaklı: Her kavramın önce neden var olduğunu, hangi problemi çözdüğünü anlatır, sonra nasıl kullanıldığını gösterirsin
- Karşılaştırmalı anlatım: Benzer kavramları yan yana koyar, farklarını ve hangi durumda hangisinin tercih edileceğini açıklarsın
- Tarihsel bağlam: Önemli kavramların Java ekosistemindeki gelişimini kısaca belirtirsin (hangi sürümde geldi, neden eklendi)"""


# ============================================================
# AŞAMA 1: SEED PROMPT — Bölüm Üretimi (tek çağrı)
# ============================================================
# LLM sadece içeriğe odaklanır. Format kaygısı yok.
# ============================================================

def build_seed_prompt(
    chapter_title: str,
    concepts: list[str],
    outline: str | None = None,
    chapter_no: int | None = None,
) -> str:
    """Bölüm üretimi için seed prompt'u oluşturur.

    Args:
        chapter_title: Bölüm başlığı (örn. "Dosya İşlemleri ve Kalıcı Veri Saklama")
        concepts: Bölümde işlenecek temel kavramlar
        outline: Varsa bölüm outline'ı (H2 başlıkları)
        chapter_no: Varsa bölüm numarası

    Returns:
        LLM'e gönderilecek kullanıcı prompt'u
    """
    # Kavramları madde işaretine çevir
    concepts_str = "\n".join(f"  - {c}" for c in concepts)

    # Outline varsa ekle
    outline_str = ""
    if outline:
        outline_str = f"\nOutline:\n{outline}\n"

    # Bölüm numarası
    no_str = f"Bölüm {chapter_no}: " if chapter_no else ""

    return f"""## {no_str}{chapter_title}

**Kapsanan kavramlar:**
{concepts_str}{outline_str}

---
İÇERİK DERİNLİĞİ KURALLARI (EN ÖNEMLİ):
- Her kavramı EN AZ 3-5 PARAGRAF ile detaylı açıkla. Kısa geçme!
- Her kavram için şu yapıyı kullan: NEDEN var? → NE işe yarar? → NASIL kullanılır? → NE ZAMAN tercih edilir?
- Günlük hayattan analojilerle kavramları somutlaştır (örnek: "arayüzler, elektrik prizi gibidir — neyin takıldığı değil, nasıl takıldığı önemlidir")
- Benzer kavramları karşılaştır: farkları, avantajları, hangi durumda hangisi seçilmeli?
- Önemli kavramların tarihsel gelişimini kısaca belirt (Java'nın hangi sürümünde geldi?)

YAZIM KURALLARI:
- H1 = bölüm başlığı, H2 = ana bölümler, H3 = alt bölümler
- Java kodları ```java bloklarında olsun (HER H2 ALTINDA MUTLAKA ÇALIŞAN ```java KOD ÖRNEĞİ OLMALI)
- Kod örnekleri açıklayıcı yorumlar içersin, çıktıları örnek olarak göster
- İstersen ```mermaid bloklarında diyagram ekleyebilirsin
- Bölüm sonunda mutlaka:
  ## Bölüm özeti
  ## Terim sözlüğü (en az 10 terim, her biri **Terim** — Açıklama formatında)
  ## Kendini değerlendirme soruları (3 adet: 1 D/Y, 1 açık uçlu, 1 kod okuma)
  ## Programlama alıştırmaları (2 adet: 1 kolay, 1 orta)

Yalnızca içeriğe odaklan. Front matter, meta etiketi, CSS, HTML veya format detayı ekleme."""


# ============================================================
# AŞAMA 3: ENRICHMENT PROMPTLARI — Eksik Kısımları Doldurma
# ============================================================
# Her biri bağımsız, küçük, hedefli LLM çağrıları.
# Context olarak bölüm başlığı + H2 başlıkları + ilk 500 karakter yeterli.
# ============================================================

def build_enrich_glossary_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
) -> str:
    """Terim sözlüğü üretimi için enrichment prompt'u."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

Bölümden bir kesit:
{context[:500]}

Bu bölüm için 10-15 maddelik bir terim sözlüğü yaz.
Her madde şu formatta:
**Terim** — Açıklama (tek cümle)

Yalnızca sözlüğü üret, başka bir şey ekleme."""


def build_enrich_questions_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
) -> str:
    """Kendini değerlendirme soruları üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

Bölümden bir kesit:
{context[:500]}

Bu bölüm için 3 kendini değerlendirme sorusu yaz:

1. **Doğru/Yanlış** — Cevabı ve kısa açıklamasıyla
2. **Açık uçlu** — Kavramsal bir soru, cevabıyla
3. **Kod okuma** — Kısa bir Java kodu ver, çıktısını sor

Her sorunun cevabını da ekle. Yalnızca soruları üret."""


def build_enrich_exercises_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
) -> str:
    """Programlama alıştırmaları üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

Bölümden bir kesit:
{context[:500]}

Bu bölüm için 2 programlama alıştırması yaz:

1. **Kolay seviye** (10-15 satır Java kodu)
   - Amaç, görev, ipucu, beklenen çıktı

2. **Orta seviye** (20-30 satır Java kodu)
   - Amaç, görev, ipucu, beklenen çıktı

Yalnızca alıştırmaları üret, başka bir şey ekleme."""


def build_enrich_summary_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
) -> str:
    """Bölüm özeti üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

Bölümden bir kesit:
{context[:500]}

Bu bölüm için 3-5 cümlelik bir özet yaz.
Bölümde öğrenilen ana kavramları ve kazanımları vurgula.
Yalnızca özet metnini üret."""


def build_enrich_bridge_prompt(
    chapter_title: str,
    next_chapter: str | None,
    headings: list[str],
    context: str,
) -> str:
    """Sonraki bölüme köprü üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    next_str = f"Bir sonraki bölüm: {next_chapter}" if next_chapter else ""
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

{next_str}

Bölümden bir kesit:
{context[:500]}

Bu bölümün sonu için 2-3 cümlelik bir köprü yaz.
Bugünkü bilgilerin bir sonraki bölüme nasıl temel oluşturduğunu anlat.
Yalnızca köprü metnini üret."""


def build_enrich_errors_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
) -> str:
    """Sık yapılan hatalar bölümü üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

Bölümden bir kesit:
{context[:500]}

Bu bölümün konusuyla ilgili 3-5 tane sık yapılan hata ve yanlış sezgi yaz.
Her hata için: hatanın ne olduğu, neden yapıldığı ve nasıl düzeltileceği.

Yalnızca hataları üret, başka bir şey ekleme."""


def build_enrich_deepen_prompt(
    chapter_title: str,
    section_heading: str,
    section_content: str,
) -> str:
    """Teorik derinleştirme için enrichment prompt'u.

    Mevcut bir bölümü alır, teorik açıklamaları genişletir.
    Kod örneklerine dokunmaz, sadece açıklamaları derinleştirir.
    """
    return f"""Bölüm: {chapter_title}
Alt Bölüm: {section_heading}

MEVCUT İÇERİK:
{section_content[:3000]}

---
GÖREV: Bu alt bölümün teorik açıklamalarını EN AZ 2 KATINA çıkar.

KURALLAR:
- Mevcut kod örneklerine DOKUNMA, onları aynen koru
- Her kavramı şu yapıyla derinleştir: NEDEN var? → Hangi problemi çözer? → Alternatifleri neler? → Ne zaman kullanılır?
- Günlük hayattan en az 1 analoji ekle
- Benzer kavramlarla karşılaştırma yap (farklar, avantaj/dezavantaj)
- Kod örneklerinden sonra "Bu kod ne yapıyor?" şeklinde satır satır açıklama ekle
- Önemli kavramların Java'daki tarihsel gelişimini kısaca belirt

ÇIKTI FORMATI:
- Aynı başlık yapısını koru (H2, H3 aynı kalsın)
- Mevcut metni genişlet, kısaltma
- Kod bloklarını aynen koru
- Yalnızca genişletilmiş alt bölüm içeriğini üret, başka bir şey ekleme"""
