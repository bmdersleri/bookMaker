# bookMaker Güncel Repo İnceleme ve Geliştirme Önerileri

> **TARIHI RAPOR (5 Mayis 2026).** Incelenen commit: `ce3f213` (baslangic).
> Onerilerin cogu gerceklesti. Studio "acele edilmemeli" uyarisi gecersiz — GUI su an 6 sekme ile calisiyor.

**Rapor tarihi:** 5 Mayıs 2026 | **Incenenen repo:** `https://github.com/bmdersleri/bookMaker`

> Not: GitHub’da erişebildiğim güncel durumda son commit `ce3f213` / `baslangic` / 3 Mayıs 2026 olarak görünmektedir. Repo toplam 2 commit göstermektedir. Daha yeni bir push yaptıysanız ancak GitHub public görünümüne yansımadıysa, rapor erişilebilen son duruma göre hazırlanmıştır.

---

## 1. Yönetici Özeti

`bookMaker`, önceki BookFactory fikrinden daha odaklı ve güçlü bir yöne evrilmiş durumdadır. Proje artık yalnızca Markdown/DOCX üretim betikleri toplamı olmaktan çıkıp **LLM destekli, yazar denetimli, kalite kapılı akademik/teknik kitap üretim stüdyosu** kimliği kazanmaya başlamıştır.

Güncel repoda üç önemli ilerleme görülmektedir:

1. **Vizyon ve mimari belgeleri oldukça olgunlaşmış:** `TODO.md`, `CODING_PLAN.md`, `CHAPTER_SPEC.md` ve `CHAPTER_AUTHORING_WORKFLOW.md` birlikte değerlendirildiğinde projenin ürün sınırları, MVP hedefi, veri modeli, pipeline tasarımı, authoring akışı ve teknik kalite kapıları belirginleşmiştir.
2. **Örnek bölüm ve semantik doğrulama hattı oluşmuş:** `sample/sample_chapter.md`, `tools/chapter_semantic_validator.py` ve `build/reports/chapter_semantic_report.*` dosyaları, `CHAPTER_SPEC` mantığının uygulanabilir olduğunu göstermektedir.
3. **Java smoke test kanıtı eklenmiş:** `sample_chapter_java_smoke.json` raporuna göre 9 kod örneğinin 6’sı geçmiş, 3’ü `review_only` nedeniyle atlanmış, 0 başarısız test vardır. Bu, proje için çok değerli bir teknik doğrulama kanıtıdır.

Buna karşılık repo hâlâ **ürünleşebilir Python paketi** düzeyine gelmemiştir. En kritik eksikler şunlardır:

- `README.md` hâlâ yalnızca başlık düzeyindedir.
- `pyproject.toml`, `src/bookmaker`, `tests`, `.github/workflows`, `.gitignore`, `.editorconfig` görünmemektedir.
- `build/`, `debug.log`, `__pycache__`, `.class` dosyaları ve üretilmiş raporlar repoya commitlenmiştir.
- `tools/chapter_semantic_validator.py` işlevsel görünse de tek dosyada yoğunlaşmıştır; paket modüllerine ayrılmalıdır.
- Örnek Markdown ve bazı dokümanlar GitHub raw görünümünde satır yapısı açısından sorunlu/gereğinden sıkışık görünmektedir.
- CLI hedefleri `CODING_PLAN.md` içinde netleşmiştir ama gerçek `bookmaker` CLI komutu henüz repo yapısında görünmemektedir.

Bu nedenle önerilen ilk hedef şudur:

> **İlk MVP:** `sample/sample_chapter.md` dosyasını al → semantik doğrula → Java kodlarını çıkar/test et → JSON/Markdown raporu üret → tek bölüm DOCX çıktısı al → tüm bunları `bookmaker` CLI komutlarıyla ve CI üzerinde çalıştır.

---

## 2. Repo Güncel Durum Özeti

### 2.1. Kök dizinde görünen ana yapı

GitHub kök görünümünde şu ana dizin/dosyalar yer almaktadır:

```text
bookMaker/
├─ build/
├─ promptlar/
├─ sample/
├─ tools/
├─ .rga-config.json
├─ CHAPTER_AUTHORING_WORKFLOW.md
├─ CHAPTER_SPEC.md
├─ CODING_PLAN.md
├─ README.md
├─ RESUME.md
├─ TODO.md
├─ WORKSPACE.md
└─ debug.log
```

### 2.2. Commit durumu

GitHub commit geçmişinde görünen durum:

```text
3 Mayıs 2026  ce3f213  baslangic
2 Mayıs 2026  4b0fd80  first commit
```

`ce3f213` commit’i 51 dosya ve 49.018 satır ekleme göstermektedir. Bu commit içinde dokümantasyon, prompt paketi, örnek chapter, validator, build çıktıları, Java smoke test klasörleri ve raporlar birlikte yer almaktadır.

### 2.3. Dil dağılımı

GitHub repo görünümünde dil dağılımı yaklaşık şu şekildedir:

```text
Python   75.2%
Java     23.7%
Mermaid   1.1%
```

Bu dağılım, projenin şu anda Python tabanlı otomasyon + Java örnek/test profili üzerine kurulduğunu göstermektedir.

---

## 3. Önceki İncelemeye Göre İlerleme

Aşağıdaki tablo önceki genel değerlendirmeye göre güncel repoda görünen ilerlemeleri özetler.

