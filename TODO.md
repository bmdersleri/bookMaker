# TODO

Bu dosya `bookMaker` projesinde kodlamaya gecmeden once netlestirilen hedefleri ve yapilacak isleri tutar.

Bu dosya ve `RESUME.md`, sonraki oturumlarda kaldigimiz yeri hizli sekilde geri yuklemek icin ana referanslardir.

## 1. Urun Hedefi

`bookMaker`, LLM modellerinden maksimum duzeyde faydalanarak bilimsel ve akademik temeli olan bilisim, programlama ve veri bilimi kitaplari hazirlamak icin gelistirilecek bir arac/studyo olacaktir.

Hedef tek basina metin ureten bir sistem degildir. Sistem kitap uretim surecini asagidaki eksenlerde yonetmelidir:

- Akademik ve pedagojik yapi
- Bolum, konu, ogrenme ciktisi ve alistirma organizasyonu
- `CHAPTER_SPEC.md` ile tanimli, semantik olarak dogrulanabilir bolum Markdown sozlesmesi
- `CHAPTER_AUTHORING_WORKFLOW.md` ile tanimli bolum yazim, revizyon, kalite kapisi ve surumleme akisi
- Kaynak, atif, ileri okuma ve bibliyografya yonetimi
- Kod ornegi, calistirilabilir uygulama, QR ve GitHub baglantisi yonetimi
- Kodlara GitHub reposu uzerinden kolay erisim
- GitHub Pages uyumlu kod sayfalari ve yayin ciktilari
- Diyagram, gorsel ve tablo uretim hatti
- Markdown tabanli kaynak metinden DOCX, PDF, EPUB, MkDocs ve HTML gibi yayin ciktilari
- CLI ve yerel web tabanli Studio arayuzu
- Manuel copy/paste odakli LLM calisma modeli
- Ileride eklenebilecek opsiyonel LLM API adapter mimarisi

## 1.1. Guncel Hedef Tanimi

`bookMaker`in temel amaci, yazarin LLM ile daginik sohbetler yaparak kitap uretmesi yerine, kitap yazim surecini asamali, denetlenebilir, tekrar uretilebilir ve kalite kapilariyla yonetilen bir otomasyona donusturmektir.

Ana hedef:

```text
Kolay kullanilan yazar arayuzu
+ kontrollu LLM promptlari
+ kullanici onayi
+ otomatik kalite kontrol
+ skor tabanli geri bildirim
+ teknik uretim/export hatti
= yuksek kaliteli akademik/teknik kitap uretimi
```

Urunun ayirt edici degeri:

- LLM'i yazarin yerine gecen kontrolsuz bir metin makinesi olarak degil, yazarin denetiminde calisan akademik uretim asistani olarak konumlandirmak.
- Her LLM ciktisini arayuze alarak puanlamak, eksiklerini gostermek ve onaydan sonra sonraki asamaya gecirmek.
- Kitap profili, kitap mimarisi, bolum tohumu, outline ve tam metni ayri ayri versionlamak.
- Yazim surecini teknik post-production hattindan ayirmak, fakat ikisini ayni pipeline modeliyle baglamak.
- GUI ile kolay kullanimi, CLI ile otomasyonu ayni cekirdek modele baglamak.

## 1.1.1. Urun Felsefesi: Hiz + Kalite Kapilari

`bookMaker`in asil amaci yalnizca daha hizli metin uretmek degildir. Sistem yazarin uretim hizini artirirken hatalari en aza indirmeli, hatalari otomatik tespit etmeli ve mumkun oldugunca standartlari karsilayan kaliteli icerik uretimini saglamalidir.

Temel prensip:

```text
Yazar hizli ilerler
+ sistem standartlari uygular
+ validator ve teknik testler hatalari yakalar
+ eksikler revizyon paketine donusur
+ onayli icerik kalite kapilarindan gecerek olusur
```

Bu nedenle:

- Yazar bos sayfa ile baslamaz; formlar, sablonlar ve promptlar tarafindan yonlendirilir.
- LLM ciktisi dogrudan kabul edilmez; her cikti olculur, raporlanir ve kullanici onayindan gecer.
- Hatalar mumkun oldugunca deterministik araclarla yakalanir.
- Deterministik araclarin yakalayamadigi pedagojik/semantik kalite sorunlari kalite raporu ve kullanici onayi ile ele alinir.
- Her hata, hem yazara okunabilir hem de LLM'e aktarilabilir acik bir issue olarak saklanir.
- Revizyon promptlari otomatik uretilir.
- Onayli bolum, standart, kalite skoru ve kullanici onayini birlikte sagladiginda olusur.

## 1.2. Ana Tasarim Ilkeleri

- **Yazar merkezli arayuz:** Yazar dosya yapisi, komutlar ve prompt muhendisligiyle bogusmamali. Arayuz her adimda yazara yalnizca o anda gerekli kararlari gostermeli.
- **Manifest tek dogruluk kaynagi:** Kitap kimligi, kapsam, bolumler, hedef kitle, kalite kapilari ve cikti ayarlari manifestlerden beslenmeli.
- **Bolum sozlesmesi net olmali:** `sample/sample_chapter.md` gibi bolumler `CHAPTER_SPEC.md` kurallarina gore uretilmeli; `SECTION_META`, `CODE_META`, `MERMAID_META`, `intentional_mismatch` ve `validation_mode` alanlari makine tarafindan dogrulanabilmeli.
- **CODE_META LLM ciktisinin parcasi olmali:** Tam metin promptu LLM'den kod bloklarindan hemen once `CODE_META` uretmesini istemeli; sistem yapistirma sonrasi bu metadata'yi otomatik parse, validate ve skorlamalidir.
- **Bolum yazim workflow'u net olmali:** Tohumdan onayli bolume kadar her adim `CHAPTER_AUTHORING_WORKFLOW.md` icindeki artifact, gate, revizyon ve surumleme kurallarina uymali.
- **Pipeline tabanli surec:** Kitap uretimi sabit butonlar toplulugu degil, tanimli adimlar, girdiler, ciktilar ve kalite kapilarindan olusan bir durum makinesi olmali.
- **LLM ciktisi dogrudan kabul edilmemeli:** Outline, tam metin, kod, alistirma ve kaynak onerileri kalite kontrolu ve kullanici onayindan gecmeden onayli icerik sayilmamali.
- **Kalite olculebilir olmali:** Her onemli asamada 100 uzerinden skor, karar, eksik oge listesi ve revizyon onerisi uretilmeli.
- **Revizyon dongusu birinci sinif kavram olmali:** Sistem sadece ileri akan bir workflow degil, outline ve tam metin icin tekrarlanabilir revizyon donguleri sunmali.
- **Manuel LLM copy/paste ana akistir:** Sistem API entegrasyonu hic olmayacakmis gibi calismali. Yazar promptu kopyalar, istedigi LLM arayuzune yapistirir, ciktıyı `bookMaker`a geri yapistirir.
- **API adapterleri opsiyoneldir:** Gelecekte OpenAI, Anthropic, Gemini, OpenRouter veya yerel LLM adapterleri eklenebilir; ancak cekirdek pipeline buna bagimli olmayacak.
- **Revizyon paketi birinci sinif kavram olmali:** Dusuk skor veya eksik tespit edildiginde sistem eksikleri LLM'e kolayca aktarilabilecek hedefli revizyon paketine donusturmeli.
- **Workflow hizlandiricilari olmali:** Akilli on doldurma, tek tik prompt uretimi, paste sonrasi otomatik analiz, metadata formlari, guvenli normalize, kisayol is akislari, presetler ve dashboard yazarin hizini artirmali.
- **Teknik uretim ayrik ama entegre olmali:** CODE_META, kod testi, Mermaid, QR, asset ve export hattı yazarlik onayindan sonra calismali.

