"""LLM ile bölüm spesifikasyonu üretme ve doğrulama.

Strateji: LLM önce "ne üreteceğini" planlar (spec), sonra plana göre üretir.
Bu sayede kod blokları, diyagramlar, sözlük gibi yapılar garantilenmiş olur.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from bookmaker.generation.prompts import SYSTEM_AUTHOR, build_system_author

if TYPE_CHECKING:
    from bookmaker.llm.openai import OpenAICompatibleClient

logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# Module-level named constants (replaces magic numbers)
# ------------------------------------------------------------
SPEC_MAX_CHARS: int = 5000

# ============================================================
# SPEC PROMPT
# ============================================================

def build_spec_prompt(
    chapter_title: str,
    concepts: list[str],
    book_context: str = "",
    chapter_no: int | None = None,
    code_language: str = "java",
) -> str:
    """LLM'e bölüm spesifikasyonu üretmesi için prompt."""
    concepts_str = "\n".join(f"  - {c}" for c in concepts)
    no_str = f"Bölüm {chapter_no}: " if chapter_no else ""
    lang = code_language or "java"

    return f"""## Görev: Bölüm Spesifikasyonu Hazırla

**Bölüm:** {no_str}{chapter_title}

**Kapsanacak kavramlar:**
{concepts_str}

{book_context}

---
Aşağıdaki başlıklarla bir PLAN hazırla. SADECE PLAN, kod veya diyagram YAZMA:

1. **KAVRAMLAR** — Her kavram için:
   - Ne olduğu (1 cümle)
   - Zorluk seviyesi (1-5 yıldız)
   - Kod örneği gerekiyor mu? (evet/hayır)
   - Hangi konuyu gösterecek? (1 cümle, kod yazma!)

2. **KOD ÖRNEKLERİ** — Her planlanan örnek için:
   - Hangi kavramı gösteriyor?
   - Dosya adı ne olacak?
   - Kod kaç satır olacak? (tahmini)
   - Hangi {lang.capitalize()} özelliklerini kullanacak?
   KOD BLOĞU YAZMA! Sadece tarif et.

3. **DİYAGRAMLAR** — Uygunsa diyagram planla:
   - Neyi görselleştirecek?
   - Hangi tür? (flowchart/sequence/class)
   - Hangi düğümler olacak? (liste halinde)
   MERMAID KODU YAZMA! Sadece tarif et.

4. **SÖZLÜK** — 10-15 terim adı listele (tanım yazma, sadece terimleri listele)

5. **DEĞERLENDİRME** — 5-10 D/Y sorusu konusu + 5-10 Boşluk Doldurma sorusu
   konusu belirle (çoktan seçmeli YOK, açık uçlu YOK)

6. **ALIŞTIRMALAR** — 2-3 alıştırma konusu ve zorluk seviyesi
   (konuyu tarif et, kodu sonra yazacağız)

7. **SIK YAPILAN HATALAR** — 3-5 hata konusu başlığı (hatanın ne olduğunu 1 cümleyle söyle)

8. **TABLOLAR** — Gerekliyse hangi verilerin karşılaştırılacağını belirt

KESIN KURAL: Bu bir PLAN'dır. ```{lang} veya ```mermaid BLOĞU YAZMAK YASAKTIR.
Sadece ne yapılacağını TARIF ET. Kodun ve diyagramın kendisini sonraki aşamada yazacağız."""


def build_spec_validation_prompt(spec: str, chapter_title: str, code_language: str = "java") -> str:
    """LLM'e spesifikasyonu doğrulatması için prompt."""
    lang = code_language or "java"
    return f"""## Görev: Spesifikasyonu Doğrula

**Bölüm:** {chapter_title}

Aşağıdaki spesifikasyonu kontrol et:

{spec[:2000]}

---
Kontrol et:
1. Tüm kavramlar kapsanmış mı?
2. PLAN formatına uygun mu? (```{lang} veya ```mermaid bloğu OLMAMALI, sadece tarif olmalı)
3. Eksik bölüm var mı?
4. Değerlendirme soruları ve alıştırmalar planlanmış mı?

Cevabını şu formatta ver:
- Geçerliyse: "PASS: [kısa açıklama]"
- Eksik varsa: "REVISION: [eksikler listesi]" """