| Alan | Önceki durum | Güncel durum | Değerlendirme |
|---|---|---|---|
| Ürün vizyonu | BookFactory’den bookMaker’a geçiş yeni netleşiyordu | `TODO.md` ve `CODING_PLAN.md` ile çok daha açık | Güçlü ilerleme |
| Chapter sözleşmesi | Tasarım düzeyindeydi | `CHAPTER_SPEC.md` + örnek bölüm + validator ilişkisi oluşmuş | Çok değerli |
| Authoring workflow | Kavramsal öneri düzeyindeydi | `CHAPTER_AUTHORING_WORKFLOW.md` ile ayrıntılandırılmış | Güçlü ilerleme |
| Semantik validator | Öneri düzeyindeydi | `tools/chapter_semantic_validator.py` mevcut | MVP çekirdeği oluşmuş |
| Örnek bölüm | Kısmi örnek vardı | 49 KB civarında kapsamlı `sample_chapter.md` var | İyi pilot örnek |
| Java test kanıtı | Öneri düzeyindeydi | `sample_chapter_java_smoke.json` 6 pass / 3 skip / 0 fail gösteriyor | Önemli teknik kanıt |
| README | Zayıftı | Hâlâ yalnızca `# bookMaker` | Kritik eksik devam ediyor |
| Paket yapısı | Yoktu | Hâlâ `src/bookmaker`, `pyproject.toml`, `tests` görünmüyor | Kritik eksik devam ediyor |
| Repo hijyeni | Build çıktıları riskliydi | `build/`, `.class`, `debug.log`, `__pycache__` commitli | Düzeltilmeli |
| CI/CD | Yoktu | Hâlâ görünmüyor | Eklenmeli |

---

## 4. Güçlü Taraflar

### 4.1. Ürün kimliği doğru yönde netleşmiş

`bookMaker` için en doğru konumlandırma şudur:

> LLM web arayüzlerini veya API modellerini doğrudan kitap yazdırma aracı gibi kullanmak yerine, yazarın denetiminde çalışan, her aşamada kalite kontrolü yapan, sürümleyen ve teknik doğrulama üreten bir akademik kitap üretim stüdyosu.

Bu yaklaşım akademik etik ve bilimsel üretim açısından doğru zemindedir. Çünkü LLM çıktısı doğrudan nihai metin sayılmamakta; normalize, validate, revise, approve aşamalarından geçirilmektedir.

### 4.2. Manuel LLM copy/paste modeli çok doğru bir MVP kararı

`CODING_PLAN.md` içinde varsayılan LLM kullanımının manuel copy/paste olması isabetlidir. Bunun avantajları:

- API bağımlılığı yoktur.
- Model bağımsızdır.
- ChatGPT, Claude, Gemini, DeepSeek vb. farklı modeller denenebilir.
- Akademik yazar çıktıyı doğrudan görür ve onaylar.
- Maliyet ve rate-limit sorunları MVP’yi bloke etmez.
- Sonradan API adapter eklenebilir.

Bu karar korunmalıdır.

### 4.3. `CHAPTER_SPEC` yaklaşımı projenin ana ayırt edici değeridir

`CHAPTER_SPEC`, sıradan Markdown üretimi yerine makine tarafından denetlenebilir akademik bölüm üretimini hedeflemektedir. Özellikle şu meta bloklar doğru düşünülmüştür:

```text
SECTION_META
SUBSECTION_META
CODE_META
MERMAID_META
SCREENSHOT_META
```

Bu sayede bölüm metni yalnızca okunabilir bir Markdown değil; aynı zamanda üretim hattında işlenebilir bir kaynak dosya hâline gelir.

### 4.4. Validator’ın kural seti MVP için iyi bir başlangıç

`chapter_semantic_validator.py` içinde aşağıdaki kontrollerin bulunduğu görülmektedir:

- Front matter zorunlu alanları
- Önerilen front matter alanları
- Tek H1 kontrolü
- Manuel numaralandırma kontrolü
- `SECTION_META` sırası ve başlık uyumu
- `CODE_META` zorunlu alanları
- `CODE_META` ile kod bloğu ilişkisi
- Java `file`, `main_class`, `public class` uyumu
- `broken_example` / `fixed_example` tutarlılığı
- Mermaid meta/fence eşleşmesi
- Final modda placeholder kontrolü
- JSON ve Markdown rapor üretimi
- Hatalı durumda non-zero exit code

Bu yapı, ileride CLI ve CI ile doğrudan kullanılabilecek bir kalite kapısı çekirdeğidir.

### 4.5. Java smoke test kanıtı çok değerli

`build/reports/sample_chapter_java_smoke.json` raporundaki özet:

```json
{
  "total": 9,
  "passed": 6,
  "skipped": 3,
  "failed": 0
}
```

Bu sonuç iki açıdan önemlidir:

1. Kitap içindeki kodların yalnızca metinsel olarak değil, teknik olarak da doğrulanabileceğini göstermektedir.
2. `review_only`/bilerek hatalı örnek ayrımı doğru çalışmaya başlamıştır.

Bu, projenin “akademik teknik kitap üretiminde güvenilirlik” iddiasını somutlaştıran en önemli kanıtlardan biridir.

---

## 5. Kritik Bulgular ve Öneriler

## 5.1. README.md kritik düzeyde yetersiz

### Bulgu

`README.md` şu anda yalnızca:

```markdown
# bookMaker
```

içermektedir.

### Etki

Bu durum dışarıdan gelen bir kullanıcı, öğrenci, akademisyen, geliştirici veya LLM agent için projeyi neredeyse görünmez hâle getirir. Repo içindeki güçlü tasarım belgeleri README’den keşfedilememektedir.

### Öneri

README aşağıdaki yapıda yeniden yazılmalıdır:

```markdown
# bookMaker

## Nedir?
## Hangi problemi çözer?
## Temel yaklaşım
## Özellikler
## Mevcut durum
## Hızlı başlangıç
## Kurulum
## Örnek kullanım
## Klasör yapısı
## Authoring Pipeline
## Production Pipeline
## Kalite kapıları
## Yol haritası
## Katkı rehberi
## Lisans
```

