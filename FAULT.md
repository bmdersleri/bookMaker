# FAULT.md — bookMaker Kitap Üretimi Hata ve Problem Kaydı

**Proje:** bookMaker (Java'nın Temelleri Kitap Üretimi)  
**Tarih:** 2026-05-04  
**Branch:** deepseek  
**Durum:** Güncel — 2 kritik + 2 önemli hata çözüldü, 2 orta seviye açık

---

## Çözülen Hatalar

### F-001: ✅ YAML Front Matter Eksik (ÇÖZÜLDÜ)

| Alan | Değer |
|---|---|
| **Öncelik** | 🔴 Kritik |
| **Çözüm tarihi** | 2026-05-04 |
| **Dosya** | `src/bookmaker/generation/postprocess.py` |

**Çözüm:** `ensure_frontmatter()` fonksiyonu güncellendi. Artık mevcut front matter'ı kontrol eder, eksik alan varsa tamamını yeniden oluşturur. Gerekli 23 alanın tamamı kontrol edilir.

### F-002: ✅ Heading Hiyerarşisi Bozuk (ÇÖZÜLDÜ)

| Alan | Değer |
|---|---|
| **Öncelik** | 🔴 Kritik |
| **Çözüm tarihi** | 2026-05-04 |
| **Dosya** | `src/bookmaker/generation/postprocess.py` |

**Çözüm:** `fix_heading_hierarchy()` — ilk `#` H1 kalır, sonraki tüm `#`'lar `##`'ye dönüşür.

### F-003: ✅ CODE_META Blokları Eksik (ÇÖZÜLDÜ)

| Alan | Değer |
|---|---|
| **Öncelik** | 🟠 Önemli |
| **Çözüm tarihi** | 2026-05-04 |
| **Dosya** | `src/bookmaker/generation/postprocess.py` |

**Çözüm:** `auto_code_meta()` — Java kod bloklarını tarar, eksik CODE_META bloklarını otomatik ekler.

### F-004: ✅ API Yanıt Süresi Çok Uzun (ÇÖZÜLDÜ)

| Alan | Değer |
|---|---|
| **Öncelik** | 🟠 Önemli |
| **Çözüm tarihi** | 2026-05-04 |
| **İlgili** | `tools/batch_v2.py` (P6/P12: combined prompt) |

**Belirti (Öncesi):** Her bölüm için 2 API çağrısı: outline (~30-40sn) + chapter (~60-80sn) = ~95-140sn/bölüm.

**Çözüm:** P12 combined prompt ile outline+chapter tek API çağrısında. P9 outline token 4096→2048. Gerçek ölçüm:
- B12 (öncesi, iki aşamalı): 6,241c outline + 26,051c chapter = **100.2sn**
- B17 (sonrası, combined): **tek çağrı**, ~80-100sn bekleniyor

### F-005: ✅ API Timeout (ÇÖZÜLDÜ)

| Alan | Değer |
|---|---|
| **Öncelik** | 🟠 Önemli |
| **Çözüm tarihi** | 2026-05-04 |
| **Dosya** | `src/bookmaker/llm/openai.py` (timeout: 120→300) |

**Çözüm:**
- `pipeline.py` client timeout: 120sn → **300sn**
- `batch_v2.py` timeout: **600sn**
- P3: 3 deneme retry mekanizması (üstel backoff: 5sn, 15sn, 45sn)

### F-006: ✅ Önerilen Front Matter Alanları Eksik (ÇÖZÜLDÜ)

| Alan | Değer |
|---|---|
| **Öncelik** | 🟡 Orta |
| **Çözüm tarihi** | 2026-05-04 |
| **Dosya** | `src/bookmaker/generation/postprocess.py` |

**Çözüm:** 23 zorunlu alanın tamamı kontrol edilir. Eksik varsa otomatik eklenir.

---

## Açık Hatalar

### F-007: Görsel/Mermaid Referansı Yok

| Alan | Değer |
|---|---|
| **Öncelik** | 🟡 Orta |
| **Dosya** | `src/bookmaker/generation/prompts.py` |

**Belirti:** LLM üretiminde hiçbir görsel veya Mermaid diyagramı referansı yok. Mevcut kitapta 502 görsel var.

**Geçici:** Sistem prompt'a Mermaid talimatı eklendi ("Her ana bölüm için 1-2 Mermaid diyagramı ekle"). Henüz doğrulanmadı.

### F-008: Bölüm Uzunluğu Dengesiz

| Alan | Değer |
|---|---|
| **Öncelik** | 🟡 Orta |
| **Dosya** | `src/bookmaker/generation/prompts.py` |

**Ölçüm (B7-B16):**

| Bölüm | Karakter | Referans | Fark |
|---|---|---|---|
| B7 | 26,108 | ~15,000 | +74% |
| B8 | 15,792 | ~15,000 | +5% |
| B9 | 22,590 | ~15,000 | +51% |
| B10 | 23,338 | ~15,000 | +56% |
| B11 | 30,640 | ~15,000 | +104% |
| B12 | 27,482 | ~15,000 | +83% |
| B13 | 28,458 | ~15,000 | +90% |
| B14 | 23,071 | ~15,000 | +54% |
| B15 | 28,907 | ~15,000 | +93% |
| B16 | 17,761 | ~15,000 | +18% |

**Not:** Bölümler referans kitaptan daha uzun — bu bir hata değil, ancak tutarlılık için gözlemlenmeli.

---

## İyileştirmeler (P1-P12)

### P1: Sıralı İşlem — ✅ Aktif
Bir bölüm bitmeden diğerine geçilmez. Çakışan süreç sorununu tamamen çözer.

### P2: requests Streaming — ✅ Aktif
httpx yerine requests kullanılır. Büyük yanıtlarda daha kararlı.

### P3: Retry Mekanizması — ✅ Aktif
3 deneme, üstel backoff (5sn, 15sn, 45sn). Henüz tetiklenmedi (API hatasız çalışıyor).

### P4: Atomik Yazma — ✅ Aktif
Önce `.tmp` dosyasına yazılır, sonra rename ile hedef dosyaya taşınır.

### P5: Progress Göstergesi — ✅ Aktif
Her 5sn'de chunk sayısı, karakter sayısı ve geçen süre gösterilir.

### P6/P12: Combined Prompt — ✅ Aktif (Varsayılan)
Outline+chapter tek API çağrısında. BOLUM_METNI ayrıştırması ile.

### P7: Hata Raporlama — ✅ Aktif
`build/reports/batch_errors.json` dosyasına detaylı hata kaydı.

### P8: Resume Desteği — ✅ Aktif
`build/reports/batch_progress.json` ile kesintide kaldığı yerden devam.

### P9: Outline Token Optimizasyonu — ✅ Aktif
Outline max_tokens=2048 (öncesi 4096). İki aşamalı modda geçerli.

### P10: Büyük Bölüm Uyarısı — ✅ Aktif
Outline >5000 chars ise uyarı verilir. İki aşamalı modda geçerli.

### P11: Preflight Check — ✅ Aktif
Batch başında API bağlantı testi. ~0.7sn'de tamamlanır.

---

## Performans Verileri

| Bölüm | Mod | Süre | Karakter | Chunk |
|-------|-----|------|----------|-------|
| B7 | İki aşamalı (kaos) | ~300sn | 26,108 | — |
| B8 | requests streaming | 52.9sn | 15,792 | 4,552 |
| B9 | requests streaming | 74.8sn | 22,590 | 6,473 |
| B10 | İki aşamalı | 134.7sn | 23,338 | — |
| B11 | İki aşamalı | 139.0sn | 30,640 | — |
| B12 | **P1-P7** | **100.2sn** | **26,051** | **7,858** |
| B13 | **P1-P7** | **99.9sn** | **26,348** | **7,826** |
| B17 | **P1-P12 combined** | **79.7s** | **19,110** | **—** |
| B18 | **P1-P12 combined** | **84.2s** | **19,222** | **—** |
| B19 | **P1-P12 combined** | **114.4s** | **31,789** | **—** |
| B20 | **P1-P12 combined** | **86.4s** | **26,826** | **—** |
| B21 | **P1-P12 combined** | **142.5s** | **47,019** | **—** |
| B22 | **P1-P12 combined** | **66.8s** | **18,587** | **—** |
| B23 | **P1-P12 combined** | **63.8s** | **19,195** | **—** |
| Ek A | **P1-P12 combined** | **99.1s** | **24,570** | **—** |
| Ek B | **P1-P12 combined** | **84.7s** | **21,963** | **—** |
| Ek C | **P1-P12 combined** | **63.1s** | **15,629** | **—** |
| Ek D | **P1-P12 combined** | **84.9s** | **21,794** | **—** |
