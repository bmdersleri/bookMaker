# RESUME

> **Yeni oturumda önce `SESSION.md` oku — 60 saniyede hazır olursun.**
> Bu dosya geçmiş kararların ve bağlamın arşividir; değişmez.

Bu dosya yeni bir sohbet veya sifir baglamla baslandiginda `bookMaker` projesi hakkinda bilinmesi gerekenleri ozetler.

## Kullanici Hedefi

Kullanici, LLM modellerinden maksimum duzeyde faydalanarak bilimsel ve akademik temeli olan bilisim ve veri bilimi icerikli kitaplar hazirlamak istiyor.

Istenen sistem:

- CLI ile calismali.
- Guzel ve kullanisli bir arayuzu de olmali.
- LLM saglayicisi olarak dis servisleri hedeflemeli.
- Akademik kitap uretim surecini sadece metin uretimi olarak degil, yapi, kaynak, kod, alistirma, rubrik, cikti ve kalite kontrol sureci olarak ele almali.

## Calisma Dizini ve Repo

- Calisma dizini: `D:\bookMaker`
- GitHub repo: `https://github.com/bmdersleri/bookMaker`
- Yerel remote: `origin https://github.com/bmdersleri/bookMaker.git`
- Baslangicta repo neredeyse bostu; sadece `README.md` vardi.
- Daha sonra `sample/` klasoru geldi.
- Git dal durumunda `sample/` henuz untracked gorunuyordu.

Git uyarisi:

```text
warning: unable to access 'C:\Users\ismai/.config/git/ignore': Permission denied
```

Bu uyarı `git status`, `remote`, `log` gibi komutlari engellemedi.

## Kullanici Tercihleri

- Kodlamaya baslamadan once problemi ve mimariyi tartismak istiyor.
- Tum dosyalarda UTF-8 kullanilmali.
- Sistem Windows ve PowerShell 7.x uzerinde calisiyor.
- PowerShell surumu kontrol edildi: `7.6.1`.
- Kullanici, kurulmasi gereken araclarda izin verdiginde kurulum yapilabilecegini kabul etti.

## Ortam

- OS: Windows
- Shell: PowerShell
- PowerShell: 7.6.1
- Python: 3.14.0
- Node.js: v24.11.1
- npm: 11.13.0
- Java/Javac: 17.0.10
- Pandoc: 3.9

Sandbox notu:

- Normal dosya okuma/yazma `D:\bookMaker` icinde yapilabilir.
- Winget/Scoop/AppData yollarindaki bazi araclara sandbox icinden dogrudan erisim engellenebiliyor.
- Gerektiginde tam executable yolu ve yukseltme izniyle calistirildi.

## Sample Klasoru Incelemesi

Kullanici daha once hazirladigi kitaplari anlamamizi istedi ve `sample` klasorune bakildi.

Dosyalar:

- `sample/Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.docx`
- `sample/Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.md`
- `sample/Kompakt_Bolum_16.md`

Ana bulgular:

- Kitap Java temelleri konulu, Turkce, pedagojik ve bolum sablonu duzenli bir kitap.
- Markdown kaynagi Pandoc metadata blogu ile basliyor.
- DOCX ciktisi var.
- Ana Markdown yaklasik 39.312 satir.
- 23 ana bolum ve 4 ek var.
- 251 adet kod kimligi var.
- 934 Java kod blogu var.
- 502 Markdown gorsel referansi var.
- DOCX icinde 534 medya dosyasi var.
- Her kod ornegi icin genellikle iki QR kullaniliyor: kod sayfasi ve kaynak kod.
- Mermaid diyagramlari var; final cikti icin PNG/SVG donusum ihtiyaci belirtilmis.

Tekrar eden bolum yapisi:

- Bolumun yol haritasi
- Bolumun konumu ve pedagojik rolu
- Ogrenme ciktilari
- On bilgi ve baslangic varsayimlari
- Ana kavramlar
- Konu anlatimi
- Adim adim kod ornekleri
- Kodun calisma mantigi ve beklenen cikti
- Uctan uca mini uygulama
- Sik yapilan hatalar ve yanlis sezgiler
- Hata ayiklama egzersizi
- Bolumun sonraki bolumlerle iliskisi
- Bolum ozeti
- Terim sozlugu
- Kendini degerlendirme sorulari
- Programlama alistirmalari
- Haftalik laboratuvar / proje gorevi
- Degerlendirme rubrigi
- Ileri okuma ve kaynaklar
- Bir sonraki bolume kopru

Kalite kontrol adaylari:

- Bolum 16 alt baslik numaralarinda tutarsizlik goruldu: `16.22` altinda `16.16.1` gibi.
- Bazi bolumlerde `Hata ayiklama egzersizi` tekrar ediyor olabilir.
- Markdown icindeki QR gorsel yollari `sample` icinde dosya olarak bulunmuyor, ancak DOCX icinde medya gomulu.

## Yapilan Arac Kurulumlari ve Kontroller

Ilk kontrolde:

