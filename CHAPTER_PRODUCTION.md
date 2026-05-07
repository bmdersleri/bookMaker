# Chapter Production Pipeline

bookMaker'da bir bölümün üretim süreci 6 aşamalı bir pipeline üzerinden gerçekleşir. Her aşama LLM (DeepSeek Chat) ile etkileşime girer ve bir önceki aşamanın çıktısını girdi olarak kullanır.

## Genel Mimari

```
SPEC → VALIDATE → SEED → NORMALIZE → ENRICH → ASSEMBLE
```

Pipeline `src/bookMaker/studio/jobs.py` içindeki `_run_pipeline()` fonksiyonu tarafından yönetilir. İşler arka planda bir worker thread tarafından sırayla işlenir.

---

## Aşama 1: SPEC (Spesifikasyon Planı)

**Dosya:** `src/bookMaker/generation/spec.py` — `generate_spec()`, `build_spec_prompt()`

Bu aşamada LLM'e bölümün başlığı ve kapsanacak kavramlar verilir. LLM'den **kod yazması değil**, bir PLAN hazırlaması istenir. Plan şu başlıkları içerir:

1. **KAVRAMLAR** — Her kavramın ne olduğu, zorluk seviyesi, kod örneği gerekip gerekmediği
2. **KOD ÖRNEKLERİ** — Hangi kavramı göstereceği, dosya adı, tahmini satır sayısı, hangi dil özelliklerini kullanacağı
3. **DİYAGRAMLAR** — Mermaid diyagram planları (türü, düğümleri)
4. **SÖZLÜK** — 10-15 terim listesi
5. **DEĞERLENDİRME** — D/Y ve boşluk doldurma soru konuları
6. **ALIŞTIRMALAR** — 2-3 alıştırma konusu
7. **SIK YAPILAN HATALAR** — 3-5 hata konusu
8. **TABLOLAR** — Karşılaştırma verileri

**Önemli:** Bu aşamada LLM'e ` ```python ` veya ` ```mermaid ` bloğu yazması **kesinlikle yasaktır**. Sadece tarif etmesi istenir.

**Çıktı:** `logs/production/{job_id}/step0_spec.md` — 800-1300 kelime arası bir plan dokümanı.

---

## Aşama 2: VALIDATE (Spesifikasyon Doğrulama)

**Dosya:** `src/bookMaker/generation/spec.py` — `validate_spec()`, `build_spec_validation_prompt()`

SPEC aşamasında üretilen plan LLM tarafından tekrar kontrol edilir:

1. Tüm kavramlar kapsanmış mı?
2. PLAN formatına uygun mu? (kod/diyagram bloğu yazılmamış olmalı)
3. Eksik bölüm var mı?
4. Değerlendirme soruları ve alıştırmalar planlanmış mı?

**Sonuç:** `PASS` veya `REVISION` — `PASS` değilse bile pipeline devam eder, sadece not düşülür.

**Çıktı:** `logs/production/{job_id}/step0_validation.md`

---

## Aşama 3: SEED (Taslak Üretimi)

**Dosya:** `src/bookMaker/generation/spec.py` — `build_seed_from_spec_prompt()`

En uzun ve en kritik aşama. SPEC planındaki tariflere göre LLM **gerçek bölüm içeriğini** üretir. Bu aşamada kullanılan 6 adımlı pedagojik derinlik zinciri:

1. **TANIM** — Kavramı 1-2 net cümleyle tanımla
2. **NEDEN VAR?** — Hangi problemi çözer?
3. **NASIL KULLANILIR?** — Çalışan kod örneği ile göster, satır satır açıkla
4. **NE ZAMAN TERCİH EDİLİR?** — Hangi senaryoda bu, hangi senaryoda alternatifi?
5. **ALTERNATİFLERİ** — Benzer kavramlarla karşılaştırma tablosu yap
6. **YAYGIN HATALAR** — Bu kavramla ilgili en sık hatayı ve çözümünü belirt

**Yazım Kuralları:**
- H1 = bölüm başlığı, H2 = ana bölümler, H3 = alt bölümler
- Her kod H2/H3 altında ` ```{dil} ` fence bloğu içinde
- Değişken isimleri anlamlı Türkçe
- Her kodda 3+ yorum satırı, `// Çıktı: ...` gösterimi
- SPEC'te planlanan HER diyagram için ` ```mermaid ` bloğu (en az 5 düğüm)
- Hedef: 6000-8000 kelime

**Truncation Yönetimi:** API `max_tokens` (8192) limitinde kesilirse, `generate_text_with_resume()` devam eder — en fazla 5 resume denenir.

**Çıktı:** `logs/production/{job_id}/step1_seed.md` — Ham LLM çıktısı.

---

## Aşama 4: NORMALIZE (Temizlik ve Front Matter)

**Dosya:** `src/bookMaker/generation/postprocess.py` — `normalize()`

SEED çıktısı 0-token işlemlerle temizlenir ve standartlaştırılır:

1. **TextCleaner** — Tırnak işaretleri, boşluklar, yazım düzeltmeleri (regex tabanlı, LLM çağrısı yok)
2. **Heading Seviyeleri** — Hiyerarşi düzeltme (H1 tek, H2→H3 atlaması yok)
3. **Front Matter** — YAML başlık bloğu ekleme:
   ```yaml
   ---
   title: "Bölüm Başlığı"
   author: "Yazar"
   project-alias: kitap-aliasi
   chapter-alias: bolum-01
   ---
   ```
4. **Fazla boşluk ve separator temizliği**

**Çıktı:** `logs/production/{job_id}/step2_normalized.md` — Temizlenmiş, front matter eklenmiş bölüm.

---

