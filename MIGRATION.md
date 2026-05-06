# Migration: Project-Based Architecture

**Branch:** `feat/project-based-architecture`  
**Başlangıç tarihi:** 2026-05-06  
**Hedef:** Framework ile kitap projesini tamamen ayırmak. Framework = motor, kitap projesi = içerik, manifest, prompt, runtime state, log ve export alanı.

---

## Güncel Mimari Kararı

```text
D:\bookMaker_Deepseek/                 # Framework / motor
├── src/bookmaker/                       # Python otomasyon kodu
├── prompts/                             # Framework/preset düzeyi örnek promptlar
├── tools/                               # Yardımcı araçlar
├── tests/                               # Framework testleri
├── docs/                                # Framework dokümantasyonu
└── book_projects/                       # Yerel kitap proje çalışma alanı
    └── <book-alias>/                    # Bağımsız kitap projesi
        ├── book_manifest.yaml           # Kullanıcı/yazar: genel kitap konfigürasyonu
        ├── pipeline_state.yaml          # Framework: runtime state
        ├── prompts/
        │   ├── default_chapter.md
        │   └── default_review.md
        ├── chapters/
        │   └── <chapter-alias>/
        │       ├── chapter_manifest.yaml
        │       ├── prompt.md
        │       └── content/
        │           ├── draft.md
        │           ├── final.md
        │           └── revisions/
        ├── exports/
        └── logs/
```

Kitap projesi ayrı bir Git reposu olarak da tutulabilir. `book_projects/` yalnızca framework ile birlikte çalışma kolaylığı sağlayan yerel bir çalışma alanıdır.

---

## Sorumluluk Ayrımı

| Bileşen | Sahip | Açıklama |
|---|---|---|
| `book_manifest.yaml` | Kullanıcı/yazar | Kitap kimliği, üretim parametreleri, stil, teknik profil, bölüm sırası |
| `chapter_manifest.yaml` | Kullanıcı/yazar | Bölüm kapsamı, hedefleri, yapı, otomasyon override ayarları |
| `prompt.md` | Kullanıcı/yazar | Bölüme özel üretim yönergesi |
| `content/draft.md` | Framework / üretici LLM | Taslak bölüm içeriği |
| `content/final.md` | Framework / yazar onayı | Onaylı bölüm içeriği |
| `pipeline_state.yaml` | Framework | Runtime state, kalite skorları, otomasyon bayrakları |
| `logs/` | Framework | Üretim, hata, review kayıtları |
| `exports/` | Framework | DOCX, PDF, birleşik Markdown çıktıları |

---

## LLM Rolleri

- **Üretici LLM:** `book_manifest.yaml`, `chapter_manifest.yaml`, `prompt.md` ve varsayılan promptları kullanarak bölüm taslağı üretir.
- **Gözlemci LLM:** Üretilen taslağı `book_manifest.yaml` ve `chapter_manifest.yaml` ile karşılaştırarak kalite raporu üretir.
- **Yardımcı LLM:** GUI/Studio içinde manifest, prompt ve kalite iyileştirme önerileri üretir.

---

## Geçişte Kaldırılan Eski Varsayımlar

Aşağıdaki eski yapı artık kanonik değildir:

```text
book_profile.yaml
book_architecture.yaml
chapters/<chapter_id>/seed/
chapters/<chapter_id>/outline_versions/
chapters/<chapter_id>/draft_versions/
chapters/<chapter_id>/approved/
build/merged/
build/reports/
```

Yeni karşılıklar:

| Eski yapı | Yeni yapı |
|---|---|
| `book_profile.yaml` | `book_manifest.yaml` |
| `book_architecture.yaml` | `book_manifest.yaml > chapters` + `chapters/<alias>/chapter_manifest.yaml` |
| `draft_versions/v001.md` | `content/draft.md` ve gerekirse `content/revisions/v001.md` |
| `approved/` | `content/final.md` |
| `build/reports/` | `logs/reviews/`, `logs/errors/`, `logs/production/` |
| `build/merged/` | `exports/md/` |
| Sabit `CHAPTER_ORDER` | `book_manifest.yaml > chapters` listesi |

---

## Uygulama Fazları

### FAZ 1 — Manifest ve Path Temeli

Eklenen/yenilenen dosyalar:

```text
src/bookmaker/manifest/models.py
src/bookmaker/manifest/__init__.py
src/bookmaker/core/paths.py
```

Hedefler:

- `BookManifest`, `ChapterManifest`, `PipelineState` modellerini tanımlamak.
- Path üretimini YAML içinden değil, convention üzerinden yapmak.
- Kitap proje kökünü `book_manifest.yaml` üzerinden tanımak.

Kontrol:

```powershell
python - <<'PY'
from pathlib import Path
from bookmaker.manifest.models import BookManifest, PipelineState
p = Path("book_projects/flutter-ile-mobil-uygulama-gelistirme")
m = BookManifest.load(p / "book_manifest.yaml")
s = PipelineState.load(p / "pipeline_state.yaml")
print(m.book.alias, len(m.chapters), s.pipeline.book_alias)
PY
```

---

### FAZ 2 — CLI Init Adaptasyonu

`bookmaker init` artık yeni mimariyi üretmelidir.

Örnek:

```powershell
bookmaker init --path book_projects/flutter-ile-mobil-uygulama-gelistirme --preset flutter-mobil --author "Prof. Dr. İsmail KIRBAŞ"
```

Üretilen yapı:

```text
book_manifest.yaml
pipeline_state.yaml
prompts/default_chapter.md
prompts/default_review.md
chapters/<alias>/chapter_manifest.yaml
chapters/<alias>/prompt.md
chapters/<alias>/content/draft.md
chapters/<alias>/content/final.md
chapters/<alias>/content/revisions/
exports/docx/
exports/pdf/
exports/md/
logs/production/
logs/errors/
logs/reviews/
```

---

### FAZ 3 — Kitap Validasyonu

`bookmaker check book` artık sabit Java bölüm listesi kullanmaz.

Yeni davranış:

- Bölüm sırası `book_manifest.yaml > chapters` listesinden okunur.
- Her bölüm için `chapters/<alias>/chapter_manifest.yaml` aranır.
- İçerikler `chapters/<alias>/content/draft.md` ve `content/final.md` üzerinden kontrol edilir.
- Raporlar `logs/reviews/` altına yazılır.

Örnek:

```powershell
bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json
```

---

### FAZ 4 — Bölüm Validasyonu

`chapter/validator.py` Java'ya sabitlenmiş test modlarından arındırılmalıdır.

Kabul edilen test değerleri:

```text
dart_analyze
dart_test
dart_format_check
flutter_analyze
flutter_test
widget_test
integration_test
screenshot_only
review_only
skip
none
```

---

### FAZ 5 — Studio ve Servis Katmanı

Studio servisleri yeni mimariye göre bölünmelidir:

| Servis | Sorumluluk |
|---|---|
| `book_service.py` | `book_manifest.yaml` CRUD |
| `chapter_service.py` | `chapter_manifest.yaml` CRUD |
| `pipeline_service.py` | `pipeline_state.yaml` okuma/güncelleme |
| `prompt_service.py` | Prompt dosyaları CRUD |
| `generation_service.py` | Üretici LLM ile bölüm üretimi |
| `observer_service.py` | Gözlemci LLM review |
| `export_service.py` | Birleştirme + DOCX/PDF export |

Durum:

```text
Başladı.
İlk adım: Studio proje seçici ve wizard project-based manifest yapıya hizalandı.
```

Tamamlanan ilk işler:

- `/api/projects` ve `/api/active-book` legacy `book_profile.yaml` yerine `book_manifest.yaml` okur.
- Studio wizard yeni kitap oluştururken project-based workspace üretir.
- Wizard artık yeni projelerde `book_profile.yaml`, `book_architecture.yaml`, `approved/`, `draft_versions/`, `seed/`, `outline_versions/` oluşturmaz.
- Aktif kitap bir proje kökü ise yeni kitap parent `book_projects/` workspace altında oluşturulur.

Sıradaki işler:

- Generation/job worker çıktısını `build/generation` yerine project-based `content/` ve `logs/` yapısına taşımak.
- `quality_service`, `build_service`, `export_service` içinde kalan legacy path varsayımlarını azaltmak.
- Prompt edit UI akışını mevcut `prompt_service` endpoint'lerine bağlamak.
- `observer_service` için review üretim/yazım sorumluluğunu netleştirmek.

---

## Test Stratejisi

Her fazdan sonra:

```powershell
uv run ruff check src/
uv run pytest tests/ -q --tb=short
```

Kitap proje validasyonu:

```powershell
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose
```

Flutter kitap projesi için beklenen temel kontroller:

- `book_manifest.yaml` var.
- `pipeline_state.yaml` var.
- `prompts/default_chapter.md` ve `prompts/default_review.md` var.
- `chapters/` altındaki tüm alias klasörleri manifestteki sırayla uyumlu.
- Her bölümde `chapter_manifest.yaml`, `prompt.md`, `content/draft.md`, `content/final.md`, `content/revisions/` var.
- Bölüm referansları alias ile yapılmış.
- Runtime state yalnızca `pipeline_state.yaml` içinde tutulmuş.
- Export ve log dosyaları kitap proje kökü içinde kalıyor.

---

## CI Notu

Geliştirme dalında CI tetiklenmesi için workflow şu branch desenini de kapsamalıdır:

```yaml
on:
  push:
    branches:
      - main
      - deepseek
      - "feat/**"
  pull_request:
    branches:
      - main
      - deepseek
      - "feat/**"
  workflow_dispatch:
```

---

## Referans Dosyalar

- `book_project_dir.md`
- `book_projects/flutter-ile-mobil-uygulama-gelistirme/book_manifest.yaml`
- `book_projects/flutter-ile-mobil-uygulama-gelistirme/pipeline_state.yaml`
- `book_projects/flutter-ile-mobil-uygulama-gelistirme/chapters/giris/chapter_manifest.yaml`
- `book_projects/flutter-ile-mobil-uygulama-gelistirme/prompts/default_chapter.md`
- `book_projects/flutter-ile-mobil-uygulama-gelistirme/prompts/default_review.md`

---

## Notlar

- `pipeline_state.yaml` framework tarafından yönetilir; ancak üretim geçmişi ve kalite durumu izlenebilir kalsın diye repoda versiyonlanabilir.
- Path'ler YAML içinde tekrarlanmaz; `BookPaths` ve `ChapterPaths` convention'larından türetilir.
- `chapter_manifest.yaml` runtime state içermez.
- `book_manifest.yaml` bölüm sırası için tekil kaynaktır.
- `check book` komutu manifest tabanlı olmalıdır; sabit bölüm listesi kullanılmamalıdır.