- `fd` sandbox icinde calismadi.
- `tokei` kurulu degildi.
- `fd` sistemde kurulu oldugu ama sandbox erisim kisitina takildigi anlasildi.
- `tokei` Winget ile kuruldu.
- `rga` varsayilan config/cache konumuna erisirken sandbox icinde `Could not parse config / Erisim engellendi` hatasi verdi.
- Cozum olarak repo kokune `.rga-config.json` eklendi ve cache kapatildi.
- Sandbox icinde `rga` kullanirken `--rga-config-file=.\.rga-config.json` verilmelidir.

Kurulan ve/veya dogrulanan araclar:

- `tokei` 12.1.2
- `ImageMagick` 7.1.2-21
- `QPDF` 12.3.2
- `Vale` 3.14.1
- `lychee` 0.23.0
- `uv` 0.11.8
- `calibre` 9.8.0
- `ExifTool` 13.57
- `markdownlint-cli2` 0.22.1
- `just` 1.50.0
- `pre-commit` 4.6.0
- `mkdocs` 1.6.1
- `mkdocs-material` 9.7.6
- `actionlint` 1.7.12
- `hyperfine` 1.20.0
- `sqlite3` 3.51.3
- `playwright` 1.59.0
- Playwright Chromium browser bileseni

Zaten mevcut/dogrulananlar:

- `rga` 0.10.9
- `pandoc` 3.9
- `mmdc` 11.12.0
- `ruff` 0.15.12
- `git-lfs` 3.4.1

Son toplu arac smoke testinde 38 arac kontrol edildi ve 38/38 PASS alindi.
Sonradan SQLite ve Playwright da kuruldu. SQLite icin tablo olusturma/sorgu smoke testi, Playwright icin headless Chromium ile HTML render ve screenshot smoke testi basarili oldu.

## Onemli Tam Yollar

Bazi araclar mevcut Codex sandbox PATH'inde dogrudan gorunmeyebilir. Gerekirse tam yollar:

```text
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\sharkdp.fd_Microsoft.Winget.Source_8wekyb3d8bbwe\fd-v10.4.2-x86_64-pc-windows-msvc\fd.exe
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\XAMPPRocky.Tokei_Microsoft.Winget.Source_8wekyb3d8bbwe\tokei.exe
C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe
C:\Program Files\qpdf 12.3.2\bin\qpdf.exe
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\errata-ai.Vale_Microsoft.Winget.Source_8wekyb3d8bbwe\vale.exe
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\lycheeverse.lychee_Microsoft.Winget.Source_8wekyb3d8bbwe\lychee.exe
C:\Users\ismai\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe
C:\Program Files\Calibre2\ebook-convert.exe
C:\Users\ismai\AppData\Local\Programs\ExifTool\ExifTool.exe
C:\Users\ismai\scoop\shims\just.exe
C:\Users\ismai\.local\bin\pre-commit.exe
C:\Users\ismai\.local\bin\mkdocs.exe
```

## Uygulama Kararlari

Simdilik kabul edilen yon:

- `bookMaker`, CLI + yerel Studio arayuzu olan bir akademik kitap uretim stüdyosu olacak.
- Cekirdek mantik CLI ve GUI tarafinda ortak kullanilacak.
- Dis LLM servisleri adapter yapisiyla desteklenecek.
- Ilk LLM saglayicisi olarak OpenAI mantikli aday, ancak henuz kesin implementasyon karari verilmedi.
- Kaynak format Markdown + YAML + BibTeX olarak dusunuluyor.
- Cikti hatti Pandoc merkezli olacak.

## Javanin Temelleri Klasoru Incelemesi

Kullanici `C:\OneDrive\OneDrive - mehmetakif.edu.tr\Javanin Temelleri` klasorunun incelenmesini istedi. Bu klasor, Java kitabi icin gercek bir uretim arsivi olarak degerlendirildi.

Ana bulgular:

- Klasor, `sample/` icindeki kitabin daha kapsamli ve gercek uretim sureci izlerini tasiyan oncul projesi gibi gorunuyor.
- Onemli klasorler: `Bolumler MD`, `Bolumler DOCX`, `kodlar`, `qr_kod_sayfasi`, `qr_kaynak_kod`, `mermaid_images`, `java_temelleri_kod_entegrasyonu_v1_3`, `java_temelleri_test_pipeline`, `oto`, `out`, `promptlar`.
- Yaklasik dosya dagilimi: 2020 `.java`, 1071 `.md`, 942 `.json`, 828 `.png`, 386 `.class`, 85 `.docx`, 64 `.mmd`, 19 `.py`.
- Git remote: `https://github.com/bmdersleri/javaninTemelleri.git`.
- Git durumunda `fatal: bad object HEAD` goruldu. `HEAD`, `refs/heads/main` isaret ediyor ama commit objesi okunamiyor. OneDrive placeholder/sync veya bozuk `.git` ihtimali var.
- Nihai Markdown: `out\Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.md`.
- Bu dosya yaklasik 39.313 satir, 23 bolum, 4 ek, 251 kod ID, 934 Java kod blogu, 28 Mermaid blogu ve 502 gorsel referansi iceriyor.
- `code_manifest_with_dual_qr.json` icinde 251 kayit var.
- `java_temelleri_kod_entegrasyonu_v1_3\code_manifest_github_linkleri_revize.json` icinde 312 kayit var.
- `kodlar` klasoru 23 `bolumXX` alt klasoru, 543 `.java`, 454 `.md`, 1 `.json` iceriyor.
- `qr_kod_sayfasi` ve `qr_kaynak_kod` klasorlerinde 251'er PNG var.
- `java_temelleri_kod_entegrasyonu_v1_3` kod bloklarini cikarma, kod sayfalari uretme, QR placeholder/PNG uretme ve Markdown link patch etme araclarini iceriyor.
- `java_temelleri_test_pipeline` Markdown'dan Java kodlarini cikarip `javac` ile derleyen ve raporlayan bir test hattina sahip.
- Son test raporunda 20 ornek test edilmis, 2 gercek derleme hatasi gorulmus: `KOD_04_016`, `KOD_05_038`.
- `donustur.bat` v18 DOCX hattinda UTF-8 `chcp 65001`, Mermaid cikarma/render ve Pandoc + reference DOCX + Lua filter kullaniyor.

