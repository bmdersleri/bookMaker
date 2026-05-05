"""LLM ile bölüm spesifikasyonu üretme ve doğrulama.

Strateji: LLM önce "ne üreteceğini" planlar (spec), sonra plana göre üretir.
Bu sayede kod blokları, diyagramlar, sözlük gibi yapılar garantilenmiş olur.
"""

from __future__ import annotations

from typing import Optional

from bookmaker.generation.prompts import SYSTEM_AUTHOR


# ============================================================
# SPEC PROMPT
# ============================================================

def build_spec_prompt(
    chapter_title: str,
    concepts: list[str],
    book_context: str = "",
    chapter_no: Optional[int] = None,
) -> str:
    """LLM'e bölüm spesifikasyonu üretmesi için prompt."""
    concepts_str = "\n".join(f"  - {c}" for c in concepts)
    no_str = f"Bölüm {chapter_no}: " if chapter_no else ""

    return f"""## Görev: Bölüm Spesifikasyonu Hazırla

**Bölüm:** {no_str}{chapter_title}

**Kapsanacak kavramlar:**
{concepts_str}

{book_context}

---
Aşağıdaki başlıklarla detaylı bir spesifikasyon hazırla:

1. **KAVRAMLAR** — Her kavram için: açıklama, zorluk seviyesi, kod örneği gerekip gerekmediği
2. **KOD ÖRNEKLERİ** — Hangi kavramlar için hangi kod örnekleri yazılacak? Her biri neyi gösterecek?
3. **DİYAGRAMLAR** — Gerekliyse mermaid diyagramları (ne görselleştirilecek?)
4. **SÖZLÜK** — 10-15 terim ve kısa tanımları
5. **DEĞERLENDİRME** — 3 soru: 1 doğru/yanlış, 1 açık uçlu, 1 kod okuma
6. **ALIŞTIRMALAR** — 2-3 programlama alıştırması (zorluk seviyeleriyle)
7. **SIK YAPILAN HATALAR** — 3-5 yaygın hata, nedenleri ve çözümleri
8. **TABLOLAR** — Gerekliyse veri yapılarını gösteren tablolar

ÖNEMLİ: Spesifikasyon net ve uygulanabilir olmalı. Kod örneklerinin neyi göstereceğini 
belirt ama kodun kendisini yazma. Sadece plan hazırla."""


def build_spec_validation_prompt(spec: str, chapter_title: str) -> str:
    """LLM'e spesifikasyonu doğrulatması için prompt."""
    return f"""## Görev: Spesifikasyonu Doğrula

**Bölüm:** {chapter_title}

Aşağıdaki spesifikasyonu kontrol et:

{spec[:2000]}

---
Kontrol et:
1. Tüm kavramlar kapsanmış mı?
2. Kod örnekleri uygun mu (başlangıç seviyesine uygun)?
3. Eksik bölüm var mı?
4. Değerlendirme soruları yeterli mi?

Cevabını şu formatta ver:
- Geçerliyse: "PASS: [kısa açıklama]"
- Eksik varsa: "REVISION: [eksikler listesi]" """


def build_seed_from_spec_prompt(spec: str, chapter_title: str) -> str:
    """Spesifikasyona dayalı seed generation prompt'u."""
    return f"""## Görev: Spesifikasyona Göre Bölüm Üret

**Bölüm:** {chapter_title}

**SPESİFİKASYON (BUNA GÖRE ÜRET):**

{spec}

---
Yazım kuralları:
- H1 = bölüm başlığı, H2 = ana bölümler, H3 = alt bölümler
- Spesifikasyonda belirtilen HER kod örneğini ```java bloğunda ver
- Spesifikasyonda belirtilen HER diyagramı ```mermaid bloğunda ver
- Bölüm sonunda: Özet, Sözlük, Sorular, Alıştırmalar, Hatalar
- Sadece içeriğe odaklan, meta etiketi ekleme

ÖNEMLİ: Spesifikasyondaki HER ŞEYİ bölüme ekle. Hiçbir şeyi atlama."""


# ============================================================
# SPEC FUNCTIONS
# ============================================================

def generate_spec(client, chapter_title: str, concepts: list[str],
                  book_context: str = "", chapter_no: Optional[int] = None) -> str:
    """LLM'e bölüm spesifikasyonu ürettirir."""
    user = build_spec_prompt(chapter_title, concepts, book_context, chapter_no)
    print(f"  [SPEC] {chapter_title} planı hazırlanıyor...")
    spec = client.generate_text(SYSTEM_AUTHOR, user)
    print(f"  [SPEC] {len(spec.split())} kelime, {len(spec)} karakter")
    return spec


def validate_spec(client, spec: str, chapter_title: str) -> dict:
    """LLM'e spesifikasyonu doğrulatır.

    Returns:
        {"status": "PASS"|"REVISION", "notes": "...", "response": "..."}
    """
    user = build_spec_validation_prompt(spec, chapter_title)
    print(f"  [VALIDATE] Spesifikasyon kontrol ediliyor...")
    result = client.generate_text(SYSTEM_AUTHOR, user)
    status = "PASS" if "PASS" in result.upper() else "REVISION"
    print(f"  [VALIDATE] {status}, {len(result.split())} kelime")
    return {"status": status, "notes": result, "response": result}
