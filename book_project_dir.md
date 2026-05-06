# Kitap Proje Klasör Yapısı

Bir bookMaker kitap projesi tamamen bağımsız bir klasördür. Framework'e ait hiçbir dosya içermez. Kitaba ait tüm içerik, konfigürasyon, prompt, log ve çıktı dosyaları bu klasörde yer alır.

---

## Sorumluluk Ayrımı

| Dosya | Kim yazar | Ne içerir |
|-------|-----------|-----------|
| `book_manifest.yaml` | Kullanıcı | Kitabın genel çizgisi, üretim parametreleri, bölüm sırası |
| `chapter_manifest.yaml` | Kullanıcı | Bölümün içerik spesifikasyonu (scope, structure, otomasyon kuralları) |
| `pipeline_state.yaml` | Framework | Runtime state, kalite skorları, otomasyon bayrakları |

---

## Klasör Yapısı

```
<book-alias>/                            # Kitap proje kök klasörü (alias = repo adı)
│
├── book_manifest.yaml                   # Kitabın ana konfigürasyon dosyası
├── pipeline_state.yaml                  # Runtime state (framework tarafından yönetilir)
│
├── prompts/                             # Varsayılan prompt dosyaları
│   ├── default_chapter.md               # Bölüm üretiminde varsayılan prompt
│   └── default_review.md                # Gözlemci LLM için varsayılan review promptu
│
├── chapters/                            # Tüm bölüm klasörleri
│   ├── <chapter-alias>/                 # Klasör adı = chapter alias
│   │   ├── chapter_manifest.yaml        # İçerik spesifikasyonu (kullanıcı yazar)
│   │   ├── prompt.md                    # Bölüme özel prompt (opsiyonel)
│   │   └── content/                     # Üretilen içerikler (framework yazar)
│   │       ├── draft.md
│   │       ├── final.md
│   │       └── revisions/
│   │           └── v001.md
│   └── <chapter-alias>/
│       └── ...
│
├── exports/                             # Export çıktıları
│   ├── docx/
│   ├── pdf/
│   └── md/
│       └── <book-alias>_birlesik.md
│
└── logs/
    ├── production/
    ├── errors/
    └── reviews/
```

---

## Dosya Şemaları

### `book_manifest.yaml`

```yaml
book:
  title: "Kitap Başlığı"
  subtitle: "Alt Başlık"
  author: "Yazar Adı"
  alias: "kitap-alias"           # repo adıyla aynı
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
  target_audience: "hedef kitle tanımı"
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
  qr_policy: dual                # none | single | dual
  github_code_export: true
  manual_asset_override: true

chapters:
  - alias: "giris"
  - alias: "dart-temelleri"
  - alias: "widget-mantigi"
```

---

### `chapter_manifest.yaml`

Kullanıcı tarafından yazılır. Sadece içerik spesifikasyonu içerir. Runtime state burada tutulmaz.

```yaml
chapter:
  title: "Bölüm Başlığı"
  alias: "bolum-alias"
  order: 1                       # book_manifest.yaml sıralamasından türetilir
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

automation:                      # book_manifest.yaml'daki genel ayarları bölüm bazında override eder
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

### `pipeline_state.yaml`

Framework tarafından otomatik oluşturulur ve güncellenir. Kullanıcı yazmaz. Path'ler ve stage tanımları framework convention'ı olduğundan burada tekrarlanmaz.

```yaml
pipeline:
  schema_version: "1.0"
  book_alias: "kitap-alias"
  current_version: "v001"
  global_state: "initialized"  # initialized | authoring | review | approved | exporting | completed | blocked
  created_at: "2026-05-06T00:00:00+03:00"
  updated_at: "2026-05-06T00:00:00+03:00"
  active_chapter: "giris"
  last_completed_chapter: null
  next_action: "..."

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

quality_gates:
  per_chapter:
    manifest_exists: true
    draft_required: true
    review_required_before_final: true
    final_required_for_export: true
    unresolved_placeholders_allowed: false
    code_meta_required_for_extractable_code: true
    screenshot_marker_required: true
  book_level:
    chapter_order_from_book_manifest: true
    chapter_alias_references_only: true
    no_framework_files_inside_project: true
    exports_stay_inside_project: true

chapters:
  - alias: "giris"
    order: 1
    status:
      state: "pending"           # pending | draft | review | revision | approved | exported | blocked
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

export_state:
  merged_markdown_generated: false
  docx_generated: false
  pdf_generated: false
  last_export_version: null
  last_exported_at: null
  included_chapters: []

history:
  - at: "2026-05-06T00:00:00+03:00"
    event: "pipeline_initialized"
    note: "pipeline_state.yaml oluşturuldu."
```

---

## Kurallar

- Klasör adı her zaman `chapter_alias` ile aynıdır.
- `book_manifest.yaml` içindeki `chapters` listesinin sırası kitap birleştirme sırasını belirler.
- `pipeline_state.yaml` framework tarafından `book_manifest.yaml`'dan otomatik senkronize edilir.
- `chapter_manifest.yaml` içerik spesifikasyonudur — runtime state içermez, framework tarafından değiştirilmez.
- Bölümler arası referanslar klasör yolu veya numara ile değil `chapter_alias` ile yapılır.
- Tüm üretim çıktıları, loglar ve exportlar kitap proje klasörü içinde kalır.
- Framework klasöründe kitaba ait hiçbir dosya bulunmaz.
