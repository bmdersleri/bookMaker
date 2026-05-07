# bookMaker Studio — GUI Geliştirme Roadmap

> Her faz **bağımsız test edilebilir**. Tamamlanan [x] ile işaretlenir.
> Yeni sohbette: **"GUI_ROADMAP.md Faz X'ten devam"** yeterli.

---

## Faz 0: Mevcut Durum ✅

```
src/bookmaker/studio/
├── __init__.py
├── app.py                          (12,572 B — monolitik, 12 endpoint)
└── templates/index.html            (24,492 B — tek dosya SPA, 3 sekme)

src/bookmaker/commands/studio.py    (CLI: bookmaker studio)
tests/unit/test_studio_app.py      (13 test, hepsi geçiyor)
```

**Backend:** 11 REST + 1 WebSocket | **Frontend:** Bölümler / Pipeline / Konfig | **Test:** 13/13 ✅

---

## Faz 1: Servis Mimarisi + Models + Jobs + Frontend Ayristirma

**Hedef:** `app.py` sadece route kalsin (logic servislere), frontend JS/CSS ayri dosyalara.

### Olusturulan Dosyalar (tamam)

```
src/bookmaker/studio/
├── models.py                       # Pydantic modeller (10+ model)
├── jobs.py                         # Job, JobManager, create/get/list/cancel
├── services/
│   ├── __init__.py
│   ├── manifest_service.py         # load_manifest, add_chapter, remove, reorder, update
│   ├── pipeline_service.py         # run_generation, cancel_generation, get_state
│   ├── llm_service.py              # configure, test_connection, get_status
│   ├── build_service.py            # build_chapter_docx, extract_code, render_mermaid
│   └── quality_service.py          # validate_chapter, quality_report, code_compile
└── static/
    ├── app.js                      # Tüm JS logic (index.html'den taşınacak)
    └── styles.css                  # Tüm CSS (index.html'den taşınacak)
```

### Değişecek Dosyalar (3)

| Dosya | Yapılacak |
|-------|----------|
| `studio/app.py` | Route'lar kalır, logic `services/`'e taşınır. `app.mount("/static")` + CORS eklenir. |
| `templates/index.html` | `<script>` ve `<style>` etiketleri kaldırılır, `<link href="/static/styles.css">` ve `<script src="/static/app.js">` eklenir |
| `tests/unit/test_studio_app.py` | Servis delegate testleri eklenecek |

