# bookMaker Coding Plan

Bu belge, kodlamaya baslamadan once kilitlenen teknik kararları, mimari taslagi, modül sinirlarini, veri modellerini, CLI/GUI yaklasimini ve ilk MVP uygulama sirasini tanimlar.

Bu dosya kod yazimina baslarken ana referans kabul edilecektir. `TODO.md` urun hedeflerini, `CHAPTER_SPEC.md` bolum Markdown sozlesmesini, `CHAPTER_AUTHORING_WORKFLOW.md` bolum yazim akisini, `RESUME.md` ise oturumlar arasi kisa hafizayi tutar. `CODING_PLAN.md` bunlari uygulama mimarisine cevirir.

## 1. Kilitlenmis Kararlar

### 1.1. Dil ve Calisma Ortami

- Ana dil: Python.
- Hedef Python surumu: Python 3.14.
- Gelistirme ortami: Windows + PowerShell 7.6.1.
- Tum dosyalar UTF-8 olarak yazilacak ve okunacak.
- Java kod testleri icin mevcut JDK/Javac kullanilacak.
- Dis araclarla entegrasyon Windows yollarina, bosluklu OneDrive yollarina ve PowerShell davranisina uyumlu yazilacak.

### 1.2. Paket ve Komut Adi

- Python paket adi: `bookmaker`.
- CLI komutu: `bookmaker`.
- Repo adi `bookMaker` olarak kalabilir; Python import/CLI tarafinda kucuk harf `bookmaker` kullanilacak.

### 1.3. Ilk Kitap Profili

Ilk resmi desteklenecek kitap profili:

```yaml
book_type: java_fundamentals
book_title: "Java Temelleri"
language: tr-TR
audience: "universite baslangic duzeyi / meslek yuksekokulu / programlamaya giris"
primary_code_language: java
first_export_target: docx
```

Bu karar, sistemi sadece Java kitabina kilitlemez. Ancak ilk MVP'de kalite kapilari, kod testleri, prompt sablonlari ve ornek fixture'lar Java Temelleri kitabi uzerinden dogrulanir.

### 1.4. LLM Calisma Modeli

- Ana ve varsayilan LLM kullanimi manuel copy/paste olacak.
- Sistem API entegrasyonu hic olmayacakmis gibi calisacak.
- API adapterleri mimari olarak mumkun olacak, ancak MVP'nin calismasi icin zorunlu olmayacak.
- Yazar promptu `bookMaker`dan kopyalar, harici LLM web arayuzune yapistirir, LLM ciktisini tekrar `bookMaker`a yapistirir.
- LLM ciktisi dogrudan onayli icerik sayilmaz; parse, normalize, kalite kontrolu, revizyon ve kullanici onayi gerekir.

### 1.5. Durum ve Surumleme Modeli

Runtime durum icin hibrit model kullanilacak:

- Dosya sistemi: asil artefaktlarin okunabilir kaynaklari.
- SQLite: indeks, event log, kalite skor gecmisi, arama ve GUI hizlandirma.

Bu yaklasim su nedenle tercih edildi:

- Markdown/YAML/JSON dosyalari Git, diff ve manuel inceleme icin uygundur.
- SQLite GUI tarafinda hizli listeleme, filtreleme, dashboard ve event sorgulari icin uygundur.
- Sistem, veritabani bozulsa bile dosya artefaktlarindan yeniden indeks uretebilmelidir.

### 1.6. Ilk Export Hedefi

- Ilk export hedefi: DOCX.
- Pandoc merkezli DOCX cikti hatti kurulacak.
- PDF, EPUB, MkDocs ve HTML ikinci fazda desteklenecek; mimari buna uyumlu kalacak.

## 2. Urun Sinirlari

### 2.1. MVP'nin Cozecegi Problem

Ilk MVP'nin asil hedefi kitap export motoru olmak degildir. Ilk ayirt edici deger, yazar odakli bolum uretim pipeline'idir:

1. Kitap profili olusturma.
2. Kitap mimarisi ve bolum listesi olusturma.
3. Bolum tohumu girme.
4. Outline promptu uretme.
5. LLM outline ciktisini yapistirma.
6. Outline kalite kontrolu ve revizyon paketi.
7. Tam metin promptu uretme.
8. LLM tam metin + inline `CODE_META` ciktisini yapistirma.
9. Markdown/meta kontrolu, normalize, kalite skoru.
10. Java kod cikarimi ve temel smoke test.
11. Onayli bolum dosyasi.
12. DOCX export.

### 2.2. MVP Disinda Kalacaklar

Asagidakiler ilk MVP'de ana hedef degildir:

- Tam otomatik LLM API ile kitap yazdirma.
- Cok kullanicili web servis.
- Bulut tabanli veritabani.
- PDF/EPUB/MkDocs'i birinci kalite hedefi yapmak.
- Tum programlama dilleri icin eksiksiz test adapterleri.
- Gelismis akademik kaynak dogrulama.
- Tam metin semantik dogrulamanin tamamen LLM ile yapilmasi.

Bu ozellikler mimaride yer acilarak sonraki fazlara birakilacak.

## 3. Teknoloji Yigini

### 3.1. Zorunlu Cekirdek

```text
Python 3.14
Typer
Rich
Pydantic v2
ruamel.yaml
FastAPI
Uvicorn
Jinja2
SQLite / sqlite3
pytest
```

Karar gerekceleri:

- `Typer`: alt komutlu CLI ve tip temelli parametre dogrulama icin uygun.
- `Rich`: CLI raporlarini okunabilir hale getirmek icin uygun.
- `Pydantic v2`: manifest, pipeline, issue, quality report ve metadata modellerinde merkezi dogrulama icin uygun.
- `ruamel.yaml`: YAML round-trip ve yorum/sira koruma ihtimali icin PyYAML'dan daha uygun.
- `FastAPI`: yerel Studio GUI icin JSON API ve statik dosya sunumu saglar.
- `sqlite3`: Python stdlib icinde; ek veritabani bagimliligi gerektirmez.
- `pytest`: validator, parser, CLI ve pipeline icin test standardi.

### 3.2. Dis Araclar

```text
pandoc       DOCX export
javac/java   Java kod derleme/calistirma
mmdc         Mermaid render
playwright   screenshot/browser smoke
sqlite3      manuel DB inceleme
rg/fd/bat    gelistirme ve inceleme
markdownlint markdown kalite kontrol
```

Ilk kodlama fazinda `pandoc`, `java`, `javac` ve mevcut `chapter_semantic_validator.py` temel dogrulama icin yeterlidir.

### 3.3. Ilk Asamada Eklenmeyecekler

- React/Vite: Studio MVP sade HTML/CSS/JS ile baslayacak.
- SQLAlchemy: ilk asamada stdlib `sqlite3` yeterli. Ihtiyac buyurse adapter katmani uzerinden eklenebilir.
- Celery/RQ: yerel tek kullanicili MVP icin fazla agir.
- Tam text editor frameworkleri: ilk Studio'da textarea + preview + rapor yeterli.

## 4. Repo ve Paket Yapisi

Hedef ilk paket yapisi:

```text
bookMaker/
  pyproject.toml
  README.md
  TODO.md
  RESUME.md
  WORKSPACE.md
  CODING_PLAN.md
  CHAPTER_SPEC.md
  CHAPTER_AUTHORING_WORKFLOW.md
  sample/
  promptlar/
  tools/
  src/
    bookmaker/
      __init__.py
      __main__.py
      cli.py
      core/
        __init__.py
        paths.py
        errors.py
        time.py
        ids.py
        encoding.py
      models/
        __init__.py
        book.py
        chapter.py
        metadata.py
        pipeline.py
        quality.py
        versioning.py
        exchange.py
      storage/
        __init__.py
        files.py
        sqlite.py
        schema.sql
        repositories.py
      chapter/
        __init__.py
        parser.py
        meta_blocks.py
        validator.py
        normalizer.py
        scoring.py
      authoring/
        __init__.py
        seed.py
        outline.py
        draft.py
        prompts.py
        revision.py
        workflow.py
      pipeline/
        __init__.py
        definitions.py
        engine.py
        gates.py
        state.py
      production/
        __init__.py
        code_extract.py
        code_manifest.py
        java_adapter.py
        pandoc_docx.py
        reports.py
      studio/
        __init__.py
        app.py
        routes.py
        services.py
        static/
          index.html
          app.js
          styles.css
      templates/
        prompts/
        manifests/
        pipelines/
        export/
  tests/
    fixtures/
    unit/
    integration/
    cli/
```