## Aşama 5: ENRICH (Zenginleştirme — Paralel)

**Dosya:** `src/bookMaker/generation/prompts.py` — `build_enrich_*` fonksiyonları

Normalize edilmiş bölüme 6 zenginleştirme bileşeni eklenir. Her biri **paralel** LLM çağrısıdır (ThreadPoolExecutor, max 4 worker):

| Bileşen | Prompt Builder | Açıklama |
|---------|---------------|----------|
| **Özet** | `build_enrich_summary_prompt()` | 3-5 cümle, ana kazanımlar |
| **Sözlük** | `build_enrich_glossary_prompt()` | En az 10 terim, `**Terim** — açıklama` formatında |
| **Soru** | `build_enrich_questions_prompt()` | 5-10 D/Y + 5-10 boşluk doldurma, açıklamalı |
| **Alıştırma** | `build_enrich_exercises_prompt()` | 3 programlama alıştırması, zorluk seviyeli |
| **Hata** | `build_enrich_errors_prompt()` | Sık yapılan hatalar ve yanlış sezgiler |
| **Köprü** | `build_enrich_bridge_prompt()` | Sonraki bölüme bağlantı |

Her bir enrichment kendi dosyasına kaydedilir.

**Çıktı:** `logs/production/{job_id}/step3_enrich_{summary,glossary,questions,exercises,errors,bridge}.md`

---

## Aşama 6: ASSEMBLE (Birleştirme)

**Dosya:** `src/bookMaker/generation/postprocess.py` — `insert_section()`, `extract_sections()`

Paralel enrichment çıktıları normalize edilmiş metne eklenir. Yerleştirme sırası (bölüm sonunda):

1. **Alıştırmalar** — `## Programlama Alıştırmaları`
2. **Sorular** — `## Kendini Değerlendirme Soruları`
3. **Sözlük** — `## Terim Sözlüğü`
4. **Özet** — `## Bölüm Özeti`
5. **Hatalar** — `## Sık Yapılan Hatalar ve Yanlış Sezgiler`
6. **Köprü** — `## Bir Sonraki Bölüme Köprü`

`insert_section()` fonksiyonu Türkçe varyasyonları (özet/özet, sözlük/sozluk, alıştırma/alistirma) akıllıca eşleştirir.

Son olarak `normalize()` tekrar çağrılır ve son hal verilir.

**Çıktı:**
- `logs/production/{job_id}/step4_final.md` — Son bölüm
- `chapters/{chapter_id}/content/draft.md` — Projenin draft dosyası
- `logs/production/{job_id}/metrics.json` — İstatistikler (kelime sayısı, süre, model)

---

## Sistem Prompt (Author Persona)

**Dosya:** `src/bookMaker/generation/prompts.py` — `build_system_author()`

Tüm LLM çağrılarında kullanılan sistem prompt'u, kitabın kod diline göre (`primary_code_language`) dinamik olarak üretilir:

- `SYSTEM_AUTHOR`: Java varsayılanı (geriye uyumlu sabit)
- `build_system_author(code_language)`: Dile özel versiyon (örn. Python için "Python kodu", "Python'a sıfırdan başlayan")

Prompt, yazarın kişiliğini tanımlar: akademik ama sade, uygulama odaklı, 6 adımlı zincirle çalışan, günlük hayattan analojiler kullanan kıdemli bir teknik yazar.

---

## İş Kuyruğu ve Worker

**Dosya:** `src/bookMaker/studio/jobs.py`

- `POST /api/generate/{chapter_id}` → `create_job("generate", chapter_id, params)` → `_JOBS` dict'ine eklenir
- Worker thread her 1 saniyede bir `_dequeue()` ile `queued` durumundaki işleri alır
- `_execute_job()` → `_run_pipeline()` çağrılır
- İlerleme `update_job()` ile anlık güncellenir (her aşama için `progress.done` artar)
- Biten iş `done` veya `error` durumuna geçer
- İşler `GET /api/jobs` ve `GET /api/jobs/{job_id}` ile sorgulanabilir

---

## Prompt Dosyaları (Chapter Prompt)

Her bölümün kendi `prompt.md` dosyası vardır: `chapters/{chapter_id}/prompt.md`

Bu dosya şunları içerir:
- Bölüm başlığı ve konular
- Hedef kitle
- Kod dili
- Özel talimatlar

Pipeline şu anda prompt.md'i **otomatik okumaz**. SPEC aşamasında kavramlar doğrudan API parametresi olarak geçilir.

---

## Konfigürasyon Akışı

1. `book_manifest.yaml` → `BookManifest` modeli
2. `BookManifest.style.code_language` → `ChapterGenerator.code_language`
3. `code_language` → `build_system_author()` → dile özel sistem prompt'u
4. `code_language` → `build_spec_prompt()`, `build_seed_from_spec_prompt()` → dile özel kullanıcı prompt'ları

---

## Bölüm Üretimini Başlatma

### GUI Üzerinden
1. Bölümler sekmesinde "Uret" butonuna tıkla
2. Pipeline sekmesi açılır, iş kuyruğa eklenir
3. Worker sırayla aşamaları işler
4. Job listesinde durum takip edilir

### API Üzerinden
```bash
POST /api/generate/{chapter_id}
Body: {
  "title": "Bölüm Başlığı",
  "concepts": ["kavram1", "kavram2", ...],
  "chapter_no": 1,
  "enrich_types": ["ozet", "sozluk", "soru", "alistirma", "hata", "kopru"]
}
```

### Doğrudan Python
```python
from bookMaker.generation.pipeline import ChapterGenerator
gen = ChapterGenerator("book_projects/kitap-adı")
# Pipeline aşamaları manuel çağrılır
```