## 1.3. Ana Isleyis Ozeti

Kitap uretim sureci iki ana pipeline katmanina ayrilmalidir:

```text
1. Authoring Pipeline
   Kitap profili
   -> Kitap mimarisi
   -> Bolum tohumu
   -> Outline promptu
   -> LLM outline ciktisi
   -> Outline kalite kontrolu
   -> Tam metin promptu
   -> LLM Markdown tam metin + inline CODE_META ciktisi
   -> Tam metin kalite kontrolu
   -> Onayli bolum

2. Production Pipeline
   Onayli bolumler
   -> CODE_META cikarimi
   -> Kod manifesti
   -> Kod testleri
   -> Mermaid / asset / QR islemleri
   -> Markdown merge
   -> DOCX / PDF / EPUB / MkDocs / HTML export
   -> Final kitap kontrolu
```

Bu ayrim kritik: BookFactory oncul sisteminde teknik uretim hattı daha belirgin, fakat `bookMaker`in asil farki guclu bir yazar odakli Authoring Pipeline kurmasi olacaktir.

## 1.4. Uretim Asamalari

### 1. Kitap Kimligi ve Kapsam

Bu asamada yazardan veya LLM destekli sihirbazdan su bilgiler alinir:

- Kitap konusu
- Kitap adi
- Alt baslik
- Yazar adi
- Hedef okuyucu kitlesi
- Okuyucu seviyesi
- On kosullar
- Kapsam ici konular
- Kapsam disi konular
- Kitabin akademik/uygulamali/refereans karakteri
- Dil ve cikti hedefleri

Bu asamanin ciktisi:

```text
book_profile.yaml
```

Kalite kapisi:

```text
Gate 1: Book Profile Approval
Kitap konusu, hedef kitle, kapsam ve yazar bilgisi netlesmeden mimari asamaya gecilmez.
```

### 2. Kitap Mimarisi

Bu asamada bolum sayisi, genel bolum basliklari, kismi/part yapisi ve her bolumun genel icerigi belirlenir.

Cikti:

```text
book_architecture.yaml
```

Icerik:

- Hedef bolum sayisi
- Part/kisim yapisi
- Bolum sirasi
- Bolum basliklari
- Her bolumun amaci
- Her bolum icin kisa outline
- Bolumler arasi on kosul iliskileri
- Kitap genelinde teori/uygulama dengesi

Kalite kapisi:

```text
Gate 2: Book Architecture Approval
Bolum sayisi, bolum sirasi, bolum amaclari ve genel outline'lar tutarli olmadan bolum tohumlamaya gecilmez.
```

### 3. Bolum Tohumlama

Bolum tohumlama, her bolum icin yazarin LLM'e yol gosterecek ozel bilgileri girdigi asamadir.

Kullanici su alanlari doldurabilmelidir:

- Bolum amaci
- Hedef okuyucu notu
- Varsayilan on bilgi
- Zorunlu kavramlar
- Zorunlu kod/ornek varliklari
- Zorunlu gorsel/diyagram/screenshot varliklari
- Mini uygulama veya bolum gorevi
- Sik yanlis anlamalar
- Kapsam disi konular
- Kaynak politikasi
- Yazar notlari

Cikti:

```text
chapters/<chapter_id>/seed.yaml
```

Kalite kapisi:

```text
Gate 3: Chapter Seed Approval
Bolum tohumu yeterli degilse outline promptu uretilmez.
```

### 4. Outline Uretimi ve Degerlendirme

Sistem kitap profili, kitap mimarisi ve bolum tohumunu birlestirerek LLM'e verilecek outline promptunu uretir.

Akis:

```text
chapter_seed
-> outline_prompt.md
-> Kullanici promptu LLM'e verir
-> LLM outline uretir
-> Kullanici outline'i arayuze yapistirir
-> Sistem outline kalite kontrolu yapar
-> Skor ve eksikler gosterilir
```

Outline kalite kriterleri:

- Bolum tohumu ile uyum
- Zorunlu kavramlarin varligi
- Kapsam disi konularin disarida tutulmasi
- Pedagojik akis
- Teori/uygulama dengesi
- Kod, gorsel, alistirma ve rubrik yerlerinin planlanmasi
- Kitap mimarisiyle tutarlilik

Karar sozlugu:

```text
PASS
PASS_WITH_MINOR_NOTES
REVISION_REQUIRED
BLOCKED
```

Varsayilan skor mantigi:

```text
90-100  PASS
80-89   PASS_WITH_MINOR_NOTES
65-79   REVISION_REQUIRED
0-64    BLOCKED
```

Kullanici skordan memnunsa outline onaylanir. Memnun degilse sistem LLM'e verilecek outline revizyon promptu uretir.

### 5. Tam Metin Uretimi ve Degerlendirme

Onayli outline temel alinarak sistem LLM'e verilecek tam metin promptunu uretir.

Akis:

```text
approved_outline
-> full_text_prompt.md
-> Kullanici promptu LLM'e verir
-> LLM Markdown tam metin uretir
-> Kullanici metni arayuze yapistirir
-> Sistem kalite kontrolu yapar
-> Skor, eksikler ve revizyon onerileri gosterilir
```

Tam metin kalite kriterleri:

- Onayli outline'a uyum
- Zorunlu kavramlarin yeterli islenmesi
- Akademik ve pedagojik anlatim kalitesi
- Bolum standart yapisina uyum
- Markdown baslik hiyerarsisi
- Manuel numaralandirma yapilmamasi
- CODE_META, MERMAID_META, ASSET_META standartlarina uyum
- LLM ciktisindaki kod bloklarinin hemen oncesinde `CODE_META` bulunmasi
- `CODE_META` bloklarinin kod fence icine veya kod blogundan sonraya yazilmamasi
- `CODE_META` zorunlu alanlarinin `CHAPTER_SPEC.md` ile uyumlu olmasi
- Gorsel/diyagram/screenshot beklentilerinin karsilanmasi
- Ozet, terim sozlugu, kendini degerlendirme, alistirma, laboratuvar/proje ve rubrik gibi zorunlu pedagojik ogelerin varligi
- Kapsam disi konularin metne girmemesi
- Teknik dogruluk kontrol adaylari

Kalite kapisi:

```text
Gate 5: Full Text Approval
Tam metin yeterli kalite puanina ulasmadan onayli bolum olarak kabul edilmez.
```

### 6. Teknik Dogrulama

Onayli bolumler icin teknik kontroller calisir:

- CODE_META cikarimi
- Kod manifesti uretimi
- Kod derleme/calistirma/test
- Mermaid bloklarini cikarma ve render etme
- Asset/QR/gorsel kontrolleri
- Link ve kaynak kontrolleri

Bu asama yalnizca "dosya var mi" kontrolu degildir. Kitap icindeki kodlar ve ekran goruntuleri okuyucuya erisilebilir, tekrar uretilebilir ve raporlanabilir hale getirilmelidir.

### 6.1. Kod Erisilebilirligi ve Calistirilabilirlik

