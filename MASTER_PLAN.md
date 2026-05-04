# MASTER_PLAN

Bu dosya `bookMaker` yazılımının tüm geliştirme aşamalarını, her aşamada yapılacak işleri, üretilecek çıktıları ve kabul kriterlerini tanımlar.

> **Oturum takibi için:** `session.md` — aktif faz, tamamlananlar, sıradaki görevler.
> Bu dosyadaki `[ ]` kutucukları görev tamamlandığında `[x]` olarak işaretlenir.

Kaynak dokümanlar: `coding_plan.md`, `todo.md`, `chapter_spec.md`, `chapter_authoring_workflow.md`.

---

## Genel Mimari

```
bookMaker
├── CLI (Typer)               → bookmaker <komut>
├── Core Models (Pydantic v2) → kitap/bölüm/pipeline veri modelleri
├── Storage (SQLite + dosya)  → artefakt, versiyon, event yönetimi
├── Chapter Engine            → parser, validator, normalizer, scorer
├── Authoring Pipeline        → seed → outline → draft → approve akışı
├── Production Pipeline       → kod testi, Mermaid, QR, asset, export
├── Studio GUI (FastAPI)      → yerel web arayüzü
└── Templates (Jinja2)        → prompt ve manifest şablonları
```

---

## Faz 0 — Proje İskeleti

**Amaç:** `bookmaker` Python paketini çalışır hale getirmek, test altyapısını kurmak.

### Yapılacaklar

1. `pyproject.toml` oluştur
   - Paket adı: `bookmaker`
   - CLI entry point: `bookmaker`
   - Bağımlılıklar: `typer`, `rich`, `pydantic>=2`, `ruamel.yaml`, `fastapi`, `uvicorn`, `jinja2`
   - Geliştirme bağımlılıkları: `pytest`, `pytest-cov`, `ruff`, `pre-commit`
   - `uv sync` ile sanal ortam oluştur

2. `src/bookmaker/` paket iskeletini oluştur
   ```
   src/bookmaker/
     __init__.py          (versiyon sabiti)
     __main__.py          (python -m bookmaker girişi)
     cli.py               (Typer app, alt komut grupları)
     core/
       __init__.py
       paths.py           (proje yol sabitleri ve yardımcılar)
       encoding.py        (UTF-8 okuma/yazma yardımcıları)
       errors.py          (özel hata sınıfları)
       ids.py             (slug, event ID üretimi)
       time.py            (ISO 8601 zaman damgası, Europe/Istanbul)
   ```

3. `tests/` iskeletini oluştur
   ```
   tests/
     conftest.py
     fixtures/
     unit/
     integration/
     cli/
   ```

4. `just` görevlerini tanımla (`justfile`)
   ```
   just dev      → uv sync
   just test     → pytest
   just lint     → ruff check + ruff format
   just check    → lint + test
   ```

5. `pre-commit` konfigürasyonunu yaz (`.pre-commit-config.yaml`)
   - ruff, markdownlint-cli2

### Kabul Kriterleri

- [ ] `uv sync` hatasız çalışır
- [ ] `python -m bookmaker --version` versiyon basar
- [ ] `bookmaker --help` alt komutları listeler
- [ ] `pytest` çalışır, en az 1 smoke testi geçer
- [ ] `just check` hatasız tamamlanır

### Çıktılar

```
pyproject.toml
justfile
.pre-commit-config.yaml
src/bookmaker/__init__.py
src/bookmaker/__main__.py
src/bookmaker/cli.py
src/bookmaker/core/
tests/conftest.py
```

---

## Faz 1 — Veri Modelleri ve Depolama

**Amaç:** Kitap, bölüm, pipeline ve versiyon veri modellerini tanımlamak; dosya sistemi ve SQLite depolama katmanını kurmak.

### 1.1 Pydantic Modelleri

`src/bookmaker/models/` altında:

| Dosya | İçerik |
|-------|--------|
| `book.py` | `BookProfile`, `BookArchitecture`, `ChapterArchEntry` |
| `chapter.py` | `ChapterSeed`, `CodeMeta`, `SectionMeta`, `MermaidMeta`, `ScreenshotMeta` |
| `pipeline.py` | `PipelineDefinition`, `PipelineStep`, `PipelineState`, `ChapterState` |
| `quality.py` | `Issue`, `QualityReport`, `GateResult` |
| `versioning.py` | `VersionEvent`, `ActiveVersion` |
| `exchange.py` | `RevisionPacket`, `RevisionIssue` |

Her model için:
- Zorunlu alan doğrulaması
- YAML yükle/kaydet metotları (`ruamel.yaml` ile round-trip)
- `model_validate` / `model_dump` kullanımı

### 1.2 Depolama Katmanı

`src/bookmaker/storage/` altında:

| Dosya | İçerik |
|-------|--------|
| `files.py` | Dosya okuma/yazma, path yardımcıları, bölüm workspace yolu üretimi |
| `schema.sql` | SQLite tablo tanımları (versiyonlu) |
| `sqlite.py` | `ensure_schema()`, bağlantı yöneticisi |
| `repositories.py` | `ChapterRepo`, `EventRepo`, `QualityRepo` — CRUD operasyonları |

SQLite tabloları: `projects`, `chapters`, `artifacts`, `version_events`, `quality_reports`, `issues`

### 1.3 Chapter Workspace Yönetimi

`bookmaker init` komutu ile üretilecek proje yapısı:

```
my-java-book/
  book_profile.yaml
  book_architecture.yaml
  pipeline_definition.yaml
  pipeline_state.yaml
  bookmaker.sqlite
  chapters/
    chapter_01/
      seed.yaml
      outline/
      draft/
      approved/
      technical/
      version_log.jsonl
      active_version.yaml
  prompts/
  assets/
    images/  mermaid/  screenshots/  qr/
  build/
    merged/  code/  reports/  docx/
  exports/
    docx/
```

### 1.4 Versiyon Kontrol Modeli

- Her artefakt değişikliği `version_log.jsonl` dosyasına event olarak yazılır
- `active_version.yaml` aktif sürümü gösterir
- Geri alma: eski sürümden yeni sürüm üretir, orijinali silmez
- SQLite `version_events` tablosu hızlı sorgulama için eş zamanlı tutulur

### Kabul Kriterleri

- [ ] Tüm Pydantic modelleri `pytest` ile doğrulama testlerini geçer
- [ ] YAML yükle/kaydet round-trip testi geçer
- [ ] `bookmaker init --preset java-temelleri --path .\build\test-book` çalışır
- [ ] Oluşan workspace UTF-8 YAML/Markdown dosyaları içerir
- [ ] SQLite dosyası oluşur ve tüm tablolar kurulur
- [ ] `version_log.jsonl` append/read döngüsü doğru çalışır

### Çıktılar

```
src/bookmaker/models/
src/bookmaker/storage/
tests/unit/test_models.py
tests/unit/test_storage.py
tests/integration/test_init_command.py
```

---

## Faz 2 — Chapter Validator Paketleme

**Amaç:** Mevcut `tools/chapter_semantic_validator.py`'yi paket içine almak, `bookmaker check chapter` komutunu kurmak.

### 2.1 Parser

`src/bookmaker/chapter/parser.py`:
- YAML front matter ayrıştırma
- Markdown heading hiyerarşisi çıkarma
- HTML yorum bloklarından meta blokları çıkarma
- `SECTION_META`, `CODE_META`, `MERMAID_META`, `SCREENSHOT_META` ayrıştırma
- Meta blok → takip eden heading/code fence ilişkisi kurma
- Kod fence dili ve içerik çıkarma

### 2.2 Validator

`src/bookmaker/chapter/validator.py` — Kontroller:

| Kategori | Kontrol |
|----------|---------|
| Front matter | Zorunlu alanlar |
| Yapı | Tek H1, elle numaralandırma uyarıları |
| SECTION_META | `order` benzersizliği, `title` uyumu |
| CODE_META | Varlık kontrolü, zorunlu alanlar, yerleşim |
| Java | `file`, `main_class`, `public class` uyumu |
| Tutarlılık | `intentional_mismatch` + `paired_with` + `validation_mode` + `test` |
| Mermaid | Meta/fence eşleşmesi |
| Final mod | Placeholder kontrolü |

### 2.3 Scorer

`src/bookmaker/chapter/scoring.py`:
```
score = 100
error   → -15
warning → -3
info    → 0
minimum = 0
```

Karar:
- `errors > 0` → `blocked` veya `revision_required`
- `score < 85` → revizyon önerilir
- `score >= 85` ve kritik hata yok → kullanıcı onayı mümkün

### 2.4 CLI Komutu

```powershell
bookmaker check chapter .\sample\sample_chapter.md
bookmaker check chapter .\sample\sample_chapter.md --json
bookmaker check chapter .\sample\sample_chapter.md --output .\build\reports\
```

Rapor formatları: JSON, Markdown

### Kabul Kriterleri

- [ ] `sample/sample_chapter.md` → `score=100`, `PASS`
- [ ] Hatalı fixture dosyaları → beklenen hataları üretir
- [ ] `bookmaker check chapter --json` geçerli JSON raporu üretir
- [ ] Raporlar `build/reports/` altına yazılır
- [ ] Mevcut validator ile skor farkı yok

### Çıktılar

```
src/bookmaker/chapter/parser.py
src/bookmaker/chapter/validator.py
src/bookmaker/chapter/scoring.py
tests/unit/test_parser.py
tests/unit/test_validator.py
tests/fixtures/valid_chapter.md
tests/fixtures/invalid_chapter_missing_code_meta.md
tests/fixtures/invalid_chapter_wrong_heading.md
tests/integration/test_check_command.py
```