Not: Mevcut `tools/chapter_semantic_validator.py` ilk asamada korunacak. Paket icine alinirken davranis degistirilmeden test altina alinacak.

## 5. Kitap Projesi Workspace Yapisi

`bookmaker init --preset java-temelleri` komutu su yapida bir kitap workspace'i uretmelidir:

```text
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
        outline_prompt_v001.md
        outline_response_v001.md
        outline_report_v001.json
      draft/
        full_text_prompt_v001.md
        draft_v001.md
        normalized_v001.md
        draft_report_v001.json
        revision_packet_v001.yaml
      approved/
        chapter_01.md
      technical/
        code_manifest_v001.json
        code_test_report_v001.json
      version_log.jsonl
      active_version.yaml
  prompts/
  assets/
    images/
    mermaid/
    screenshots/
    qr/
  build/
    merged/
    code/
    reports/
    docx/
  exports/
    docx/
```

Kurallar:

- Insan tarafindan okunabilir ana artefaktlar dosya sisteminde kalir.
- SQLite bu dosyalari indeksler; dosyalarin yerine gecmez.
- Her chapter klasoru kendi `version_log.jsonl` ve `active_version.yaml` dosyasini tasir.
- Onayli bolum dosyasi `approved/chapter_XX.md` altinda kilitli kabul edilir; degisiklik yeni surumle yapilir.

## 6. Veri Modelleri

### 6.1. BookProfile

```yaml
book_id: java_temelleri
title: "Java Temelleri"
subtitle: ""
author: ""
language: tr-TR
audience: ""
level: beginner
domain: programming
primary_code_language: java
export_targets:
  - docx
quality_profile: academic_technical_book_v1
```

Pydantic modeli:

- `book_id`: slug.
- `title`: zorunlu.
- `author`: zorunlu ama ilk init sirasinda placeholder olabilir.
- `language`: varsayilan `tr-TR`.
- `primary_code_language`: ilk preset icin `java`.
- `export_targets`: MVP'de en az `docx`.

### 6.2. BookArchitecture

```yaml
chapters:
  - chapter_id: chapter_01
    order: 1
    title: "Java'ya Giriş"
    chapter_type: core
    status: planned
    expected_learning_outcomes: []
    mandatory_concepts: []
```

Kurallar:

- Bolum `chapter_id` degerleri benzersiz olmalı.
- `order` degerleri tekrar etmemeli.
- Her bolumun title, type ve status alani olmalı.
- Kitap mimarisi onaylanmadan bolum tohumu final sayilmamali.

### 6.3. ChapterSeed

Bolum tohumu, LLM'e verilecek bolum ozelindeki niyeti tasir:

```yaml
chapter_id: chapter_03
purpose: ""
audience_notes: ""
prerequisites: []
learning_outcomes: []
mandatory_concepts: []
required_code_examples: []
required_diagrams: []
required_exercises: []
out_of_scope: []
source_policy: ""
author_notes: ""
```

Kurallar:

- `purpose`, `learning_outcomes`, `mandatory_concepts`, `out_of_scope` bos olmamali.
- Java presetinde `required_code_examples` en az bir ornek icermeli veya neden icermedigi belirtilmeli.
- Seed onaylanmadan outline promptu uretilebilir ama "approved seed" statüsüne gecemez.

### 6.4. CodeMeta

`CODE_META` LLM tarafindan uretilen bolum metninin icinde bulunur.

Zorunlu alanlar:

```yaml
order: 001
code_id: dosya_islemleri_001
extension: java
kind: example
title: "Temel dosyaya yazma ve okuma"
file: DosyaIslemleriTemel.java
main_class: DosyaIslemleriTemel
link: "{repo}/{project-alias}/{chapter-alias}/{file}"
qrfile: dosya_islemleri_001.png
extract: true
test: compile_run_assert
github: true
qr_policy: dual
intentional_mismatch: false
validation_mode: runnable
```