Kitap icindeki her anlamli kod ornegi su hedefleri desteklemelidir:

```text
1. Kitap icinde okunabilir olmalı.
2. Dosya olarak cikarilabilir olmali.
3. GitHub veya benzeri bir yerde internet uzerinden erisilebilir olmali.
4. QR/link ile okuyucuya sunulmali.
5. Mumkunse tarayicidan veya bulut ortamindan calistirilabilir olmali.
6. Yayin oncesinde otomatik testten gecmeli.
7. GitHub reposunda bolum ve kod ID'si uzerinden kolayca bulunabilir olmali.
8. GitHub Pages uyumlu kod sayfalariyla okunabilir web ciktisina baglanabilmeli.
9. Ayni kod icin kaynak, kod sayfasi ve calistirma hedefi arasinda net link haritasi olmali.
```

Tam metin uretiminde `CODE_META` sonradan sadece sistemin ekleyecegi gizli bir veri degil, LLM tarafindan uretilen Markdown kaynaginin acik parcasi olmalidir. Her kod blogundan hemen once ilgili `CODE_META` bulunmali; sistem bu bloklari otomatik okumali, eksik/hatalı alanlari issue olarak raporlamali ve gerekirse LLM'e aktarilabilir metadata repair paketi uretmelidir.

Her kod blogu calistirilabilir olmak zorunda degildir. Kirik ornek, hata gosterimi, pseudo-code veya sadece kavramsal parca olarak kullanilan kodlar metadata ile acikca isaretlenmelidir.

Calistirilabilir kod icin genisletilmis `CODE_META` taslagi:

```yaml
id: ch05_loop_01
chapter_id: chapter_05
language: java
file: LoopExample.java
kind: runnable_example
test: compile_run_assert
main_class: LoopExample
expected_stdout_contains:
  - "Toplam: 15"
timeout_sec: 10
github: true
qr: auto
online:
  enabled: true
  modes:
    - github_source
    - github_codespaces
  preferred: github_codespaces
```

Calistirilmamasi gereken ornek:

```yaml
id: ch05_buggy_loop_01
chapter_id: chapter_05
language: java
file: BuggyLoopExample.java
kind: broken_example
test: skip
github: false
qr: none
online:
  enabled: false
```

Dil ve konuya gore online calisma hedefleri:

```text
Java         -> GitHub repo + Codespaces + javac test
Python       -> GitHub repo + Colab/JupyterLite/Codespaces
JavaScript   -> StackBlitz/CodeSandbox/GitHub Codespaces
HTML/CSS/JS  -> Canli preview / GitHub Pages
SQL          -> SQLite wasm / hazir .db dosyasi
Data science -> Notebook + dataset + Colab
Mermaid      -> Render edilmis gorsel + kaynak .mmd
```

Kod item rapor modeli:

```yaml
code_item:
  id: ch05_loop_01
  chapter_id: chapter_05
  language: java
  file: LoopExample.java
  extracted_path: build/code/chapter_05/ch05_loop_01/LoopExample.java
  github_url: ""
  github_pages_url: ""
  code_page_url: ""
  runnable_url: ""
  qr_image: ""
  test_status: passed
  online_status: verified
```

GitHub repo hedef yapi taslagi:

```text
github_repo/
  README.md
  kodlar/
    chapter_01/
      ch01_intro_01/
        HelloWorld.java
        README.md
    chapter_02/
      ch02_variables_01/
        VariablesDemo.java
        README.md
  docs/
    index.md
    kodlar/
      chapter_01/
        ch01_intro_01.md
      chapter_02/
        ch02_variables_01.md
  mkdocs.yml
```

Kod erisimi icin uretilmesi gereken link turleri:

```text
github_source_url      GitHub uzerindeki ham/normal kaynak kod sayfasi
github_folder_url      Ornegin tum kod klasoru
github_pages_url       GitHub Pages uzerindeki okunabilir kod aciklama sayfasi
runnable_url           Codespaces/Colab/StackBlitz gibi calistirma hedefi
raw_download_url       Dogrudan dosya indirme linki
```

GitHub repo erisim ilkeleri:

- Her calistirilabilir kod, kitap bolumu ve kod ID'si ile baglantili olmalidir.
- GitHub source klasoru ile GitHub Pages code page'i birbirinden ayrilmali ama iki yonlu baglantilanmalidir.
- QR kodlar tek bir hedefe degil, manifest politikasina gore source, code page veya runnable URL'ye gidebilmelidir.
- Code page'ler, okuyucunun kodu anlamasi icin kisa aciklama, dosya listesi, test sonucu ve link seti icermelidir.

Kitap icinde okuyucuya sunulacak link/QR politikasi:

```text
Kisa kodlar:
  - Kitap icinde kod
  - GitHub source linki opsiyonel
  - QR genellikle yok

Orta/uzun kodlar:
  - Kitap icinde ana parca
  - GitHub source linki
  - GitHub Pages code page linki
  - QR auto

Proje tabanli ornekler:
  - Kitap icinde aciklama ve kritik dosyalar
  - GitHub folder linki
  - Runnable URL
  - QR auto
```

Kod erisilebilirlik kalite kapisi:

```yaml
gate:
  id: runnable_code_gate
  required_for:
    - runnable_example
  checks:
    extracted_file: required
    local_test: required
    github_url: required_if_github_true
    github_pages_url: required_if_pages_true
    runnable_url: optional
    qr_image: required_if_qr_auto
    link_validation: required
```

### 6.2. Kod Calistirma ve Raporlama Otomasyonu

Kitap icindeki kodlar otomatik olarak denenmeli ve sonuc raporlari uretilmelidir.

Ana akis:

```text
Onayli bolumler
  -> CODE_META bloklarini cikar
  -> Kod dosyalarini uret
  -> Kod manifesti olustur
  -> Uygun dil adapteriyle derle/calistir/test et
  -> stdout/stderr/uretilen dosya/sure bilgilerini yakala
  -> Beklenen sonuc ile karsilastir
  -> JSON/Markdown/HTML raporu uret
  -> Hatalar icin LLM repair promptu uret
```

Desteklenecek test tipleri:

```text
none                 Test yok
compile              Sadece derle/syntax kontrol
run                  Sadece calistir
run_assert           Calistir ve cikti kontrol et
compile_run          Derle ve calistir
compile_run_assert   Derle, calistir, cikti kontrol et
notebook_run         Notebook hucrelerini calistir
ui_screenshot        UI ac, screenshot uret
dataset_check        Veri dosyasi var/kullanilabilir mi kontrol et
```

Kod test raporu taslagi:

```yaml
code_test_report:
  generated_at: "2026-05-03T02:10:00"
  summary:
    total: 120
    passed: 113
    failed: 4
    skipped: 3
  by_language:
    java:
      total: 80
      passed: 78
      failed: 2
    python:
      total: 30
      passed: 28
      failed: 2
  failures:
    - id: ch05_loop_01
      chapter_id: chapter_05
      language: java
      status: failed
      reason: stdout_assertion_failed
      expected:
        - "Toplam: 15"
      actual_stdout: "Toplam: 10"
      command:
        - javac
        - "-encoding"
        - UTF-8
        - LoopExample.java
```

Uretilmesi gereken raporlar:

```text
build/reports/code_test_report.json
build/reports/code_test_report.md
build/reports/code_test_report.html
```

Kod test kalite kapisi:

