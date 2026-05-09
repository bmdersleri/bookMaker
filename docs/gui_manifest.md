# bookMaker Studio — GUI Gereksinim Manifesti

> **TARIHI KAYIT (2026-05-04).** Bu dokuman GUI'nin ilk gereksinim manifestidir.
> Aktif gelistirme takibi icin: `GUI_ROADMAP.md` (repo kökü).
> Bircok ozellik (inline edit, pipeline detail, export kontrolleri) bu manifestte yoktur.

**Versiyon:** 2.0 | **Tarih:** 2026-05-04 | **Durum:** Onaylı — kodlamaya hazır

---

## 1. Amaç

Akademik/teknik kitapların uçtan uca üretimi için web tabanlı kontrol paneli.

**Temel iş akışı:** Kitap oluştur → LLM ile bölüm üret → Düzenle → Kalite kontrol → DOCX/PDF/EPUB çıktı al

---

## 2. 5 Sekmeli Dashboard

```
┌──────────────────────────────────────────────────────────────────┐
│ 📚 bookMaker Studio              Kitap: Java'nın Temelleri       │
│ [27 Bölüm] [18 Onaylı] [production] [🟢 deepseek-chat]           │
│ 🔄 Yenile | ⚙️ LLM Ayarları | 📊 Pipeline Durumu                 │
├──────────────────────────────────────────────────────────────────┤
│ [📖 Bölümler] [🔧 Pipeline] [⚙️ Konfig] [📄 Build] [📊 Kalite]   │
└──────────────────────────────────────────────────────────────────┘
```

| Sekme | İşlevler | Durum |
|-------|----------|-------|
| **📖 Bölümler** | Tablo, filtre, sırala, sürükle-bırak, CRUD, toplu işlem, 👁Gör/✓Kontrol/📄Build/▶Üret | ⚠️ Kısmen |
| **🔧 Pipeline** | SPEC→SEED→ENRICH→ASSEMBLE formu, WS canlı progress, prompt/response takibi, iptal, toast | ⚠️ Kısmen |
| **⚙️ Konfig** | LLM sağlayıcı/key/model, sıcaklık, timeout, retry, bağlantı testi | ✅ |
| **📄 Build** | Kod çıkarma, Mermaid→PNG, bölüm→DOCX, birleştir→DOCX/PDF/EPUB/HTML | 🔲 |
| **📊 Kalite** | Skor tablosu, hata listesi, kod derleme, kitap istatistikleri | 🔲 |

---

## 3. İş Akışları

### 3.1 Kitap Sihirbazı (5 adım)
Ad, plan (LLM), API, çıktı ayarları, onay → yeni kitap projesi oluşturur.

### 3.2 Bölüm Üretimi
▶ Üret → SPEC(30s) → SEED(65s) → NORM → ENRICH×6(28s) → ASSEMBLE → kaydet → versiyonla

### 3.3 Kalite Döngüsü
✓ Kontrol → Skor/Hata → Düzelt → Tekrar → Skor≥80 → Onayla

### 3.4 Toplu Üretim
Seç → Toplu Üret → Sıralı kuyruk → Her bölüm pipeline → Hata→(Devam/Atla/İptal)

---

## 4. Backend API (29 endpoint)

### 4.1 Proje & Durum (4)
| Yöntem | Yol | Durum |
|--------|-----|-------|
| `GET` | `/` | ✅ Dashboard HTML |
| `GET` | `/api/status` | ✅ Sunucu durumu |
| `GET` | `/api/project` | ✅ Kitap bilgisi |
| `POST` | `/api/book/create` | 🔲 Yeni kitap oluştur |

### 4.2 Bölümler (6)
| Yöntem | Yol | Durum |
|--------|-----|-------|
| `GET` | `/api/chapters` | ✅ Liste |
| `GET` | `/api/chapters/{id}` | 🔲 Detay |
| `POST` | `/api/chapters` | 🔲 Ekle |
| `PUT` | `/api/chapters/{id}` | 🔲 Güncelle |
| `DELETE` | `/api/chapters/{id}` | 🔲 Sil |
| `PUT` | `/api/chapters/reorder` | 🔲 Sürükle-bırak sırala |

