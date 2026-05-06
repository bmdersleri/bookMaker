# Migration: Project-Based Architecture

**Branch:** `feat/project-based-architecture`  
**Başlangıç tarihi:** 2026-05-06  
**Hedef:** Framework ile kitap projesini tamamen ayır. Framework = motor, Kitap projesi = içerik.

---

## Mimari Karar Özeti

### Yeni yapı
```
bookMaker/                         # framework (bu repo)
book_projects/
  <book-alias>/                    # kitap projesi (bağımsız)
    book_manifest.yaml             # kullanıcı yazar → kitabın genel çizgisi
    pipeline_state.yaml            # framework yazar → runtime state
    prompts/
      default_chapter.md
      default_review.md
    chapters/
      <chapter-alias>/
        chapter_manifest.yaml      # kullanıcı yazar → içerik spesifikasyonu
        prompt.md                  # opsiyonel
        content/
          draft.md
          final.md
          revisions/
    exports/
    logs/
```

### Sorumluluk ayrımı
| Dosya | Kim yazar | Ne içerir |
|-------|-----------|-----------|
| `book_manifest.yaml` | Kullanıcı | Kitabın genel çizgisi, üretim parametreleri, bölüm sırası |
| `chapter_manifest.yaml` | Kullanıcı | İçerik spesifikasyonu (scope, structure, otomasyon kuralları) |
| `pipeline_state.yaml` | Framework | Runtime state, kalite skorları, otomasyon bayrakları |

### LLM rolleri
- **Üretici:** bölüm içeriği yazar
- **Gözlemci:** süreci izler, hata ve öneri üretir
- Her ikisi GUI'den bağımsız olarak yapılandırılabilir

---

## Ne Tutulacak, Ne Yeniden Yazılacak