```yaml
gate:
  id: code_execution_gate
  min_pass_rate: 0.95
  fail_on_compile_error: true
  fail_on_assertion_error: true
  allow_skipped:
    - broken_example
    - pseudo_code
```

Hata durumunda sistem LLM repair promptu uretmelidir:

```text
Kod ID: ch05_loop_01
Beklenen çıktı: Toplam: 15
Gerçek çıktı: Toplam: 10

Görev:
Kod örneğini ve açıklamasını uyumlu hale getir.
CODE_META alanlarını koru.
Tam bölüm metnini değiştirme; yalnızca ilgili kod bloğunu düzelt.
```

### 6.3. Screenshot Otomasyonu

Ekran goruntuleri otomatik cekilip kitabin uygun yerlerine yerlestirilebilmelidir. Bu ozellikle web, mobil, veri bilimi gorsellestirme, terminal ve GUI iceren kitaplarda kritik bir gereksinimdir.

Ana akis:

```text
Bolum metnindeki screenshot ihtiyaci
  -> SCREENSHOT_META / ASSET_META ile tanimlanir
  -> Screenshot manifest uretilir
  -> Uygulama/komut/URL hazirlanir
  -> Playwright/headless browser veya uygun aracla ekran goruntusu alinir
  -> Gorsel kalite kontrolu yapilir
  -> Markdown referansi dogrulanir veya enjekte edilir
  -> Rapor uretilir
```

`SCREENSHOT_META` taslagi:

```markdown
<!-- SCREENSHOT_META
id: ch07_login_form
chapter_id: chapter_07
title: "Giriş formu"
kind: browser_page
source:
  url: "http://127.0.0.1:5173/login"
  viewport: "1440x900"
  wait_for: "text:Giriş Yap"
output:
  file: "assets/auto/screenshots/ch07_login_form.png"
  format: png
placement: inline
caption: "Giriş formunun ilk görünümü"
-->
```

Kitap icindeki referans:

```markdown
![Giriş formunun ilk görünümü](../assets/auto/screenshots/ch07_login_form.png)
```

Desteklenecek screenshot turleri:

```text
browser_page       Playwright ile tam web sayfasi
browser_element    Sayfadaki belirli element
terminal           Komut ciktisi veya terminal benzeri render
notebook_output    Jupyter/Colab hucre ciktisi
desktop_app        Manuel veya script kontrollu sinirli destek
mobile_view        Responsive/mobile viewport
data_plot          Python/R grafigi dosya olarak uretme
```

Screenshot manifest taslagi:

```yaml
screenshot_manifest:
  items:
    - id: ch07_login_form
      chapter_id: chapter_07
      kind: browser_page
      url: "http://127.0.0.1:5173/login"
      viewport:
        width: 1440
        height: 900
      wait_for:
        type: text
        value: "Giriş Yap"
      output_file: "assets/auto/screenshots/ch07_login_form.png"
      caption: "Giriş formunun ilk görünümü"
      required: true
```

Screenshot raporu taslagi:

```yaml
screenshot_report:
  summary:
    total: 18
    passed: 17
    failed: 1
  failures:
    - id: ch07_login_form
      reason: wait_for_text_not_found
      url: "http://127.0.0.1:5173/login"
```

Screenshot kalite kontrolleri:

- Screenshot dosyasi uretildi mi?
- Gorsel bos veya tek renk degil mi?
- Minimum cozunurluk saglaniyor mu?
- Beklenen text/element gorunuyor mu?
- Dosya yolu Markdown icinde dogru referanslanmis mi?
- Caption var mi?
- Ayni ID tekrar ediyor mu?
- Cikti hedef formatlara uygun mu?

Kalite kapisi:

```yaml
gate:
  id: screenshot_gate
  required: true
  min_pass_rate: 1.0
  fail_on_missing_required: true
  allow_manual_override: true
```

Manuel override desteklenmelidir:

```text
assets/manual/screenshots/
assets/locked/screenshots/
assets/auto/screenshots/
assets/final/screenshots/
```

Asset onceligi:

```text
manual > locked > auto
```

Yazar manuel daha iyi bir ekran goruntusu koyduysa otomasyon onu ezmemelidir.

### 7. Cikti Uretimi

Onayli ve teknik olarak dogrulanmis bolumler birlestirilerek yayin ciktilari uretilir:

- Birlesik Markdown
- DOCX
- EPUB
- PDF
- MkDocs sitesi
- Tek sayfa HTML veya bolunmus HTML site

Nihai cikti hedefleri:

```text
docx    Akademik/kurumsal duzenleme ve Word tabanli son okuma icin
pdf     Sabit sayfa duzeni ve dagitim icin
epub    E-kitap okuyucular icin
mkdocs  Web dokumantasyonu / ders sitesi / GitHub Pages yayini icin
html    Tek sayfa veya bolumlere ayrilmis web ciktisi icin
```

Export hatti, ayni onayli kitap iceriginden birden fazla formata cikti alabilmelidir. Formatlara ozgu stiller, asset yollari, tablo/gorsel olcekleri ve link davranislari ayri ayri kontrol edilmelidir.

MkDocs hedefi icin ek gereksinimler:

- `mkdocs.yml` uretimi
- Bolumlerin `docs/` altina uygun sirayla kopyalanmasi veya render edilmesi
- Navigasyon yapisinin manifestten uretilmesi
- Mermaid, screenshot, QR ve kod sayfalari icin asset yollarinin web uyumlu hale getirilmesi
- `mkdocs-material` tema destegi
- GitHub Pages veya statik hosting icin yayinlanabilir cikti
- Kitap bolumleri ile kod sayfalari arasinda iki yonlu linkleme
- GitHub Actions ile otomatik Pages build/deploy icin workflow sablonu
- Kod sayfalarini ve kitap sayfalarini ayni Pages alaninda veya bagli alanlarda yayinlama secenegi

GitHub Pages uyumlu cikti hedefleri:

```text
docs/
  index.md
  chapters/
    chapter_01.md
    chapter_02.md
  code/
    chapter_01/
      ch01_intro_01.md
  assets/
    screenshots/
    qr/
    diagrams/
mkdocs.yml
.github/workflows/deploy_pages.yml
```

GitHub Pages kalite kontrolleri:

- `mkdocs build` basarili mi?
- Tum chapter sayfalari navigasyonda var mi?
- Kod sayfalari uretilmis mi?
- Kitap icindeki kod linkleri Pages sayfalarina gidiyor mu?
- GitHub source linkleri dogru mu?
- QR linkleri Pages veya GitHub hedeflerine gidiyor mu?
- Asset yollari web ciktisinda calisiyor mu?
- `lychee` ile linkler dogrulandi mi?
- Kod sayfasi ile kitap sayfasi arasinda kopuk link var mi?
- Pages workflow dosyasi gecerli mi?

## 1.5. Pipeline Definition Model

Pipeline tanimi ile runtime durum ayrilmalidir.

Tanım dosyasi:

```text
pipeline_definition.yaml
```

Bu dosya ne yapilacagini, hangi sirayla yapilacagini, her adimin girdisini/ciktisini, kalite kapisini ve UI davranisini tanimlar.

Runtime durum:

```text
pipeline_state.yaml
```

veya ileride:

```text
bookmaker.sqlite
```

Bu dosya/veritabani her kitap ve bolumun o anda hangi asamada oldugunu tutar.

Onerilen step tipleri:

```text
form                Kullanici yapilandirilmis veri girer
prompt_render       Sistem LLM promptu uretir
manual_copy         Kullanici promptu harici LLM arayuzune tasir
manual_paste        Kullanici LLM ciktisini bookMaker'a yapistirir
evaluation          Sistem skor/rapor uretir
revision_packet     Kalite raporunu LLM'e aktarilabilir revizyon paketine cevirir
version_checkpoint  Icerik degisikligini surum olarak kaydeder
diff_review         Iki surum arasindaki farklari gosterir
restore_version     Eski surumden yeni aktif surum uretir
approval            Kullanici onaylar veya revizyon ister
automation          CLI/tool calisir
export              Yayin ciktisi uretir
```

Ornek pipeline step modeli:

```yaml
id: evaluate_outline
title: "Outline Kalite Kontrolu"
scope: chapter
input:
  - chapter_seed
  - outline_candidate
output:
  - outline_quality_report
gate:
  min_score: 80
  block_below: 65
  decisions:
    pass: approve_outline
    revision_required: generate_outline_revision_packet
    blocked: revise_chapter_seed
ui:
  screen: chapter_studio
  panel: outline_review
execution:
  mode: local
```

## 1.5.1. Revizyon Paketi Modeli

LLM ciktisi hedef skoru alamadiginda veya eksikler tespit edildiginde sistem sadece hata listesi gostermemelidir. Eksikler LLM'e kolayca aktarilabilecek bir `revision_packet` haline getirilmelidir.

Amac:

```text
quality_report
-> issue listesi
-> hedefli revizyon paketi
-> kopyalanabilir revizyon promptu
-> yeni LLM ciktisi
-> tekrar degerlendirme
```

Onerilen model:

```yaml
revision_packet:
  id: outline_revision_packet_v1
  target_artifact: chapter_outline_v1
  current_score: 72
  required_score: 85
  decision: REVISION_REQUIRED
  revision_mode: targeted_revision
  preserve:
    - book_profile
    - chapter_scope
    - correct_existing_structure
    - CHAPTER_SPEC rules
  issues:
    - id: issue_001
      severity: blocking
      type: missing_required_concept
      location: "outline"
      expected: "try-with-resources kavrami ayri islenmeli"
      current: "Outline icinde yalnizca dosya yazma geciyor"
      instruction: "try-with-resources icin ayri alt baslik ve kod ornegi plani ekle"
      acceptance_criteria:
        - "Outline'da try-with-resources basligi var"
        - "Kod ornegi plani var"
```

Arayuz eylemleri:

```text
Eksikleri Goster
Revizyon Paketi Olustur
Revizyon Promptunu Kopyala
LLM Yanitini Yapistir
Tekrar Degerlendir
```

Her issue su alanlari tasimalidir:

```text
id
severity
type
location
expected
current
instruction
acceptance_criteria
```

Ornek runtime state:

```yaml
pipeline_state:
  book_id: java_temelleri
  pipeline_id: academic_technical_book_v1
  book:
    book_profile:
      status: approved
      version: 3
    book_architecture:
      status: approved
      score: 88
  chapters:
    chapter_03:
      current_step: evaluate_outline
      seed:
        status: approved
        version: 2
      outline:
        status: revision_required
        score: 74
        version: 1
      full_text:
        status: not_started
```

## 1.6. Chapter Workspace Modeli

Her bolum icin sistem tarafinda ayrik bir calisma alani tutulmalidir. Yazar bunu arayuzde sade sekilde gorur, fakat dosya sistemi/versionlama icin bu yapi faydalidir.

Onerilen yapi:

```text
chapters_workspace/
  chapter_03/
    seed.yaml
    outline_prompt.md
    outline_versions/
      outline_v1.md
      outline_v1_report.json
      outline_v2.md
      outline_v2_report.json
    full_text_prompt.md
    draft_versions/
      draft_v1.md
      draft_v1_report.json
      draft_v2.md
      draft_v2_report.json
    approved/
      chapter_03.md
    version_log.jsonl
    active_version.yaml
```

Bu yapi sayesinde:

- LLM ciktisi kaybolmaz.
- Her revizyonun skoru izlenir.
- Onceki surume donus mumkun olur.
- Kalite gelisimi olculebilir.
- GUI "v1, v2, onaylandi" gibi basit bir gorunum sunabilir.

## 1.6.1. Bolum Surum Kontrol Modeli

Uretilen bolumlerde uygulama icinde bir surum kontrol sistemi olmalidir. Yazar yapilan degisiklikleri takip edebilmeli, surumler arasindaki farklari gorebilmeli ve gerekirse onceki bir surume donebilmelidir.

Tasarim ilkesi:

```text
Eski surumler degistirilmez.
Geri alma islemi eski dosyayi ezmez.
Secilen eski surumden yeni bir aktif surum olusturur.
```

Surumlenecek artefaktlar:

- `chapter_seed`
- `outline_prompt`
- `outline_candidate`
- `outline_quality_report`
- `revision_packet`
- `full_text_prompt`
- `full_text_candidate`
- `full_text_quality_report`
- `approved_chapter`
- `code_test_report`
- `asset_report`

Onerilen surum kaydi:

```yaml
version:
  id: draft_v003
  artifact_type: full_text_candidate
  chapter_id: chapter_03
  parent_version: draft_v002
  created_at: "2026-05-03T11:30:00+03:00"
  created_by: user
  source: manual_paste
  llm_label: "ChatGPT web"
  change_reason: "Outline revizyon paketindeki eksikler giderildi"
  score: 91
  decision: PASS
  file: draft_versions/draft_v003.md
  report_file: draft_versions/draft_v003_report.json
```

`version_log.jsonl` olay gunlugu gibi davranmalidir:

```json
{"event":"created","artifact_type":"outline_candidate","version":"outline_v001","score":72}
{"event":"revision_packet_created","target":"outline_v001","version":"outline_revision_v001"}
{"event":"created","artifact_type":"outline_candidate","version":"outline_v002","score":88}
{"event":"approved","artifact_type":"outline_candidate","version":"outline_v002"}
{"event":"restored","from":"draft_v002","to":"draft_v004","reason":"draft_v003 kapsam disi konu ekledi"}
```

Geri alma davranisi:

- Kullanici onceki surumu secer.
- Sistem farklari gosterir.
- Kullanici onaylarsa eski surumden yeni bir surum uretir.
- `active_version.yaml` yeni surume isaret eder.
- Geri alma islemi de `version_log.jsonl` icine kaydedilir.

GUI gereksinimleri:

- Surum gecmisi paneli.
- Iki surum arasinda Markdown diff.
- Skor degisimi grafigi veya listesi.
- "Bu surume don" eylemi.
- "Bu surumden revizyon promptu uret" eylemi.
- Onayli surumleri kilitleme.

Git ile iliski:

- Uygulama ici surumleme bolum/artefakt duzeyinde calisir.
- Git proje geneli snapshot, paylasim ve harici yedekleme icin kullanilir.
- GUI geri alma islemleri Git komutlarina bagimli olmamalidir.
- Istenirse onayli bolum veya export sonrasi otomatik Git commit onerilebilir; kullanici onayi olmadan commit/push yapilmamalidir.

## 1.7. GUI Yaklasimi

Studio arayuzu pipeline tanimindan beslenmelidir. Sabit ve daginik butonlar yerine, aktif asama ve sonraki mantikli is gosterilmelidir.

Yazar her zaman sunlari gorebilmelidir:

- Aktif kitap
- Genel kitap ilerleme durumu
- Her bolumun bulundugu asama
- Son kalite skoru
- Eksik zorunlu ogeler
- Siradaki onerilen islem

Bolum ekrani su sekmelerden olusabilir:

```text
1. Tohum
2. Outline Promptu
3. Outline Ciktisi
4. Outline Kalite Raporu
5. Tam Metin Promptu
6. Tam Metin Ciktisi
7. Tam Metin Kalite Raporu
8. Onayli Bolum
9. Surum Gecmisi
10. Fark Goruntuleme
```

Kullanici deneyimi ilkesi:

- Yazar prompt muhendisligi yapmak zorunda kalmamali.
- "Promptu hazirla", "LLM ciktisini yapistir", "Kalite kontrolu yap", "Revizyon promptu uret", "Onayla" gibi net eylemler olmali.
- Skor tek basina yetmez; eksikler ve revizyon metni de uretilmeli.
- Her kaydetme, yapistirma, degerlendirme, onay ve geri alma islemi surum gecmisine yazilmali.
- Yazar onceki surumleri gorebilmeli, farklari inceleyebilmeli ve guvenli sekilde onceki surumden yeni aktif surum olusturabilmeli.
- Arayuz her durumda tek bir "sonraki en mantikli is" onermeli.
- LLM ciktisi yapistirildigi anda otomatik on analiz calismali.
- Guvenli normalize ve metadata formu yazarin YAML/Markdown ayrintilariyla ugrasmasini azaltmali.
- Revizyon paketi uretimi tek tikla yapilabilmeli.
- Kitap turu presetleri bolum tohumu, prompt ve kalite kapilarini onceden doldurabilmeli.

## 1.8. LLM Calisma Modlari

Ana ve varsayilan calisma sekli manuel copy/paste modudur. Sistem API entegrasyonu hic kullanilmayacakmis gibi tasarlanmalidir.

```text
manual_paste:
  Sistem prompt uretir.
  Kullanici promptu harici LLM arayuzune yapistirir.
  Kullanici LLM ciktisini bookMaker arayuzune yapistirir.
  Sistem kalite kontrolu yapar.

provider_api:
  Sistem prompt uretir.
  Secili LLM provider'a API ile gonderir.
  Cevabi otomatik alir.
  Kullanici ciktıyı onaylar veya revizyon ister.
```

`provider_api` cekirdek akisin parcasi degil, ileride eklenebilecek opsiyonel executor olmalidir.

Manuel mod ana tasarimdir; cunku farkli LLM modelleriyle hizli deneme yapmayi saglar ve API maliyet/anahtar/gizlilik/kurum politikasi bagimliligini azaltir.

Arayuzde ana eylemler sunlar olmalidir:

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

## 2. Ana Kullanim Bicimleri

Sistem iki arayuzle calismalidir:

- CLI: otomasyon, script, toplu uretim ve ileri kullanicilar icin.
- Studio GUI: kitap projesi secme, bolum duzenleme, LLM gorevlerini calistirma, kaynaklari yonetme ve cikti alma icin.

Ilk dusunulen komutlar:

```text
bookmaker init
bookmaker outline
bookmaker draft chapter-03
bookmaker review chapter-03
bookmaker check citations
bookmaker check code
bookmaker build docx
bookmaker build html
bookmaker studio
```

## 3. Ilk Teknik Yon

Tercih edilen ilk mimari:

- Ana dil: Python
- CLI: Typer veya argparse; karar daha sonra mevcut ihtiyaca gore verilecek.
- Backend/Studio: FastAPI tabanli yerel web uygulamasi.
- Frontend: once sade ve guvenilir HTML/CSS/JS; gerekirse daha sonra React/Vite.
- Kaynak format: Markdown + YAML manifest + BibTeX.
- Cikti hatti: Pandoc merkezli.
- Diyagram hatti: Mermaid kaynaklarindan `mmdc` ile PNG/SVG uretimi.
- Gorsel isleme: ImageMagick.
- Link dogrulama: lychee.
- Markdown kalite kontrol: markdownlint-cli2.
- Dil/stil kontrol: Vale.
- Python kalite kontrol: ruff.
- Otomasyon: just ve pre-commit.

## 4. Sample Kitap Incelemesinden Cikan Model

`sample` klasorundeki Java kitabi, `bookMaker` icin ana referans kaliptir.

Incelenen dosyalar:

- `sample/Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.md`
- `sample/Java_Temelleri_Kompakt_Birlesik_cift_qr_gomulu.docx`
- `sample/Kompakt_Bolum_16.md`

Temel bulgular:

- Kitap Markdown tabanli yazilmis.
- Pandoc metadata blogu var.
- DOCX ciktisi uretilmis.
- Ana Markdown yaklasik 39.312 satir.
- 23 ana bolum ve 4 ek var.
- 251 adet kod kimligi var.
- 934 Java kod blogu var.
- 502 Markdown gorsel referansi var.
- DOCX icinde 534 medya dosyasi gomulu.
- Kod ornekleri icin genellikle iki QR var: kod sayfasi ve kaynak kod.
- Mermaid diyagramlari ham blok olarak duruyor ve final cikti once gorsel donusum gerektiriyor.

Tekrar eden bolum sablonu:

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

## 5. Book Project Format Taslagi

Ilk dusunulen proje yapisi:

```text
my-book/
  book.yaml
  glossary.yaml
  bibliography.bib
  sources/
  chapters/
    01-giris.md
    02-temel-kavramlar.md
  figures/
  diagrams/
  qr/
  code/
  datasets/
  notebooks/
  build/
```

## 6. Manifest Ihtiyaclari

`book.yaml` su bilgileri tasimalidir:

- Kitap basligi, alt baslik, yazar, tarih, dil
- Hedef kitle
- Seviye
- Kapsam ve kapsam disi konular
- Bolum listesi
- LLM calisma modu: varsayilan `manual_paste`
- Opsiyonel LLM saglayici/model etiketleri; API bagimliligi zorunlu degildir
- Surumleme politikasi
- Geri alma ve onayli surum kilitleme politikasi
- Cikti hedefleri
- Kaynak ve atif politikasi
- Terim politikasi
- Kod ornegi ve QR politikasi
- Kod erisilebilirlik politikasi
- Online calistirma politikasi
- Kod test politikasi
- GitHub repo politikasi
- GitHub Pages yayin politikasi
- Screenshot otomasyon politikasi
- Asset override politikasi
- Pandoc ayarlari
- DOCX export ayarlari
- PDF export ayarlari
- EPUB export ayarlari
- MkDocs export ayarlari
- HTML export ayarlari

Bolum bazinda ek manifest gerekebilir:

- Bolum no
- Baslik
- Ogrenme ciktisi listesi
- On bilgi varsayimlari
- Ana kavramlar
- Kod ornegi listesi
- Calistirilabilir kod listesi
- Beklenen kod ciktilari
- GitHub/code page hedefleri
- Screenshot plani
- Gorsel/diyagram/asset plani
- Alistirma ve soru turleri
- Kaynaklar
- Kalite kontrol durumu

## 7. LLM Mimarisi

LLM kullanimi esas olarak harici web arayuzleriyle manuel copy/paste uzerinden yapilacaktir. Sistem prompt uretir, yazar istedigi LLM modeline yapistirir, ciktıyı geri getirir.