### İlk README açılış paragrafı önerisi

```markdown
bookMaker, akademik ve teknik kitapların LLM destekli fakat yazar denetimli biçimde üretilmesi için geliştirilen yerel bir kitap üretim stüdyosudur. Sistem; bölüm tohumu oluşturma, outline üretimi, tam metin değerlendirme, metadata doğrulama, kod çıkarma, Java smoke test, görsel/QR yönetimi ve DOCX çıktısı gibi adımları kalite kapılı bir pipeline içinde yönetmeyi hedefler.
```

---

## 5.2. Python paket yapısı henüz yok

### Bulgu

`CODING_PLAN.md` içinde hedef paket yapısı ayrıntılı olarak verilmiş olsa da public repo kökünde şu dosya/klasörler görünmemektedir:

```text
pyproject.toml
src/bookmaker/
tests/
.github/workflows/
```

### Etki

Bu eksiklikler nedeniyle proje şu an:

- `pip install -e .` ile kurulabilir paket değildir.
- `bookmaker` CLI komutu üretmez.
- Test runner standardı yoktur.
- CI üzerinde otomatik doğrulanamaz.
- Geliştirici onboarding süreci zayıftır.

### Öneri

Aşağıdaki minimal paket iskeleti derhal eklenmelidir:

```text
bookMaker/
├─ pyproject.toml
├─ src/
│  └─ bookmaker/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ cli.py
│     ├─ doctor.py
│     └─ chapter/
│        ├─ __init__.py
│        ├─ parser.py
│        ├─ validator.py
│        └─ reports.py
└─ tests/
   ├─ fixtures/
   └─ test_chapter_validator.py
```

### Önerilen `pyproject.toml`

```toml
[build-system]
requires = ["hatchling>=1.25"]
build-backend = "hatchling.build"

[project]
name = "bookmaker"
version = "0.1.0"
description = "LLM destekli, kalite kapılı akademik ve teknik kitap üretim stüdyosu."
readme = "README.md"
requires-python = ">=3.12"
authors = [
  { name = "Prof. Dr. İsmail KIRBAŞ" }
]
dependencies = [
  "typer>=0.12",
  "rich>=13.7",
  "pydantic>=2.8",
  "ruamel.yaml>=0.18",
  "jinja2>=3.1"
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "ruff>=0.6"
]
studio = [
  "fastapi>=0.115",
  "uvicorn>=0.30"
]

[project.scripts]
bookmaker = "bookmaker.cli:app"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Not

`CODING_PLAN.md` Python 3.14 hedefini belirtiyor. 2026 itibarıyla Python 3.14 kararlı sürümdür; ancak üçüncü parti paket uyumluluğu ve kullanıcı kurulum kolaylığı açısından MVP’de `requires-python = ">=3.12"` daha kapsayıcı olabilir. Proje geliştirici ortamında Python 3.14 kullanılabilir; paket gereksinimi ise 3.12+ tutulabilir.

---

## 5.3. Repo hijyeni acilen düzeltilmeli

### Bulgu

Repo içinde şu dosyalar commitlenmiş görünmektedir:

```text
build/
debug.log
tools/__pycache__/
*.class
*.docx
build/reports/*.json
build/reports/*.md
```

Özellikle `build/chapter_java_smoke/` altında `.class` dosyaları, örnek test çalıştırma çıktıları ve metin/CSV dosyaları bulunmaktadır.

### Etki

Bu durum:

- Repo boyutunu gereksiz büyütür.
- Kaynak kod ile build çıktısını karıştırır.
- Git diff kalitesini düşürür.
- CI ve lokal build çıktılarının takibini zorlaştırır.
- İleride gizli/kişisel log sızıntısı riskini artırır.

### Öneri

Kaynak, örnek ve build çıktısı ayrımı yapılmalıdır.

Önerilen düzen:

```text
examples/
├─ java_fundamentals/
│  ├─ sample_chapter.md
│  └─ expected_reports/
│     ├─ chapter_semantic_report.json
│     └─ sample_chapter_java_smoke.json
dist/              # Git dışı
build/             # Git dışı
```

Önerilen `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/
.env

# Logs
*.log
debug.log

# Build / generated
build/
dist/
exports/
*.tmp

# Java generated
*.class

# bookMaker generated reports
build/reports/
build/code/
build/docx/

# OS / editors
.DS_Store
Thumbs.db

# Large generated book outputs
*.docx
*.pdf
*.epub

# Allow intentional sample outputs if needed
!examples/**/*.expected.json
!examples/**/*.expected.md
```

Eğer örnek DOCX özellikle gösterilmek isteniyorsa, `sample/` yerine `examples/outputs/` altında tutulmalı ve README’de “örnek çıktı” olarak açıklanmalıdır.

---

## 5.4. Markdown satır biçimi normalleştirilmeli

### Bulgu

GitHub raw görünümünde bazı Markdown dosyaları ve Python dosyası çok az satıra sıkışmış görünmektedir. Örneğin `sample/sample_chapter.md` GitHub preview tarafında 1451 satır olarak görünürken raw görünümde çok daha az mantıksal satıra sıkışık akmaktadır. Benzer şekilde `tools/chapter_semantic_validator.py` raw görünümde iki büyük satır gibi görünmektedir.

### Olası nedenler

- Dosya satır sonlarının hatalı dönüştürülmesi
- LLM çıktısının paragraf/başlık boşluklarını ezmesi
- Copy/paste sırasında line-break kaybı
- Minify benzeri yanlış formatlama
- GitHub raw/web araçlarının satır sonu algısı

### Etki

Bu durum:

- Kod incelemeyi zorlaştırır.
- Git diff kalitesini bozar.
- Python dosyasında gerçek çalıştırma ve lint süreçlerinde sorun yaratabilir.
- Markdown/Pandoc dönüşümlerinde beklenmeyen sonuçlara yol açabilir.
- LLM agent’ların dosyayı güvenilir biçimde işlemesini zorlaştırır.

### Öneri

`tools/normalize_markdown.py` ve `.editorconfig` eklenmelidir.

Önerilen `.editorconfig`:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
max_line_length = off

[*.py]
indent_style = space
indent_size = 4
max_line_length = 100

[*.yaml]
indent_style = space
indent_size = 2

[*.yml]
indent_style = space
indent_size = 2
```