Bu klasor, `bookMaker` icin dogrudan fixture/oncul uretim modeli olarak ele alinmali: kod manifesti, QR ciftligi, Mermaid donusumu, Pandoc DOCX hatti ve Java kod test pipeline'i genellestirilebilir.

## BookFactory Klasoru Incelemesi

Kullanici `C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory` klasorunu dikkatli incelememi istedi. Kod degisikligi yapilmadi; amac mevcut oncul sistemi ve bilesenlerini anlamakti.

### Genel Kimlik

- Proje adi dokumanlarda **Parametric Computer Book Factory** olarak geciyor.
- README tanimi: manifest tabanli, LLM destekli, kod dogrulamali ve GUI destekli teknik kitap uretim framework'u.
- README ve `bookfactory/__init__.py` surumu `4.1.0`.
- `dev/pyproject.toml` surumu `4.1.0`.
- Studio ana kullanma yolu olarak konumlanmis; varsayilan adres `http://127.0.0.1:8765`.
- Iki katmanli mimari benimsenmis:
  - Framework reposu: CLI, Studio, tools, schema, templates, kalite ve post-production araclari.
  - Kitap reposu: belirli kitap projesinin `book_manifest.yaml`, `chapters/`, `prompts/`, `assets/`, `build/`, `exports/` klasorleri.

Temel uretim akisi:

```text
Kitap fikri
  -> Manifest
  -> Bolum girdi promptlari
  -> Bolum tam metinleri
  -> Markdown kalite kontrolu
  -> CODE_META cikarimi ve kod testleri
  -> Mermaid / screenshot / QR uretimi
  -> GitHub sync / code pages / Codespaces kontrolu
  -> Export: Markdown / DOCX / HTML / EPUB / PDF
```

### Repo ve Calisma Agaci Durumu

- BookFactory klasoru OneDrive altinda bir reparse/sync path olarak gorunuyor.
- Git branch: `v3.2-stabilization-cli`.
- Worktree oldukca kirli: cok sayida modified/deleted/untracked dosya var.
- Root `pyproject.toml`, `requirements.txt`, `CHANGELOG.md`, `PROJECT_BRIEF.md`, `SETUP.md`, `schemas/` gibi bazi dosyalar silinmis gorunuyor; bunlarin bir kismi `dev/` altina tasinmis olabilir.
- Yeni veya tasinmis yapilar: `core/configs/`, `core/schemas/`, `dev/`, `templates/manifests/`, `scripts/run_studio.*`, `tests/e2e/`.
- Bazi `pytest-cache-files-*` klasorlerine erisim engeli goruldu.
- Git yine `C:\Users\ismai/.config/git/ignore` icin izin uyarisi veriyor.

### Ana Bilesenler

- `bookfactory/`: Ana CLI paketi.
- `bookfactory/cli.py`: CLI orkestratoru. Komutlari `tools/` altindaki scriptlere dagitiyor.
- `bookfactory/commands/init.py`: Yeni kitap projesi olusturma/scaffold araci.
- `bookfactory_studio/`: FastAPI tabanli Studio GUI.
- `bookfactory_studio/static/`: Tek sayfa arayuz: `index.html`, `app.js`, `styles.css`.
- `bookfactory_studio/services/`: Studio servis katmani.
- `tools/`: Kod, kalite, post-production, export, GitHub, cloud, indexing, memory/RAG araclari.
- `core/`: LLM sozlesmeleri, standartlar, politikalar ve semalar.
- `templates/`: Manifest, reference DOCX, Lua filter, HTML/EPUB CSS, cloud/Codespaces sablonlari.
- `docs/briefs/`: LLM icin yukleme sirasi, proje kurallari ve standartlar.
- `tests/`: CLI smoke, Studio GUI ve E2E testleri.

### CLI Komutlari

`bookfactory.cli` icinde gorulen ana komutlar:

- `version`
- `init`
- `doctor`
- `validate`
- `build`
- `extract-code`
- `validate-code-meta`
- `test-code`
- `repair-prompts`
- `sync-github`
- `qr-from-code`
- `render-code-pages`
- `export`
- `build-index`
- `codespaces-init`
- `codespaces-check`
- `dashboard`

