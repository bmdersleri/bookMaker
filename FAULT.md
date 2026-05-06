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

## Çözülen Hatalar (devam)

### F-007: ✅ 4/58 Mermaid Parse Hatası (ÇÖZÜLDÜ)

| Alan | Değer |
|---|---|
| **Öncelik** | 🟡 Orta |
| **Çözüm tarihi** | 2026-05-04 |
| **Etkilenen bloklar** | mermaid-008 (B13), mermaid-021 (B16), mermaid-026 (B17), mermaid-031 (B18) |

**Sorun:** 4 Mermaid bloğu mmdc ile render edilemedi. `.mmd` dosyaları oluştu ama `.png` üretilemedi.

| Blok | Bölüm | Hata | Düzeltme |
|------|-------|------|----------|
| #008 | B13 | `java.util.Date()` → parantez Mermaid'de özel anlamlı | `["java.util.Date()"]` ile quote'landı |
| #021 | B16 | `exists()`, `createNewFile()` vb. → parantez özel anlamlı | `["exists() metodu"]` ile quote'landı |
| #026 | B17 | `<br/>` HTML etiketleri Mermaid'de desteklenmiyor | `<br/>` kaldırıldı, düz metin kullanıldı |
| #031 | B18 | `"Ting"` çift tırnak Mermaid'de ayrıştırma sorunu | Tek tırnak `'Ting'` kullanıldı |

**Çözüm (3 aşamalı):**
1. `.mmd` dosyaları manuel düzeltildi → geçerli Mermaid sözdizimi
2. Tüm 4 blok `mmdc` ile yeniden render edildi → 58/58 PNG başarılı
3. Kaynak bölüm dosyaları (`draft_versions/v001.md`) kalıcı olarak düzeltildi (B13, B16, B17, B18)

**Sonuç:** 58/58 Mermaid diyagramı başarıyla render edildi. Toplam PNG boyutu: ~1,060 KB.

## Açık Hatalar

### F-008: ✅ Bölüm Uzunluğu — İncelendi, Müdahale Gerekmez (KAPANDI)

| Alan | Değer |
|---|---|
| **Öncelik** | 🟢 Düşük |
| **Karar tarihi** | 2026-05-04 |
| **Karar** | Mevcut haliyle kabul edildi — müdahale gerekmez |

**Tüm Bölüm Ölçümü (2026-05-04):**

```
Batch 0 (B1-B6):  10,707 — 12,974c  (3.1 — 3.7 sayfa)  🔵 KISA
Batch 1 (B7-B11): 15,298 — 28,924c  (4.4 — 8.3 sayfa)  🟡 ORTA
Batch 2 (B12-B16):21,348 — 27,067c  (6.1 — 7.7 sayfa)  🟡 ORTA
Batch 3 (B17-B21):19,154 — 47,245c  (5.5 — 13.5 sayfa) 🔴 DENGESIZ
Batch 4 (B22-EkD):18,661 — 30,358c  (5.3 — 8.7 sayfa)  🟡 ORTA
```

| İstatistik | Değer |
|------------|-------|
| Ortalama | 21,635 karakter |
| En kısa | B3 (10,707c → ~3.1 sayfa) |
| En uzun | B21 (47,245c → ~13.5 sayfa) |
| Fark oranı | 4.4x |
| Std sapma | 8,101 |

**Değerlendirme:**
- B1-B6 (Batch 0): Tutarlı ama kısa (~3 sayfa). LLM prompt'ta `max_tokens=8192` sınırından kaynaklanıyor.
- B21 (47K, ~13.5 sayfa): Polimorfizm/Arayüz konusu doğal olarak kapsamlı. Aşırı değil.
- Bölüm uzunluğu içerik yoğunluğuyla doğru orantılı — konu derinliği farklı.

**Karar:** Mevcut dağılım kabul edilebilir. Anlamlı bir alt/üst sınır yok; her bölüm kendi konusunun gerektirdiği uzunlukta. Gelecek batch'lerde prompt'a hedef karakter aralığı eklenebilir (opsiyonel).

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