API adapter yaklasimi opsiyoneldir ve cekirdek MVP icin zorunlu degildir:

```text
llm/
  manual_exchange.py
  revision_packet.py
  base.py
  openai_provider.py
  anthropic_provider.py
  google_provider.py
  openrouter_provider.py
```

`base.py` ve provider dosyalari ileride eklenebilir. Ilk tasarimda `manual_exchange.py` ve `revision_packet.py` daha kritik olmalidir.

LLM gorevleri:

- Kitap plani olusturma
- Bolum plani olusturma
- Bolum taslagi uretme
- Ogrenme ciktisi uretme ve iyilestirme
- Kod ornegi uretme
- Hata ayiklama egzersizi uretme
- Soru, alistirma ve rubrik uretme
- Terim sozlugu cikarma
- Bolum ozeti uretme
- Ileri okuma/kaynak oneri taslagi uretme
- Akademik ton ve anlatim revizyonu
- Teknik dogruluk kontrol listesi uretme
- Eksikleri LLM'e aktaracak revizyon paketi uretme

LLM tek basina otorite sayilmamalidir. Akademik iddialar kaynaklara baglanmali; kaynak gerektiren alanlarda dogrulama hatti tasarlanmalidir.

## 8. Kalite Kontrol Hatti

Ilk kalite kontroller:

- Markdown baslik hiyerarsisi dogru mu?
- Bolum numaralari tutarli mi?
- Alt baslik numaralari bolumle uyumlu mu?
- Tekrar eden zorunlu bolum bloklari var mi?
- Kod kimlikleri benzersiz mi?
- Kod kimligi ile GitHub linki uyumlu mu?
- QR gorselleri var mi?
- Mermaid bloklari final cikti once gorsele cevrildi mi?
- Linkler calisiyor mu?
- Kaynaklar ve ileri okumalar bos mu?
- Terim sozlugu bolum kavramlariyla uyumlu mu?
- Kod bloklari dil etiketi tasiyor mu?
- Gerekli cikti dosyalari uretilebiliyor mu?
- Kalite raporundaki her hata/eksik issue olarak saklandi mi?
- Dusuk skor veya eksikler icin revizyon paketi uretildi mi?
- Revizyon paketinde `expected`, `current`, `instruction`, `acceptance_criteria` alanlari var mi?
- Calistirilabilir olarak isaretlenen kodlar dosya olarak cikarildi mi?
- Calistirilabilir kodlar derleme/calistirma/test adimlarindan gecti mi?
- Kod test raporlarinda basarisiz veya atlanan kritik ornek var mi?
- Beklenen stdout/stderr/dosya ciktisi dogrulandi mi?
- Kodlar internet uzerinden erisilebilir GitHub/code page URL'lerine sahip mi?
- Online calistirma hedefleri uretildi ve dogrulandi mi?
- Kod QR/linkleri gecerli mi?
- SCREENSHOT_META / ASSET_META bloklari cikarilabiliyor mu?
- Zorunlu screenshot dosyalari otomatik uretilmis veya manuel override ile saglanmis mi?
- Screenshotlar bos/tek renk veya hatali sayfa goruntusu degil mi?
- Screenshot referanslari Markdown icinde dogru yere yerlestirilmis mi?
- Gorsel captionlari var mi?

Sample incelemesinde gorulen kontrol adaylari:

- Bolum 16 alt baslik numaralarinda `16.22` altinda `16.16.1` gibi tutarsizlik var.
- `Hata ayiklama egzersizi` bazi bolumlerde iki kez geciyor olabilir.
- Markdown'daki QR gorsel yollari `sample` icinde bulunmuyor; DOCX icinde gomulu medya var.

## 9. MVP Onerisi

Ilk MVP, teknik exporttan once yazarlik pipeline'ini dogru kurmaya odaklanmalidir. Teknik uretim hatti tamamen dislanmamalidir, ancak ilk ayirt edici deger `Bolum Muhendisligi` ve kalite kapilari olmalidir.

### MVP-1: Authoring Pipeline Cekirdegi

1. Yeni kitap projesi olusturma: `bookmaker init`
2. `book_profile.yaml` standardi
3. `book_architecture.yaml` standardi
4. `pipeline_definition.yaml` standardi
5. `pipeline_state.yaml` veya SQLite tabanli durum takibi
6. Bolum workspace yapisi
7. Bolum artefaktlari icin surum kontrol modeli
8. Surum gecmisi, diff ve guvenli geri alma modeli
9. Kitap profili formu
10. Kitap mimarisi formu veya manuel LLM icin prompt uretimi
11. Bolum tohumlama formu
12. Bolum tohumlama icin akilli on doldurma
13. Tek tik outline promptu uretimi
14. LLM outline ciktisini yapistirma alani
15. Paste sonrasi otomatik outline on analiz
16. Outline kalite kontrolu ve 100 uzerinden skor
17. Outline revizyon paketi ve kopyalanabilir revizyon promptu uretimi
18. Tek tik tam metin promptu uretimi
19. Tam metin promptunda LLM'e inline `CODE_META` uretme zorunlulugunu acikca verme
20. Markdown tam metin ve LLM tarafindan uretilmis `CODE_META` bloklarini yapistirma alani
21. Paste sonrasi otomatik `CODE_META` parse/validate + normalize + on analiz
22. Metadata formu ile `CODE_META` / `MERMAID_META` duzenleme
23. Tam metin kalite kontrolu ve 100 uzerinden skor
24. Tam metin revizyon paketi ve kopyalanabilir revizyon promptu uretimi
25. Sonraki en mantikli is onerisi
26. Onayli bolum dosyasi uretimi

### MVP-2: Teknik Kontrol ve Export

1. Markdown bolumlerini parse edip yapi raporu uretme
2. CODE_META bloklarini cikarma
3. Eksik, yanlis yerde veya hatali `CODE_META` icin otomatik issue ve repair paketi uretme
4. Kod kimligi ve dosya yolu tutarliligini kontrol etme
5. Java/Python/JavaScript icin basit kod test adapterleri
6. Kod test raporlarini JSON/Markdown olarak uretme
7. Hatalar icin revizyon paketi / LLM repair promptu uretme
8. GitHub/code page URL alanlarini manifestte modelleme
9. Online runnable URL alanlarini modelleme
9. QR/link referanslarini cikarma
10. GitHub repo klasor yapisi uretme
11. Kod ornekleri icin README/code page uretme
12. GitHub Pages uyumlu `docs/` ve `mkdocs.yml` uretme
13. GitHub Actions Pages deploy workflow sablonu uretme
14. SCREENSHOT_META / ASSET_META bloklarini cikarip screenshot manifest uretme
15. Playwright ile browser_page screenshot alimi
16. Screenshot raporu uretme
17. Manuel/locked/auto/final asset onceligi modelini uygulama
18. Mermaid bloklarini tespit edip `mmdc` ile gorsel uretme
19. Basit asset varlik kontrolu
20. Pandoc ile DOCX cikti alma
21. Pandoc veya uygun aracla PDF cikti alma
22. Pandoc ile EPUB cikti alma
23. MkDocs site yapisi ve `mkdocs.yml` uretme
24. Tek sayfa veya bolumlu HTML cikti alma
25. Link dogrulama icin lychee entegrasyonu
26. Markdown kalite kontrol icin markdownlint-cli2 entegrasyonu

### MVP-3: Studio GUI