CLI, `FRAMEWORK_ROOT = Path(__file__).resolve().parent.parent` ile framework kokunu cozuyor. `run_python()` araclari in-process calistirmayi destekliyor, `BOOKFACTORY_SUBPROCESS_MODE=1` ile subprocess modu var.

### Studio GUI

Studio, FastAPI uygulamasi olarak `bookfactory_studio/app.py` icinde. Ana ekranlar:

- Dashboard
- Kontrol Paneli
- Kitap Sihirbazi
- Manifest
- Bolumler
- Production
- Raporlar
- GitHub & Cloud
- Medya Kutuphanesi

Studio servisleri:

- `ManifestService`: Manifest okuma, normalizasyon, dogrulama, bolum dosyasi cozumleme.
- `PathService`: Framework koku ve kitap koku ayrimi, guvenli path cozumleme.
- `HealthService`: Control panel snapshot, raporlar, kod testleri, screenshot ve export durumu.
- `PromptService`: Adaptif prompt uretimi ve prompt fragmentlerini birlestirme.
- `AssetService`: Gorsel ve veri seti yukleme/listeleme.
- `CloudService`: `.devcontainer` ve GitHub Actions sablonlarini kitap projesine ekleme.
- `CodeService`: CODE_META icindeki belirli kod blogunu bulma ve guncelleme.

### Bolum Muhendisligi Notu

BookFactory icindeki `azar.txt` dosyasi cok onemli bir kullanici geri bildirimi iceriyor. Ana fikir:

- Arayuzun en onemli bolumu kitap bolumlerinin hazirlandigi bolumdur.
- Bolumlerin hatasiz hazirlanabilmesi icin `chapter_input` promptu eksiksiz ve bolume ozel olmali.
- Kullanici bolum amaci, hedef kitle, on kosullar, zorunlu kavramlar, kod/gorsel varliklar, mini uygulama, kapsam disi konular ve kaynak politikasi gibi alanlari dogrudan girebilmeli.
- Bu alanlar doldurulurken LLM tarafindan ipuclari uretilebilmeli.
- Sonra LLM once sadece outline uretmeli.
- Arayuzde LLM outline'inin yapistirilacagi/duzenlenecegi alan olmali.
- Outline kalite ve uygunluk acisindan test edilmeli, puan ve geri bildirim verilmeli.
- Kullanici bu geri bildirimle LLM'e donmeli ve nihai tam metin uretmeli.

Studio'da bunun kismi uygulamasi var:

- `Bölüm Stüdyosu` sekmeleri: `Girdi (Brief)`, `Taslak (Outline)`, `Değerlendirme`, `Tam Metin`.
- Brief alanlari: bolum amaci, zorunlu kavramlar, zorunlu kod ornekleri, gorsel/diyagram plani.
- Outline alani ve basit kalite kontrol butonu var.
- Tam metin tarafinda Markdown editor, preview ve CODE_META wizard var.

Ancak backend tarafinda ipucu uretimi su an gercek LLM entegrasyonu degil; daha cok stub/sablon. Outline kalite kontrolu de yuzeysel kurallara dayaniyor.

`bookMaker` icin en kritik tasarim dersi: urunun kalbi manifest editoru degil, `chapter_input -> outline -> evaluation -> full text -> quality gates` dongusu olmali.

### Tools Katmani

`tools/` altinda gorulen kategoriler:

- `tools/code`: CODE_META cikarimi, dogrulama, kod testleri, repair promptlari.
- `tools/code/language_adapters`: Java, Python, JavaScript test adapterleri.
- `tools/postproduction`: merge, Mermaid, QR, asset resolve, Pandoc, DOCX fix, table optimize, syllabus, index, website.
- `tools/export`: Markdown/HTML/EPUB/DOCX/PDF/site export.
- `tools/github`: Kod repo sync, code pages, GitHub Pages setup.
- `tools/cloud`: Codespaces ve cloud kontrolleri.
- `tools/quality`: Bolum Markdown kalite kontrolu, semantic consistency, editor promptlari.
- `tools/memory`: RAG/context memory.
- `tools/indexing`: Glossary ve index uretimi.
- `tools/utils`: YAML/JSON, path ve process yardimcilari.

Kod test akisi:

- `extract_code_blocks.py` sadece `CODE_META` ile isaretli fenced code bloklarini cikarir.
- JSON ve YAML code manifest uretir.
- `run_code_tests.py` manifestteki itemlari Java/Python/JavaScript adapterlerine dagitir.
- Java adapter `javac -encoding UTF-8` ve `java -Dfile.encoding=UTF-8` kullaniyor.

Post-production akisi:

- `post_production_pipeline.py` su stage'leri orkestre ediyor: `validate`, `merge`, `prepare-mermaid`, `render-mermaid`, `generate-qr`, `resolve-assets`, `inject-qr`, `pandoc`, `fix-docx`, `optimize-tables`, `generate-syllabus`, `generate-indexing`, `generate-web-site`.
- `export_book.py` Markdown, HTML, EPUB, DOCX, PDF ve split site ciktilarini destekliyor.