---

## Faz 3 — Pipeline ve Versiyon Motoru

**Amaç:** Pipeline durum makinesini, geçiş motorunu ve bölüm versiyon yönetimini kodlamak.

### 3.1 Pipeline Definition

`src/bookmaker/pipeline/definitions.py`:
- `pipeline_definition.yaml` yükleyici
- Adım tipleri: `form`, `prompt_render`, `manual_paste`, `evaluation`, `revision_packet`, `version_checkpoint`, `approval`, `automation`, `export`
- Adım → sonraki adım geçiş kuralları
- Gate tanımları: `min_score`, `block_below`, karar → sonraki adım eşlemeleri

### 3.2 Pipeline Engine

`src/bookmaker/pipeline/engine.py` — Operasyonlar:

| Operasyon | Açıklama |
|-----------|----------|
| `start_step` | Aktif adımı günceller |
| `save_artifact` | Artefaktı dosyaya yazar, SQLite'a kaydeder |
| `create_version` | `version_log.jsonl` + `active_version.yaml` günceller |
| `evaluate` | Kalite raporu üretir, gate değerlendirir |
| `approve` | Sürümü onaylar, sürüm event yazar |
| `request_revision` | Revizyon paketi üretir |
| `diff_versions` | İki sürüm arasında Markdown diff |
| `restore_version` | Eski sürümden yeni aktif sürüm üretir |

### 3.3 Kalite Kapıları

`src/bookmaker/pipeline/gates.py`:
- `chapter_seed_complete`: Zorunlu alanlar dolu mu?
- `outline_quality`: Outline skoru eşiği
- `full_text_quality`: Tam metin skoru eşiği
- `technical_check`: Java derleme/çalıştırma geçti mi?

### 3.4 CLI Komutları

```powershell
bookmaker project status
bookmaker chapter list
bookmaker version list chapter_03
bookmaker version diff chapter_03 draft_v001 draft_v002
bookmaker version restore chapter_03 draft_v001
```

### Kabul Kriterleri

- [ ] Pipeline tanımı YAML'dan yüklenir ve doğrulanır
- [ ] Adım geçişleri doğru sürüm eventi yazar
- [ ] Geri alma eski dosyayı silmez, yeni sürüm üretir
- [ ] `bookmaker version diff` iki sürüm farkını basar
- [ ] `bookmaker project status` pipeline durumunu gösterir

### Çıktılar

```
src/bookmaker/pipeline/
src/bookmaker/templates/pipelines/academic_technical_book_v1.yaml
tests/unit/test_pipeline.py
tests/integration/test_versioning.py
```

---

## Faz 4 — Authoring Akışı

**Amaç:** Tohumdan onaylı bölüme kadar tüm yazarlık akışını CLI ile çalıştırılabilir hale getirmek.

### 4.1 Java Temelleri Preset

`src/bookmaker/templates/` altında:
- `book_profile_java_temelleri.yaml.j2` — ön doldurulmuş kitap profili
- `book_architecture_java_temelleri.yaml.j2` — 23 bölüm + 4 ek yapısı
- `chapter_seed_template.yaml.j2` — `book_architecture`'dan ön doldurulmuş seed formu

Seed ön doldurma davranışı: `seed.py` seed formu açıldığında `book_architecture.yaml`'ın ilgili bölüm girişinden `purpose`, `prerequisites`, `learning_outcomes`, `mandatory_concepts` alanlarını otomatik önerir. Kullanıcı onayı olmadan kesinleşmez. Sistem her alanın kaynağını (mimariden mi, preset'ten mi geldiğini) gösterir.

### 4.2 Prompt Şablonları

`src/bookmaker/templates/prompts/` altında:

| Şablon | Kullanım |
|--------|---------|
| `outline_prompt.md.j2` | Bölüm outline promptu |
| `outline_revision_prompt.md.j2` | Outline revizyon promptu |
| `full_text_prompt.md.j2` | Tam metin promptu (CODE_META kuralları dahil) |
| `full_text_revision_prompt.md.j2` | Tam metin revizyon promptu |
| `metadata_repair_prompt.md.j2` | CODE_META onarım promptu |
| `code_repair_prompt.md.j2` | Kod hatası onarım promptu |

### 4.3 Authoring Modülleri

`src/bookmaker/authoring/` altında:

| Dosya | İçerik |
|-------|--------|
| `seed.py` | Seed formu üretimi, doğrulama |
| `outline.py` | Outline prompt render, outline evaluator |
| `draft.py` | Tam metin prompt render, paste alıcı |
| `normalizer.py` | CODE_META parse, heading normalize, placeholder temizleme |
| `revision.py` | Revizyon paketi üretimi |
| `workflow.py` | Authoring pipeline orchestration |