Markdown normalizer ilk fazda şunları yapmalıdır:

```text
- YAML front matter alanlarını satır satır koru
- Başlık öncesi/sonrası boş satır ekle
- Liste ve tablo bloklarını bozmadan ayır
- Fenced code block öncesi/sonrası boş satır ekle
- HTML meta yorum bloklarını ayrı satırlara taşı
- Birden çok boş satırı en fazla iki boş satıra indir
- UTF-8 + LF standardına dönüştür
```

---

## 5.5. Validator paketlenmeli ve modülerleştirilmeli

### Bulgu

`tools/chapter_semantic_validator.py` işlevsel bir çekirdek içeriyor; ancak tek dosyada çok fazla sorumluluk var:

```text
front matter parse
meta block parse
heading kontrolü
section kontrolü
code meta kontrolü
Java class/file kontrolü
Mermaid kontrolü
placeholder kontrolü
skorlama
rapor üretimi
CLI argüman parse
```

### Etki

Kısa vadede sorun değil; ancak proje büyüdükçe bakım zorlaşır. Yeni dil adapterleri, screenshot meta, QR meta, DOCX export, pipeline gate ve GUI entegrasyonu eklendikçe tek dosya sürdürülemez hâle gelir.

### Önerilen modüler yapı

```text
src/bookmaker/chapter/
├─ parser.py
├─ meta_blocks.py
├─ validator.py
├─ rules_frontmatter.py
├─ rules_headings.py
├─ rules_sections.py
├─ rules_code_meta.py
├─ rules_java.py
├─ rules_mermaid.py
├─ rules_placeholders.py
├─ scoring.py
└─ reports.py
```

### Geçiş stratejisi

1. Mevcut dosyanın davranışı korunur.
2. Önce `tests/fixtures/valid_sample_chapter.md` ile mevcut PASS sonucu sabitlenir.
3. Sonra fonksiyonlar modüllere taşınır.
4. Her taşıma sonrası test çalıştırılır.
5. `tools/chapter_semantic_validator.py` geriye dönük uyumluluk için wrapper yapılır.

Örnek wrapper:

```python
from pathlib import Path
from bookmaker.chapter.validator import validate
from bookmaker.chapter.reports import write_reports

def main() -> int:
    ...
```

---

## 5.6. CLI gerçek komuta dönüştürülmeli

### Bulgu

`CODING_PLAN.md` içinde CLI komutları çok iyi tanımlanmış; ancak repo yapısında `bookmaker` CLI giriş noktası görünmemektedir.

### Önerilen ilk CLI kapsamı

İlk dalgada yalnızca aşağıdaki komutlar yeterlidir:

```powershell
bookmaker --version
bookmaker doctor
bookmaker check chapter .\sample\sample_chapter.md
bookmaker check chapter .\sample\sample_chapter.md --json
bookmaker check chapter .\sample\sample_chapter.md --final
```

İkinci dalga:

```powershell
bookmaker init --preset java-temelleri --path .\my-java-book
bookmaker code extract .\sample\sample_chapter.md --out .\build\code
bookmaker code test .\build\code_manifest.json
bookmaker build docx --project .\my-java-book
```

### Typer tabanlı minimal CLI örneği

```python
from pathlib import Path

import typer
from rich.console import Console

from bookmaker.chapter.validator import validate

app = typer.Typer(help="bookMaker CLI")
console = Console()

@app.callback()
def main() -> None:
    pass

@app.command()
def version() -> None:
    console.print("bookMaker 0.1.0")

check_app = typer.Typer(help="Validation commands")
app.add_typer(check_app, name="check")

@check_app.command("chapter")
def check_chapter(
    path: Path,
    final: bool = typer.Option(False, "--final"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    result = validate(path, final_mode=final)
    if json_output:
        console.print_json(data=result.model_dump())
    else:
        console.print(f"[bold]{result.decision}[/bold] score={result.score}")
    raise typer.Exit(code=1 if result.summary.errors else 0)
```

---

## 5.7. Test altyapısı ve CI eklenmeli

### Bulgu

Repo içinde test kanıtı üretilmiş rapor olarak var; ancak `tests/` klasörü ve CI workflow görünmemektedir.

### Etki

Gelecekte validator veya parser değiştirildiğinde `sample_chapter.md` hâlâ PASS veriyor mu, Java smoke test bozuldu mu, prompt dosyaları formatı koruyor mu otomatik anlaşılmaz.

### Önerilen `tests/` yapısı

```text
tests/
├─ fixtures/
│  ├─ valid_sample_chapter.md
│  ├─ missing_frontmatter.md
│  ├─ missing_code_meta.md
│  ├─ bad_java_class_name.md
│  ├─ broken_example_wrong_test.md
│  └─ mermaid_without_meta.md
├─ unit/
│  ├─ test_frontmatter_parser.py
│  ├─ test_meta_block_parser.py
│  ├─ test_code_meta_rules.py
│  ├─ test_java_rules.py
│  └─ test_scoring.py
└─ integration/
   ├─ test_validate_sample_chapter.py
   └─ test_cli_check_chapter.py
```

