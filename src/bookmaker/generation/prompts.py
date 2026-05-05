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

Her kavramı şu 6 adımlı zincirle işlersin:
1. TANIM: Kavram nedir? (1-2 cümle, net)
2. NEDEN VAR?: Hangi problemi çözer? Bu kavram olmasaydı ne olurdu?
3. NASIL KULLANILIR?: Çalışan Java kodu ile göster, sonra kodu satır satır açıkla
4. NE ZAMAN TERCİH EDİLİR?: Hangi senaryoda bu, hangi senaryoda alternatifi?
5. ALTERNATİFLERİ: Benzer kavramlarla yan yana karşılaştır, fark tablosu ver
6. YAYGIN HATALAR: Bu kavramla ilgili en sık yapılan 1-2 hatayı ve çözümünü belirt

Mermaid diyagramları (isteğe bağlı, uygun yerlerde kullan):
- Karmaşık akışları görselleştirmek için ```mermaid diyagramı ekleyebilirsin
- Diyagram eklediğinde en az 5 düğüm, karar noktaları (elmas) içersin
- Sadece flowchart değil, uygun yerlerde sequence diagram veya class diagram da kullan
- Diyagramın altında 1-2 cümlelik açıklama olsun

Kod yazma kuralların:
- Değişken isimleri anlamlı ve Türkçe okunabilir olsun (notDegeri, ogrenciListesi gibi)
- Her kod bloğunda en az 3 satır açıklayıcı yorum olsun
- Kod çıktısını örnek olarak göster (// Çıktı: ... şeklinde)
- Aynı bölümdeki kod örnekleri birbiriyle bağlantılı olsun, sonraki öncekini temel alsın

Günlük hayattan analoji zorunludur: her ana kavram için en az 1 somut benzetme yap.
Tarihsel bağlam: Önemli kavramların Java'nın hangi sürümünde geldiğini ve neden eklendiğini belirt."""


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
İÇERİK DERİNLİĞİ KURALLARI:
Her kavramı şu 6 adımla işle (sırayla):
1. TANIM — Kavramı 1-2 net cümleyle tanımla
2. NEDEN VAR? — Hangi problemi çözer? Bu kavram olmasaydı ne eksik kalırdı?
3. NASIL KULLANILIR? — Çalışan Java kodu ile göster, sonra kodu satır satır açıkla
4. NE ZAMAN TERCİH EDİLİR? — Hangi senaryoda bu, hangi senaryoda alternatifi seçilmeli?
5. ALTERNATİFLERİ — Benzer kavramlarla karşılaştırma tablosu yap
6. YAYGIN HATALAR — Bu kavramla ilgili en sık yapılan 1-2 hatayı ve çözümünü belirt

Her adım için 1-2 paragraf yaz. Günlük hayattan 1 analoji ekle.
Toplam bölüm uzunluğu 6000-8000 kelime arası olsun.
Önemli kavramların Java'nın hangi sürümünde geldiğini ve neden eklendiğini belirt.

YAZIM KURALLARI:
- H1 = bölüm başlığı, H2 = ana bölümler, H3 = alt bölümler
- Kod yazmaya uygun her H2 ve H3 altında ```java kod örneği ver
  (Şu başlıklarda kod ZORUNLU DEĞİL: yol haritası, konum/pedagojik rol,
   öğrenme çıktıları, ön bilgi, özet, sözlük, sorular, rubrik, kaynaklar, köprü)