### 4.4 Outline Evaluator

`src/bookmaker/authoring/outline.py` — İki katmanlı değerlendirme:

**Katman 1 — Deterministik (LLM gerektirmez):**
- Zorunlu başlık bölümlerinin varlığı (giriş, kavramlar, kod planı, özet, alıştırma)
- Kapsam dışı anahtar kelimelerin outline'a sızdığının tespiti
- `chapter_seed.mandatory_concepts` listesindeki terimlerin outline metninde geçip geçmediği (kelime eşleştirmesi)
- Kod/görsel/alıştırma planı varlığı (en az bir placeholder referansı)
- Kitap mimarisiyle bölüm sırası tutarlılığı

**Katman 2 — Kullanıcı Onaylı Checklist (LLM isteğe bağlı):**
- "Pedagojik akış mantıklı mı?" → kullanıcı onaylar
- "Zorunlu kavramlar yeterince derinlemesine planlanmış mı?" → kullanıcı onaylar
- Tam semantik değerlendirme için opsiyonel LLM çağrısı (MVP dışı, mimari hazır)

Karar: Katman 1 hataları olmadan ve kullanıcı checklist'i onaylamadan outline `PASS` almaz.

### 4.5 Tam Metin Evaluator

`src/bookmaker/authoring/draft.py` — Ek kontroller:
- Onaylı outline'a uyum
- Zorunlu pedagojik ögelerin varlığı (özet, terim sözlüğü, alıştırmalar, rubrik)
- CODE_META yerleşim kuralları (kod bloğundan hemen önce, fence dışında)
- CODE_META eksik kod blokları → fallback tespiti ve aday metadata önerisi
- Manuel başlık numaralandırması yasağı
- Placeholder kontrolü

Revizyon promptu PRESERVE kuralı: `revision.py` her revizyon paketi ürettiğinde mevcut onayli/hatasız kod bloklarını, SECTION/MERMAID META bloklarını ve doğru işlenen kavram paragraflarını `preserve` listesine otomatik olarak ekler.

### 4.6 CLI Komutları

```powershell
bookmaker init --preset java-temelleri --path .\my-java-book
bookmaker chapter seed chapter_03
bookmaker chapter prompt outline chapter_03
bookmaker chapter paste outline chapter_03 --from-file .\outline.md
bookmaker chapter evaluate outline chapter_03
bookmaker chapter revision outline chapter_03
bookmaker chapter approve outline chapter_03
bookmaker chapter prompt draft chapter_03
bookmaker chapter paste draft chapter_03 --from-file .\draft.md
bookmaker chapter normalize chapter_03
bookmaker chapter evaluate draft chapter_03
bookmaker chapter approve chapter_03
```

### Kabul Kriterleri

- [ ] `bookmaker init --preset java-temelleri` hatasız çalışır
- [ ] Outline prompt Jinja2 şablonundan doğru render edilir
- [ ] Outline paste → evaluate → revision paketi döngüsü çalışır
- [ ] Tam metin paste sonrası otomatik CODE_META analizi çalışır
- [ ] Normalizer başlıkları, placeholder'ları ve CODE_META'yı düzeltir
- [ ] Onaylı bölüm `approved/chapter_XX.md` altına kilitli yazılır
- [ ] Her adım `version_log.jsonl` event yazar

### Çıktılar

```
src/bookmaker/authoring/
src/bookmaker/templates/prompts/
src/bookmaker/templates/manifests/
tests/integration/test_authoring_flow.py
```

---

## Faz 5 — Java Teknik Kontrol

**Amaç:** Onaylı bölümlerden Java kodlarını çıkarmak, derlemek, çalıştırmak ve test raporları üretmek.

### 5.1 Kod Çıkarımı

`src/bookmaker/production/code_extract.py`:
- Onaylı Markdown'dan `extract: true` olan CODE_META + kod bloklarını çıkar
- `build/code/chapter_XX/code_id/FileName.java` olarak yaz
- `test: skip` ve `validation_mode: review_only` olanları manifestte tut, çalıştırma

### 5.2 Kod Manifesti

`src/bookmaker/production/code_manifest.py`:

```json
{
  "chapter_id": "chapter_03",
  "items": [
    {
      "code_id": "dosya_islemleri_001",
      "file": "DosyaIslemleriTemel.java",
      "extracted_path": "build/code/chapter_03/...",
      "test": "compile_run_assert",
      "expected_stdout_contains": ["Dosya yazıldı"],
      "github": true,
      "qr_policy": "dual"
    }
  ]
}
```

### 5.3 Java Adaptörü

`src/bookmaker/production/java_adapter.py` — Test tipleri:

| Tip | Açıklama |
|-----|---------|
| `compile_only` | Sadece `javac` |
| `compile_run` | `javac` + `java` |
| `compile_run_assert` | `javac` + `java` + stdout kontrolü |
| `skip` | Çalıştırılmaz, raporda `skipped` |