### Önerilen ilk GitHub Actions workflow

```yaml
name: ci

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: windows-latest

    strategy:
      matrix:
        python-version: ["3.12", "3.13", "3.14"]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install package
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint
        run: |
          ruff check .

      - name: Tests
        run: |
          pytest -q

      - name: Validate sample chapter
        run: |
          bookmaker check chapter .\sample\sample_chapter.md --final
```

Java smoke test de ayrı job olarak eklenebilir:

```yaml
  java-smoke:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "21"
      - uses: actions/setup-python@v5
        with:
          python-version: "3.14"
      - run: |
          python -m pip install -e ".[dev]"
          bookmaker code extract .\sample\sample_chapter.md --out .\build\code
          bookmaker code test .\build\code_manifest.json
```

---

## 5.8. Python 3.14 hedefi yeniden formüle edilmeli

### Bulgu

`CODING_PLAN.md` hedef Python sürümünü 3.14 olarak belirtiyor.

### Değerlendirme

Python 3.14 artık kararlı ana sürümdür; dolayısıyla “henüz erken” riski önceki yıllara göre azalmıştır. Ancak proje dış kullanıma açılacaksa 3.12+ veya 3.13+ hedeflemek daha pratik olabilir. Çünkü akademisyenlerin, öğrencilerin ve Windows kullanıcılarının çoğunda hâlen 3.12/3.13 kurulu olabilir.

### Öneri

- Geliştirici ortamı: Python 3.14
- Paket minimumu: Python 3.12+
- CI matrisi: 3.12, 3.13, 3.14
- Windows ana platform testi: zorunlu
- Linux testi: ileride opsiyonel ama faydalı

---

## 5.9. `sample/` ve `examples/` ayrımı yapılmalı

### Bulgu

`sample/` içinde hem kaynak Markdown hem birleşik büyük Markdown hem de DOCX çıktı bulunmaktadır:

```text
sample/
├─ Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.docx
├─ Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.md
└─ sample_chapter.md
```

### Öneri

Aşağıdaki ayrım daha temiz olur:

```text
examples/
├─ java_fundamentals/
│  ├─ chapters/
│  │  └─ sample_chapter.md
│  ├─ expected/
│  │  ├─ chapter_semantic_report.json
│  │  └─ java_smoke_report.json
│  └─ README.md
docs/
└─ screenshots/
dist/        # Git dışı
build/       # Git dışı
```

Birleşik kitap çıktıları GitHub Releases veya ayrı bir `sample_outputs` release asset olarak sunulabilir.

---

## 5.10. Prompt paketi korunmalı ama dokümante edilmeli

### Bulgu

`promptlar/` klasörü oldukça zengin görünmektedir. İçinde kullanım kılavuzu, nihai içindekiler, ana sistem promptu, çıktı format standardı, kaynaklar, bölüm yapısı, manifest standardı, kalite kapıları ve örnekler bulunmaktadır.

### Risk

Prompt dosyaları çok değerli; fakat README’den veya docs indeksinden görünür değilse proje dış kullanıcı için keşfedilemez.

### Öneri

`docs/prompt_package.md` oluşturulmalıdır:

```markdown
# Prompt Paketi

## Amaç
## Dosya listesi
## Hangi sırayla kullanılmalı?
## LLM'e verilecek sistem promptu
## Bölüm girdi promptu üretimi
## Tam metin üretimi
## Outline kontrolü
## Metadata repair promptu
## Kalite kapısı promptları
```

Ayrıca promptlar sürümle ilişkilendirilmeli:

```text
promptlar/v1_3/
promptlar/v1_4/
```

veya dosya adındaki sürüm korunup `paket_manifest_v1_3.json` ile yönetilmelidir.

---

## 6. Önerilen Hedef Mimari

Aşağıdaki yapı `bookMaker` için daha sürdürülebilir bir çekirdek sağlar:

```text
bookMaker/
├─ README.md
├─ LICENSE
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ pyproject.toml
├─ .gitignore
├─ .editorconfig
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ docs/
│  ├─ architecture.md
│  ├─ authoring_pipeline.md
│  ├─ chapter_spec.md
│  ├─ cli_reference.md
│  ├─ prompt_package.md
│  └─ mvp_roadmap.md
├─ src/
│  └─ bookmaker/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ cli.py
│     ├─ doctor.py
│     ├─ core/
│     │  ├─ paths.py
│     │  ├─ encoding.py
│     │  ├─ subprocesses.py
│     │  └─ errors.py
│     ├─ models/
│     │  ├─ book.py
│     │  ├─ chapter.py
│     │  ├─ metadata.py
│     │  ├─ quality.py
│     │  └─ pipeline.py
│     ├─ chapter/
│     │  ├─ parser.py
│     │  ├─ meta_blocks.py
│     │  ├─ validator.py
│     │  ├─ normalizer.py
│     │  ├─ scoring.py
│     │  └─ reports.py
│     ├─ authoring/
│     │  ├─ seed.py
│     │  ├─ prompts.py
│     │  ├─ workflow.py
│     │  └─ revision.py
│     ├─ production/
│     │  ├─ code_extract.py
│     │  ├─ java_adapter.py
│     │  ├─ mermaid_adapter.py
│     │  ├─ pandoc_docx.py
│     │  └─ reports.py
│     ├─ storage/
│     │  ├─ files.py
│     │  ├─ sqlite.py
│     │  └─ schema.sql
│     └─ studio/
│        ├─ app.py
│        ├─ routes.py
│        ├─ services.py
│        └─ static/
├─ examples/
│  └─ java_fundamentals/
├─ promptlar/
├─ tests/
│  ├─ fixtures/
│  ├─ unit/
│  ├─ integration/
│  └─ cli/
└─ tools/
   └─ chapter_semantic_validator.py  # backward-compatible wrapper
```