Ek kurallar:

- `CODE_META` kod fence icinde olmayacak.
- `CODE_META` ile kod blogu arasina baslik veya paragraf girmeyecek.
- Java icin `file` ile `public class` ve `main_class` uyumlu olacak.
- `broken_example` icin `intentional_mismatch: true`, `validation_mode: review_only`, `test: skip` beklenir.
- `fixed_example` icin `paired_with` beklenir.

### 6.5. Issue

Kalite raporlarinin atomik birimi:

```yaml
issue_id: issue_0001
severity: error
category: code_meta
location:
  file: chapters/chapter_03/draft/normalized_v001.md
  line: 120
message: "CODE_META ile kod blogu arasinda aciklama var."
expected: "CODE_META blogundan hemen sonra fenced code block gelmeli."
current: "Araya paragraf girmis."
instruction: "Paragrafi kod blogundan sonraya tasi veya CODE_META'yi kod blogunun hemen onune al."
acceptance_criteria:
  - "Validator CODE_META placement hatasi vermemeli."
llm_repair_hint: ""
```

Issue tasarimi iki amaca hizmet eder:

- GUI'de yazara net hata gosterimi.
- LLM'e yapistirilabilir revizyon paketi uretimi.

### 6.6. QualityReport

```yaml
artifact_type: draft
artifact_version: draft_v001
score: 87
decision: revision_required
errors: 1
warnings: 4
issues: []
checks:
  - id: heading_hierarchy
    status: pass
  - id: code_meta_required_fields
    status: fail
```

Karar degerleri:

- `pass`
- `revision_required`
- `blocked`

### 6.7. VersionEvent

```yaml
event_id: evt_000001
created_at: "2026-05-03T12:00:00+03:00"
chapter_id: chapter_03
event_type: draft_pasted
artifact_type: draft
artifact_version: draft_v001
path: draft/draft_v001.md
score: null
parent_version: null
user_action: true
notes: ""
```

Kurallar:

- Her paste, normalize, evaluate, approve, restore islemi event uretir.
- Geri alma eski dosyayi ezmez; eski surumden yeni aktif surum olusturur.
- SQLite event tablosu ile `version_log.jsonl` uyumlu tutulur.

## 7. SQLite Taslagi

SQLite dosyasi: `bookmaker.sqlite`

Ilk tablo seti:

```sql
CREATE TABLE IF NOT EXISTS projects (
  id TEXT PRIMARY KEY,
  root_path TEXT NOT NULL,
  title TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chapters (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  chapter_id TEXT NOT NULL,
  title TEXT NOT NULL,
  chapter_order INTEGER NOT NULL,
  status TEXT NOT NULL,
  active_version TEXT,
  last_score INTEGER,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS artifacts (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  chapter_id TEXT,
  artifact_type TEXT NOT NULL,
  artifact_version TEXT NOT NULL,
  path TEXT NOT NULL,
  checksum TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS version_events (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  chapter_id TEXT,
  event_type TEXT NOT NULL,
  artifact_type TEXT,
  artifact_version TEXT,
  path TEXT,
  score INTEGER,
  payload_json TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_reports (
  id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  chapter_id TEXT,
  artifact_type TEXT NOT NULL,
  artifact_version TEXT NOT NULL,
  score INTEGER NOT NULL,
  decision TEXT NOT NULL,
  report_path TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS issues (
  id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  severity TEXT NOT NULL,
  category TEXT NOT NULL,
  file_path TEXT,
  line INTEGER,
  message TEXT NOT NULL,
  expected TEXT,
  current TEXT,
  instruction TEXT,
  status TEXT NOT NULL DEFAULT 'open'
);
```

Ilk fazda migration sistemi basit tutulacak:

- `schema.sql` versiyonlu tutulur.
- `storage.sqlite.ensure_schema()` tablo olusturur.
- `schema_version` tablosu ikinci fazda eklenebilir.

## 8. Pipeline Modeli

### 8.1. Pipeline Definition