### Kontrol Listesi
- [x] `app.py` < 300 satir (temiz route-only)
- [x] 9 servis dosyasi olusturuldu
- [x] `models.py` 15 Pydantic model iceriyor
- [x] `jobs.py`: create_job, get_job, list_jobs, cancel_job calisiyor
- [x] `app.js` bagimsiz calisiyor (index.html'den ayrı)
- [x] `styles.css` tum stilleri iceriyor
- [x] CORS header'lari aktif
- [x] `/static/` mount calisiyor
- [x] Mevcut testler geciyor (24 test)
- [x] `test_studio_services.py` yazildi

---

## Faz 2: Bölüm Yönetim Paneli

**Hedef:** Filtreleme, sıralama, sayfalama, drag-drop sıralama, CRUD, toplu işlem.

### Değişecek Dosyalar (5)

| Dosya | Yapılacak |
|-------|----------|
| `studio/app.py` | CRUD endpoint'leri: `POST/PUT/DELETE /api/chapters`, `PUT /api/chapters/reorder` |
| `services/manifest_service.py` | `add_chapter()`, `remove_chapter()`, `reorder_chapters()`, `update_chapter()` |
| `models.py` | `ChapterCreate`, `ChapterUpdate`, `ChapterReorder` |
| `templates/index.html` | Filtre barı, checkbox sütunu, drag handle (`⋮⋮`) |
| `static/app.js` | `filterChapters()`, `sortChapters()`, `dragDrop()`, `bulkSelect()`, sayfalama |

### Yeni Endpoint'ler
```
POST   /api/chapters              # Bölüm ekle
PUT    /api/chapters/{id}         # Güncelle (başlık, sıra)
DELETE /api/chapters/{id}         # Sil (onay modal'lı)
PUT    /api/chapters/reorder      # Sürükle-bırak sıralaması
GET    /api/chapters?status=approved&sort=score&page=1&per=20
```

### Kontrol Listesi
- [x] Durum dropdown'ı ile filtreleme çalışıyor
- [x] Sütun başlıkları tıklanınca sıralama yapıyor (↕)
- [x] Bölümler sürükle-bırak ile yeniden sıralanabiliyor
- [x] Yeni bölüm eklenebiliyor
- [x] Bölüm silinebiliyor (onay modal'ı ile)
- [x] Sayfalama çalışıyor (>20 bölüm varsa)
- [x] Toplu işlem butonları (seçili bölümlere üret/build/onayla)
- [x] Manifest otomatik güncelleniyor

---

## Faz 3: Pipeline Geliştirme + Prompt Takibi

**Hedef:** Enrich seçimi, sıcaklık slider'ı, iptal/duraklat, toast sistemi, LLM prompt/response canlı takip.

### Oluşturulacak Dosyalar (1 yeni)
```
static/toast.js                    # Toast bildirim modülü (showToast, 3 seviye)
```

### Değişecek Dosyalar (6)

| Dosya | Yapılacak |
|-------|----------|
| `studio/app.py` | İptal endpoint'i, `/api/llm-test` |
| `services/pipeline_service.py` | `cancel_job()`, `pause_job()`, sıcaklık parametresi |
| `jobs.py` | `cancel_job()`, `get_job_log()`, durum güncellemeleri |
| `models.py` | `GenerateRequest`'e `temperature`, `enrich_types`, `show_prompts` ekle |
| `templates/index.html` | Enrich checkbox grubu, sıcaklık slider, iptal butonu, prompt paneli |
| `static/app.js` | Toast entegrasyonu, enrich seçimi, WebSocket cancel, prompt/response paneli |

### Yeni Endpoint'ler
```
POST   /api/llm-test               # Bağlantı testi
POST   /api/generate/{id}/cancel   # Pipeline iptal
GET    /api/jobs/{id}/log          # İş log'u
GET    /api/jobs                   # İş listesi
```

### Kontrol Listesi
- [x] 6 enrich tipi checkbox ile seçilebiliyor
- [x] Sıcaklık slider'ı çalışıyor (0.0-1.5, varsayılan 0.7)
- [x] Pipeline iptal edilebiliyor (WS kapanır, job durumu güncellenir)
- [x] LLM prompt paneli: Gönderilen prompt ve alınan yanıt görüntüleniyor
- [x] Toast bildirimleri 3 seviyede çalışıyor (auto-dismiss)
- [x] İş geçmişi tablosu listeleniyor
- [x] İş log'u görüntüleniyor
- [x] Fallback stratejisi aktif (SPEC/ENRICH hatalarında)

---

## Faz 4: Kalite Kontrol Paneli (5. Sekme)

**Hedef:** Skor tablosu, hata listesi, kod derleme (`javac`), kitap istatistik dashboard'u.

### Oluşturulacak Dosyalar (1 yeni)
```
services/quality_service.py        # validate, code_compile, stats
```

### Değişecek Dosyalar (4)

| Dosya | Yapılacak |
|-------|----------|
| `studio/app.py` | `/api/quality/report`, `/api/code/validate`, `/api/stats`, `/api/search` |
| `templates/index.html` | 5. sekme (📊 Kalite) HTML |
| `static/app.js` | Kalite paneli JS, bar chart, kod derleme UI |
| `static/styles.css` | Kalite paneli stilleri, bar chart CSS |

### Yeni Endpoint'ler
```
GET    /api/quality/report          # Tüm bölümler kalite raporu
GET    /api/quality/report/{id}     # Tek bölüm kalite
POST   /api/code/validate           # Kod derle (javac)
GET    /api/stats                   # Kitap istatistikleri
GET    /api/search?q=...&regex=true # Tam metin arama
```

### Kontrol Listesi
- [x] 5. sekme görünür ve çalışıyor
- [x] Skor tablosu tüm bölümleri listeliyor, sıralanabiliyor
- [x] Hata/uyarı listesi kategorilere ayrılmış, filtrelenebiliyor
- [x] `javac` ile kod derleme çalışıyor, sonuçlar gösteriliyor
- [x] Kitap istatistikleri doğru (toplam kelime, kod, diyagram, okuma süresi)
- [x] Bar chart (kelime dağılımı) CSS ile render ediliyor

---

## Faz 5: Kitap Sihirbazı

**Hedef:** 5 adımlı wizard ile sıfırdan kitap projesi başlatma.

### Oluşturulacak Dosyalar (1 yeni)
```
services/wizard_service.py         # LLM plan oluşturma, proje başlatma
```

### Değişecek Dosyalar (4)

| Dosya | Yapılacak |
|-------|----------|
| `studio/app.py` | `/api/book/create`, `/api/wizard/plan` |
| `templates/index.html` | Wizard modal HTML (5 adım stepper) |
| `static/app.js` | Wizard JS (adım geçişleri, validasyon, LLM plan call) |
| `static/styles.css` | Wizard stilleri (stepper, kart animasyonları) |

### Yeni Endpoint'ler
```
POST   /api/book/create             # Yeni kitap oluştur
POST   /api/wizard/plan             # LLM ile bölüm planı öner
```

### Kontrol Listesi
- [x] Wizard modal açılıyor (header'dan "Yeni Kitap" butonu)
- [x] 3 adım Next/Back ile ilerliyor
- [x] Her adım valide ediliyor
- [x] LLM bölüm planı başarıyla oluşturuluyor
- [x] Kitap projesi dizinde oluşturuluyor
- [x] Manifest/state/config dosyaları yazılıyor

---

## Faz 6: Build & Export Merkezi

**Hedef:** Kod çıkarma, Mermaid→PNG, bölüm birleştirme, çoklu format export (DOCX/PDF/EPUB/HTML).

### Oluşturulacak Dosyalar (1 yeni)
```
services/assemble_service.py       # Birleştirme, indeks, glossary
```

### Değişecek Dosyalar (6)

| Dosya | Yapılacak |
|-------|----------|
| `studio/app.py` | `/api/extract`, `/api/render/mermaid`, `/api/assemble`, `/api/export`, `/api/backup` |
| `services/build_service.py` | `extract_code()`, `render_mermaid()`, `build_docx()`, `build_pdf()` |
| `services/assemble_service.py` | `assemble_book()`, `generate_index()`, `generate_glossary()` |
| `services/manifest_service.py` | `backup_project()`, `restore_project()` |
| `templates/index.html` | Build sekmesi güncellemesi |
| `static/app.js` | Build paneli JS, işlem sırası, sonuç gösterme |

### Yeni Endpoint'ler
```
POST   /api/extract/{id}            # Kod çıkarma (.java dosyaları)
POST   /api/extract/all             # Tüm bölümlerden kod çıkar
POST   /api/render/mermaid/{id}     # Mermaid→PNG render
POST   /api/render/mermaid/all      # Tüm bölümlerden mermaid render
POST   /api/assemble                # Tüm bölümleri birleştir
POST   /api/export/docx             # Birleşik→DOCX
POST   /api/export/pdf              # Birleşik→PDF
POST   /api/export/epub             # Birleşik→EPUB
POST   /api/export/html             # Birleşik→HTML
POST   /api/backup                  # .zip yedekle
POST   /api/restore                 # Yedekten geri yükle
```

### Kontrol Listesi
- [x] Kod çıkarma: `build/code/{bolum}/` altına `.java` dosyaları yazılıyor
- [x] Kod derleme: `javac` ile kontrol, sonuçlar gösteriliyor
- [x] Mermaid→PNG: `build/mermaid_images/` altına PNG'ler yazılıyor, önizleme var
- [x] Birleştirme: tüm bölümler tek `.md` olarak birleşiyor
- [x] DOCX export: referans şablonlu, mermaid gömülü
- [x] PDF/EPUB/HTML export çalışıyor
- [x] `.zip` yedekleme ve geri yükleme çalışıyor

---

## Faz 7: İleri Seviye (v2.0)

**Hedef:** Çoklu kitap, kullanıcı rolleri, reader modu, bildirimler, Docker/PWA.

### Yeni Endpoint'ler
```
GET    /api/books                   # Kitap listesi
POST   /api/auth/login              # Kullanıcı girişi
POST   /api/notifications/subscribe  # Bildirim aboneliği
```

### Kontrol Listesi
- [ ] Çoklu kitap projesi desteği (header'da kitap seçici)
- [ ] Login sayfası + kullanıcı rolleri
- [ ] Reader modu (tam ekran, sayfa düzeni, karanlık mod)
- [ ] Bildirim merkezi (🔔 + dropdown liste + tarayıcı bildirimi)
- [ ] Çapraz referans takibi
- [ ] Docker container desteği
- [ ] PWA (manifest + service worker)

---

## 📊 Ilerleme Takip Tablosu

| Faz | Aciklama | Durum | Kritik Cikti |
|-----|----------|-------|-------------|
| 0 | Mevcut durum | ✅ | Monolitik app.py |
| 1 | Servis mimarisi + Models + Jobs | ✅ | 9 servis + models.py + jobs.py + static/ |
| 2 | Bolum yonetim paneli | ✅ | Filter/sort/drag-drop + CRUD |
| 3 | Pipeline + Prompt takibi | ✅ | Toast/iptal/prompt paneli |
| 4 | Kalite kontrol paneli | ✅ | 5. sekme + javac + stats |
| 5 | Kitap sihirbazi | ✅ | 5 adimli wizard |
| 6 | Build & Export merkezi | ✅ | Kod cikarma + PNG + DOCX/PDF/EPUB/HTML |
| 7 | Ileri seviye (v2.0) | 🔲 | Coklu kitap + reader + bildirim + PWA |

---

## 🔄 Yeni Sohbete Devam Promptu

```
bookMaker Studio GUI geliştirmesine devam edelim.
GUI_ROADMAP.md Faz {X}'ten başla.
Proje: D:\bookMaker_Deepseek
Dosyalar: GUI_MANIFEST.md ve GUI_ROADMAP.md güncel.
```
