# bookMaker

`bookMaker`, akademik ve teknik kitapların LLM destekli, kalite kapılı ve proje tabanlı üretilmesi için tasarlanmış bir kitap üretim framework'üdür.

Bu repo artık iki sorumluluğu birbirinden ayırır:

```text
D:\bookMaker_Deepseek/       # Framework / motor
├── src/bookmaker/             # Python otomasyon kodu
├── prompts/                   # Framework düzeyi örnek/preset promptlar
├── tools/                     # Yardımcı araçlar
├── tests/                     # Testler
├── docs/                      # Dokümantasyon
└── book_projects/             # Kitap projelerinin yerel çalışma alanı
    └── <book-alias>/          # Bağımsız kitap projesi
```

> Not: `book_projects/<book-alias>/` klasörleri framework dosyası içermez. Her kitap projesi kendi `book_manifest.yaml`, `pipeline_state.yaml`, `chapters/`, `prompts/`, `exports/` ve `logs/` klasörleriyle bağımsızdır.

---

## Kitap proje yapısı

Güncel kitap proje standardı:

```text
<book-alias>/
├── book_manifest.yaml
├── pipeline_state.yaml
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

Ana kurallar:

- Kitabın genel yapısı `book_manifest.yaml` içindedir.
- Bölüm sırası `book_manifest.yaml > chapters` listesinden alınır.
- Her bölümün içerik kapsamı `chapters/<chapter-alias>/chapter_manifest.yaml` içinde tutulur.
- Runtime durum, kalite skoru ve otomasyon bayrakları `pipeline_state.yaml` içinde tutulur.
- Üretim çıktıları `exports/`, loglar `logs/` altında kalır.
- Framework klasörüne kitaba özgü üretim dosyası yazılmaz.

---

## Örnek Flutter kitap projesi

Bu dalda örnek kitap projesi:

```text
book_projects/flutter-ile-mobil-uygulama-gelistirme/
```

Bu proje Flutter kitabı için 16 bölümlük manifest, bölüm manifestleri, varsayılan üretim/review promptları, export klasörleri ve log klasörlerini içerir.

---

## Kurulum

```powershell
git clone https://github.com/bmdersleri/bookMaker.git D:\bookMaker_Deepseek
cd D:\bookMaker_Deepseek
git checkout feat/project-based-architecture

uv venv --python 3.12
uv sync
```

Alternatif olarak mevcut Python ortamınızda:

```powershell
pip install -e .
```

---

## Yeni kitap projesi oluşturma

Flutter preset'iyle yeni kitap projesi:

```powershell
bookmaker init --path book_projects/flutter-ile-mobil-uygulama-gelistirme --preset flutter-mobil --author "Prof. Dr. İsmail KIRBAŞ"
```

Boş proje:

```powershell
bookmaker init --path book_projects/yeni-kitap --author "Yazar Adı"
```

---

## Kalite kontrol

Kitap proje kökünden:

```powershell
cd book_projects/flutter-ile-mobil-uygulama-gelistirme
bookmaker check book
```

Framework kökünden:

```powershell
bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme
```

Tek bölüm içeriği kontrolü:

```powershell
bookmaker check chapter book_projects/flutter-ile-mobil-uygulama-gelistirme/chapters/giris/content/draft.md
```

JSON rapor üretimi:

```powershell
bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json
```

Raporlar yeni mimaride `logs/reviews/` altına yazılır.

---

## Önemli dokümanlar

- `book_project_dir.md`: Güncel kitap proje klasör standardı.
- `MIGRATION.md`: Project-based architecture geçiş planı.
- `book_projects/flutter-ile-mobil-uygulama-gelistirme/README.md`: Flutter kitabı örnek proje açıklaması.

---

## Geliştirme ilkeleri

- Manifest tabanlı ilerle.
- Bölüm alias'larını tekil kaynak olarak kullan.
- Path'leri YAML içinde tekrarlama; convention'dan türet.
- `pipeline_state.yaml` dosyasını runtime durum kaydı olarak yönet.
- Çıkarılabilir/test edilebilir kodlarda `CODE_META`, ekran çıktılarında `SCREENSHOT_META` + `[SCREENSHOT:...]` kullan.
