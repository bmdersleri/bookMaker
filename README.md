# bookMaker

`bookMaker`, akademik ve teknik kitaplarin LLM destekli, kalite kapili ve proje tabanli uretilmesi icin tasarlanmis bir kitap uretim framework'udur.

```text
bookMaker/
├── src/bookmaker/             # Python otomasyon kodu
├── tests/                     # Testler
├── docs/                      # Dokumantasyon
├── book_projects/             # Kitap projeleri
│   ├── flutter-ile-mobil-uygulama-gelistirme/
│   └── python-programlama-giris/
└── tools/                     # Yardimci araclar
```

> Her kitap projesi kendi `book_manifest.yaml`, `pipeline_state.yaml`, `chapters/`, `prompts/`, `exports/` ve `logs/` klasorleriyle bagimsizdir.

---

## Kitap Proje Yapisi

```text
<book-alias>/
├── book_manifest.yaml          # TEK konfigurasyon kaynagi
├── pipeline_state.yaml         # Runtime durum, skor, otomasyon bayraklari
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
│   ├── docx/
│   ├── pdf/
│   └── md/
└── logs/
    ├── production/
    ├── errors/
    └── reviews/
```

**Ana kurallar:**
- Tek konfigurasyon kaynagi: `book_manifest.yaml`
- Bolum sirasi `book_manifest.yaml > chapters` listesinden alinir
- Runtime durum `pipeline_state.yaml` icinde tutulur
- Uretim ciktilari `exports/`, loglar `logs/` altinda kalir
- `book_profile.yaml` artik kullanilmiyor

---

## Kurulum

```powershell
git clone https://github.com/bmdersleri/bookMaker.git
cd bookMaker
uv sync
```

---

## Kullanim

### Studio GUI

```powershell
uv run python -m bookmaker.studio.app
# http://localhost:8765
```

6 sekme: Bolumler, Pipeline, Kalite, Build/Export, Promptlar, Yapilandirma

### CLI

```powershell
# Kalite kontrol
bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme
bookmaker check chapter chapters/giris/content/draft.md --book-root book_projects/...

# JSON rapor
bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json
```

### Yeni kitap olusturma (GUI Wizard)

Studio > "Yeni Kitap" butonu > 3 adimli sihirbaz

---

## Pipeline

6 asamali bolum uretim pipeline'i:

```text
SPEC → VALIDATE → SEED → NORMALIZE → ENRICH → ASSEMBLE
```

Detaylar: `CHAPTER_PRODUCTION.md`

---

## Test

```powershell
uv run ruff check src/           # lint
uv run pytest tests/ -q --tb=short  # test (218 passed)
```

---

## Onemli Dokumanlar

| Dosya | Amac |
|-------|------|
| `SESSION.md` | Oturum gunlugu |
| `CLAUDE.md` | Agent talimatlari |
| `CHAPTER_PRODUCTION.md` | 6 asamali pipeline dokumantasyonu |
| `GUI_ROADMAP.md` | Studio GUI yol haritasi (Faz 1-6 tamam) |
| `CHANGELOG.md` | Surum gecmisi |
| `MIGRATION.md` | project-based mimari gecis kaydi (tamamlandi) |
| `book_project_dir.md` | Kitap proje klasor standardi |
| `docs/` | Tarihi tasarim ve planlama dokumanlari |

---

## Gelistirme Ilkeleri

- Manifest tabanli ilerle (`book_manifest.yaml` tek kaynak)
- Bolum alias'larini tekil kaynak olarak kullan
- Path'leri YAML icinde tekrarlama; convention'dan turet
- Kucuk, test edilebilir commit'lerle ilerle
- Her degisiklik sonrasi: `ruff check` + `pytest`