def build_seed_from_spec_prompt(spec: str, chapter_title: str, code_language: str = "java") -> str:
    """Spesifikasyona dayalı seed generation prompt'u."""
    spec_short = spec[:SPEC_MAX_CHARS]
    if len(spec) > SPEC_MAX_CHARS:
        spec_short += "\n\n... (planin devami var, tum maddeleri isle)"
    lang = code_language or "java"
    lang_cap = lang.capitalize()

    return f"""## Görev: Spesifikasyona Göre Bölüm Üret

**Bölüm:** {chapter_title}

**SPESİFİKASYON (plan — kodları ve diyagramları SEN yazacaksın):**

{spec_short}

---
Spesifikasyon bir PLANDIR, içindeki tariflere göre kodları ve diyagramları SEN üreteceksin.

İÇERİK DERİNLİĞİ KURALLARI:
Her kavramı şu 6 adımla işle (sırayla):
1. TANIM — Kavramı 1-2 net cümleyle tanımla
2. NEDEN VAR? — Hangi problemi çözer?
3. NASIL KULLANILIR? — Çalışan {lang_cap} kodu ile göster, sonra kodu satır satır açıkla
4. NE ZAMAN TERCİH EDİLİR? — Hangi senaryoda bu, hangi senaryoda alternatifi?
5. ALTERNATİFLERİ — Benzer kavramlarla karşılaştırma tablosu yap
6. YAYGIN HATALAR — Bu kavramla ilgili en sık hatayı ve çözümünü belirt

Her adım için 1-2 paragraf yeterli. Günlük hayattan 1 analoji ekle.
Toplam bölüm uzunluğu 6000-8000 kelime arası olsun.

Yazım kuralları:
- H1 = bölüm başlığı, H2 = ana bölümler, H3 = alt bölümler
- Kod yazmaya uygun H2/H3 altında ```{lang} örneği ver
  (Kod ZORUNLU DEĞİL: yol haritası, öğrenme çıktıları, ön bilgi,
   özet, sözlük, sorular, rubrik, kaynaklar, köprü)
- Değişken isimleri anlamlı Türkçe, her kodda 3+ yorum satırı, // Çıktı: ... gösterimi
- Bölüm sonunda: Özet, Sözlük, Sorular, Alıştırmalar, Hatalar
- Spesifikasyonda DİYAGRAMLAR bölümü varsa, HER diyagramı ```mermaid kod bloğu olarak üret
  (en az 5 düğüm, karar noktaları için elmas, altına 1-2 cümle açıklama)

ÖNEMLİ: Spesifikasyondaki HER PLANI içeriğe dönüştür. Hiçbir şeyi atlama."""


# ============================================================
# SPEC FUNCTIONS
# ============================================================

def generate_spec(client: OpenAICompatibleClient, chapter_title: str, concepts: list[str],
                  book_context: str = "", chapter_no: int | None = None,
                  code_language: str = "java") -> str:
    """LLM'e bölüm spesifikasyonu ürettirir.

    Args:
        client: OpenAICompatibleClient instance
        chapter_title: Bölüm başlığı
        concepts: Kapsanacak kavram listesi
        book_context: Kitap bağlamı (hedef kitle vb.)
        chapter_no: Bölüm numarası (None = numarasız)
        code_language: Kod dili (java, python, dart vb.)

    Returns:
        Spesifikasyon metni (Markdown formatında)

    """
    user = build_spec_prompt(chapter_title, concepts, book_context, chapter_no,
                             code_language=code_language)
    system = build_system_author(code_language) if code_language != "java" else SYSTEM_AUTHOR
    logger.info("SPEC: %s plani hazirlaniyor...", chapter_title)
    spec = client.generate_text(system, user)
    logger.info("SPEC: %s kelime, %s karakter", len(spec.split()), len(spec))
    return spec


def validate_spec(client: OpenAICompatibleClient, spec: str, chapter_title: str,
                  code_language: str = "java") -> dict[str, str]:
    """LLM'e spesifikasyonu doğrulatır.

    Args:
        client: OpenAICompatibleClient instance
        spec: Doğrulanacak spesifikasyon metni
        chapter_title: Bölüm başlığı
        code_language: Kod dili

    Returns:
        {"status": "PASS"|"REVISION", "notes": "...", "response": "..."}

    """
    user = build_spec_validation_prompt(spec, chapter_title,
                                        code_language=code_language)
    system = build_system_author(code_language) if code_language != "java" else SYSTEM_AUTHOR
    logger.info("VALIDATE: Spesifikasyon kontrol ediliyor...")
    result = client.generate_text(system, user)
    status = "PASS" if "PASS" in result.upper() else "REVISION"
    logger.info("VALIDATE: %s, %s kelime", status, len(result.split()))
    return {"status": status, "notes": result, "response": result}