Her test için:
- stdout, stderr, dönüş kodu yakalanır
- `timeout_sec` aşımı izlenir
- `expected_stdout_contains` karşılaştırması yapılır
- Hata durumunda `javac stderr` otomatik ayrıştırılır ve `code_repair_prompt.md.j2` şablonu doldurularak `build/reports/code_repair_<code_id>.md` üretilir
- GUI'de "Onarım Promptunu Kopyala" butonu aktif hale gelir; kullanıcı düzeltilmiş kodu yapıştırınca teknik kontrol otomatik tekrar çalışır

### 5.4 QR Üretimi

`src/bookmaker/production/qr_generator.py`:
- `qr_policy: dual` → iki QR: GitHub source + GitHub Pages code page
- `qr_policy: single` → tek QR
- `qr_policy: none` → QR üretilmez
- Çıktı: `assets/qr/code_id_source.png`, `assets/qr/code_id_page.png`
- CLI aracı: `qr --output ...` komutu

### 5.5 Raporlar

`build/reports/code_test_report.json` ve `.md`:
```yaml
summary:
  total: 9
  passed: 6
  failed: 0
  skipped: 3
failures: []
```

### 5.6 CLI Komutları

```powershell
bookmaker chapter check technical chapter_03
bookmaker build code                       # tüm bölümler
bookmaker build qr chapter_03             # QR üretimi
```

### Kabul Kriterleri

- [ ] `sample/sample_chapter.md` → 6 geçti, 3 atlandı, 0 hata
- [ ] `intentional_mismatch: true` olanlar `skipped` sayılır
- [ ] `expected_stdout_contains` assertion çalışır
- [ ] Hata durumunda repair promptu üretilir
- [ ] QR dosyaları `qr_policy`'e göre doğru üretilir
- [ ] Test raporu JSON ve Markdown olarak yazılır

### Çıktılar

```
src/bookmaker/production/code_extract.py
src/bookmaker/production/code_manifest.py
src/bookmaker/production/java_adapter.py
src/bookmaker/production/qr_generator.py
src/bookmaker/production/reports.py
tests/integration/test_java_adapter.py
```

---

## Faz 6 — Export Hattı

**Amaç:** Onaylı bölümlerden DOCX, PDF, EPUB ve MkDocs çıktıları üretmek.

### 6.1 Mermaid Render

`src/bookmaker/production/mermaid.py`:
- Bölümlerden `MERMAID_META` + fence bloklarını çıkar
- `mmdc` ile PNG/SVG üretir
- Markdown referanslarını günceller
- Hata durumunda rapor yazar

### 6.2 Pre-Build Gate

`src/bookmaker/production/pre_build_gate.py` — `bookmaker build` başlamadan önce çalışır:

| Kontrol | Bloklayıcı mı? |
|---------|----------------|
| Tüm bölümler `approved` durumunda | Evet |
| `code_id` değerleri kitap genelinde benzersiz | Evet |
| Zorunlu Mermaid render'ları mevcut | Evet |
| `qr_policy` ile işaretlenen QR dosyaları üretilmiş | Evet |
| `lychee` ile iç linkler doğrulandı | Evet |
| Çözümsüz kırık link | Evet |

Herhangi bir bloklayıcı varsa build başlamaz; `build/reports/pre_build_gate.json` raporu üretilir.

### 6.3 Birleştirme

`src/bookmaker/production/merger.py`:
- Onaylı bölümleri sıraya göre birleştirir
- Mermaid placeholder'larını render edilmiş görselle değiştirir
- Asset yollarını çıktı formatına göre normalize eder
- `build/merged/book_merged.md` üretir

### 6.3 DOCX Export

`src/bookmaker/production/pandoc_docx.py`:
```powershell
pandoc book_merged.md -o exports/docx/book.docx --from markdown
```
- Pandoc log kaydedilir
- Export raporu üretilir
- Opsiyonel: reference DOCX desteği

### 6.4 PDF Export (Faz 6.4 — WeasyPrint)

```powershell
pandoc book_merged.md -o exports/pdf/book.pdf --pdf-engine=weasyprint
```

### 6.5 EPUB Export

```powershell
pandoc book_merged.md -o exports/epub/book.epub
```

### 6.6 MkDocs Export

`src/bookmaker/production/mkdocs_export.py`:
- `mkdocs.yml` manifestten üretir
- Bölümleri `docs/chapters/` altına kopyalar
- Kod sayfalarını `docs/code/` altına üretir
- Asset yollarını web uyumlu hale getirir
- GitHub Actions Pages deploy workflow şablonu üretir

### 6.7 CLI Komutları

```powershell
bookmaker build docx
bookmaker build pdf
bookmaker build epub
bookmaker build mkdocs
bookmaker build all
```