### Core ve Prompt Standartlari

`core/` altinda LLM ve uretim politikalarini tarif eden belgeler var:

- LLM execution contract
- Manifest schema
- General system prompt
- Output format standard
- Chapter structure standard
- Chapter input generator prompt
- Outline review prompt
- Full text generation prompt
- Quality gate contract
- Manual asset override policy
- Multilingual policy
- Approval gate policy
- Project starter prompt
- Post-production pipeline standard
- DOCX build policy
- Generated package protocol
- Editor review prompt

Onemli ilkeler:

- Manifest tek dogruluk kaynagidir.
- LLM manifestte olmayan bolum/asset/kaynak uydurmamali.
- Cikti karar formati: `PASS`, `REVISION_REQUIRED`, `BLOCKED`.
- Manuel numaralandirma yapilmamali; numaralandirma build-time atanir.
- Uydurma API, kaynak veya teknik bilgi yazilmamali.
- Approval gate'ler kullanilmali.

### Semalar ve Sablonlar

- `core/schemas/book_manifest_schema.json`
- `core/schemas/code_meta_schema.json`
- `core/schemas/manifest_minimum_required_fields.json`
- `templates/manifests/book_manifest.yaml`
- `templates/reference_docs/referenceV17_java_temelleri.docx`
- `templates/lua_filters/styles_revised_v17.lua`
- `templates/export/html/bookfactory.css`
- `templates/export/epub/epub.css`
- `templates/cloud/.devcontainer/devcontainer.json`
- `templates/cloud/.github/workflows/deploy_pages.yml`
- `templates/cloud/.github/workflows/validate_book.yml`

### Testler ve Beklenen Davranis

Testler sunlari dogrulamayi hedefliyor:

- CLI parser komutlari.
- `python -m bookfactory version`.
- Paket version metadata tutarliligi.
- Console script entry pointleri.
- Studio health endpoint.
- Static shell icinde `app.js` ve `styles.css`.
- Manifest parse/render round trip.
- Pipeline step listesi.
- Studio frontend tarafindaki DOM ID'lerin HTML'de bulunmasi.
- Control panel snapshot'in uretim artefaktlarini okuması.
- E2E minimal pipeline: init, validate, CODE_META ile bolum ekleme, test-code, export.

Not: Bazi testler mevcut koda gore stale veya kirik olabilir. Ornegin testler `/api/project` route'unu bekliyor ama `app.py` icinde bu route gorunmedi.

### Gorulen Riskler ve Tutarsizliklar

- `bookfactory/__init__.py` ve `dev/pyproject.toml` surumu `4.1.0`, fakat `bookfactory/commands/init.py` icinde `FRAMEWORK_VERSION = "v3.5.0"`.
- Studio frontend `/api/project` cagiriyor ve testler de bekliyor; `app.py` icinde bu route gorunmedi.
- `app.py` icinde `/api/reports` iki kez tanimli.
- `app.py` icinde `datetime.now()` kullaniliyor ama `datetime` import edilmemis gorunuyor.
- `app.py` icinde `CodeService` kullaniliyor ama import edilmemis gorunuyor.
- `tools/code/run_code_tests.py` icinde `re.compile` kullaniliyor ama `import re` yok.
- CODE_META dokuman ve testlerinde `expected_output` geciyor; extractor ve adapter tarafinda asil beklenen alan `expected_stdout_contains`. Bu, beklenen cikti dogrulamasini sessizce etkisiz birakabilir.
- Root `pyproject.toml` ve bazi temel dosyalar silinmis/tasinmis gorunuyor; aktif repo stabil bir release degil, reorganization halinde.
- OneDrive/reparse path ve cache klasorleri izin/placeholder problemleri uretebilir.
- Git worktree kirli oldugu icin BookFactory dogrudan referans alinirken once stabilize edilmeli.

### bookMaker Icin Cikarim

BookFactory'den alinmasi gereken ana fikirler:

- Manifest tek dogruluk kaynagi.
- Framework koku ile kitap koku ayrimi.
- CLI ve GUI ayni cekirdek fonksiyonlari kullanmali.
- `CODE_META` ile kod bloklari test edilebilir olmali.
- Java/Python/JavaScript gibi diller adapter modeliyle test edilmeli.
- Mermaid, QR, screenshot, asset override ve Pandoc export hatti genellestirilmeli.
- Production adimlari job/log/report modeliyle izlenmeli.
- LLM kurallari, promptlar ve kalite kapilari repo icinde versionlanmali.

Ancak `bookMaker` icin oncelik BookFactory'den farkli kurulmalı:

1. Once kitap ve bolum uretim surecinin pedagojik/akademik modeli netlestirilmeli.
2. Manifest editorunden once veya en az onun kadar guclu bir `Bolum Muhendisligi` modulu tasarlanmali.
3. Her bolum icin zengin `chapter_input` modeli olmali:
   - manifest identity
   - chapter purpose
   - audience and prerequisites
   - mandatory concepts
   - required code/application assets
   - required diagram/visual/screenshot assets
   - mini application / chapter task
   - out-of-scope topics
   - source policy
   - outline generation instruction
   - full-text generation note