---

## 7. Önceliklendirilmiş Yol Haritası

## 7.1. Faz 0 — Repo hijyeni ve görünürlük

**Süre:** 1–2 gün  
**Amaç:** Projeyi dışarıdan anlaşılır ve kurulabilir hâle getirmek.

Yapılacaklar:

```text
1. README.md yeniden yaz.
2. .gitignore ekle.
3. .editorconfig ekle.
4. LICENSE ekle.
5. CHANGELOG.md ekle.
6. debug.log dosyasını repodan çıkar.
7. __pycache__ ve .class dosyalarını repodan çıkar.
8. build/ klasörünü Git dışına al.
9. Örnek raporları examples/.../expected altına taşı.
10. README içine “mevcut durum: pre-MVP” notu ekle.
```

Kabul kriterleri:

```text
git status temiz
README proje amacını açıklıyor
build çıktıları takip edilmiyor
```

---

## 7.2. Faz 1 — Paket iskeleti ve temel CLI

**Süre:** 2–4 gün  
**Amaç:** Projeyi gerçek Python paketi hâline getirmek.

Yapılacaklar:

```text
1. pyproject.toml oluştur.
2. src/bookmaker iskeletini kur.
3. bookmaker --version çalışsın.
4. bookmaker doctor çalışsın.
5. tools/chapter_semantic_validator.py davranışını bozmadan paket içine taşı.
6. bookmaker check chapter komutunu ekle.
7. sample_chapter validator testini ekle.
```

Kabul kriterleri:

```powershell
pip install -e ".[dev]"
bookmaker --version
bookmaker check chapter .\sample\sample_chapter.md
pytest -q
```

---

## 7.3. Faz 2 — Validator güvenceye alınsın

**Süre:** 3–5 gün  
**Amaç:** Semantik validator kalitesini testlerle sabitlemek.

Yapılacaklar:

```text
1. Valid fixture: PASS 100.
2. Eksik frontmatter fixture: FAIL.
3. Eksik CODE_META fixture: FAIL.
4. Java class/file mismatch fixture: FAIL.
5. broken_example yanlış test modu fixture: FAIL.
6. Mermaid meta/fence mismatch fixture: FAIL.
7. Placeholder final mode fixture: FAIL.
8. Markdown ve JSON rapor snapshot testleri.
```

Kabul kriterleri:

```text
pytest tüm fixture testlerini çalıştırır
validator davranışı modülerleştirme sonrası değişmez
```

---

## 7.4. Faz 3 — Java code extract + smoke test

**Süre:** 5–7 gün  
**Amaç:** Örnek bölümdeki Java kodlarını otomatik çıkarıp çalıştırmak.

Yapılacaklar:

```text
1. CODE_META bloklarını manifest’e dönüştür.
2. extract: true olanları dosyaya yaz.
3. test: skip olanları manifestte tut ama çalıştırma.
4. validation_mode: review_only olanları skipped yap.
5. javac/java subprocess adapter yaz.
6. expected_stdout_contains doğrula.
7. JSON + Markdown smoke test raporu üret.
```

Kabul kriterleri:

```powershell
bookmaker code extract .\sample\sample_chapter.md --out .\build\code
bookmaker code test .\build\code_manifest.json --report .\build\reports\java_smoke.json
```

Beklenen rapor:

```json
{
  "total": 9,
  "passed": 6,
  "skipped": 3,
  "failed": 0
}
```

---

## 7.5. Faz 4 — DOCX export MVP

**Süre:** 5–7 gün  
**Amaç:** Tek bölümden DOCX üretmek.

Yapılacaklar:

```text
1. Pandoc varlık kontrolü.
2. Markdown kaynak hazırlama.
3. Mermaid görsellerini opsiyonel render etme.
4. DOCX export komutu.
5. Pandoc log kaydı.
6. Export raporu.
```

İlk komut:

```powershell
bookmaker build docx --input .\sample\sample_chapter.md --out .\dist\sample_chapter.docx
```

---

## 7.6. Faz 5 — Authoring workflow MVP

**Süre:** 1–2 hafta  
**Amaç:** Yazarın LLM copy/paste akışını bookMaker üzerinden yönetmek.

İlk komutlar:

```powershell
bookmaker init --preset java-temelleri --path .\my-java-book
bookmaker chapter seed chapter_01
bookmaker chapter prompt outline chapter_01
bookmaker chapter paste outline chapter_01 --from-file .\outline.md
bookmaker chapter evaluate outline chapter_01
bookmaker chapter prompt draft chapter_01
bookmaker chapter paste draft chapter_01 --from-file .\draft.md
bookmaker chapter normalize chapter_01
bookmaker chapter evaluate draft chapter_01
bookmaker chapter approve chapter_01
```

---

## 8. GitHub Issue Önerileri

Aşağıdaki başlıklar doğrudan GitHub Issues olarak açılabilir.

### Issue 1 — README.md yeniden yazılsın

**Etiket:** `documentation`, `priority-high`  
**Kabul kriterleri:**

```text
- Proje amacı açıklanmalı.
- Kurulum komutları eklenmeli.
- Mevcut pre-MVP durumu belirtilmeli.
- Örnek kullanım verilmelidir.
- Klasör yapısı açıklanmalıdır.
```

### Issue 2 — Repo hijyeni: build/debug/cache dosyaları temizlensin

**Etiket:** `repo-hygiene`, `priority-high`  
**Kabul kriterleri:**

```text
- .gitignore eklendi.
- build/ Git takibinden çıkarıldı.
- debug.log silindi.
- __pycache__ silindi.
- .class dosyaları Git takibinden çıkarıldı.
```

