# FAULT.md — bookMaker Kitap Üretimi Hata ve Problem Kaydı

**Proje:** bookMaker (Java'nın Temelleri Kitap Üretimi)  
**Tarih:** 2026-05-03  
**Branch:** deepseek  
**İlgili Faz:** LLM API Entegrasyonu + Generation Pipeline  
**Durum:** Açık — düzeltme bekliyor

---

## İçindekiler

1. [Kritik Hatalar](#1-kritik-hatalar)
2. [Önemli Problemler](#2-önemli-problemler)
3. [Orta Seviye Sorunlar](#3-orta-seviye-sorunlar)
4. [İyileştirme Önerileri](#4-iyileştirme-önerileri)
5. [Performans Verileri](#5-performans-verileri)
6. [Etki Analizi](#6-etki-analizi)

---

## 1. Kritik Hatalar

### F-001: YAML Front Matter Eksik

| Alan | Değer |
|---|---|
| **Öncelik** | 🔴 Kritik |
| **Dosya** | `src/bookmaker/generation/pipeline.py` (generate_chapter metodu) |
| **İlgili** | `src/bookmaker/generation/prompts.py` (SYSTEM_PROMPT_CHAPTER) |
| **Keşif** | Batch 1, Bölüm 1 üretiminde tespit edildi |

**Belirti:**  
LLM (DeepSeek-v4-flash) yalnızca Markdown gövdesi üretiyor. YAML front matter (`--- title: ... ---`) çıktının başında yer almıyor.

```
LLM Çıktısı (Hatalı):
# Java'ya Giriş
## Bölümün yol haritası
...

Beklenen Çıktı:
---
title: "Java'ya Giriş"
subtitle: "Java'nın Temelleri"
...
---
# Java'ya Giriş
```

**Kök Sebep:**  
Sistem prompt'taki "YAML front matter ile başla" talimatı DeepSeek modeli tarafından yeterince önemsenmiyor. Model, çıktıyı doğrudan Markdown gövdesi olarak üretmeyi tercih ediyor.

**Geçici Çözüm:**  
`generation/pipeline.py` içinde `generate_chapter()` metoduna front matter fallback eklendi: eğer çıktı `---` ile başlamıyorsa, otomatik olarak eksiksiz bir YAML front matter prepend ediliyor.

```python
if not chapter_text.lstrip().startswith("---"):
    fm = "---\ntitle: ...\n---\n\n"
    chapter_text = fm + chapter_text
```

**Önerilen Kalıcı Çözüm:**  
Front matter oluşturma işlemini LLM'den ayır. Her chapter için pipeline içinde deterministik olarak YAML front matter oluştur ve LLM çıktısına otomatik ekle. Sistem prompt'ta yalnızca "Markdown gövdesini üret" talimatı ver.

---

### F-002: Çoklu H1 Başlık (Heading Hiyerarşisi Bozuk)

| Alan | Değer |
|---|---|
| **Öncelik** | 🔴 Kritik |
| **Dosya** | `src/bookmaker/generation/prompts.py` |
| **İlgili** | `src/bookmaker/chapter/validator.py` (heading.h1_count kontrolü) |
| **Keşif** | Batch 1, Bölüm 1 validasyonunda tespit edildi |

**Belirti:**  
LLM tüm alt başlıkları `#` (H1) seviyesinde üretiyor. Validator "Expected exactly one H1 heading, found 31" hatası veriyor (Score: 88 → 73 düşüş, Decision: pass → revision_required).

```
LLM Çıktısı (Hatalı):
# Java'ya Giriş, Çalışma Modeli
# Bölümün yol haritası        ← Hata: ## olmalıydı
# Java'nın kullanım alanları   ← Hata: ### olmalıydı
# JVM, JRE, JDK kavramları     ← Hata: ### olmalıydı

Doğru:
# Java'ya Giriş, Çalışma Modeli
## Bölümün yol haritası
### Java'nın kullanım alanları
### JVM, JRE, JDK kavramları
```

**Kök Sebep:**  
Model, tüm başlık seviyelerinde `#` kullanıyor. Sistem prompt'taki "Başlıklar elle numaralandırılmasın" talimatı başlık seviyesi (`#` vs `##`) ile ilgili değil.

**Geçici Çözüm:**  
`tools/fix_headings.py` post-processing script'i yazıldı. İlk `#` H1 olarak korunur, sonraki tüm `#`'lar `##`'ye dönüştürülür.

```python
def fix_heading_hierarchy(text):
    # İlk H1 kalır, sonrakiler ## olur
```

**Önerilen Kalıcı Çözüm:**  
Sistem prompt'una net başlık hiyerarşisi şablonu ekle:
```markdown
# [Bölüm Adı]        ← SADECE BİR TANE
## [Alt Bölüm]        ← Ana konu başlıkları
### [Alt Başlık]      ← Detay konuları
```

Veya post-processing'i pipeline'a entegre et: draft paste edilirken otomatik heading fix uygula.

---

## 2. Önemli Problemler

### F-003: CODE_META Blokları Eksik

| Alan | Değer |
|---|---|
| **Öncelik** | 🟠 Önemli |
| **Dosya** | `src/bookmaker/generation/prompts.py` |
| **İlgili** | `src/bookmaker/build/extractor.py` |
| **Keşif** | Batch 1, tüm bölümlerde |

**Belirti:**  
Java kod blokları `CODE_META` olmadan üretiliyor. Build pipeline kodları bulamıyor. Örnek:
````
```java              ← Sadece kod, CODE_META yok
// Dosya: Ornek.java
public class Ornek { ... }
```
````

**Kök Sebep:**  
DeepSeek modeli `<!-- CODE_META ... -->` formatını üretmiyor. Sistem prompt'ta "Her kod bloğundan önce CODE_META bloğu olsun" talimatı uygulanmıyor.

**Etki:**  
- `bookmaker build chapter` → 0 kod çıkarılır, 0 derlenir
- `bookmaker production full` → QR üretilemez
- GitHub sync → yapılamaz

**Önerilen Çözüm:**  
LLM'den CODE_META beklemek yerine, pipeline içinde kod bloklarını tara ve otomatik CODE_META üret. Alternatif olarak, farklı bir model (ör. GPT-4o) dene.

---

### F-004: API Yanıt Süresi Çok Uzun

| Alan | Değer |
|---|---|
| **Öncelik** | 🟠 Önemli |
| **Dosya** | `src/bookmaker/llm/openai.py` |
| **İlgili** | `src/bookmaker/generation/pipeline.py` |
| **Keşif** | İlk 5 bölüm üretimi sırasında |

**Belirti:**  
Her bölüm üretimi 90-120 saniye sürüyor. 31 bölüm için toplam ~50 dakika.

**Ölçüm Verileri:**

| Bölüm | API Süresi | Karakter | Token (Tahmini) |
|---|---|---|---|
| B1: Java'ya Giriş | 42sn | 11.337 | ~3.400 |
| B2: Program Yapısı | ~90sn | 10.876 | ~3.200 |
| B3: Tip Dönüşümleri | ~95sn | 10.601 | ~3.100 |
| B4: Konsol Girişi | ~100sn | 12.949 | ~3.800 |
| B5: Karar Yapıları | ~100sn | 10.893 | ~3.200 |

**Ortalama: ~95sn/bölüm, ~3.400 token/bölüm**

**Kök Sebep:**  
Her bölüm için 2 API çağrısı sırayla yapılıyor:
1. Outline üretimi (~30-40sn, ~1.500 token)  
2. Chapter üretimi (~60-80sn, ~3.400 token)

**Önerilen Çözüm:**  
- Tek bir API çağrısında hem outline hem chapter üret (tek prompt)
- Paralel API çağrıları (birden fazla bölümü aynı anda)
- Daha hızlı model kullan (deepseek-chat yerine daha hızlı bir varyant)
- Token limitini düşür (max_tokens: 4096 → 2048 pilot)

---

### F-005: API Timeout

| Alan | Değer |
|---|---|
| **Öncelik** | 🟠 Önemli |
| **Dosya** | `src/bookmaker/llm/openai.py` (timeout=120) |
| **İlgili** | CLI üzerinden 180sn timeout override |
| **Keşif** | B5 üretiminde (2 kez timeout) |

**Belirti:**  
Bazı API çağrıları 120+ saniyede timeout atıyor. Özellikle büyük çıktı üreten bölümlerde.

**Kök Sebep:**  
OpenAI client varsayılan timeout=120sn. DeepSeek API'si bazen 90-120sn arasında yanıt veriyor.

**Geçici Çözüm:**  
CLI çağrılarında timeout=180sn kullanıldı.

**Önerilen Çözüm:**  
- timeout değerini 300sn'ye çıkar
- Retry mekanizması ekle (3 deneme, üstel backoff)
- Token limitini düşürerek yanıt süresini kısalt

---

## 3. Orta Seviye Sorunlar

### F-006: Önerilen Front Matter Alanları Eksik

| Alan | Değer |
|---|---|
| **Öncelik** | 🟡 Orta |
| **Dosya** | `src/bookmaker/generation/pipeline.py` (fallback) |
| **Keşif** | Tüm bölümlerde |

**Belirti:**  
4 önerilen front matter alanı eksik: `chapter_spec`, `processing_stage`, `placeholder_policy`, `snippet_policy`.

**Etki:**  
Her bölümde 4 warning → Score=88 (100 yerine). Karar `pass_with_warnings`.

**Çözüm:**  
Fallback front matter'a bu alanları da ekle. Pipeline'da otomatik olarak:
```yaml
chapter_spec: chapter_spec_v0_1
processing_stage: authoring_source
placeholder_policy: source_template
snippet_policy: non_meta_code_is_explanatory
```

---

### F-007: Görsel/Mermaid Referansı Yok

| Alan | Değer |
|---|---|
| **Öncelik** | 🟡 Orta |
| **Dosya** | `src/bookmaker/generation/prompts.py` |
| **Keşif** | Tüm bölümlerde |

**Belirti:**  
LLM üretiminde hiçbir görsel veya Mermaid diyagramı referansı yok. Mevcut kitapta 502 görsel var.

**Etki:**  
DOCX çıktısı görsel içermiyor. Kitap görsel destekli referans kitaptan daha düşük kalitede.

**Çözüm:**  
Sistem prompt'una şu talimatı ekle: "Her ana bölüm için 1-2 Mermaid diyagramı ekle. Ekran görüntüsü gereken yerlerde `<!-- SCREENSHOT_META -->` kullan."

---

### F-008: Bölüm Uzunluğu Dengesiz

| Alan | Değer |
|---|---|
| **Öncelik** | 🟡 Orta |
| **Dosya** | `src/bookmaker/generation/prompts.py` |
| **Keşif** | Batch 1 sonunda |

**Ölçüm:**

| Bölüm | Karakter | Referans Kitap | Fark |
|---|---|---|---|
| B1 | 11.337 | ~15.000 | -24% |
| B2 | 10.876 | ~15.000 | -27% |
| B3 | 10.601 | ~15.000 | -29% |
| B4 | 12.949 | ~15.000 | -14% |
| B5 | 10.893 | ~15.000 | -27% |

**Çözüm:**  
Prompt'a "Her bölüm en az 15.000 karakter olmalı" veya "En az 5 kod örneği içermeli" gibi tutarlılık kuralı ekle.

---

### F-009: Özel Java Karakterleri (İ, Ğ, Ü, Ş, Ç)

| Alan | Değer |
|---|---|
| **Öncelik** | 🟡 Orta |
| **Dosya** | Tümü |
| **Keşif** | PowerShell UTF-8 sorunları |

**Belirti:**  
PowerShell üzerinden çalıştırılan komutlarda Türkçe karakterler (`İ`, `Ğ`, `Ü`, `Ş`, `Ç`) bazen bozuluyor.

**Etki:**  
Çıktı formatında karakter bozulmaları. `SESSION.md`'de `AKTİF İŞ` → `AKT�F ��` olarak kaydedildi.

**Çözüm:**  
Tüm dosyalarda UTF-8 encoding zorunlu. PowerShell'de `[Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8` ayarlanmalı.

---

## 4. İyileştirme Önerileri

### I-001: Post-Processing Pipeline Tek Komutta

**Mevcut Durum:**  
Her batch sonunda 4 ayrı adım:
1. `python tools/fix_headings.py bolum-XX` (heading fix)
2. `python tools/fix_fm.py` (front matter fix)
3. `bookmaker check chapter ...` (validasyon)
4. Tekrarlı

**Öneri:**  
Tek komut:
```bash
bookmaker chapter post-process bolum-XX
```
Tüm düzeltmeleri topluca yapar.

---

### I-002: Üretim Logu Tutma

**Öneri:**  
Her `generate chapter` çağrısı bir JSON log dosyasına yazılmalı:
```json
{
  "chapter_id": "bolum-01",
  "timestamp": "2026-05-03T23:30:00",
  "duration_sec": 42,
  "characters": 11337,
  "score": 88,
  "errors": 0,
  "warnings": 4
}
```

---

### I-003: Batch Üretim Modu

**Öneri:**  
```bash
bookmaker generate batch bolum-01 bolum-02 bolum-03
```
Tek komutla birden fazla bölümü sırayla üretir, her biri arasında post-processing yapar.

---

### I-004: Hızlı Model Desteği

**Öneri:**  
İlk outline için hızlı/ucuz model, chapter için ana model kullan. Veya her ikisi için aynı model:
```bash
bookmaker llm configure --model deepseek-chat --fast-model deepseek-chat
```

---

## 5. Performans Verileri

### Batch 1 (B1-B5) Üretim Raporu

| Metrik | Değer |
|---|---|
| Toplam süre | ~8 dakika |
| Bölüm başına ortalama | ~95 saniye |
| Toplam karakter | ~56.656 |
| Ortalama karakter/bölüm | ~11.331 |
| API çağrısı/bölüm | 2 (outline + chapter) |
| Toplam API çağrısı | 10 |
| Başarılı çağrı | 9/10 |
| Timeout | 1 (B5, ilk deneme) |

### Tahmini Tüm Kitap (31 Bölüm)

| Metrik | Değer |
|---|---|
| Toplam süre | ~49 dakika |
| Toplam API çağrısı | ~62 |
| Toplam karakter | ~351.000 |
| Beklenen timeout | ~3-5 |

---

## 6. Etki Analizi

| Hata Kodu | Validasyon | Build | Production | DOCX Çıktısı |
|---|---|---|---|---|
| F-001 (Front Matter) | ❌ Score düşer | ✅ | ✅ | ✅ |
| F-002 (Heading) | ❌ FAIL | ✅ | ✅ | ⚠️ Hiyerarşi bozuk |
| F-003 (CODE_META) | ✅ | ❌ Kod çıkmaz | ❌ QR yok | ✅ |
| F-004 (Süre) | ✅ | ✅ | ✅ | ✅ |
| F-005 (Timeout) | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| F-006 (Alanlar) | ⚠️ Score düşer | ✅ | ✅ | ✅ |
| F-007 (Görsel) | ✅ | ✅ | ❌ Mermaid yok | ❌ Görsel yok |
| F-008 (Uzunluk) | ✅ | ✅ | ✅ | ⚠️ Dengesiz |

**Öncelikli Çözüm Sırası:**
1. F-003: CODE_META otomatik üretimi
2. F-002: Heading fix pipeline'a entegre
3. F-001: Front matter deterministik oluşturma
4. F-004: Tek API çağrısı (outline + chapter)
5. F-007: Görsel/Mermaid prompt'ları
6. F-006: Eksik alanları tamamlama

---

*Kayıt Tarihi: 2026-05-03 | Son Güncelleme: 2026-05-03 | Toplam: 9 hata + 4 iyileştirme*