`pipeline_definition.yaml` statik tanimdir:

```yaml
pipeline_id: academic_technical_book_v1
steps:
  - id: edit_book_profile
    title: "Kitap Profili"
    type: form
    required_artifacts:
      - book_profile
    next:
      - edit_book_architecture

  - id: seed_chapter
    title: "Bolum Tohumu"
    type: form
    required_artifacts:
      - chapter_seed
    gate: chapter_seed_complete
    next:
      - generate_outline_prompt

  - id: generate_outline_prompt
    title: "Outline Promptu"
    type: prompt_render
    output_artifact: outline_prompt
    next:
      - paste_outline

  - id: paste_outline
    title: "Outline Ciktisi"
    type: manual_paste
    output_artifact: outline_candidate
    next:
      - evaluate_outline

  - id: evaluate_outline
    title: "Outline Kalite Kontrolu"
    type: evaluation
    gate: outline_quality
    next:
      - approve_outline
      - revise_outline

  - id: generate_full_text_prompt
    title: "Tam Metin Promptu"
    type: prompt_render
    output_artifact: full_text_prompt
    next:
      - paste_full_text

  - id: paste_full_text
    title: "Tam Metin Ciktisi"
    type: manual_paste
    output_artifact: full_text_candidate
    next:
      - normalize_full_text

  - id: normalize_full_text
    title: "Normalize"
    type: automation
    output_artifact: normalized_chapter
    next:
      - evaluate_full_text

  - id: evaluate_full_text
    title: "Tam Metin Kalite Kontrolu"
    type: evaluation
    gate: full_text_quality
    next:
      - technical_check
      - revise_full_text

  - id: technical_check
    title: "Teknik Kontrol"
    type: automation
    gate: technical_check
    next:
      - approve_chapter

  - id: build_docx
    title: "DOCX Export"
    type: export
```

### 8.2. Pipeline State

`pipeline_state.yaml` kullanici tarafindan okunabilir aktif durumdur:

```yaml
project_id: java_temelleri
pipeline_id: academic_technical_book_v1
current_stage: authoring
chapters:
  chapter_03:
    current_step: evaluate_full_text
    active_seed: seed_v001
    active_outline: outline_v002
    active_draft: normalized_v001
    last_score: 84
    blocked_by:
      - issue_0007
```

SQLite bu durumun hizli indeksidir; tek dogruluk kaynagi dosya sistemi + state dosyalaridir.

## 9. CLI Taslagi

Ilk komutlar:

```powershell
bookmaker --version
bookmaker init --preset java-temelleri --path .\my-java-book
bookmaker project status
bookmaker chapter list
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
bookmaker chapter check technical chapter_03
bookmaker chapter approve chapter_03
bookmaker version list chapter_03
bookmaker version diff chapter_03 draft_v001 draft_v002
bookmaker version restore chapter_03 draft_v001
bookmaker check chapter .\sample\sample_chapter.md
bookmaker build docx
bookmaker studio --host 127.0.0.1 --port 8765
```

CLI ilkeleri:

- Tum komutlar `--json` opsiyonu alabilmeli.
- Hata durumunda cikis kodlari tutarli olmali.
- Insan okunur rapor Rich ile, makine okunur rapor JSON ile verilmeli.
- Dosya yazan komutlar hangi dosyayi yazdigini acikca raporlamali.
- Onayli dosyayi ezen komut olmamali; yeni surum uretmeli.

## 10. Studio GUI Taslagi

Ilk Studio sade HTML/CSS/JS + FastAPI olacak.

### 10.1. Ana Ekranlar

1. Dashboard
   - Aktif kitap.
   - Bolum sayisi.
   - Asama dagilimi.
   - Ortalama kalite skoru.
   - Bloklu bolumler.
   - Son eventler.

2. Kitap Profili
   - `book_profile.yaml` formu.
   - Yazar, kitap adi, hedef kitle, dil, export hedefleri.

3. Kitap Mimarisi
   - Bolum listesi.
   - Bolum sirasi, baslik, tur, durum.

4. Bolum Stüdyosu
   - Sol panel: bolum listesi.
   - Orta panel: aktif is alani.
   - Sag panel: kalite raporu, issue listesi, siradaki eylem.