### Kabul Kriterleri

- [ ] Pre-build gate bloklayıcı varsa build başlamaz, rapor üretir
- [ ] `bookmaker build docx` → geçerli DOCX üretir
- [ ] `bookmaker build mkdocs` → `mkdocs build` hatasız tamamlanır
- [ ] Mermaid görselleri DOCX'te gömülü, MkDocs'ta doğru yolda
- [ ] Kod sayfaları MkDocs navigasyonunda yer alır
- [ ] `lychee` ile iç linkler doğrulanır

### Çıktılar

```
src/bookmaker/production/pre_build_gate.py
src/bookmaker/production/mermaid.py
src/bookmaker/production/merger.py
src/bookmaker/production/pandoc_docx.py
src/bookmaker/production/mkdocs_export.py
tests/integration/test_export.py
tests/integration/test_pre_build_gate.py
```

---

## Faz 7 — Studio GUI

**Amaç:** Yazarlık sürecini görsel olarak yönetmek için yerel web arayüzü kurmak.

### 7.1 Backend (FastAPI)

`src/bookmaker/studio/app.py`:
- `/api/health` → sistem durumu
- `/api/project/status` → aktif kitap ve bölüm özeti
- `/api/chapter/{id}/seed` → seed CRUD
- `/api/chapter/{id}/prompt/outline` → outline promptu render
- `/api/chapter/{id}/paste/outline` → outline yapıştır + otomatik analiz
- `/api/chapter/{id}/evaluate/outline` → outline değerlendir
- `/api/chapter/{id}/revision/outline` → revizyon paketi üret (PRESERVE bloğu otomatik)
- `/api/chapter/{id}/prompt/draft` → tam metin promptu render
- `/api/chapter/{id}/paste/draft` → draft yapıştır + normalize + analiz
- `/api/chapter/{id}/evaluate/draft` → tam metin değerlendir
- `/api/chapter/{id}/approve` → bölümü onayla
- `/api/chapter/{id}/versions` → versiyon listesi
- `/api/chapter/{id}/diff` → versiyon farkı
- `/api/chapter/{id}/restore` → sürüm geri alma
- `/api/chapter/{id}/code-repair/{code_id}` → derleyici hatası onarım promptu üret
- `/api/chapter/{id}/concept-coverage` → zorunlu kavram kapsam raporu
- `/api/chapter/{id}/section-revision` → seçili section için kısmi revizyon promptu üret
- `/api/project/check-book` → kitap geneli tutarlılık raporu
- `/api/project/provider-stats` → LLM sağlayıcı bazında kalite istatistikleri
- `/api/project/health-score` → bileşik kitap sağlık skoru
- `/api/build/gate` → pre-build gate kontrolü
- `/api/build/{format}` → export tetikle (canlı SSE akışı ile)

### 7.2 Frontend (HTML/CSS/JS)

`src/bookmaker/studio/static/` altında sade, vanilla JS:

**Ekranlar:**
1. **Dashboard** — kitap sağlık skoru özeti, bölüm ilerleme matrisi (renk kodlu), son eventler, bloklu bölümler, LLM sağlayıcı analiz tablosu
2. **Kitap Profili** — `book_profile.yaml` formu
3. **Kitap Mimarisi** — bölüm listesi, sıra/başlık/durum tablosu, bölüm bağımlılık görünümü
4. **Bölüm Stüdyosu** — çok sekmeli, paralel bölüm desteği:
   - Tohum | Outline Promptu | Outline Çıktısı | Outline Kalite Raporu | Outline Revizyon Paketi
   - Tam Metin Promptu | Tam Metin Çıktısı | Tam Metin Kalite Raporu | Tam Metin Revizyon Paketi
   - Teknik Kontrol | Onaylı Bölüm | Sürüm Geçmişi | Fark Görüntüleme
5. **Raporlar** — kalite, kod testi, screenshot, pre-build gate raporları
6. **Export** — format seçimi, canlı build akışı, asset galerisi, export raporu

**UI İlkeleri:**
- Her ekranda "Sıradaki en mantıklı iş" paneli
- Yapıştır → otomatik ön analiz → kalite raporu akışı
- Metadata formu (CODE_META alanları, YAML yazmadan)
- Sürüm geçmişi paneli + Markdown diff + revizyon trend sparkline
- Revizyon paketi → kopyala butonu

**10 UX Özelliği:**