### Issue 3 — pyproject.toml ve paket iskeleti eklensin

**Etiket:** `packaging`, `cli`, `priority-high`  
**Kabul kriterleri:**

```text
- pip install -e . çalışıyor.
- python -m bookmaker --version çalışıyor.
- bookmaker --version çalışıyor.
```

### Issue 4 — Validator paket içine taşınsın

**Etiket:** `validator`, `refactor`  
**Kabul kriterleri:**

```text
- tools/chapter_semantic_validator.py wrapper oldu.
- src/bookmaker/chapter/validator.py eklendi.
- Mevcut sample rapor sonucu değişmedi.
```

### Issue 5 — Test fixture seti oluşturulsun

**Etiket:** `testing`, `quality-gate`  
**Kabul kriterleri:**

```text
- tests/fixtures altında en az 6 fixture var.
- pytest -q çalışıyor.
- valid sample PASS veriyor.
- hatalı fixture’lar beklenen hata kodlarını üretiyor.
```

### Issue 6 — GitHub Actions CI eklensin

**Etiket:** `ci`, `automation`  
**Kabul kriterleri:**

```text
- push ve pull_request üzerinde çalışıyor.
- pytest çalışıyor.
- ruff check çalışıyor.
- sample chapter validate ediliyor.
```

### Issue 7 — Java code extract ve smoke test CLI eklensin

**Etiket:** `java`, `code-testing`, `mvp`  
**Kabul kriterleri:**

```text
- CODE_META bloklarından code manifest üretiliyor.
- Java dosyaları build/code altına çıkarılıyor.
- javac/java ile test raporu üretiliyor.
- sample bölüm 6 pass / 3 skip / 0 fail sonucunu veriyor.
```

### Issue 8 — Markdown normalizer eklensin

**Etiket:** `markdown`, `formatter`, `authoring`  
**Kabul kriterleri:**

```text
- YAML front matter korunuyor.
- Başlıklar ve kod blokları doğru boşluklandırılıyor.
- Meta bloklar ayrı satırlara taşınıyor.
- İçerik anlamı değişmiyor.
```

---

## 9. Risk Analizi

| Risk | Olasılık | Etki | Önlem |
|---|---:|---:|---|
| Repo build çıktılarıyla şişer | Yüksek | Orta | `.gitignore`, Releases, expected fixtures |
| Validator refactor sırasında davranış bozulur | Orta | Yüksek | Önce snapshot/fixture testleri |
| LLM `CODE_META` üretimini tutarsız yapar | Yüksek | Yüksek | Metadata repair promptu + GUI form |
| Windows/OneDrive yol sorunları | Orta | Yüksek | `Path`, subprocess arg listesi, boşluklu path testleri |
| Python 3.14 bağımlılık uyumu | Orta | Orta | CI matrix 3.12/3.13/3.14 |
| Markdown line-break bozulmaları | Yüksek | Orta | `.editorconfig`, normalizer, pre-commit |
| DOCX export stil sorunları | Orta | Orta | reference.docx + Pandoc profile |
| Studio GUI’ye erken geçiş | Orta | Yüksek | Önce CLI/pipeline MVP |
| Çok fazla özellik eklenmesi | Yüksek | Yüksek | MVP kabul kriterlerini kilitle |
| Prompt dosyalarının sürüm karmaşası | Orta | Orta | `promptlar/vX_Y/` veya manifest tabanlı sürümleme |

---

## 10. Teknik Karar Önerileri

### 10.1. `bookMaker` repo adı, `bookmaker` paket adı korunmalı

Bu karar doğru:

```text
Repo adı: bookMaker
Python paket adı: bookmaker
CLI komutu: bookmaker
```

Neden?

- Python import isimlerinde küçük harf standardına uygundur.
- CLI’da kolay yazılır.
- GitHub repo adı marka olarak kalabilir.

### 10.2. `BookFactory` kodu doğrudan taşınmamalı

BookFactory güçlü bir deneyim tabanı sağlıyor; ancak `bookMaker` daha temiz çekirdek ile başlamalıdır.

Öneri:

```text
BookFactory → fikir, fixture, deneyim kaynağı
bookMaker   → temiz MVP çekirdeği
```

Kod taşınacaksa:

```text
1. Önce test altına alın.
2. Sonra sadeleştirin.
3. Sonra bookMaker modülüne taşıyın.
```

### 10.3. Studio GUI için acele edilmemeli

Studio çok değerli olacak; ancak şu sırayla ilerlemek daha güvenli:

```text
1. CLI
2. Validator
3. Java smoke test
4. DOCX export
5. Authoring state/versioning
6. Studio
```

Studio, stabil olmayan CLI üzerine kurulursa hatalar arayüzde gizlenir ve debug zorlaşır.

### 10.4. SQLite iyi fikir ama dosya sistemi ana kaynak kalmalı

`CODING_PLAN.md` içindeki hibrit yaklaşım doğru:

```text
Dosya sistemi = ana artefakt
SQLite = indeks, dashboard, hızlandırma
```

Bu korunmalıdır. SQLite bozulsa bile proje klasöründen yeniden indeks üretilebilmelidir.

---

## 11. İlk MVP İçin Keskin Kabul Kriterleri

Aşağıdaki koşullar sağlandığında `bookMaker v0.1.0 MVP` etiketi verilebilir:

```text
1. pip install -e ".[dev]" başarılı.
2. bookmaker --version çalışıyor.
3. bookmaker doctor çalışıyor.
4. bookmaker check chapter .\sample\sample_chapter.md PASS veriyor.
5. JSON ve Markdown validation raporu üretiliyor.
6. pytest -q başarılı.
7. ruff check . başarılı.
8. CODE_META bloklarından Java dosyaları çıkarılıyor.
9. Java smoke test raporu 0 failed üretiyor.
10. Tek bölüm DOCX export alınabiliyor.
11. README kurulum ve örnek kullanım içeriyor.
12. build/cache/log çıktıları Git takibinde değil.
13. GitHub Actions CI yeşil.
```

