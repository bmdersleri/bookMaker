# bookMaker

LLM destekli, kalite kapili, proje tabanli akademik/teknik kitap uretim framework'u.

```text
Kitap projesi  →  book_manifest.yaml  →  6 asamali pipeline  →  DOCX/PDF/EPUB/HTML
                                     →  Studio GUI (localhost:8765)
```

> **LLM'ler icin:** Projeyi tam olarak anlamak isteyen AI ajanlari `LLM_EXPLANATION.md` dosyasini okumali. Bu dosya mimari, pipeline, GUI ve tum ozellikleri tek bir dokumanda aciklar.

---

## Icerik

- [Kurulum](#kurulum)
- [Studio GUI](#studio-gui)
- [Kitap Proje Yapisi](#kitap-proje-yapisi)
- [Pipeline](#pipeline)
- [CLI Kullanim](#cli-kullanim)
- [Test](#test)
- [Dokumanlar](#dokumanlar)
- [Gelistirme Ilkeleri](#gelistirme-ilkeleri)

---

## Kurulum

```powershell
git clone https://github.com/bmdersleri/bookMaker.git
cd bookMaker
uv sync
```

**Baslangic:**
```powershell
uv run python -m bookmaker.studio.app    # GUI (http://localhost:8765)
bookmaker check book <kitap-dizini>      # CLI kalite kontrol
```

---

## Studio GUI

6 sekme, vanilla JS, karanlik/aydinlik mod destegi olmayan sade arayuz.

| Sekme | Ozellikler |
|-------|-----------|
| **Bolumler** | Tablo (sirala, filtrele, sayfala), drag-drop siralama, **basliklara cift tiklayip inline edit**, toplu silme, bolum ekleme wizard'i, bolum bazli Gor/ Kontrol/Build/Uret butonlari |
| **Pipeline** | Manuel tetikleme, canli progress bar, **job detay paneli** (adim adim prompt→cikti eslesmesi + sure), iptal, job gecmisi |
| **Kalite** | Kitap ozeti (skor/karar/hata/uyari), bolum kalite tablosu, kontrol modali, istatistikler, tam metin arama |
| **Build/Export** | Export hedefleri, **readiness pre-check** (`/api/export/readiness`), referans DOCX / lua filter / TOC derinligi secimi, kod cikarma, Mermaid render, birlestirme, format export, yedekleme |
| **Promptlar** | Varsayilan/bolum prompt editoru, dirty-state uyarisi, yukle/kaydet |
| **Yapilandirma** | `book_manifest.yaml` full editor (Kitap Bilgisi, Uretim, Stil, Otomasyon, Export alt sekmeleri) |

---

## Kitap Proje Yapisi

Her kitap `book_projects/` altinda bagimsiz bir dizindir:

```text
<kitap-adi>/
├── book_manifest.yaml          # TEK konfigurasyon kaynagi (kitap, uretim, stil, pandoc, output, bolumler)
├── pipeline_state.yaml         # Runtime durum, kalite skoru, otomasyon bayraklari
├── prompts/
│   ├── default_chapter.md      # Varsayilan bolum uretim promptu
│   └── default_review.md       # Varsayilan review promptu
├── chapters/
│   └── <bolum-alias>/
│       ├── chapter_manifest.yaml
│       ├── prompt.md
│       └── content/
│           ├── draft.md        # Uretilen taslak
│           ├── final.md        # Onaylanmis final
│           └── revisions/
├── exports/                    # Build ciktilari
│   ├── docx/
│   ├── pdf/
│   └── md/
└── logs/                       # Runtime loglar
    ├── production/             # Pipeline adim ciktilari (job bazli)
    │   └── export_<ts>.json    # Export readiness + sonuc raporu
    ├── errors/
    └── reviews/                # Kalite review raporlari
```

**Kurallar:**
- `book_manifest.yaml` tek konfigurasyon kaynagidir; `book_profile.yaml` sadece legacy okuma fallback'idir
- Bolum sirasi `book_manifest.yaml > chapters` listesinden alinir
- Dosya yollari YAML'de tekrarlanmaz — alias'tan convention ile turetilir
- `pipeline_state.yaml` runtime durumu tutar, framework tarafindan yonetilir

**Desteklenen Python sürümü:** en az 3.12, geliştirme ortamında 3.14.x kullanılır.

---

## Pipeline

6 asamali LLM destekli bolum uretim hatti:

```text
SPEC ──→ VALIDATE ──→ SEED ──→ NORMALIZE ──→ ENRICH ──→ ASSEMBLE
(plan)    (kontrol)    (uretim)  (temizlik)    (paralel)    (birlestirme)
```

| Asama | Surec | Cikti |
|-------|-------|-------|
| **SPEC** | LLM'e baslik + kavram verilir, KOD YAZMAZ, plan hazirlar | `step0_spec.md` + `prompt0_spec.txt` |
| **VALIDATE** | SPEC ciktisi format ve kapsam acisindan kontrol edilir | `step0_validation.md` |
| **SEED** | 6 adimli pedagojik zincirle gercek bolum icerigi uretilir | `step1_seed.md` + `prompt1_seed.txt` |
| **NORMALIZE** | 0-token regex temizligi, front matter ekleme, heading duzeltme | `step2_normalized.md` |
| **ENRICH** | 6 paralel LLM cagrisi (ozet, sozluk, soru, alistirma, hata, kopru) | `step3_enrich_*.md` (6 dosya) |
| **ASSEMBLE** | Zenginlestirmeler birlestirilir, son normalize, draft'a yazilir | `step4_final.md` → `draft.md` |

6 adimli pedagojik derinlik zinciri: **TANIM → NEDEN VAR? → NASIL KULLANILIR? → NE ZAMAN TERCİH EDİLİR? → ALTERNATİFLERİ → YAYGIN HATALAR**

Detayli dokumantasyon: [`CHAPTER_PRODUCTION.md`](CHAPTER_PRODUCTION.md)

---

## CLI Kullanim

```powershell
# Kalite kontrol
bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme
bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose

# Tek bolum kontrolu
bookmaker check chapter chapters/giris/content/draft.md --book-root book_projects/...
```

---

## Test

```powershell
uv run ruff check src/                      # lint
uv run pytest tests/ -q --tb=short           # 223 passed
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json
```

---

## Dokumanlar

| Dosya | Amac |
|-------|------|
| `LLM_EXPLANATION.md` | **AI ajanlari icin** eksiksiz proje aciklamasi (mimari, pipeline, GUI, API, tasarim kararlari) |
| `SESSION.md` | Oturum gunlugu — her oturum sonunda guncellenir |
| `CLAUDE.md` | Claude Code agent talimatlari |
| `CHAPTER_PRODUCTION.md` | 6 asamali pipeline detayli dokumantasyonu |
| `GUI_ROADMAP.md` | Studio GUI gelistirme yol haritasi (Faz 1-6 ✅, Faz 7 planlandi) |
| `CHANGELOG.md` | Surum gecmisi (v0.1.0, v0.2.0) |
| `TODO.md` | Yapilacaklar listesi |
| `MIGRATION.md` | Project-based mimari gecis kaydi (tamamlandi) |
| `book_project_dir.md` | Kitap proje klasor standardi |
| `docs/` | Tarihi tasarim ve planlama dokumanlari arsivi |

---

## Gelistirme Ilkeleri

- `book_manifest.yaml` tek dogruluk kaynagi — burada olmayan konfigurasyon yoktur
- Bolumleri alias ile referansla, numeric ID veya path ile degil
- Her patch sonrasi 3'lu kontrol: `ruff check` → `pytest` → `bookmaker check book`
- Kucuk, review edilebilir commit'ler; buyuk refactor'dan kacin
- `llm_config.json` ve `.claude/settings.local.json` asla commit edilmez
- Pipeline hata durumunda durmaz — non-fatal hatalarda devam eder, log'a yazar