- Değişken isimleri anlamlı Türkçe olsun (notDegeri, ogrenciListesi gibi)
- Her kod bloğunda en az 3 satır açıklayıcı yorum olsun
- Kod çıktısını // Çıktı: ... şeklinde göster
- Karmaşık akışları ```mermaid diyagramı ile görselleştir (isteğe bağlı, en az 5 düğümlü)
- Aynı bölümdeki kod örnekleri birbiriyle bağlantılı olsun
- Bölüm sonunda mutlaka şu başlıklar altında içerik üret:
  ## Bölüm özeti (3-5 cümle, ana kazanımları vurgula)
  ## Terim sözlüğü (en az 10 terim, HER BIRI şu formatta: **Terim** — açıklama. Örnek: **Immutable** — Oluşturulduktan sonra değeri değiştirilemeyen nesne.)
  ## Kendini değerlendirme soruları
    ### Doğru/Yanlış Soruları (5-10 adet, her biri D/Y cevaplı ve açıklamalı)
    ### Boşluk Doldurma Soruları (5-10 adet, her biri cevaplı ve açıklamalı)
    (Çoktan seçmeli soru YOK, açık uçlu soru YOK)
  ## Programlama alıştırmaları (HER BIRI şu formatta:
    **Alıştırma Adı**
    - Amaç: ...
    - Görev: ...
    - İpucu: ...
    - Beklenen Çıktı: ...)

Yalnızca içeriğe odaklan. Front matter, meta etiketi, CSS, HTML veya format detayı ekleme."""


# ============================================================
# AŞAMA 3: ENRICHMENT PROMPTLARI — Eksik Kısımları Doldurma
# ============================================================
# Her biri bağımsız, küçük, hedefli LLM çağrıları.
# Context olarak bölümün başı+sonu + kavram listesi + H2 başlıkları.
# ============================================================

def build_enrich_glossary_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
    concepts: list[str] | None = None,
) -> str:
    """Terim sözlüğü üretimi için enrichment prompt'u."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    concepts_str = "\n".join(f"  - {c}" for c in concepts) if concepts else ""
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

İşlenen kavramlar:
{concepts_str}

Bölüm içeriği (baş ve son):
{context[:2000]}

Bu bölüm için 10-15 maddelik bir terim sözlüğü yaz.
Kavram listesindeki her terimi ve bölümde geçen önemli terimleri kapsa.

HER MADDE ŞU FORMATA KESINLIKLE UYMALI:
**Terim** — Açıklama (tek cümle)

Örnek format:
**Immutable** — Oluşturulduktan sonra değeri değiştirilemeyen nesne.
**String Pool** — JVM'in aynı değerli String literal'larını sakladığı özel bellek alanı.

Tablo, numaralı liste veya başka format KULLANMA. Sadece yukarıdaki format.
Yalnızca sözlüğü üret, başka bir şey ekleme."""


def build_enrich_questions_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
    concepts: list[str] | None = None,
) -> str:
    """Kendini değerlendirme soruları üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    concepts_str = "\n".join(f"  - {c}" for c in concepts) if concepts else ""
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

İşlenen kavramlar:
{concepts_str}

Bölüm içeriği (baş ve son):
{context[:2000]}

Bu bölüm için kendini değerlendirme soruları yaz.
Sorular kavram listesindeki ana konuları kapsasın.

## Doğru/Yanlış Soruları (5-10 adet)
Her soru şu formatta:
**Soru N: [soru metni]**
- Cevap: Doğru / Yanlış
- Açıklama: [1-2 cümle]

## Boşluk Doldurma Soruları (5-10 adet)
Her soru şu formatta:
**Soru N: [içinde boşluk olan cümle]**
- Cevap: [doğru kelime/ifade]
- Açıklama: [1 cümle]

Çoktan seçmeli SORU YAZMA. Açık uçlu soru YAZMA. Kod okuma sorusu YAZMA.
Sadece D/Y ve Boşluk Doldurma. Yalnızca soruları üret."""


def build_enrich_exercises_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
    concepts: list[str] | None = None,
) -> str:
    """Programlama alıştırmaları üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    concepts_str = "\n".join(f"  - {c}" for c in concepts) if concepts else ""
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

İşlenen kavramlar:
{concepts_str}

Bölüm içeriği (baş ve son):
{context[:2000]}

Bu bölüm için 2 programlama alıştırması yaz.
Alıştırmalar kavram listesindeki konuları kapsasın.

HER ALIŞTIRMA ŞU FORMATA KESINLIKLE UYMALI:

**Alıştırma 1: [Ad] (Kolay)**
- Amaç: Bu alıştırmada ne öğreneceksin?
- Görev: Tam olarak ne yapman gerekiyor?
- İpucu: Hangi metodları/sınıfları kullanabilirsin?
- Beklenen Çıktı: Programın ekrana ne yazdırması gerekiyor?

**Alıştırma 2: [Ad] (Orta)**
- Amaç: ...
- Görev: ...
- İpucu: ...
- Beklenen Çıktı: ...

Tablo formatı KULLANMA. Sadece yukarıdaki başlık ve liste formatı.
Yalnızca alıştırmaları üret, başka bir şey ekleme."""


def build_enrich_summary_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
    concepts: list[str] | None = None,
) -> str:
    """Bölüm özeti üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    concepts_str = "\n".join(f"  - {c}" for c in concepts) if concepts else ""
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

İşlenen kavramlar:
{concepts_str}

Bölüm içeriği (baş ve son):
{context[:2000]}

Bu bölüm için 3-5 cümlelik bir özet yaz.
Bölümde öğrenilen ana kavramları ve kazanımları vurgula.
Yalnızca özet metnini üret."""


def build_enrich_bridge_prompt(
    chapter_title: str,
    next_chapter: str | None,
    headings: list[str],
    context: str,
    concepts: list[str] | None = None,
) -> str:
    """Sonraki bölüme köprü üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    next_str = f"Bir sonraki bölüm: {next_chapter}" if next_chapter else ""
    concepts_str = "\n".join(f"  - {c}" for c in concepts) if concepts else ""
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

İşlenen kavramlar:
{concepts_str}

Bölüm içeriği (baş ve son):
{context[:2000]}

{next_str}

Bu bölümün sonu için 2-3 cümlelik bir köprü yaz.
Bugünkü bilgilerin bir sonraki bölüme nasıl temel oluşturduğunu anlat.
Yalnızca köprü metnini üret."""


def build_enrich_errors_prompt(
    chapter_title: str,
    headings: list[str],
    context: str,
    concepts: list[str] | None = None,
) -> str:
    """Sık yapılan hatalar bölümü üretimi."""
    headings_str = "\n".join(f"  - {h}" for h in headings)
    concepts_str = "\n".join(f"  - {c}" for c in concepts) if concepts else ""
    return f"""Bölüm: {chapter_title}

Bölüm başlıkları:
{headings_str}

İşlenen kavramlar:
{concepts_str}

Bölüm içeriği (baş ve son):
{context[:2000]}

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