4. LLM dis servis entegrasyonu bu donguye yerlestirilmeli:
   - ipucu uret
   - outline uret
   - outline'i puanla
   - revizyon geri bildirimi uret
   - tam metin uret
   - tam metni kalite kapilarindan gecir
5. BookFactory kodu dogrudan kopyalanmadan once bu riskler temizlenmeli veya `bookMaker` icin daha kucuk, temiz bir cekirdek tasarlanmalı.

## Son Durum

Bu dosyalar kullanici istegiyle olusturuldu:

- `TODO.md`: yapilacaklar ve urun/teknik plan
- `RESUME.md`: yeni sohbette bilinmesi gerekenler
- `WORKSPACE.md`: sistem imkanlari ve arac envanteri
- `CHAPTER_SPEC.md`: bolum Markdown dosyasinin semantik ve teknik sozlesmesi
- `CHAPTER_AUTHORING_WORKFLOW.md`: bolum yazim, manuel LLM, kalite kapilari, revizyon paketi ve surumleme workflow'u
- `tools/chapter_semantic_validator.py`: bolum sozlesmesi icin ilk deterministik validator

Ilk kodlama adimi basladi. Bu asamada amac ortam, araclar, sample kitap yapisi, bolum sozlesmesi, validator ve urun hedefini netlestirmekti.

### 2026-05-03 Urun Kararlari

Ana urun hedefi:

- Yazarın uretim hizini artirmak.
- Hatalari mumkun oldugunca otomatik tespit etmek.
- LLM ciktisini dogrudan kabul etmeden standartlara ve kalite kapilarina gore puanlamak.
- Eksikleri yazara net gostermek.
- Eksikleri LLM'e kolayca aktarilabilecek revizyon paketlerine donusturmek.
- Standartlari karsilayan kaliteli akademik/teknik icerik uretimini sistematik hale getirmek.

LLM calisma karari:

- Ana ve varsayilan akış manuel copy/paste olacak.
- Sistem API entegrasyonu hic olmayacakmis gibi calismali.
- Yazar promptu `bookMaker`dan kopyalar, istedigi LLM arayuzune yapistirir, ciktıyı `bookMaker`a geri yapistirir.
- API adapterleri gelecekte opsiyonel olarak eklenebilir, fakat MVP ve cekirdek pipeline API'ye bagimli olmayacak.

Arayuzde ana eylemler:

```text
Promptu Olustur
Promptu Kopyala
LLM Yanitini Yapistir
Yanitı Dogrula
Revizyon Paketi Olustur
Revizyon Promptunu Kopyala
Tekrar Degerlendir
Onayla
```

Revizyon paketi karari:

- Kalite raporundaki her eksik/hata `issue` olarak saklanmali.
- Her issue `id`, `severity`, `type`, `location`, `expected`, `current`, `instruction`, `acceptance_criteria` alanlarini tasimali.
- Dusuk skor veya eksik tespitinde sistem kopyalanabilir revizyon promptu uretmeli.
- Revizyon sonrasi ayni issue'lar tekrar kontrol edilmeli.

Surum kontrol karari:

- Uretilen bolumlerde uygulama ici surum kontrol sistemi olmali.
- Yazar yapilan degisiklikleri takip edebilmeli, surumler arasindaki farklari gorebilmeli ve onceki surume donebilmeli.
- Eski surumler degistirilmemeli; geri alma islemi eski surumu ezmek yerine ondan yeni aktif surum uretmeli.
- Surumlenecek artefaktlar: `chapter_seed`, `outline_prompt`, `outline_candidate`, `outline_quality_report`, `revision_packet`, `full_text_prompt`, `full_text_candidate`, `full_text_quality_report`, `approved_chapter`, `code_test_report`, `asset_report`.
- Her bolum workspace'i `version_log.jsonl` ve `active_version.yaml` gibi izleme dosyalari tasimali.
- GUI'de `Surum Gecmisi`, `Fark Goruntuleme`, `Bu surume don`, `Bu surumden revizyon promptu uret` eylemleri olmali.
- Git proje geneli snapshot/paylasim/yedekleme icin kullanilabilir; GUI geri alma islemleri Git komutlarina bagimli olmamali.
- Kullanici onayi olmadan otomatik commit veya push yapilmamali.

### 2026-05-03 Chapter Authoring Workflow Notu

`CHAPTER_AUTHORING_WORKFLOW.md` olusturuldu.

Belge sunlari tanimliyor:

- Hedef cikti: `sample/sample_chapter.md` kalitesinde `CHAPTER_SPEC.md` uyumlu bolum.
- Artifact sozlugu: seed, prompt, LLM response, quality report, revision packet, normalized chapter, approved chapter, technical reports.
- Durum makinesi: `planned`, `seeded`, `outline_prompt_ready`, `outline_pasted`, `outline_reviewed`, `outline_approved`, `full_text_prompt_ready`, `full_text_pasted`, `normalized`, `full_text_reviewed`, `full_text_approved`, `technical_check_passed`, `approved`, `ready_for_export`.
- Adimlar: bolum secimi, tohumlama, outline prompt, outline paste, outline kalite, revizyon dongusu, outline onayi, tam metin prompt, tam metin paste, normalize, tam metin kalite, teknik kontrol, bolum onayi, surum gecmisi.
- GUI modeli: sol bolum listesi, orta aktif is/editör, sag kalite raporu/issue/surum ozeti.
- CLI karsiliklari: `bookmaker chapter ...` ve `bookmaker version ...` komut taslaklari.
- Kalite kapilari ve acik kararlar.

### 2026-05-03 Workflow Hizlandirma Kararlari

Yazar hizini artirmak icin workflow'a eklenen ilkeler:

- Bolum tohumlama ekrani bos form olarak acilmayacak; `book_profile`, `book_architecture`, onceki bolumler ve kitap turu presetlerinden akilli on doldurma yapacak.
- Outline, tam metin, revizyon ve repair promptlari tek tikla uretilip kopyalanabilecek.
- LLM ciktisi yapistirildigi anda otomatik on analiz calisacak: baslik hiyerarsisi, zorunlu bloklar, CODE_META, MERMAID_META, kapsam sinyalleri, eksik kavramlar.
- Yazar metadata YAML yazmak zorunda kalmayacak; `CODE_META`, `MERMAID_META`, `SCREENSHOT_META` gibi alanlar form panelinden duzenlenecek.
- Guvenli normalize adimi olacak: gorunur `Kod 1` basliklarini duzeltme, fazla bosluklari temizleme, eksik front matter onermek, somut `code_id` uretmek, `paired_with` adaylari onermek.
- Dusuk skor veya eksik durumunda sistem issue listesini otomatik gruplar ve tek tikla revizyon paketi uretir.
- Kisayol is akislari olacak: `Outline'i Degerlendir ve Revizyon Paketi Hazirla`, `Tam Metni Normalize Et ve Kontrol Et`, `Teknik Kontrolleri Calistir`, `Onaya Hazirla`.
- Kitap turu presetleri olacak: Java/programlama, veri bilimi, web gelistirme, akademik ders kitabi, laboratuvar kitabi.
- Surum karsilastirma karar destegi sunacak: skor degisimi, cozulmus issue sayisi, yeni issue sayisi, diff, teknik test durum degisimi.
- Dashboard kitap genelinde planlanan/tohumlanan/onaylanan/bloklu bolumleri, ortalama kalite skorunu ve en sik issue tiplerini gosterecek.
- Arayuz her durumda tek bir "sonraki en mantikli is" onerecek.

### 2026-05-03 CODE_META LLM Ciktisi Karari

Kabul edilen karar:

- Kod metadata verileri sonradan sadece sistem tarafindan gizli olarak uretilmeyecek; LLM'den gelen tam metin Markdown ciktisinin icinde bulunacak.
- Tam metin promptu LLM'den her ilgili kod blogundan hemen once `CODE_META` uretmesini acikca istemeli.
- `CODE_META` kod fence icine yazilmayacak ve kod blogundan sonra gelmeyecek.
- Gerekli alanlar en az `code_id`, `extension`, `kind`, `title`, `file`, `main_class`, `link`, `qrfile`, `extract`, `test`, `github`, `qr_policy`, `intentional_mismatch`, `validation_mode` olacak.
- Bilerek hatali orneklerde `kind: broken_example`, `intentional_mismatch: true`, `validation_mode: review_only`, `test: skip`, `mismatch_*`, `expected_outcome` ve `paired_with` kullanilacak.
- Duzeltilmis karsiliklarda `kind: fixed_example`, `paired_with` ve `intentional_mismatch: false` bulunacak.
- Gelistirilecek sistem, LLM ciktisi yapistirildigi anda `CODE_META` varligini, yerini, zorunlu alanlarini, kod ile tutarliligini ve `intentional_mismatch` iliskilerini otomatik kontrol edecek.
- Eksik veya hatali `CODE_META`, onay engeli olan issue olarak raporlanacak; sistem aday metadata veya metadata repair paketi uretebilir, fakat kabul icin kullanici onayi ve validator gecisi gerekir.

### 2026-05-03 Coding Plan Kararlari

`CODING_PLAN.md` olusturuldu ve kodlamaya baslarken ana teknik taslak olarak kabul edildi.

Kilitlenen kararlar:

- Hedef Python surumu: Python 3.14.
- Python paketi ve CLI komutu: `bookmaker`.
- Runtime durum modeli: dosya sistemi + SQLite hibriti.
- Ilk desteklenecek kitap profili: Java Temelleri / Java programlama kitabi.
- Ilk export hedefi: DOCX.
- PDF, EPUB, MkDocs ve HTML sonraki faz hedefleri olacak.
- Ilk Studio frontend sade HTML/CSS/JS + FastAPI olacak; React/Vite ilk MVP'ye alinmayacak.
- Ilk kodlama baslangici: `pyproject.toml`, `src/bookmaker` iskeleti, `bookmaker --version`, temel Pydantic modeller, UTF-8 dosya helperlari ve pytest smoke.

