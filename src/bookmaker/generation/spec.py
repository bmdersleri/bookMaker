"""LLM ile bölüm spesifikasyonu üretme ve doğrulama.

Strateji: LLM önce "ne üreteceğini" planlar (spec), sonra plana göre üretir.
Bu sayede kod blokları, diyagramlar, sözlük gibi yapılar garantilenmiş olur.
"""

from __future__ import annotations

from bookmaker.generation.prompts import SYSTEM_AUTHOR, build_system_author

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
    spec_short = spec[:5000]
    if len(spec) > 5000:
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

def generate_spec(client, chapter_title: str, concepts: list[str],
                  book_context: str = "", chapter_no: int | None = None,
                  code_language: str = "java") -> str:
    """LLM'e bölüm spesifikasyonu ürettirir."""
    user = build_spec_prompt(chapter_title, concepts, book_context, chapter_no,
                             code_language=code_language)
    system = build_system_author(code_language) if code_language != "java" else SYSTEM_AUTHOR
    print(f"  [SPEC] {chapter_title} planı hazırlanıyor...")
    spec = client.generate_text(system, user)
    print(f"  [SPEC] {len(spec.split())} kelime, {len(spec)} karakter")
    return spec


def validate_spec(client, spec: str, chapter_title: str,
                  code_language: str = "java") -> dict:
    """LLM'e spesifikasyonu doğrulatır.

    Returns:
        {"status": "PASS"|"REVISION", "notes": "...", "response": "..."}
    """
    user = build_spec_validation_prompt(spec, chapter_title,
                                        code_language=code_language)
    system = build_system_author(code_language) if code_language != "java" else SYSTEM_AUTHOR
    print("  [VALIDATE] Spesifikasyon kontrol ediliyor...")
    result = client.generate_text(system, user)
    status = "PASS" if "PASS" in result.upper() else "REVISION"
    print(f"  [VALIDATE] {status}, {len(result.split())} kelime")
    return {"status": status, "notes": result, "response": result}