| # | Özellik | Davranış |
|---|---------|---------|
| 1 | **Issue → Editör Highlight** | Kalite raporunda issue tıklanınca orta panelde ilgili satıra atlar, sarı/kırmızı highlight; `←` `→` ile gezinti |
| 2 | **Revizyon Trend Sparkline** | Her bölüm başlığında `v1:72 → v2:81 → v3:91 ✓` mini grafiği; geri gidiş kırmızı |
| 3 | **Paralel Bölüm Sekmeleri** | Birden fazla bölüm aynı anda açık; bir bölüm LLM beklerken diğeri düzenlenebilir |
| 4 | **Kavram Kapsam Takipçisi** | Paste sonrası `mandatory_concepts` listesi canlı tara; ✓/✗ ile göster; eksikler revizyon paketine otomatik ekle |
| 5 | **Kısmi Bölüm Revizyonu** | Preview'da bir `##` başlığı seçince "Bu Bölümü Revize Et" butonu; sadece o section için dar prompt üret |
| 6 | **Pano Akıllı Tespiti** | Pano LLM yanıtına benziyorsa ekran köşesinde toast: "Panoda LLM yanıtı var — yapıştır?"; tek tık |
| 7 | **Issue Triyajı** | Her issue için 🔴 Şimdi / 🟡 Sonra / ⚪ Kabul etiketleri; kabul edilen issue override event yazar |
| 8 | **Odak (Zen) Modu** | `F11` ile tüm paneller kapanır, sadece editör + minimal araç çubuğu; `Esc` ile geri |
| 9 | **Canlı Build Akışı + Asset Galerisi** | Build sırasında pandoc/mmdc çıktısı satır satır SSE ile akar; yan panelde QR/diyagram/screenshot galerisi |
| 10 | **Kitap Sağlık Skoru** | Dashboard'da bileşik skor: bölüm ilerlemesi + ortalama kalite + teknik kontrol + bloklu bölüm + export hazırlığı; her metriğe tıklanınca detay |

### 7.3 Klavye Kısayolları

```text
Ctrl+Enter     → Aktif adımı çalıştır (evaluate / normalize / check)
Ctrl+K         → Promptu panoya kopyala
Ctrl+Shift+V   → LLM yanıtını yapıştır
Ctrl+R         → Revizyon paketi üret
Ctrl+Shift+A   → Bölümü onayla
Ctrl+Z / Ctrl+Y → Sürüm geri al / ileri al
F11            → Odak (Zen) modu aç/kapat
← / →          → Issue'lar arasında gezin (rapor paneli aktifken)
Ctrl+Tab       → Açık bölüm sekmeleri arasında geçiş
```

### 7.4 Playwright Smoke Testleri

- FastAPI uygulaması import edilebilir
- `/api/health` → 200 döner
- Ana HTML sayfası yüklenir
- Dashboard bölüm sayısını ve sağlık skorunu gösterir
- Bölüm Stüdyosu açılır, sekme geçişi çalışır
- Issue tıklanınca highlight tetiklenir

### 7.5 CLI Komutu

```powershell
bookmaker studio --host 127.0.0.1 --port 8765
```

### Kabul Kriterleri

- [ ] `bookmaker studio` tarayıcıda açılır
- [ ] Dashboard kitap sağlık skorunu ve bileşenlerini gösterir
- [ ] Bölüm Stüdyosu tüm sekmelerde çalışır; paralel sekmeler açılabilir
- [ ] Outline yapıştır → kavram kapsam takipçisi → kalite raporu → revizyon paketi akışı GUI'den tamamlanır
- [ ] Issue tıklanınca editörde highlight çalışır
- [ ] Issue triyajı override event yazar
- [ ] Kısmi bölüm revizyonu dar prompt üretir
- [ ] Pano tespiti çalışır (test: mock clipboard ile)
- [ ] F11 Zen modu açılır/kapanır
- [ ] Build ekranında SSE canlı akış çalışır; asset galerisi görünür
- [ ] Revizyon trend sparkline sürüm geçmişinden veri alır
- [ ] Sürüm geçmişi gösterilir, geri alma çalışır
- [ ] `/api/health` smoke testi geçer

### Çıktılar

```
src/bookmaker/studio/app.py
src/bookmaker/studio/routes.py
src/bookmaker/studio/services.py
src/bookmaker/studio/static/index.html
src/bookmaker/studio/static/app.js
src/bookmaker/studio/static/styles.css
src/bookmaker/studio/static/components/
  issue_panel.js       — issue listesi + highlight tetikleyici
  sparkline.js         — revizyon trend grafiği
  concept_tracker.js   — kavram kapsam takipçisi
  zen_mode.js          — odak modu
  asset_gallery.js     — QR/diyagram/screenshot galerisi
  build_stream.js      — SSE canlı build akışı
  clipboard_detect.js  — pano akıllı tespiti
tests/cli/test_studio_smoke.py
```

---

## Faz 8 — Kalite ve Otomasyon Kapamaları

**Amaç:** Proje geneli kalite araçlarını entegre etmek, CI/CD ve otomasyon hatlarını tamamlamak.

### Yapılacaklar