### 4.3 İçerik & Kalite (6)
| Yöntem | Yol | Durum |
|--------|-----|-------|
| `GET` | `/api/view/{id}` | ✅ İçerik |
| `GET` | `/api/check/{id}` | ✅ Validasyon |
| `GET` | `/api/quality/report` | 🔲 Kalite raporu |
| `POST` | `/api/code/validate` | 🔲 Kod derle (`javac`) |
| `GET` | `/api/stats` | 🔲 Kitap istatistik |
| `GET` | `/api/search?q=` | 🔲 Tam metin arama |

### 4.4 Build & Export (6)
| Yöntem | Yol | Durum |
|--------|-----|-------|
| `GET` | `/api/build/{id}` | ✅ Bölüm→DOCX |
| `POST` | `/api/build/all` | 🔲 Tüm bölümler→DOCX |
| `POST` | `/api/extract/{id}` | 🔲 Kod çıkarma (.java) |
| `POST` | `/api/render/mermaid/{id}` | 🔲 Mermaid→PNG |
| `POST` | `/api/assemble` | 🔲 Birleştir→tek .md |
| `POST` | `/api/export/{fmt}` | 🔲 DOCX/PDF/EPUB/HTML |

### 4.5 LLM & Pipeline (6)
| Yöntem | Yol | Durum |
|--------|-----|-------|
| `GET` | `/api/llm-status` | ✅ LLM durumu |
| `POST` | `/api/llm-configure` | ✅ Konfigüre et |
| `POST` | `/api/llm-test` | 🔲 Bağlantı testi |
| `POST` | `/api/generate/{id}` | ✅ Pipeline başlat |
| `GET` | `/api/pipeline-state` | ✅ Pipeline durumu |
| `POST` | `/api/generate/{id}/cancel` | 🔲 İptal et |

### 4.6 Yedekleme & Diğer (2)
| `POST` | `/api/backup` | 🔲 .zip yedekle |
| `POST` | `/api/restore` | 🔲 Geri yükle |

### 4.7 WebSocket (1)
| `ws://.../ws/api/generate/{id}` | ✅ Canlı progress |

---

## 5. Pipeline Kontrol Merkezi

### 5.1 Canlı Progress

| Gösterge | Açıklama |
|----------|----------|
| Ana Bar | Yüzde + gradient, her adımda güncellenir |
| Adım Listesi | ✅⚡⏸❌ simge + kelime + süre + genişletilebilir detay |
| Geçen Süre | `2m 14s`, her saniye güncellenir |
| ETA | `(kalan_adım × ortalama_süre) + (kalan_API × ortalama_API)` |
| İstatistik | Anlık: kelime, kod, diyagram, tablo, hata sayısı |

### 5.2 LLM Prompt/Response Canlı Takip

Pipeline sırasında her adım genişletilince:
- **Gönderilen Prompt** tam metni (gizlenecek alanlar maskelenir)
- **Alınan Yanıt** ilk 300 karakter + [Tamamını Gör →]
- **Token Bilgisi**: prompt/response token sayıları (API dönerse)

### 5.3 Hata Yönetimi

| Kategori | Kullanıcıya Yansıma |
|----------|-------------------|
| API Bağlantı | 🔴 Toast + retry sayacı + öneri |
| API Yanıt | 🟡 Toast + fallback içerik |
| İçerik Kalitesi | Uyarı kartı + düzeltme seçenekleri |
| Dosya Sistemi | 🔴 Modal + çözüm önerisi |

**Toast seviyeleri:** 🔴 Hata | 🟡 Uyarı | 🟢 Başarılı