1. Aktif kitap secme
2. Dashboard: kitap ve bolum ilerleme durumu
3. Pipeline durum matrisi
4. Kitap profili ekrani
5. Kitap mimarisi ekrani
6. Bolum Stüdyosu:
   - Tohum
   - Outline Promptu
   - Outline Ciktisi
   - Outline Kalite Raporu
   - Outline Revizyon Paketi
   - Tam Metin Promptu
   - Tam Metin Ciktisi
   - Tam Metin Kalite Raporu
   - Tam Metin Revizyon Paketi
   - Onayli Bolum
   - Surum Gecmisi
   - Fark Goruntuleme
7. Metadata form paneli
8. Sonraki en mantikli is paneli
9. Dashboard: kitap geneli skor, bloklu bolumler, en sik issue tipleri
10. Raporlar ekrani
11. Export ekrani

### MVP-4: Manuel LLM Exchange ve Opsiyonel Adapter Iskeleti

1. Manuel copy/paste modu
2. Prompt template sistemi
3. Promptu kopyalama ve LLM ciktisini yapistirma kaydi
4. Revizyon paketi modeli
5. Prompt ve LLM cevap versionlama
6. Artefakt surumleme, diff ve restore modeli
7. Opsiyonel LLM provider base interface
8. Opsiyonel OpenAI adapter taslagi
9. Model/provider etiketlerini proje seviyesinde saklama; API zorunlu degildir

## 10. Kodlamadan Once Netlestirilecek Kararlar

- Ilk resmi proje dili Turkce mi olacak?
- Ilk kitap turu karara baglandi: Java Temelleri / Java programlama kitabi preset'i ile baslanacak.
- CLI paket adi karara baglandi: Python paketi ve CLI komutu `bookmaker` olacak.
- Ilk LLM calisma modu manuel copy/paste olarak kesin kabul edildi; API entegrasyonu MVP icin zorunlu degil.
- Opsiyonel API adapterleri daha sonra eklenecekse API anahtarlari `.env` ile mi, sistem ortam degiskeniyle mi yonetilecek?
- Ilk cikti hedefi karara baglandi: DOCX.
- PDF, EPUB, MkDocs ve HTML ikinci faz hedefleri olarak kalacak; mimari uyumlu tasarlanacak.
- GitHub repo yapisi kitap reposunun icinde mi uretilmeli, yoksa ayri kod reposu mu hedeflenmeli?
- GitHub Pages yayini kitap sitesi, kod sayfalari veya ikisini birden mi icermeli?
- QR kodlar GitHub source URL'lerine mi, GitHub Pages code page'lerine mi, yoksa runnable URL'lere mi gitmeli?
- Bu oturumdan sonra kaldigimiz yeri hizli toparlamak icin `TODO.md` ve `RESUME.md` birlikte okunacak mi?
- Sample dosyalari repo icinde kalacak mi, yoksa test fixture olarak duzenlenecek mi?
- Pipeline state karara baglandi: dosya sistemi + SQLite hibrit model kullanilacak.
- Bolum surum gecmisi karara baglandi: okunabilir `version_log.jsonl` / `active_version.yaml` dosyalari asil artefakt; SQLite hizli indeks ve event sorgu katmani olacak.
- Onayli surumler kilitlenince yalnizca yeni surum uzerinden mi duzenlenebilecek?
- Studio frontend ilk surumde sade HTML/CSS/JS mi kalacak, yoksa React/Vite mi kullanilacak?
- Kalite kontrollerinin ilk surumu tamamen programatik kurallar mi olacak, yoksa LLM destekli degerlendirme de olacak mi?
- Outline ve tam metin icin varsayilan gecme skorlari ne olmali?
- Kullanici dusuk skorlu ciktiyi manuel override ile onaylayabilmeli mi?
- Her bolum icin kac version saklanmali?
- Dis LLM API modu MVP'ye dahil edilmeyecek; tasarim uyumlu kalacak.
- `bookMaker` BookFactory kodundan parca devralacak mi, yoksa temiz bir cekirdek mi yazilacak?

## 11. Ilk Uygulama Adimlari

Baslanan ilk teknik parca:

- `tools/chapter_semantic_validator.py` eklendi.
- `CHAPTER_SPEC.md` kurallarinin ilk mekanik dogrulamalari kodlandi.
- `sample/sample_chapter.md` validator ile `PASS score=100` sonucunu veriyor.
- `sample/sample_chapter.md` kanonik ornek haline getirildi: somut `code_id`, net `CODE_META.kind`, `main_class`, `extract`, `test`, `github`, `qr_policy`, `expected_stdout_contains`, gorunur `## Gövde Metni`, numarasiz kod basliklari.
- Java smoke dogrulamasi yapildi: 9 kod blogu icinde 6 gecen, 3 bilincli `review_only`/`skip`, 0 hata.
- Mermaid diyagrami `mmdc` ile render edildi ve PNG uretildi.
- Raporlar `build/reports/chapter_semantic_report.json` ve `build/reports/chapter_semantic_report.md` olarak uretiliyor.

Calistirma komutu:

```powershell
python .\tools\chapter_semantic_validator.py .\sample\sample_chapter.md
```

Kodlamaya baslandiginda onerilen sira:

1. `chapter_semantic_validator` icin kucuk test fixture'lari olustur.
2. Validator'i gelecekteki `bookmaker check chapter` komutuna baglanabilecek sekilde paketle.
3. Python proje iskeletini olustur.
4. `pyproject.toml` icinde paket, CLI ve kalite araclarini tanimla.
5. `bookmaker` paket klasorunu olustur.
6. `book_profile`, `book_architecture`, `chapter_seed`, `pipeline_definition`, `pipeline_state` veri modellerini yaz.
7. `artifact_version`, `version_event`, `active_version` veri modellerini yaz.
8. Ornek `academic_technical_book_v1` pipeline tanimini olustur.
9. Pipeline engine icin temel durum gecislerini yaz:
   - start_step
   - save_artifact
   - create_version
   - diff_versions
   - restore_version
   - evaluate
   - approve
   - request_revision
10. Prompt template sistemini kur.
11. Outline prompt renderer yaz.
12. Full text prompt renderer yaz.
13. Outline evaluator icin ilk programatik kontrol setini yaz.
14. Full text evaluator icin ilk programatik kontrol setini yaz.
15. Chapter workspace versionlama mantigini yaz.
16. `bookmaker init` komutunu ekle.
17. `bookmaker pipeline status` komutunu ekle.
18. `bookmaker prompt outline chapter_03` komutunu ekle.
19. `bookmaker evaluate outline chapter_03` komutunu ekle.
20. `bookmaker evaluate draft chapter_03` komutunu ekle.
21. `bookmaker version list chapter_03` komutunu ekle.
22. `bookmaker version diff chapter_03 draft_v002 draft_v003` komutunu ekle.
23. `bookmaker version restore chapter_03 draft_v002` komutunu ekle.
24. Markdown parser ve heading extractor yaz.
25. Sample kitap icin analiz komutu yaz.
26. Zorunlu bolum bloklarini tanimla.
27. `bookmaker check` komutunu ekle.
28. Pandoc build komutunu sar.
29. Mermaid donusum komutunu sar.
30. Studio icin FastAPI iskeletini ekle.
31. Studio'da once Kitap Profili, Kitap Mimarisi, Bolum Stüdyosu ve Surum Gecmisi ekranlarini yap.
32. Pre-commit ve just otomasyonunu ekle.
