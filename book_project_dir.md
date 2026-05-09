# Kitap Proje Klasör Yapısı

Bir bookMaker kitap projesi tamamen bağımsız bir klasördür. Framework'e ait hiçbir dosya içermez. Kitaba ait tüm içerik, konfigürasyon, prompt, runtime state, log ve çıktı dosyaları bu klasörde yer alır.

Kitap projesi ayrı bir Git reposu olabilir veya framework reposu içinde `book_projects/<book-alias>/` altında yerel çalışma alanı olarak tutulabilir. Her iki durumda da klasörün iç yapısı aynıdır.

---

## Sorumluluk Ayrımı

| Dosya | Kim yazar/günceller | Ne içerir |
|---|---|---|
| `book_manifest.yaml` | Kullanıcı / yazar | Kitabın genel çizgisi, üretim parametreleri, bölüm sırası |
| `chapter_manifest.yaml` | Kullanıcı / yazar | Bölümün içerik spesifikasyonu: scope, structure, otomasyon kuralları |
| `prompt.md` | Kullanıcı / yazar veya LLM destekli editör | Bölüme özel üretim yönlendirmesi |
| `content/draft.md` | Framework / üretici LLM | Taslak bölüm metni |
| `content/final.md` | Framework / yazar onayı sonrası | Onaylanmış bölüm metni |
| `pipeline_state.yaml` | Framework | Runtime state, kalite skorları, otomasyon bayrakları |
| `logs/` | Framework | Üretim, hata ve review kayıtları |
| `exports/` | Framework | DOCX, PDF ve birleşik Markdown çıktıları |

---

## Klasör Yapısı

```text
<book-alias>/                            # Kitap proje kök klasörü, alias = repo adı
│
├── book_manifest.yaml                   # Kitabın ana konfigürasyon dosyası
├── pipeline_state.yaml                  # Runtime state; framework tarafından yönetilir
│
├── prompts/                             # Varsayılan prompt dosyaları
│   ├── default_chapter.md               # Bölüm üretiminde varsayılan prompt
│   └── default_review.md                # Gözlemci LLM için varsayılan review promptu
│
├── chapters/                            # Tüm bölüm klasörleri
│   ├── <chapter-alias>/                 # Klasör adı = chapter alias
│   │   ├── chapter_manifest.yaml        # İçerik spesifikasyonu
│   │   ├── prompt.md                    # Bölüme özel prompt; opsiyonel ama önerilir
│   │   └── content/                     # Üretilen içerikler
│   │       ├── draft.md                 # Taslak içerik
│   │       ├── final.md                 # Onaylı final içerik
│   │       └── revisions/               # Revizyon geçmişi
│   │           ├── v001.md
│   │           └── v002.md
│   └── <chapter-alias>/
│       └── ...
│
├── exports/                             # Export çıktıları
│   ├── docx/
│   │   ├── <book-alias>_v001.docx
│   │   └── <book-alias>_v002.docx
│   ├── pdf/
│   │   └── <book-alias>_v001.pdf
│   └── md/
│       └── <book-alias>_birlesik.md
│
└── logs/
    ├── production/
    │   ├── <chapter-alias>_20260506.log
    │   └── ...
    ├── errors/
    │   └── errors_20260506.log
    └── reviews/
        ├── <chapter-alias>_review_20260506.md
        └── book_quality_report.json
```

---

## `book_manifest.yaml`

Kitabın tüm genel yapısını, üretim parametrelerini ve bölüm sıralamasını tanımlar.

```yaml
book:
  title: "Kitap Başlığı"
  subtitle: "Alt Başlık"
  author: "Yazar Adı"
  alias: "kitap-alias"
  repo: "https://github.com/..."
  language: tr
  version: 1.0.0
  edition: "1"
  year: 2026

production:
  producer_model: "deepseek-chat"
  observer_model: "deepseek-chat"
  producer_params:
    temperature: 0.7
    max_tokens: 8000
  observer_params:
    temperature: 0.3
    max_tokens: 4000
  generation_mode: chapter_based
  approval_required: true

style:
  target_audience: "Hedef kitle tanımı"
  tone: "akademik ama sade"
  code_language: dart
  framework: flutter
  terminology: "Türkçe açıklama + ilk geçtiği yerde İngilizce teknik terim"
  chapter_pattern:
    - Kavram
    - Küçük örnek
    - Çalışan uygulama
    - Ekran çıktısı
    - Kod açıklaması
    - Sık hata
    - Mini görev
    - Bölüm sonu laboratuvarı

technical_profile:
  flutter_channel: stable
  flutter_version: "3.x"
  dart_version: "3.x"
  primary_platform: android
  secondary_platforms:
    - ios
    - web
  ide:
    - Visual Studio Code
    - Android Studio

automation:
  code_meta_required: true
  screenshot_required: true
  minimum_screenshots_per_chapter: 1
  qr_policy: dual
  github_code_export: true
  manual_asset_override: true

chapters:
  - alias: "giris"
  - alias: "dart-temelleri"
  - alias: "widget-mantigi"
```