**Fallback stratejisi:** SPEC↓→ direkt SEED | ENRICH↓→ varsayılan | Tüm ENRICH↓→ ASSEMBLE uyarılı

---

## 6. Build & Export Merkezi

### 6.1 Kod Çıkarma
Tüm ` ```java ` bloklarını `.md`'den ayırır, `build/code/{bolum}/` altına `.java` dosyası olarak kaydeder.
`javac` ile derler, sonucu bildirir. **Backend:** `build/extractor.py` zaten var.

### 6.2 Diyagram Render
` ```mermaid ` bloklarını `mmdc` ile PNG'e çevirir, `build/mermaid_images/` altına kaydeder.
Önizleme gösterir. **Backend:** `production/mermaid.py` zaten var.

### 6.3 Kitap Birleştirme
Tüm bölüm `.md` dosyalarını tek bir `kitap_birlestirilmis.md` olarak birleştirir.
İçindekiler otomatik eklenir. Başlık numaraları sıralı hale getirilir.

### 6.4 Format Dönüşümü
| Format | Araç | Açıklama |
|--------|------|----------|
| DOCX | Pandoc + Lua filtresi | Referans şablonlu, mermaid PNG gömülü |
| PDF | Pandoc + LaTeX | Profesyonel sayfa düzeni |
| EPUB | Pandoc | E-kitap okuyucu uyumlu |
| HTML | Pandoc | GitHub Pages için statik site |

**Backend:** `production/pandoc.py` ve `production/pipeline.py` zaten var.

---

## 7. Eksik / Eklenecek 10 Özellik

| # | Özellik | Açıklama |
|---|---------|----------|
| 1 | 🔄 Drag-drop sıralama | Bölümleri sürükle-bırak ile yeniden sırala |
| 2 | 📚 Merkezi glossary | Kitap çapında tek terim listesi, çakışmaları birleştir |
| 3 | 📑 İndeks | Tüm bölümleri tara, terim-konu indeksi çıkar |
| 4 | 🔗 Çapraz referans | "Bölüm X'te gördüğümüz gibi" referanslarını takip et |
| 5 | ✅ Kod validasyonu | Her Java bloğunu `javac` ile derle, hataları işaretle |
| 6 | 🔍 Tam metin arama | Regex destekli, bağlamlı (3 satır), bölüme göre gruplu |
| 7 | 📊 İstatistik dashboard | Toplam kelime/kod/diyagram/okuma süresi, bar chart |
| 8 | 💾 Yedekleme | Tek tıkla `.zip` export/import |
| 9 | 📝 Reader modu | Basılmış gibi oku, sayfa düzeni, karanlık mod |
| 10 | 🔔 Bildirim | Pipeline bitti/hata oluştu, tarayıcı bildirimi |

---

## 8. Versiyon Takip

| Düzey | Format | Depolama |
|-------|--------|----------|
| Kitap | `v1.0.0` (semver) | `version_history/book_v{ver}/` |
| Bölüm | `v{major}.{minor}` | `chapters/{id}/versions/v{m}.{n}.md` |
| Pipeline | Zaman damgası | `pipeline_state.yaml` |
| Konfig | Zaman damgası | `llm_config.json` yedeği |

---

## 9. Teknoloji Yığını

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python 3.14 + FastAPI + Starlette (WebSocket) |
| Frontend | HTML/CSS/JS (tek dosya SPA), CSS Grid/Flexbox |
| LLM | DeepSeek v4 Flash, OpenAI uyumlu API |
| Build | Pandoc + Lua + Mermaid (mmdc) + javac |
| Test | pytest + FastAPI TestClient |

---

## Ek A: Bölüm Durum Makinesi
`planned → spec_generated → seed_generated → enriched → full_text_pasted → approved`

## Ek B: Durum Renkleri
`approved`/`full_text_pasted`: 🟢 | `enriched`/`seed_generated`: 🔵 | `spec_generated`: 🟠 | `planned`: ⚪ | `revision_required`: 🔴