### Tut (adapte et)
- `production/pandoc.py` — Markdown → DOCX (path'ler güncellenecek)
- `production/mermaid.py` — Mermaid → PNG (path'ler güncellenecek)
- `production/qrcode.py` — QR üretimi
- `core/encoding.py` — read_text, write_text
- `core/errors.py` — exception sınıfları
- `core/time.py` — now_iso, now_date
- `core/ids.py` — slugify, new_event_id

### Yeniden yaz
- `manifest/models.py` — Yeni şemaya göre tamamen yeniden yaz
- `core/config.py` — Framework config (multi-book, project path registry)
- `core/paths.py` — Yeni klasör konvansiyonuna göre
- `studio/app.py` — Multi-book desteği, yeni servis mimarisi
- `studio/services/` — Tüm servisler yeni manifest okuma/yazma ile
- `commands/` — Yeni manifest yapısına göre CLI komutları

### Sil
- `core/config.py` içindeki `BookConfig` (book_profile.yaml okuma) → `book_manifest.yaml` okuma ile değiştirilecek
- `studio/services/wizard_service.py` → Yeni project init akışıyla değiştirilecek
- Framework içindeki kitaba özgü tüm YAML/JSON dosyalar

---

## Faz Planı

---

### FAZ 1 — Yeni Manifest Modelleri
**Dosya:** `src/bookmaker/manifest/models.py`  
**Tahmini süre:** 1 oturum

Mevcut modelleri (BookManifest, ChapterState, PipelineState) sil.  
Yeni Pydantic modelleri yaz:

#### 1.1 `BookManifest` (book_manifest.yaml)
```python
class BookInfo(BaseModel):
    title: str
    subtitle: str | None = None
    author: str
    alias: str          # repo adıyla aynı
    repo: str
    language: str = "tr"
    version: str = "1.0.0"
    edition: str = "1"
    year: int

class ProductionConfig(BaseModel):
    producer_model: str = "deepseek-chat"
    observer_model: str = "deepseek-chat"
    producer_params: dict = {}
    observer_params: dict = {}
    generation_mode: str = "chapter_based"
    approval_required: bool = True

class StyleConfig(BaseModel):
    target_audience: str
    tone: str
    code_language: str
    framework: str | None = None
    terminology: str | None = None
    chapter_pattern: list[str] = []

class TechnicalProfile(BaseModel):  # opsiyonel, kitaba özgü
    model_config = ConfigDict(extra="allow")

class AutomationConfig(BaseModel):
    code_meta_required: bool = True
    screenshot_required: bool = False
    minimum_screenshots_per_chapter: int = 0
    qr_policy: str = "none"         # none | single | dual
    github_code_export: bool = False
    manual_asset_override: bool = False

class ChapterRef(BaseModel):
    alias: str

class BookManifest(BaseModel):
    book: BookInfo
    production: ProductionConfig
    style: StyleConfig
    technical_profile: TechnicalProfile | None = None
    automation: AutomationConfig = AutomationConfig()
    chapters: list[ChapterRef]

    @classmethod
    def load(cls, path: Path) -> "BookManifest": ...
    def save(self, path: Path) -> None: ...
    def chapter_aliases(self) -> list[str]: ...
```

#### 1.2 `ChapterManifest` (chapter_manifest.yaml)
```python
class ChapterRef(BaseModel):
    alias: str
    relation: str   # prerequisite | next

class SectionDef(BaseModel):
    title: str
    type: str       # text | text+code | text+code+screenshot | exercise

class ScopeConfig(BaseModel):
    topics: list[str] = []
    objectives: list[str] = []
    exclusions: list[str] = []
    mini_project: str | None = None

class StructureConfig(BaseModel):
    sections: list[SectionDef] = []
    estimated_pages: int | None = None
    code_examples_count: int | None = None
    screenshot_examples_count: int | None = None

class ChapterAutomation(BaseModel):
    code_meta_required: bool = True
    screenshot_required: bool = False
    default_code_language: str | None = None
    default_framework: str | None = None
    validation_modes: list[str] = []
    github_export: bool = False
    qr_policy: str = "none"

class ChapterInfo(BaseModel):
    title: str
    alias: str
    order: int
    references: list[ChapterRef] = []

class ChapterManifest(BaseModel):
    chapter: ChapterInfo
    scope: ScopeConfig
    structure: StructureConfig
    automation: ChapterAutomation = ChapterAutomation()

    @classmethod
    def load(cls, path: Path) -> "ChapterManifest": ...
    def save(self, path: Path) -> None: ...
```

#### 1.3 `PipelineState` (pipeline_state.yaml)
```python
class ChapterStatus(BaseModel):
    state: str = "pending"  # pending|draft|review|revision|approved|exported|blocked
    draft_generated: bool = False
    review_completed: bool = False
    revision_required: bool = False
    final_approved: bool = False
    exported: bool = False
    quality_score: float | None = None
    last_review: str | None = None
    last_updated: str | None = None
    issues: list[str] = []
    suggestions: list[str] = []

class ChapterAutomationState(BaseModel):
    code_extraction_done: bool = False
    code_tests_done: bool = False
    screenshots_done: bool = False
    qr_generation_done: bool = False
    github_links_patched: bool = False

class ChapterPipelineEntry(BaseModel):
    alias: str
    order: int
    status: ChapterStatus = ChapterStatus()
    automation: ChapterAutomationState = ChapterAutomationState()

class InputPolicy(BaseModel):
    use_book_manifest: bool = True
    use_chapter_manifest: bool = True
    use_chapter_prompt_if_exists: bool = True
    fallback_to_default_chapter_prompt: bool = True

class ReviewPolicy(BaseModel):
    observer_review_required: bool = True
    fallback_to_default_review_prompt: bool = True
    minimum_quality_score_for_approval: int = 85

class ProductionContext(BaseModel):
    producer_model: str
    observer_model: str
    generation_mode: str
    approval_required: bool
    default_input_policy: InputPolicy = InputPolicy()
    review_policy: ReviewPolicy = ReviewPolicy()

class QualityGatesPerChapter(BaseModel):
    manifest_exists: bool = True
    draft_required: bool = True
    review_required_before_final: bool = True
    final_required_for_export: bool = True
    unresolved_placeholders_allowed: bool = False
    code_meta_required_for_extractable_code: bool = True
    screenshot_marker_required: bool = True

class QualityGatesBookLevel(BaseModel):
    chapter_order_from_book_manifest: bool = True
    chapter_alias_references_only: bool = True
    no_framework_files_inside_project: bool = True
    exports_stay_inside_project: bool = True

class QualityGates(BaseModel):
    per_chapter: QualityGatesPerChapter = QualityGatesPerChapter()
    book_level: QualityGatesBookLevel = QualityGatesBookLevel()

class ExportState(BaseModel):
    merged_markdown_generated: bool = False
    docx_generated: bool = False
    pdf_generated: bool = False
    last_export_version: str | None = None
    last_exported_at: str | None = None
    included_chapters: list[str] = []

class PipelineInfo(BaseModel):
    schema_version: str = "1.0"
    book_alias: str
    current_version: str = "v001"
    global_state: str = "initialized"
    created_at: str
    updated_at: str
    active_chapter: str | None = None
    last_completed_chapter: str | None = None
    next_action: str | None = None

class HistoryEntry(BaseModel):
    at: str
    event: str
    note: str = ""

class PipelineState(BaseModel):
    pipeline: PipelineInfo
    production_context: ProductionContext
    quality_gates: QualityGates = QualityGates()
    chapters: list[ChapterPipelineEntry] = []
    export_state: ExportState = ExportState()
    history: list[HistoryEntry] = []

    @classmethod
    def load(cls, path: Path) -> "PipelineState": ...
    def save(self, path: Path) -> None: ...

    @classmethod
    def init_from_book_manifest(cls, manifest: BookManifest, production: ProductionContext) -> "PipelineState":
        # book_manifest.yaml'dan chapters listesini alıp pipeline_state.yaml oluşturur
        ...

    def sync_chapters(self, manifest: BookManifest) -> None:
        # book_manifest.yaml chapter sırası değişince pipeline_state'i senkronize eder
        ...

    def get_chapter(self, alias: str) -> ChapterPipelineEntry | None: ...
    def update_chapter_status(self, alias: str, **kwargs) -> None: ...
```

---

### FAZ 2 — Framework Config ve Project Registry
**Dosya:** `src/bookmaker/core/config.py` (tamamen yeniden yaz)  
**Tahmini süre:** 0.5 oturum

Framework config: Hangi kitap projelerinin nerede olduğunu tutar.

```python
# ~/.bookmaker/config.yaml veya proje dizininde llm_config.json yanında
class BookProject(BaseModel):
    name: str
    alias: str
    repo: str | None = None
    path: Path           # kitap proje klasörünün mutlak yolu

class FrameworkConfig(BaseModel):
    projects: list[BookProject] = []
    active_project: str | None = None   # alias

    @classmethod
    def load(cls, path: Path) -> "FrameworkConfig": ...
    def save(self, path: Path) -> None: ...
    def get_project(self, alias: str) -> BookProject | None: ...
    def add_project(self, project: BookProject) -> None: ...
```

**Config dosyası yeri:** `~/.bookmaker/config.yaml` (global) veya proje root'unda `bookmaker_config.yaml`

---

### FAZ 3 — Yeni Path Sistemi
**Dosya:** `src/bookmaker/core/paths.py` (tamamen yeniden yaz)  
**Tahmini süre:** 0.5 oturum

Tüm path'ler convention-based, config'den türetilmez:

```python
class BookPaths:
    def __init__(self, project_root: Path):
        self.root = project_root

    @property
    def book_manifest(self) -> Path:
        return self.root / "book_manifest.yaml"

    @property
    def pipeline_state(self) -> Path:
        return self.root / "pipeline_state.yaml"

    @property
    def chapters_dir(self) -> Path:
        return self.root / "chapters"

    @property
    def prompts_dir(self) -> Path:
        return self.root / "prompts"

    @property
    def default_chapter_prompt(self) -> Path:
        return self.prompts_dir / "default_chapter.md"

    @property
    def default_review_prompt(self) -> Path:
        return self.prompts_dir / "default_review.md"

    @property
    def exports_dir(self) -> Path:
        return self.root / "exports"

    @property
    def logs_dir(self) -> Path:
        return self.root / "logs"

    def chapter(self, alias: str) -> "ChapterPaths":
        return ChapterPaths(self.chapters_dir / alias)


class ChapterPaths:
    def __init__(self, chapter_root: Path):
        self.root = chapter_root
        self.alias = chapter_root.name

    @property
    def manifest(self) -> Path:
        return self.root / "chapter_manifest.yaml"

    @property
    def prompt(self) -> Path:
        return self.root / "prompt.md"

    @property
    def content_dir(self) -> Path:
        return self.root / "content"

    @property
    def draft(self) -> Path:
        return self.content_dir / "draft.md"

    @property
    def final(self) -> Path:
        return self.content_dir / "final.md"

    @property
    def revisions_dir(self) -> Path:
        return self.content_dir / "revisions"
```

---

### FAZ 4 — LLM Servisi (Üretici + Gözlemci)
**Dosya:** `src/bookmaker/llm/` (mevcut llm/ modülünü adapte et)  
**Tahmini süre:** 1 oturum

#### 4.1 Producer (Üretici)
- `book_manifest.yaml` → genel bağlam
- `chapter_manifest.yaml` → bölüm spesifikasyonu
- `chapters/<alias>/prompt.md` varsa → onu kullan, yoksa `prompts/default_chapter.md`
- Sonuç → `chapters/<alias>/content/draft.md`

#### 4.2 Observer (Gözlemci)
- Üretim sırasında `draft.md`'yi okur
- `prompts/default_review.md` promptuyla analiz eder
- Kalite skoru, hata ve öneriler üretir
- Sonuç → `pipeline_state.yaml`'daki chapter status'a yazar
- Log → `logs/reviews/<alias>_review_<date>.md`

#### 4.3 Prompt yükleme önceliği
```python
def load_chapter_prompt(book_paths: BookPaths, alias: str) -> str:
    chapter_prompt = book_paths.chapter(alias).prompt
    if chapter_prompt.exists():
        return chapter_prompt.read_text(encoding="utf-8")
    default = book_paths.default_chapter_prompt
    if default.exists():
        return default.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt bulunamadı: {alias}")
```

---

### FAZ 5 — Production Pipeline Adaptasyonu
**Dosya:** `src/bookmaker/production/pipeline.py`  
**Tahmini süre:** 0.5 oturum

Mevcut `run()` fonksiyonu yeni `BookPaths` ve `ChapterPaths` kullanacak şekilde adapte edilecek:
- Input: `book_paths.chapter(alias).final` (approved content)
- Mermaid render: `ChapterPaths.content_dir` içinde
- DOCX export: `book_paths.exports_dir / "docx" / f"{alias}.docx"`
- Birleşik export: `book_paths.exports_dir / "md" / f"{book_alias}_birlesik.md"`

---

### FAZ 6 — Studio Yeniden Yapılandırma
**Dosya:** `src/bookmaker/studio/`  
**Tahmini süre:** 2-3 oturum (en büyük faz)

#### 6.1 Multi-book desteği
- Studio başlarken `FrameworkConfig`'den proje listesini okur
- Aktif proje değiştirilebilir
- Her proje için ayrı `BookPaths` instance'ı

#### 6.2 Yeni servisler (services/ yeniden yaz)

| Servis | Sorumluluk |
|--------|-----------|
| `book_service.py` | book_manifest.yaml CRUD |
| `chapter_service.py` | chapter_manifest.yaml CRUD |
| `pipeline_service.py` | pipeline_state.yaml okuma/güncelleme |
| `prompt_service.py` | Prompt dosyaları CRUD |
| `generation_service.py` | Üretici LLM ile bölüm üretimi |
| `observer_service.py` | Gözlemci LLM review |
| `export_service.py` | Birleştirme + DOCX/PDF export |
| `llm_assist_service.py` | GUI'den LLM destek (YAML/prompt düzenleme yardımı) |

#### 6.3 Studio sekmeleri (app.py endpoint'leri)

**Sekme 1: Kitap Yönetimi**
- GET  `/api/books` — Proje listesi
- POST `/api/books/activate/{alias}` — Aktif kitap değiştir
- GET  `/api/books/{alias}/manifest` — book_manifest.yaml oku
- PUT  `/api/books/{alias}/manifest` — book_manifest.yaml güncelle
- POST `/api/books/{alias}/manifest/llm-assist` — LLM ile manifest iyileştirme önerisi

**Sekme 2: Bölüm Yönetimi**
- GET  `/api/chapters` — Bölüm listesi (pipeline_state ile birleşik)
- GET  `/api/chapters/{alias}/manifest` — chapter_manifest.yaml oku
- PUT  `/api/chapters/{alias}/manifest` — chapter_manifest.yaml güncelle
- GET  `/api/chapters/{alias}/prompt` — prompt.md oku
- PUT  `/api/chapters/{alias}/prompt` — prompt.md güncelle
- POST `/api/chapters/{alias}/prompt/llm-assist` — LLM ile prompt iyileştirme önerisi

**Sekme 3: Üretim**
- POST `/api/production/generate/{alias}` — Bölüm üret (üretici LLM)
- POST `/api/production/review/{alias}` — Bölüm gözden geçir (gözlemci LLM)
- POST `/api/production/approve/{alias}` — Bölümü onayla
- GET  `/api/production/status` — Tüm pipeline durumu
- WS   `/ws/production/{alias}` — Canlı üretim akışı

**Sekme 4: Birleştirme & Export**
- POST `/api/export/merge` — Onaylı bölümleri birleştir
- POST `/api/export/docx` — DOCX üret
- POST `/api/export/pdf` — PDF üret
- GET  `/api/export/list` — Export listesi

**Sekme 5: Kalite & İzleme**
- GET  `/api/quality/dashboard` — Tüm bölümlerin kalite özeti
- GET  `/api/quality/{alias}` — Bölüm kalite detayı
- GET  `/api/logs/production/{alias}` — Üretim logları
- GET  `/api/logs/errors` — Hata logları
- GET  `/api/logs/reviews/{alias}` — Gözlemci review logları

#### 6.4 Frontend (static/app.js)
Mevcut app.js'i yeni endpoint'lere göre yeniden yaz.  
Beş sekme, canlı WebSocket akışı, YAML editör (CodeMirror veya benzeri), kalite dashboard.

---

### FAZ 7 — CLI Komutları
**Dosya:** `src/bookmaker/commands/`  
**Tahmini süre:** 0.5 oturum

Mevcut komutları yeni yapıya adapte et:

```
bookmaker project add --path /path/to/kitap-projesi   # proje ekle
bookmaker project list                                 # proje listesi
bookmaker project activate <alias>                     # aktif proje seç

bookmaker chapter list                                 # bölüm listesi
bookmaker chapter generate <alias>                     # bölüm üret
bookmaker chapter review <alias>                       # gözlemci review
bookmaker chapter approve <alias>                      # onayla

bookmaker export merge                                 # birleştir
bookmaker export docx                                  # DOCX üret

bookmaker studio                                       # web UI başlat
```

---

### FAZ 8 — Temizlik
**Tahmini süre:** 0.5 oturum

Silinecekler:
- `commands/init.py` → `project add` komutuyla değiştirildi
- `commands/manifest.py` → book/chapter servislerine dağıtıldı
- `studio/services/wizard_service.py` → artık gerekli değil
- Framework içindeki tüm kitaba özgü YAML/JSON dosyalar
- `book_profile.yaml` okuma kodu tamamen kaldırılacak
- `models/` altındaki kullanılmayan modeller

---

## Uygulama Sırası

```
FAZ 1: manifest/models.py          ← her şeyin temeli
FAZ 2: core/config.py              ← framework config
FAZ 3: core/paths.py               ← path sistemi
FAZ 4: llm/ adaptasyonu            ← üretici + gözlemci
FAZ 5: production/ adaptasyonu     ← pipeline path'leri
FAZ 6: studio/ yeniden yapı        ← en büyük faz
FAZ 7: commands/ güncelleme        ← CLI
FAZ 8: temizlik                    ← kullanılmayan kod sil
```

Her faz tamamlandığında bir commit atılacak.

---

## Test Stratejisi

Her faz sonunda şu kontroller:

**FAZ 1 sonrası:**
- `BookManifest.load(flutter_project / "book_manifest.yaml")` çalışıyor mu?
- `ChapterManifest.load(flutter_project / "chapters/giris/chapter_manifest.yaml")` çalışıyor mu?
- `PipelineState.init_from_book_manifest(manifest, ctx)` doğru bölüm listesi üretiyor mu?

**FAZ 2-3 sonrası:**
- `BookPaths` tüm path'leri doğru döndürüyor mu?
- `FrameworkConfig` projeyi bulabiliyor mu?

**FAZ 4-5 sonrası:**
- `chapters/giris/prompt.md` okunabiliyor mu?
- `draft.md` doğru path'e yazılıyor mu?

**FAZ 6 sonrası:**
- Studio açılıyor mu?
- YAML editör kaydedebiliyor mu?
- Bölüm üretimi WebSocket'ten canlı akış veriyor mu?

---

## Referans Dosyalar

Bu oturumda oluşturulan referans belgeler:

- `book_project_dir.md` — Kitap proje klasör yapısı ve şema açıklamaları
- `book_projects/flutter-ile-mobil-uygulama-gelistirme/` — Örnek kitap projesi
  - `book_manifest.yaml` — Gerçek örnek şema
  - `chapters/giris/chapter_manifest.yaml` — Gerçek örnek şema
  - `pipeline_state.yaml` — Gerçek örnek şema

---

## Notlar

- `pipeline_state.yaml` içindeki chapters listesi `book_manifest.yaml`'dan otomatik türetilir. Kullanıcı elle yazmaz, framework `sync_chapters()` ile günceller.
- Path'ler YAML'da tekrarlanmaz, framework convention'dan türetir.
- `chapter_manifest.yaml` runtime state içermez (status, quality yok). Bunlar `pipeline_state.yaml`'da.
- Studio'da LLM destek: hem üretici hem gözlemci hem de GUI içi yardımcı olarak 3 ayrı kullanım bağlamı var. Hepsini aynı model yapabilir ama endpoint'ler ayrı.