5. Surum Gecmisi
   - Artifact surumleri.
   - Diff.
   - Bu surume don.
   - Bu surumden revizyon promptu uret.

6. Export
   - DOCX build.
   - Pandoc log.
   - Build raporu.

### 10.2. Bolum Stüdyosu Tableri

```text
Tohum
Outline Promptu
Outline Ciktisi
Outline Kalite Raporu
Tam Metin Promptu
Tam Metin Ciktisi
Normalize
Tam Metin Kalite Raporu
Teknik Kontrol
Onayli Bolum
Surum Gecmisi
```

### 10.3. Metadata Formlari

Yazar YAML yazmak zorunda kalmamalidir.

Kod bloklari algilaninca sag panelde su form gosterilir:

- `code_id`
- `order`
- `kind`
- `title`
- `file`
- `main_class`
- `extract`
- `test`
- `github`
- `qr_policy`
- `intentional_mismatch`
- `paired_with`
- `validation_mode`

Form degisiklikleri dogrudan onayli dosyayi ezmez; yeni normalized/draft surumu uretir.

## 11. Chapter Parser ve Validator

Ilk hedef, mevcut `tools/chapter_semantic_validator.py` davranisini paketlemek ve test etmektir.

### 11.1. Parser Sorumluluklari

- YAML front matter ayrisitirma.
- Markdown heading hiyerarsisini cikarma.
- HTML yorum bloklarindan meta bloklari cikarma.
- `SECTION_META`, `SUBSECTION_META`, `CODE_META`, `MERMAID_META`, `SCREENSHOT_META` ayristirma.
- Meta blok ile takip eden heading/code fence iliskisini kurma.
- Kod fence dilini ve icerigini cikarma.

### 11.2. Validator Sorumluluklari

- Front matter zorunlu alanlari.
- Tek H1 kontrolu.
- Elle numaralandirma uyarilari.
- `SECTION_META.order` benzersizligi.
- `SECTION_META.title` ile baslik uyumu.
- `CODE_META` varligi ve yeri.
- `CODE_META` zorunlu alanlari.
- Java `file`, `main_class`, `public class` uyumu.
- `intentional_mismatch`, `paired_with`, `validation_mode`, `test` tutarliligi.
- Mermaid meta/fence eslesmesi.
- Final modda placeholder kontrolu.

### 11.3. Skorlama

Ilk skorlama kurali:

```text
score = 100
error   -> -15
warning -> -3
info    -> 0
minimum score = 0
```

Karar:

- `errors > 0`: `blocked` veya `revision_required`.
- `score < 85`: full text icin revizyon onerilir.
- `score >= 85` ve kritik hata yoksa kullanici onayi mumkun.

## 12. Prompt Sistemi

Prompt sablonlari dosya tabanli olacak:

```text
src/bookmaker/templates/prompts/
  outline_prompt.md.j2
  outline_revision_prompt.md.j2
  full_text_prompt.md.j2
  full_text_revision_prompt.md.j2
  metadata_repair_prompt.md.j2
  code_repair_prompt.md.j2
```

### 12.1. Full Text Prompt Zorunlu Kurallari

Tam metin promptu LLM'e sunlari acikca soylemelidir:

- Cikti Markdown olacak.
- Basliklar elle numaralandirilmayacak.
- `CHAPTER_SPEC.md` yapisi izlenecek.
- Her dosyaya cikarilacak/test edilecek kod blogundan hemen once `CODE_META` uretilecek.
- `CODE_META` kod fence icine yazilmayacak.
- Bilerek hatali ornekler `broken_example`, `intentional_mismatch: true`, `validation_mode: review_only`, `test: skip` ile isaretlenecek.
- Duzeltilmis ornekler `fixed_example` ve `paired_with` ile baglanacak.
- Java kodlarinda dosya adi, `main_class` ve `public class` uyumlu olacak.

### 12.2. Revision Packet

Revizyon paketi LLM'e kopyalanabilir bicimde uretilecek:

```yaml
revision_packet:
  target_artifact: normalized_v001.md
  objective: "CODE_META eksiklerini gider."
  issues:
    - issue_id: issue_0003
      severity: error
      location: "line 240"
      expected: ""
      current: ""
      instruction: ""
      acceptance_criteria: []
  constraints:
    - "Tam bolumu yeniden yazma."
    - "CODE_META alanlarini koru."
    - "Sadece belirtilen bloklari duzelt."
```

## 13. Java Kod Hatti

Ilk production adapter Java olacak.

### 13.1. Code Extraction

Girdi:

- Onayli veya normalized bolum Markdown.

Cikti:

```text
build/code/chapter_03/code_id/FileName.java
build/reports/code_manifest.json
```

Kurallar:

- Sadece `extract: true` kodlar dosyaya cikarilir.
- `test: skip` olanlar manifestte kalir ama calistirilmaz.
- `validation_mode: review_only` olanlar raporda `skipped` sayilir.

### 13.2. Java Test

Komut modeli:

```powershell
javac -encoding UTF-8 FileName.java
java -Dfile.encoding=UTF-8 MainClass
```

Test tipleri:

- `compile_only`
- `compile_run`
- `compile_run_assert`
- `skip`

`compile_run_assert` icin `expected_stdout_contains` gerekir.

## 14. DOCX Export Hatti

Ilk DOCX hattinin kapsami:

1. Onayli bolumleri siraya gore bul.
2. Birlesik Markdown olustur.
3. Mermaid ve asset placeholderlarini ilk fazda bozmadan tasiyabil.
4. Pandoc ile DOCX uret.
5. Pandoc logunu kaydet.
6. Export raporu uret.

Ilk komut:

```powershell
bookmaker build docx
```

Ilk fazda reference DOCX opsiyonel olacak. Java Temelleri presetinde mevcut ornek reference DOCX daha sonra eklenebilir.

## 15. Test Stratejisi

### 15.1. Unit Testler

- Pydantic model validation.
- YAML load/save.
- Meta block parser.
- `CODE_META` placement.
- Java file/class uyumu.
- Issue generation.
- Score calculation.

### 15.2. Integration Testler

- `sample/sample_chapter.md` validator PASS.
- Hatalı fixture'lar validator FAIL.
- `bookmaker check chapter` JSON raporu uretir.
- `bookmaker init --preset java-temelleri` workspace olusturur.
- Chapter paste/evaluate/normalize flow dosya ve event uretir.
- Java smoke test basarili/skipped/failed durumlarini ayirir.

### 15.3. CLI Smoke Testleri

```powershell
bookmaker --help
bookmaker --version
bookmaker check chapter .\sample\sample_chapter.md --json
bookmaker init --preset java-temelleri --path .\build\smoke\java-book
bookmaker project status --project .\build\smoke\java-book
```

### 15.4. Studio Smoke Testleri

- FastAPI uygulamasi import edilebilir.
- `/api/health` 200 doner.
- `/api/project/status` proje durumunu JSON doner.
- Ana HTML sayfasi yuklenir.
- Playwright ile ilk ekran screenshot alinabilir.

## 16. Kodlama Sirasina Gore Fazlar

### Faz 0: Hazirlik

1. `pyproject.toml` olustur.
2. `src/bookmaker` paket iskeletini olustur.
3. `bookmaker --version` calisir hale getir.
4. `pytest` ve ilk smoke test altyapisini kur.
5. UTF-8 dosya okuma/yazma helper'larini yaz.

### Faz 1: Modeller ve Dosya Deposu

1. `BookProfile`, `BookArchitecture`, `ChapterSeed` modelleri.
2. `Issue`, `QualityReport`, `VersionEvent` modelleri.
3. YAML load/save.
4. Chapter workspace path helper'lari.
5. `version_log.jsonl` append/read.
6. `active_version.yaml` read/write.

### Faz 2: Chapter Validator Paketleme

1. Mevcut validator davranisini bozmadan `bookmaker.chapter.validator` altina al.
2. `sample/sample_chapter.md` fixture testini ekle.
3. `bookmaker check chapter` komutunu ekle.
4. JSON/Markdown rapor cikti opsiyonlarini ekle.

