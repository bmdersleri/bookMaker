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
   - Hangi Java özelliklerini kullanacak?
   KOD BLOĞU YAZMA! Sadece tarif et.

3. **DİYAGRAMLAR** — Uygunsa diyagram planla:
   - Neyi görselleştirecek?
   - Hangi tür? (flowchart/sequence/class)
   - Hangi düğümler olacak? (liste halinde)
   MERMAID KODU YAZMA! Sadece tarif et.

4. **SÖZLÜK** — 10-15 terim adı listele (tanım yazma, sadece terimleri listele)

5. **DEĞERLENDİRME** — 3 soru tipini belirle: 1 D/Y konusu, 1 açık uçlu konu, 1 kod okuma konusu

6. **ALIŞTIRMALAR** — 2-3 alıştırma konusu ve zorluk seviyesi (konuyu tarif et, kodu sonra yazacağız)

7. **SIK YAPILAN HATALAR** — 3-5 hata konusu başlığı (hatanın ne olduğunu 1 cümleyle söyle)

8. **TABLOLAR** — Gerekliyse hangi verilerin karşılaştırılacağını belirt

KESIN KURAL: Bu bir PLAN'dır. ```java veya ```mermaid BLOĞU YAZMAK YASAKTIR.
Sadece ne yapılacağını TARIF ET. Kodun ve diyagramın kendisini sonraki aşamada yazacağız."""


def build_spec_validation_prompt(spec: str, chapter_title: str) -> str:
    """LLM'e spesifikasyonu doğrulatması için prompt."""
    return f"""## Görev: Spesifikasyonu Doğrula

**Bölüm:** {chapter_title}

Aşağıdaki spesifikasyonu kontrol et:

{spec[:2000]}

---
Kontrol et:
1. Tüm kavramlar kapsanmış mı?
2. PLAN formatına uygun mu? (```java veya ```mermaid bloğu OLMAMALI, sadece tarif olmalı)
3. Eksik bölüm var mı?
4. Değerlendirme soruları ve alıştırmalar planlanmış mı?

Cevabını şu formatta ver:
- Geçerliyse: "PASS: [kısa açıklama]"
- Eksik varsa: "REVISION: [eksikler listesi]" """


def build_seed_from_spec_prompt(spec: str, chapter_title: str) -> str:
    """Spesifikasyona dayalı seed generation prompt'u."""
    # Spec'i kisalt: sadece ilk 5000 karakter yeterli (plan formatinda)
    spec_short = spec[:5000]
    if len(spec) > 5000:
        spec_short += "\n\n... (planin devami var, tum maddeleri isle)"

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
3. NASIL KULLANILIR? — Çalışan Java kodu ile göster, sonra kodu satır satır açıkla
4. NE ZAMAN TERCİH EDİLİR? — Hangi senaryoda bu, hangi senaryoda alternatifi?
5. ALTERNATİFLERİ — Benzer kavramlarla karşılaştırma tablosu yap
6. YAYGIN HATALAR — Bu kavramla ilgili en sık hatayı ve çözümünü belirt

Her adım için 1-2 paragraf yeterli. Günlük hayattan 1 analoji ekle.
Toplam bölüm uzunluğu 6000-8000 kelime arası olsun.

Yazım kuralları:
- H1 = bölüm başlığı, H2 = ana bölümler, H3 = alt bölümler
- Kod yazmaya uygun H2/H3 altında ```java örneği ver
  (Kod ZORUNLU DEĞİL: yol haritası, öğrenme çıktıları, ön bilgi, özet, sözlük, sorular, rubrik, kaynaklar, köprü)
- Değişken isimleri anlamlı Türkçe, her kodda 3+ yorum satırı, // Çıktı: ... gösterimi
- Bölüm sonunda: Özet, Sözlük, Sorular, Alıştırmalar, Hatalar

ÖNEMLİ: Spesifikasyondaki HER PLANI içeriğe dönüştür. Hiçbir şeyi atlama."""


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