---

## 12. Önerilen İlk PR Sırası

Aynı PR içinde çok fazla şeyi değiştirmemek için şu sırayı öneririm:

```text
PR-01: README + .gitignore + .editorconfig + LICENSE
PR-02: pyproject.toml + src/bookmaker minimal iskelet + version CLI
PR-03: validator wrapper + paket içi validator + fixture testleri
PR-04: GitHub Actions CI + ruff + pytest
PR-05: Java code extract + smoke test CLI
PR-06: DOCX export MVP
PR-07: authoring workspace init komutu
PR-08: prompt package docs
```

Bu sıra hem güvenli hem de her PR’ın net bir kabul kriteri olmasını sağlar.

---

## 13. Claude/Codex ile Çalışmak İçin Önerilen Proje Talimatı

Repo köküne `CLAUDE.md` veya `AGENTS.md` eklenmesi çok faydalı olur.

Önerilen içerik:

```markdown
# bookMaker Agent Instructions

## Project Identity
bookMaker is an LLM-assisted, author-controlled, quality-gated academic and technical book authoring studio.

## Core Rules
- Keep repository name `bookMaker`; keep Python package and CLI name `bookmaker`.
- Prefer small, reviewable patches.
- Do not rewrite large Markdown files unless explicitly requested.
- Never commit generated build outputs, logs, cache files, `.class` files, or temporary DOCX/PDF outputs.
- Preserve Turkish academic writing style in documentation and prompt files.
- Use UTF-8 and Windows-compatible path handling.
- Use `pathlib.Path`; avoid shell-string command composition.
- Subprocess calls must use argument lists.

## MVP Priority
1. README and repo hygiene.
2. Python package skeleton.
3. `bookmaker check chapter` command.
4. Validator tests.
5. Java code extract and smoke test.
6. DOCX export.

## Validation Commands
```powershell
python -m pytest -q
ruff check .
bookmaker check chapter .\sample\sample_chapter.md --final
```
```

---

## 14. Sonuç

`bookMaker` güncel haliyle güçlü bir proje fikrinden çalışan bir MVP çekirdeğine doğru geçiş yapmış durumda. En değerli kazanımlar şunlardır:

```text
- Chapter semantic validator var.
- Örnek akademik/teknik Java bölümü var.
- Semantik rapor PASS 100 üretiyor.
- Java smoke test 6 pass / 3 skip / 0 fail üretiyor.
- Authoring workflow ve coding plan net.
```

Ancak proje hâlâ “kurulabilir, test edilebilir, CI ile doğrulanabilir Python paketi” aşamasına geçmemiştir. Bu nedenle en doğru kısa vadeli strateji:

```text
Önce repo hijyeni
Sonra paket iskeleti
Sonra validator testleri
Sonra Java smoke test CLI
Sonra DOCX export
Sonra authoring workflow
En son Studio GUI
```

Bu sıra izlenirse `bookMaker`, akademik ve teknik kitap üretiminde gerçekten farklılaşan, güvenilir, sürdürülebilir ve LLM modelleriyle etkili çalışabilen bir yerel üretim stüdyosuna dönüşebilir.

---

## 15. Kullanılan Kaynaklar

Aşağıdaki kaynaklar rapor hazırlanırken incelenmiştir:

1. bookMaker GitHub repo ana sayfası: `https://github.com/bmdersleri/bookMaker`
2. bookMaker commit geçmişi: `https://github.com/bmdersleri/bookMaker/commits/main/`
3. Son commit `ce3f213`: `https://github.com/bmdersleri/bookMaker/commit/ce3f21311aaf00f579a91a0d2f1a20f75d18926a`
4. `README.md`: `https://raw.githubusercontent.com/bmdersleri/bookMaker/main/README.md`
5. `CODING_PLAN.md`: `https://raw.githubusercontent.com/bmdersleri/bookMaker/main/CODING_PLAN.md`
6. `TODO.md`: `https://raw.githubusercontent.com/bmdersleri/bookMaker/main/TODO.md`
7. `CHAPTER_SPEC.md`: `https://raw.githubusercontent.com/bmdersleri/bookMaker/main/CHAPTER_SPEC.md`
8. `CHAPTER_AUTHORING_WORKFLOW.md`: `https://raw.githubusercontent.com/bmdersleri/bookMaker/main/CHAPTER_AUTHORING_WORKFLOW.md`
9. `sample/sample_chapter.md`: `https://github.com/bmdersleri/bookMaker/blob/main/sample/sample_chapter.md`
10. `tools/chapter_semantic_validator.py`: `https://github.com/bmdersleri/bookMaker/blob/main/tools/chapter_semantic_validator.py`
11. Semantic validation report: `https://raw.githubusercontent.com/bmdersleri/bookMaker/main/build/reports/chapter_semantic_report.json`
12. Java smoke test report: `https://raw.githubusercontent.com/bmdersleri/bookMaker/main/build/reports/sample_chapter_java_smoke.json`
13. Python Packaging User Guide — `pyproject.toml`: `https://packaging.python.org/en/latest/guides/writing-pyproject-toml/`
14. pytest configuration documentation: `https://docs.pytest.org/en/stable/reference/customize.html`
15. Ruff configuration documentation: `https://docs.astral.sh/ruff/configuration/`
16. GitHub Actions Python guide: `https://docs.github.com/actions/guides/building-and-testing-python`
17. Python 3.14 release information: `https://www.python.org/downloads/release/python-3140/`