### 2026-05-03 Chapter Spec Notu

`sample/sample_chapter.md` dosyasi bolum uretim hatti icin referans ornek olarak incelendi ve semantik olarak daha makine-okunur hale getirildi.

Yapilan duzenlemeler:

- `CODE_META` icine `intentional_mismatch`, `mismatch_kind`, `mismatch_summary`, `expected_outcome`, `paired_with`, `validation_mode` alanlari eklendi.
- Bilerek hatali kodlar `validation_mode: review_only` olarak isaretlendi.
- Normal kodlar `runnable`, interaktif mini uygulama `compile_only` olarak isaretlendi.
- Hatalı/düzeltilmiş kod çiftleri `paired_with` ile baglandi.
- Mermaid blogu `MERMAID_META` ile isaretlendi.
- `Gövde Metni` icin `section_type: body_group` eklendi.
- `SECTION_META` order tekrarları temizlendi.
- Rubrik icin ayri `SECTION_META` eklendi.
- Düzeltilmiş Java örneklerinde `file` ile `public class` uyumu saglandi.
- Final kaynakta elle duran `BÖLÜM SONU` etiketi kaldirildi.

Kuru kontrolde:

- `SECTION_META` sirasi `001-017` araliginda benzersiz.
- Mermaid blogu ve `MERMAID_META` sayisi uyumlu.
- `runnable` ve `compile_only` Java kodlarinda dosya adi ile `public class` adi uyumlu.
- `DIAGRAM_META`, `extention` ve `BÖLÜM SONU` gibi yasak/eski isaretler kalmadi.

### 2026-05-03 Chapter Semantic Validator Notu

`tools/chapter_semantic_validator.py` eklendi.

Calistirma:

```powershell
python .\tools\chapter_semantic_validator.py .\sample\sample_chapter.md
```

Varsayilan raporlar:

- `build/reports/chapter_semantic_report.json`
- `build/reports/chapter_semantic_report.md`

Son calisma sonucu:

```text
PASS score=100 errors=0 warnings=0
```

Validator ilk surumde sunlari kontrol ediyor:

- YAML front matter zorunlu/onerilen alanlari.
- Tek H1 baslik ve manuel numaralandirma kullanimi.
- Yasak/eski isaretler: `DIAGRAM_META`, `extention`, `BÖLÜM SONU`.
- `SECTION_META` order tekrarları, siralama ve baslik uyumu.
- `CODE_META` zorunlu alanlari.
- `intentional_mismatch` ve `validation_mode` tutarliligi.
- `paired_with` hedeflerinin varligi.
- `runnable` ve `compile_only` Java kodlarinda dosya adi / `public class` uyumu.
- Mermaid blogu ve `MERMAID_META` eslesmesi.
- `--final` modunda cozulmemis placeholder kontrolu.

### 2026-05-03 Canonical sample_chapter Notu

`sample/sample_chapter.md` dosyasi daha kanonik ve semantik olarak kolay islenebilir hale getirildi.

Yapilan ek duzenlemeler:

- `processing_stage: authoring_source`, `chapter_spec`, `placeholder_policy`, `snippet_policy` front matter alanlari eklendi.
- `Gövde Metni` artik gorunur `## Gövde Metni` basligi ile basliyor; alt anlatim basliklari `###/####` duzeylerine indirildi.
- Gorunur `Kod 1`, `Kod 2`, `Kod 3` numaralari kaldirildi; kod sirasi sadece `CODE_META.order` icinde tutuluyor.
- Sabit bolum numarasi referanslari kaldirildi; onceki/sonraki bolumler kavramsal ifadelerle anlatiliyor.
- `code_id` ve `paired_with` alanlari somut degerlere cevrildi.
- `CODE_META` bloklarina `kind`, `main_class`, `extract`, `test`, `github`, `qr_policy`, `expected_stdout_contains` alanlari eklendi.
- `Csv...`, `Hatasi`, fazla baslik boslugu, `Diyagram :`, `kayitleri` gibi yazim/tutarlilik problemleri temizlendi.

Son dogrulamalar:

```text
python .\tools\chapter_semantic_validator.py .\sample\sample_chapter.md
PASS score=100 errors=0 warnings=0
```

Java smoke sonucu:

```text
total=9 passed=6 skipped=3 failed=0
```

Mermaid render:

- `build/reports/dosya_islemleri_diagram_001.png` uretildi.

Not: Mermaid CLI sandbox icinde Chromium/Puppeteer baslatamadigi icin `mmdc` komutu onayli/escalated calistirildi.

## Sonraki Mantikli Adim

Kullanici kodlamaya gec derse, once asagidaki kararlar netlestirilmeli:

- Ilk sonraki adim validator test fixture'lari mi olacak, yoksa proje/paket iskeleti mi baslatilacak?
- Python paket/CLI adi ne olacak?
- OpenAI entegrasyonu ilk MVP'ye dahil mi?
- GUI ilk MVP'de sadece proje/bolum goruntuleme mi yapacak, yoksa LLM gorevi de calistiracak mi?