---

## `chapter_manifest.yaml`

Her bölüme özgü içerik kapsamını, bölüm yapısını ve otomasyon davranışını tanımlar. Runtime durum içermez.

```yaml
chapter:
  title: "Bölüm Başlığı"
  alias: "bolum-alias"
  order: 1
  references:
    - alias: "onceki-bolum"
      relation: prerequisite
    - alias: "sonraki-bolum"
      relation: next

scope:
  topics:
    - "Konu 1"
    - "Konu 2"
  objectives:
    - "Okuyucu X yapabilmeli"
  exclusions:
    - "Bu bölümde işlenmeyecek konular"
  mini_project: "Bölüm mini proje açıklaması"

structure:
  sections:
    - title: "Bölümün Yol Haritası"
      type: text
    - title: "Temel Örnek"
      type: text+code
    - title: "Çalışan Mini Uygulama"
      type: text+code+screenshot
    - title: "Sık Yapılan Hatalar"
      type: text
    - title: "Bölüm Sonu Laboratuvarı"
      type: exercise
    - title: "Özet"
      type: text
  estimated_pages: 18
  code_examples_count: 4
  screenshot_examples_count: 1

automation:
  code_meta_required: true
  screenshot_required: true
  default_code_language: dart
  default_framework: flutter
  validation_modes:
    - flutter_analyze
    - flutter_test
    - widget_test
  github_export: true
  qr_policy: dual
```

---

## `pipeline_state.yaml`

Framework tarafından oluşturulur ve güncellenir. Bölüm üretim durumu, kalite skorları ve otomasyon bayrakları burada tutulur.

```yaml
pipeline:
  schema_version: "1.0"
  book_alias: "kitap-alias"
  current_version: "v001"
  global_state: "initialized"
  created_at: "2026-05-06T00:00:00+03:00"
  updated_at: "2026-05-06T00:00:00+03:00"
  active_chapter: "giris"
  last_completed_chapter: null
  next_action: "İlk bölüm taslağı üretilecek."

production_context:
  producer_model: "deepseek-chat"
  observer_model: "deepseek-chat"
  generation_mode: "chapter_based"
  approval_required: true
  default_input_policy:
    use_book_manifest: true
    use_chapter_manifest: true
    use_chapter_prompt_if_exists: true
    fallback_to_default_chapter_prompt: true
  review_policy:
    observer_review_required: true
    fallback_to_default_review_prompt: true
    minimum_quality_score_for_approval: 85

chapters:
  - alias: "giris"
    order: 1
    status:
      state: "pending"
      draft_generated: false
      review_completed: false
      revision_required: false
      final_approved: false
      exported: false
      quality_score: null
      last_review: null
      last_updated: null
      issues: []
      suggestions: []
    automation:
      code_extraction_done: false
      code_tests_done: false
      screenshots_done: false
      qr_generation_done: false
      github_links_patched: false
```

---

## Kurallar

- Klasör adı her zaman `chapter_alias` ile aynıdır.
- Bölüm klasörleri daima `chapters/<chapter-alias>/` altında yer alır.
- `book_manifest.yaml` içindeki `chapters` listesinin sırası kitap birleştirme sırasını belirler.
- `pipeline_state.yaml`, `book_manifest.yaml` içinden otomatik senkronize edilir.
- `chapter_manifest.yaml`, içerik spesifikasyonudur; runtime state içermez.
- Bölümler arası referanslar klasör yolu veya bölüm numarasıyla değil, `chapter_alias` ile yapılır.
- Tüm üretim çıktıları, loglar ve exportlar kitap proje klasörü içinde kalır.
- Framework klasöründe kitaba ait runtime/üretim dosyası bulunmaz.