### Faz 3: Pipeline ve Versioning

1. `pipeline_definition.yaml` modeli.
2. `pipeline_state.yaml` modeli.
3. Pipeline transition engine.
4. Gate result modeli.
5. Version event yazimi.
6. SQLite indeksleme.

### Faz 4: Authoring Flow

1. Java Temelleri preset.
2. `bookmaker init --preset java-temelleri`.
3. Seed form dosyasi uretimi.
4. Outline prompt render.
5. Outline paste/evaluate.
6. Full text prompt render.
7. Draft paste/normalize/evaluate.
8. Revision packet uretimi.

### Faz 5: Java Teknik Kontrol

1. `CODE_META` extraction.
2. Code manifest.
3. Java adapter.
4. Smoke test report.
5. Technical gate.

### Faz 6: DOCX Export

1. Approved chapter merge.
2. Pandoc wrapper.
3. DOCX output.
4. Export report.

### Faz 7: Studio MVP

1. FastAPI app.
2. Static HTML/CSS/JS.
3. Dashboard.
4. Chapter Studio.
5. Prompt copy/paste workflow.
6. Quality report panel.
7. Version history panel.

## 17. Ilk Kabul Kriterleri

Ilk kodlama dalgasinin basarili sayilmasi icin:

1. `python -m bookmaker --version` calismali.
2. `bookmaker --help` calismali.
3. `bookmaker check chapter .\sample\sample_chapter.md` PASS vermeli.
4. Validator mevcut raporla uyumlu skor uretmeli.
5. `bookmaker init --preset java-temelleri` calismali.
6. Olusan workspace UTF-8 YAML/Markdown dosyalari icermeli.
7. SQLite dosyasi olusmali ve temel tablolar kurulmalı.
8. En az bir chapter seed dosyasi uretilebilmeli.
9. Full text prompt sablonu inline `CODE_META` kuralini icermeli.
10. Test suite `pytest` ile calismali.

## 18. Riskler ve Onlemler

### 18.1. Python 3.14 Uyumlulugu

Risk: Bazi ucuncu parti paketlerin Python 3.14 destegi gecikmis olabilir.

Onlem:

- Bagimliliklari ilk asamada az tut.
- Mümkün olduğunca stdlib kullan.
- Paket seciminde Python 3.14 uyumlulugunu kurulum/test ile dogrula.

### 18.2. OneDrive ve Bosluklu Yol Problemleri

Risk: Dis araclar bosluklu yollarda veya OneDrive placeholder dosyalarinda hata verebilir.

Onlem:

- Tum subprocess komutlarinda arguman listesi kullan.
- Shell string birlestirmeden kacin.
- Dosya yolu islerinde `Path` kullan.
- Test fixture'larinda bosluklu path senaryosu ekle.

### 18.3. Metadata'nin LLM Tarafindan Eksik Uretilmesi

Risk: LLM tam metinde `CODE_META` bloklarini eksik veya yanlis yerde uretebilir.

Onlem:

- Full text prompt bunu cok acik belirtir.
- Paste sonrasi otomatik analiz hemen issue uretir.
- Metadata repair promptu tek tikla uretilebilir.
- GUI metadata formu ile kullanici dogrudan duzeltebilir.

### 18.4. BookFactory'den Fazla Kod Devralma

Risk: Oncul BookFactory kodu guclu ama karmasik; dogrudan kopyalama yeni cekirdegi agirlastirabilir.

Onlem:

- Ilk cekirdek temiz ve kucuk yazilacak.
- BookFactory fikir/fixture kaynagi olarak kullanilacak.
- Kod devri gerekiyorsa once test altina alinacak, sonra sadeleştirilecek.

## 19. Kodlama Baslangic Karari

Kodlamaya baslandiginda ilk uygulanacak is:

```text
Faz 0 + Faz 1'in baslangici:
pyproject.toml
src/bookmaker paket iskeleti
bookmaker --version
temel Pydantic modeller
UTF-8 dosya helperlari
pytest smoke
```

Bundan sonra mevcut `tools/chapter_semantic_validator.py` paket icine alinip `bookmaker check chapter` komutuna baglanacaktir.