1. **Vale** — akademik Türkçe stil kuralları için Vale konfigürasyonu
2. **markdownlint-cli2** — tüm Markdown dosyaları için kural seti
3. **lychee** — link doğrulama, export sonrası ve pre-build gate'te otomatik çalışır
4. **actionlint** — GitHub Actions workflow dosyaları doğrulaması
5. **`bookmaker check book`** — kitap geneli tutarlılık kontrolü:
   - `code_id` benzersizliği kitap genelinde
   - Terim sözlüğü çelişki tespiti
   - Kavram çakışma raporu (farklı bölümlerde zıt tanımlar)
   - Kapsam dışı konu ihlali (bir bölümün kapsam dışını başka bölüm işliyor mu?)
6. **GitHub Actions** — CI workflow:
   - `pytest` çalıştır
   - `ruff check` çalıştır
   - `bookmaker check chapter` smoke testi
   - `bookmaker build docx` smoke testi
7. **GitHub Pages** — MkDocs otomatik deploy workflow
8. **pre-commit** hookları:
   - `ruff` format/lint
   - `markdownlint-cli2`
   - `bookmaker check chapter` (değişen MD dosyaları için)
9. **hyperfine** — kritik komut performans benchmarkları

### Kabul Kriterleri

- [ ] CI tüm testleri otomatik geçirir
- [ ] `pre-commit run --all-files` hatasız tamamlanır
- [ ] `lychee` sıfır kırık link rapor eder
- [ ] `bookmaker check book` tutarsız tanım/`code_id` çakışması tespit eder
- [ ] GitHub Pages deploy çalışır

### Çıktılar

```
.github/workflows/ci.yml
.github/workflows/pages.yml
.vale.ini
.markdownlint.yaml
.lychee.toml
```

---

## Genel Kabul Kriterleri (Tüm Fazlar)

Yazılım tamamlandı sayılmak için:

- [ ] `bookmaker --version` çalışır
- [ ] `bookmaker check chapter .\sample\sample_chapter.md` → PASS, score=100
- [ ] `bookmaker check book .\my-java-book` → tutarlılık raporu üretir
- [ ] `bookmaker init --preset java-temelleri` → workspace oluşturur, seed formu book_architecture'dan ön doldurulur
- [ ] `bookmaker chapter prompt outline chapter_03` → prompt dosyası üretir
- [ ] `bookmaker chapter evaluate outline chapter_03` → 2 katmanlı değerlendirme + kullanıcı checklist
- [ ] `bookmaker chapter evaluate draft chapter_03` → kalite raporu üretir, CODE_META fallback tespiti çalışır
- [ ] `bookmaker chapter check technical chapter_03` → kod testi raporu üretir; hata varsa onarım promptu üretilir
- [ ] Revizyon paketleri PRESERVE bloğunu otomatik içerir
- [ ] `bookmaker build gate` → pre-build gate raporu üretir
- [ ] `bookmaker build docx` → geçerli DOCX üretir
- [ ] `bookmaker build mkdocs` → `mkdocs build` hatasız tamamlanır
- [ ] `bookmaker studio` → tarayıcıda tam GUI çalışır; LLM sağlayıcı istatistikleri dashboard'da görünür
- [ ] `pytest` → tüm testler geçer
- [ ] `just check` → lint + test hatasız tamamlanır

---

## Teknoloji Yığını Özeti

| Katman | Araç/Kütüphane |
|--------|----------------|
| Dil | Python 3.14 |
| CLI | Typer + Rich |
| Veri modelleri | Pydantic v2 |
| YAML | ruamel.yaml |
| Backend | FastAPI + Uvicorn |
| Şablonlar | Jinja2 |
| Veritabanı | SQLite (stdlib) |
| Test | pytest |
| Lint/Format | ruff |
| Otomasyon | just + pre-commit |
| DOCX export | pandoc |
| PDF export | pandoc + weasyprint |
| EPUB export | pandoc |
| MkDocs | mkdocs-material |
| Mermaid | mmdc |
| Görseller | ImageMagick |
| Screenshot | playwright |
| QR | qrcode[pil] |
| Link doğrulama | lychee |
| Markdown kalite | markdownlint-cli2 |
| Dil/stil | Vale |
| Java derleme | javac + java (JDK 17) |

---

## Faz Sırası ve Bağımlılıklar

```
Faz 0 (İskelet)
  └── Faz 1 (Modeller + Depolama)
        ├── Faz 2 (Validator)
        │     └── Faz 3 (Pipeline Motoru)
        │           └── Faz 4 (Authoring Akışı)
        │                 ├── Faz 5 (Java Teknik Kontrol)
        │                 └── Faz 6 (Export Hattı)
        │                       └── Faz 7 (Studio GUI)
        │                             └── Faz 8 (Kalite + CI/CD)
        └── [Faz 2, 3, 4, 5, 6, 7, 8 Faz 1'e bağımlı]
```

Her faz bir öncekinin kabul kriterlerini karşılamasına bağlıdır.
