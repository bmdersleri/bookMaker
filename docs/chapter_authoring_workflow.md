# Chapter Authoring Workflow v0.1

> **TARIHI KAYIT (2026-05-03).** Book_profile/book_architecture tabanli eski workflow.
> Guncel pipeline: SPEC → VALIDATE → SEED → NORMALIZE → ENRICH → ASSEMBLE (bkz. `CHAPTER_PRODUCTION.md`).

Bu belge, `bookMaker` icinde tek bir bolumun nasil uretilecegini tanimlar.

Ana tasarim kararlari:

1. Varsayilan LLM kullanimi manuel copy/paste akisi olacak.
2. API entegrasyonu opsiyonel executor olarak tasarlanabilir, fakat cekirdek workflow API'ye bagimli olmayacak.
3. LLM ciktisi dogrudan onayli icerik sayilmayacak.
4. Her onemli cikti artifact olarak kaydedilecek ve surumlenecek.
5. Her kalite sorunu issue olarak saklanacak ve revizyon paketine donusturulecek.
6. Geri alma eski surumu ezmeyecek; secilen eski surumden yeni aktif surum olusturacak.

## 1. Hedef Cikti

Workflow'un hedefi, kanonik ornek olan `sample/sample_chapter.md` kalitesinde bir bolum uretmektir.

Onayli bolum sunlari saglamalidir:

- Tek H1 baslik.
- Standart bolum akisi.
- `SECTION_META`, `SUBSECTION_META`, `CODE_META`, `MERMAID_META`, `ASSET_META` / `SCREENSHOT_META` kurallarina uyum.
- LLM tarafindan uretilen tam metnin icinde kod bloglarindan hemen once `CODE_META` bulunmasi.
- Somut ve benzersiz kod kimlikleri.
- Hatalı ornekler icin `intentional_mismatch` ve `paired_with`.
- Derlenebilir/calistirilabilir kodlar icin test metadata'si.
- Validator sonucu `PASS`.
- Kod smoke testlerinde kritik hata olmamasi.
- Gerekli Mermaid/gorsel ciktisinin uretilebilmesi.

## 2. Temel Artifact Sozlugu

Her adim dosya veya veritabani kaydi olarak artifact uretmelidir.

| Artifact | Aciklama |
|---|---|
| `book_profile` | Kitap kimligi, hedef kitle, kapsam, kapsam disi konular |
| `book_architecture` | Bolum listesi, bolum amaclari, siralama |
| `chapter_seed` | Bolume ozel yazar girdileri |
| `outline_prompt` | Harici LLM'e verilecek outline promptu |
| `outline_response` | LLM'den yapistirilan outline |
| `outline_quality_report` | Outline skor ve issue listesi |
| `outline_revision_packet` | Outline eksiklerini LLM'e aktaracak revizyon paketi |
| `full_text_prompt` | Harici LLM'e verilecek tam metin promptu |
| `full_text_response` | LLM'den yapistirilan Markdown taslak |
| `normalized_chapter` | Sistem tarafindan CHAPTER_SPEC'e yaklastirilmis taslak |
| `full_text_quality_report` | Tam metin skor ve issue listesi |
| `full_text_revision_packet` | Tam metin eksiklerini LLM'e aktaracak revizyon paketi |
| `approved_chapter` | Kullanici tarafindan onaylanmis bolum Markdown dosyasi |
| `code_test_report` | Kod derleme/calistirma/test raporu |
| `asset_report` | Mermaid, screenshot, asset, QR/link raporu |
| `version_log` | Artifact olay gunlugu |
| `active_version` | Aktif artifact surumlerini gosteren indeks |

## 3. Durum Makinesi

Bolum state'i tek bir serbest metin alanindan ibaret olmamalidir. Her ana artifact kendi durumunu tasimalidir.

Onerilen ana bolum durumlari:

```text
planned
seeded
outline_prompt_ready
outline_pasted
outline_reviewed
outline_revision_required
outline_approved
full_text_prompt_ready
full_text_pasted
normalized
full_text_reviewed
full_text_revision_required
full_text_approved
technical_check_running
technical_check_failed
technical_check_passed
approved
ready_for_export
```

Durum gecis ilkeleri:

1. `book_profile` ve `book_architecture` onaylanmadan bolum uretimine gecilmez.
2. `chapter_seed` onaylanmadan outline promptu final sayilmaz.
3. Outline onaylanmadan tam metin promptu uretilmez.
4. Tam metin kalite kapisindan gecmeden `approved_chapter` olusmaz.
5. Teknik kontroller gecmeden bolum `ready_for_export` olmaz.
6. Manuel override varsa gerekce ve kullanici kimligi/version event olarak kaydedilir.

## 4. Workflow Adimlari

### 4.1. Bolum Secimi

Amaç: Yazarin kitap mimarisinden calisilacak bolumu secmesi.

Girdi:

- `book_profile`
- `book_architecture`
- bolum kimligi

Cikti:

- aktif `chapter_workspace`
- `current_step: collect_chapter_seed`

UI eylemleri:

- Bolum sec.
- Bolum amacini gor.
- Zorunlu kavramlari gor.
- Onceki durumu gor.

Kalite kurali:

- Bolum `book_architecture` icinde tanimli degilse workflow baslamaz.

### 4.2. Bolum Tohumlama

Amaç: Yazarin bolume ozel niyetini ve zorunlu ogeleri yapilandirilmis sekilde girmesi.

Girdi:

- bolum metadata
- yazar notlari

Cikti:

- `chapter_seed`
- `seed_v001`

Zorunlu alanlar:

```yaml
chapter_seed:
  chapter_id: chapter_03
  purpose: ""
  target_reader_state: ""
  learning_outcomes: []
  prerequisites: []
  mandatory_concepts: []
  required_examples: []
  required_code_items: []
  intentional_mismatch_examples: []
  required_diagrams: []
  required_assets: []
  mini_application: ""
  common_mistakes: []
  exercises: []
  lab_task: ""
  out_of_scope: []
  author_notes: ""
```

Surumleme:

- Her kaydetme yeni seed surumu uretir.
- `version_log` icine `seed_created` veya `seed_updated` olayi yazilir.

UI eylemleri:

- Tohumu kaydet.
- Eksik alanlari goster.
- Tohumu onayla.
- Onceki seed surumune bak.

Kalite kapisi:

- `purpose`, `learning_outcomes`, `mandatory_concepts`, `out_of_scope` bos olmamali.
- Yazar seed'i onaylamadan outline promptu final uretilmez.

### Kitap Mimarisinden Otomatik On Doldurma

Seed formu bos acilmamalidir. Sistem `book_architecture.yaml` icindeki ilgili bolum girisinden asagidaki alanlari otomatik onermelidir:

- Bolum amaci (`purpose`) — mimarideki `chapter_purpose` alanından
- On kosullar (`prerequisites`) — mimarideki bolum bağimlilik ilişkisinden
- Ogrenme ciktilari (`learning_outcomes`) — mimarideki `expected_learning_outcomes` alanından
- Zorunlu kavramlar (`mandatory_concepts`) — mimarideki `mandatory_concepts` alanından

Ek on doldurma kaynaklari:

- Onceki bolumlerin `out_of_scope` listelerinden kapsam disi aday onerileri.
- Secili preset (java_temelleri vb.) icin varsayilan ornek ve hata adaylari.

Kural: On doldurulan hicbir alan yazar onayi olmadan kesinlesmis sayilmaz. Sistem hangi alanin nereden on dolduruldugunu gostermelidir.

### 4.3. Outline Promptu Uretimi

Amaç: Harici LLM'e verilecek kontrollu outline promptunu uretmek.

Girdi:

- `book_profile`
- `book_architecture`
- `chapter_seed`
- `chapter_spec.md`
- prompt template

Cikti:

- `outline_prompt_v001.md`

Prompt sabit bolumleri:

- Kitap baglami.
- Bolum amaci.
- Hedef kitle.
- Zorunlu kavramlar.
- Kapsam disi konular.
- Istenen outline formatı.
- Tam metin yazmama uyarisi.
- Kalite beklentileri.

UI eylemleri:

- Promptu olustur.
- Promptu kopyala.
- Prompt surum gecmisini gor.

Kalite kapisi:

- Prompt icinde `chapter_seed` zorunlu alanlari bulunmali.
- `CHAPTER_SPEC` ve cikti formati kurallari prompttan cikarilamaz.

### 4.4. Outline Ciktisini Yapistirma

Amaç: Yazarin harici LLM'den aldigi outline'i sisteme aktarmasi.

Girdi:

- `outline_prompt`
- harici LLM ciktisi

Cikti:

- `outline_response_v001.md`
- `manual_exchange` kaydi

Manual exchange kaydi:

```yaml
manual_exchange:
  id: outline_exchange_v001
  mode: manual_paste
  prompt_version: outline_prompt_v001
  provider_label: "ChatGPT web"
  pasted_response_file: outline_versions/outline_v001.md
  created_at: ""
```

UI eylemleri:

- LLM yanitini yapistir.
- Kaynak/model etiketi gir.
- Kaydet.

Surumleme:

- Her yapistirma yeni outline response surumu uretir.

### 4.5. Outline Kalite Kontrolu

Amaç: Outline'in seed, mimari ve kalite kurallariyla uyumunu olcmek.

Girdi:

- `chapter_seed`
- `outline_response`
- `book_architecture`

Cikti:

- `outline_quality_report`
- issue listesi

Skor kategorileri:

```text
structure_score
seed_alignment_score
mandatory_concepts_score
pedagogy_score
scope_control_score
code_asset_plan_score
```

Karar:

```text
PASS
PASS_WITH_WARNINGS
REVISION_REQUIRED
BLOCKED
```

UI eylemleri:

- Kalite kontrolu yap.
- Eksikleri gor.
- Revizyon paketi olustur.
- Outline'i onayla.

Kalite kapisi:

- Minimum skor varsayilan `80`.
- `BLOCKED` kararinda outline onaylanamaz.
- Düsük skorlu onay ancak manuel override gerekcesiyle yapilabilir.

### 4.6. Outline Revizyon Dongusu

Amaç: Eksikleri LLM'e kolay aktararak outline'i iyilestirmek.

Girdi:

- `outline_quality_report`
- mevcut `outline_response`

Cikti:

- `outline_revision_packet`
- kopyalanabilir revizyon promptu
- yeni `outline_response`

Issue alanlari:

```yaml
issue:
  id: issue_001
  severity: blocking
  type: missing_required_concept
  location: outline
  expected: ""
  current: ""
  instruction: ""
  acceptance_criteria: []
```

UI eylemleri:

- Revizyon paketini olustur.
- Revizyon promptunu kopyala.
- Yeni LLM yanitini yapistir.
- Tekrar degerlendir.

Surumleme:

- Revizyon paketi de surumlenir.
- Yeni outline eski outline'i ezmez.

Revizyon promptu PRESERVE kurali:

Her outline revizyon promptuna degismemesi gereken parcalarin listesi otomatik eklenmeli:

```yaml
preserve:
  - Onaylanan bolum basliklari ve sirasi
  - Kapsam ici olarak isaretlenen tum kavramlar
  - Dogru olan kod/gorsel/alistirma planlari
  - CHAPTER_SPEC kurallari
  - Kapsam disi konular listesi
```

Bu blok promptun basinа sabit olarak eklenir. Amac: LLM'in tum outline'i yeniden yazmak yerine yalnizca belirtilen eksiklikleri gidermesi.

### 4.7. Outline Onayi

Amaç: Tam metin asamasina gecilecek outline surumunu sabitlemek.

Girdi:

- `outline_response`
- `outline_quality_report`

Cikti:

- `approved_outline`
- `active_version.outline`

UI eylemleri:

- Outline'i onayla.
- Onay gerekcesi ekle.
- Onayli surumu kilitle.

Kural:

- Onayli outline dogrudan degistirilmez.
- Degisiklik gerekirse yeni outline surumu olusturulur.

### 4.8. Tam Metin Promptu Uretimi

Amaç: Onayli outline'a gore tam bolum Markdown uretimi icin prompt hazirlamak.

Girdi:

- `book_profile`
- `book_architecture`
- `chapter_seed`
- `approved_outline`
- `chapter_spec.md`
- `sample/sample_chapter.md` referans ozeti

Cikti:

- `full_text_prompt_v001.md`

Prompt kurallari:

- Markdown uret.
- `chapter_spec.md` kurallarina uy.
- Basliklari elle numaralandirma.
- Kod bloklarindan hemen once `CODE_META` uret; metadata'yi kod blogunun icine yazma.
- Her `CODE_META` icin `code_id`, `extension`, `kind`, `title`, `file`, `main_class`, `link`, `qrfile`, `extract`, `test`, `github`, `qr_policy`, `intentional_mismatch`, `validation_mode` alanlarini doldur.
- Bilerek hatali kodlarda `kind: broken_example`, `intentional_mismatch: true`, `mismatch_kind`, `mismatch_summary`, `expected_outcome`, `paired_with`, `validation_mode: review_only`, `test: skip` kullan.
- Duzeltilmis karsiliklarda `kind: fixed_example`, `paired_with`, `intentional_mismatch: false` kullan.
- `MERMAID_META`, `intentional_mismatch`, `paired_with` kurallarini uygula.
- `sample_chapter.md` yapisini hedef kalite ornegi olarak izle.
- Kapsam disi konulari ekleme.

UI eylemleri:

- Tam metin promptu olustur.
- Promptu kopyala.
- Prompt surumunu gor.

### 4.9. Tam Metin Ciktisini Yapistirma

Amaç: Harici LLM'den gelen Markdown bolum taslagini sisteme almak.

Girdi:

- `full_text_prompt`
- harici LLM Markdown ciktisi

Cikti:

- `full_text_response_v001.md`
- `manual_exchange` kaydi

UI eylemleri:

- LLM yanitini yapistir.
- Kaydet.
- On izleme ac.

Kural:

- Yapistirilan ciktı dogrudan `approved_chapter` olmaz.

### 4.10. Normalize / Repair Adayi

Amaç: LLM ciktisindeki mekanik uyumsuzluklari onaydan once islenebilir hale getirmek.

Girdi:

- `full_text_response`
- `chapter_spec.md`

Cikti:

- `normalized_chapter_v001.md`
- `normalization_report`

Normalize edilebilecek ornekler:

- Gorunur `Kod 1`, `Kod 2` gibi baslik numaralarini kaldirma.
- Fazla baslik bosluklarini temizleme.
- `DIAGRAM_META` -> `MERMAID_META` onerisi.
- Eksik front matter alanlarini tamamlama.
- `SECTION_META.order` siralarini onermek.
- `code_id` sablonlarini somutlastirma onerisi.
- Eksik `CODE_META` blogu icin aday metadata uretme.
- Kod blogundan sonra gelen metadata'yi kod blogundan onceye tasima onerisi.
- `CODE_META` icinde eksik `kind`, `main_class`, `test`, `qr_policy`, `expected_stdout_contains` alanlarini isaretleme.

### CODE_META Fallback Tespiti

Normalize adiminda `CODE_META` oncesiz kod bloklari otomatik taranmalidir:

1. Java kodu ise regex ile `public class` adi, `main` metot varligi ve dosya adi adayi tahmin edilir.
2. Aday `code_id`, `file`, `main_class`, `extension` degerleri form olarak sunulur.
3. Yazar degerleri onaylar ya da duzeltir.
4. Onaylanan metadata `normalized_chapter`'a islenir ve `normalization_report` icine `code_meta_auto_suggested` olayi yazilir.

Kural:

- Riskli icerik degisikligi otomatik uygulanmaz; kullanici onayi gerekir.
- Normalize raporu surumlenir.
- `CODE_META` eksikligi onay engeli olarak raporlanir; sistem aday metadata uretse bile kullanici onayi ve validator gecisi gerekir.

### 4.11. Tam Metin Kalite Kontrolu

Amaç: Bolumun yapisal, pedagojik ve teknik kalitesini olcmek.

Girdi:

- `normalized_chapter`
- `chapter_seed`
- `approved_outline`
- `chapter_spec.md`

Cikti:

- `full_text_quality_report`
- issue listesi

Skor kategorileri:

```text
structural_score
chapter_spec_score
outline_compliance_score
mandatory_concepts_score
pedagogical_score
metadata_score
code_score
asset_mermaid_score
export_readiness_score
```

Zorunlu mekanik kontrol:

```powershell
python .\tools\chapter_semantic_validator.py .\path\to\chapter.md
```

UI eylemleri:

- Kalite kontrolu yap.
- Eksikleri gor.
- Revizyon paketi olustur.
- Teknik kontrollere gec.

Kalite kapisi:

- Varsayilan minimum skor `85`.
- `chapter_semantic_validator` error uretirse bolum onaylanamaz.

### 4.12. Tam Metin Revizyon Dongusu

Amaç: Eksikleri LLM'e hedefli aktararak tam metni iyilestirmek.

Girdi:

- `full_text_quality_report`
- `normalized_chapter`

Cikti:

- `full_text_revision_packet`
- yeni `full_text_response`
- yeni `normalized_chapter`

UI eylemleri:

- Revizyon paketini olustur.
- Revizyon promptunu kopyala.
- Yeni LLM ciktisini yapistir.
- Tekrar normalize et.
- Tekrar degerlendir.

Kural:

- Revizyon promptu "tum bolumu yeniden yaz" yerine mumkunse hedefli degisiklik istemelidir.
- Her tam metin revizyon promptuna PRESERVE blogu otomatik eklenmeli:

```yaml
preserve:
  - Onaylanan ve hatasiz tum kod bloklari ve CODE_META'lari
  - Onaylanan MERMAID_META ve SECTION_META bloklari
  - Kapsam ici kavramlarin dogru islendigi paragraflar
  - CHAPTER_SPEC kurallari
  - Kapsam disi konular listesi
changes_only:
  - <issue listesindeki hedefli degisiklikler buraya siralenir>
```

Bu blok promptun basina sabit olarak eklenir; LLM'in degistirmemesi gereken alanlar somut olarak listelenir.

### 4.13. Teknik Kontrol

Amaç: Onay adayi bolumun teknik olarak uretilebilir oldugunu dogrulamak.

Girdi:

- `normalized_chapter`

Cikti:

- `chapter_semantic_report`
- `code_test_report`
- `mermaid_report`
- `asset_report`

Kontroller:

- `CHAPTER_SPEC` validator.
- `CODE_META` extraction.
- Java/Python/JS test adapterleri.
- `review_only` / `intentional_mismatch` kodlarin skip olarak raporlanmasi.
- Mermaid render.
- Screenshot/asset varlik kontrolu.
- QR/link alan kontrolu.

UI eylemleri:

- Teknik kontrolleri calistir.
- Hatalari gor.
- Repair/revizyon paketi olustur.
- Onaya hazirla.

Kalite kapisi:

- Runnable kodlarda kritik derleme/calistirma hatasi varsa onay engellenir.
- Mermaid render zorunlu diyagramlarda basarisizsa onay engellenir.

### Derleyici Hatasi Onarim Paketi

Teknik kontrol asamasinda `javac` veya `java` hata verdiginde sistem otomatik onarim paketi uretmelidir:

1. `javac stderr` ciktisi ayrisitirilir; hata satiri, hata turu ve mesaj cikarilir.
2. Hatali `code_id`, dosya adi ve ham hata mesaji tespit edilir.
3. `code_repair_prompt.md.j2` sablonuna doldurularak onarim promptu uretilir.
4. Kullanici tek tikla promptu kopyalayip LLM'e goturebilir.
5. Duzeltilmis kod yapistirildiktan sonra teknik kontrol otomatik tekrar calisir.

Onarim promptu icerigi:

```text
Hatali kod blogu (oldugu gibi)
javac/java hata mesaji (ham)
Beklenen calisma davranisi (expected_stdout_contains)
CODE_META alanlari (degistirilmemeli)
Talimat: "Yalnizca kodu duzelt; CODE_META, yorum satirlari ve sinif adi degistirme."
```

### 4.14. Bolum Onayi

Amaç: Teknik ve icerik kalite kapilarini gecen surumu onayli bolum yapmak.

Girdi:

- `normalized_chapter`
- kalite raporlari
- teknik raporlar

Cikti:

- `approved_chapter`
- kilitli onay surumu
- `active_version.approved_chapter`

UI eylemleri:

- Onayla.
- Onay notu ekle.
- Onayli surumu kilitle.

Kural:

- `approved_chapter` dogrudan duzenlenmez.
- Degisiklik icin yeni draft surumu uretilir.

### 4.15. Surum Gecmisi ve Geri Alma

Amaç: Degisikliklerin izlenmesi ve geri alinabilmesi.

Girdi:

- herhangi iki artifact surumu

Cikti:

- diff raporu
- restore edilmis yeni aktif surum

UI eylemleri:

- Surumleri listele.
- Iki surumu karsilastir.
- Bu surume don.
- Bu surumden revizyon promptu uret.

Kural:

- Restore islemi eski surumu aktif dosyaya kopyalayıp gecmisi silmez.
- Restore, yeni bir surum ve `restored` event'i uretir.

## 5. Workspace Yapisi

Onerilen bolum calisma alani:

```text
chapters_workspace/
  chapter_03/
    seed/
      seed_v001.yaml
      seed_v002.yaml
    prompts/
      outline_prompt_v001.md
      full_text_prompt_v001.md
    outline_versions/
      outline_v001.md
      outline_v001_report.json
      outline_revision_packet_v001.yaml
      outline_v002.md
      outline_v002_report.json
    draft_versions/
      draft_v001.md
      normalized_v001.md
      draft_v001_report.json
      full_text_revision_packet_v001.yaml
      draft_v002.md
      normalized_v002.md
      draft_v002_report.json
    approved/
      chapter_03_v001.md
    technical_reports/
      code_test_report_v001.json
      mermaid_report_v001.json
      asset_report_v001.json
    version_log.jsonl
    active_version.yaml
```

`active_version.yaml` ornegi:

```yaml
chapter_id: chapter_03
seed: seed_v002
outline: outline_v002
full_text: normalized_v002
approved_chapter: chapter_03_v001
current_step: technical_check_passed
```

## 6. UI Modeli

Bolum Stüdyosu soldan saga isleyen bir is akisi sunmalidir.

Ana alanlar:

```text
Sol panel:
  Bolum listesi (durum ikonu + son skor + sparkline)
  Paralel acik bolum sekmeleri

Orta panel:
  Aktif adim sekmeleri
  Form / editor / paste alani
  Markdown preview (issue highlight destekli)
  Kismi bolum revizyonu butonu (baslik secilince)

Sag panel:
  Kalite raporu
  Issue listesi (triyaj etiketleri: Simdi / Sonra / Kabul)
  Kavram kapsam takipcisi
  Siradaki onerilen eylem
  Surum ozeti + revizyon skor sparkline
```

Sekmeler:

```text
Tohum
Outline Promptu
Outline Ciktisi
Outline Kalite Raporu
Outline Revizyon Paketi
Tam Metin Promptu
Tam Metin Ciktisi
Tam Metin Kalite Raporu
Tam Metin Revizyon Paketi
Teknik Kontrol
Onayli Bolum
Surum Gecmisi
Fark Goruntuleme
```

Yazar teknik YAML yazmak zorunda kalmamalidir; metadata alanlari form olarak sunulmalidir.

### 6.0. On UX Ilkesi

Uretim hizini ve kalitesini artiran 10 temel UX ozelligi:

**1. Issue → Editorde Anlik Vurgulama**
Kalite raporundaki her issue tiklanabilir. Tiklaninca orta panelde o satira atlanir, Markdown preview'da sari/kirmizi highlight gosterilir. `←` `→` ile issue'lar arasi gezinti.

**2. Revizyon Kalite Trend Sparkline**
Her bolum basliginda ve surum gecmisi panelinde surumler arasi skor degisimi mini grafigi:
```
v1:72 → v2:81 → v3:91 ✓
```
Geri gidis kirmizi, ilerleme yesil gosterilir.

**3. Paralel Bolum Sekmeleri**
Birden fazla bolum ayni anda acik olabilir. Bir bolum LLM beklerken diger bolumun seed formu doldurulabirdir. Her sekme bagimsiz state tasir.

**4. Zorunlu Kavram Kapsam Takipcisi**
Tam metin yapistirildiktan sonra `seed.yaml`'daki `mandatory_concepts` listesi otomatik taranir:
```
try-with-resources    ✓ (satir 142)
BufferedWriter        ✓ (satir 98)
FileNotFoundException ✗ Eksik → revizyon paketine ekle
```
Eksik kavramlar tek tikla revizyon paketine eklenir.

**5. Kismi Bolum Revizyonu**
Markdown preview'da bir `## baslik` secilince "Bu Bolumu Revize Et" butonu belirir. Sistem sadece o section + ilgili seed gereksinimleri + CHAPTER_SPEC kurallari ile dar kapsamli bir revizyon promptu uretir.

**6. Pano Akilli Tespiti**
Studio arka planda klipboardi izler. Icerik LLM yanitina benziyorsa (Markdown + yeterli uzunluk) ekran kosesinde toast:
```
"Panoda LLM yaniti var — yapistir?"  [Evet] [Hayir]
```

**7. Issue Triyaji**
Her issue icin 3 etiket:
- 🔴 Simdi Duzelt → revizyon paketine gir; onay engeli
- 🟡 Sonra Duzelt → bir sonraki revizyonda ele al
- ⚪ Kabul Edilebilir → gerekcesiyle override event yaz; dashboard'da izlenir

**8. Odak (Zen) Yazma Modu**
`F11` ile tum paneller kapanir; sadece orta editör + minimal arac cubugu kalir. `Esc` ile normal görünüme don.

**9. Canli Build Akisi + Asset Galerisi**
Build sirasinda pandoc/mmdc ciktisi SSE ile satir satir akar; her adim yesil tik veya kirmizi hata ikonu alir. Yan panelde QR/Mermaid/screenshot kutucuklari hangi bolumden geldigi etiketiyle gosterilir.

**10. Kitap Saglik Skoru**
Dashboard'da bilesik skor:
```
Kitap Saglik Skoru: 74 / 100

Bolum Ilerlemesi  ██████░░░░  60%  (15/25 onayli)
Ortalama Kalite   ████████░░  82/100
Teknik Kontrol    ███████░░░  70%  (hatali 2 kod)
Bloklu Bolumler   ██░░░░░░░░  3 adet
Export Hazirlik   ██████░░░░  60%
```
Her metrige tiklaninca ilgili rapora gidilir.

## 6.1. Workflow Hizlandiricilari

Arayuzun ana hedefi, yazarin uretim hizini artirirken kalite kapilarini zayiflatmamaktir. Bu nedenle sistem her adimda yazara "siradaki en mantikli is"i gostermelidir.

### Akilli On Doldurma

Bolum tohumlama ekrani bos form olarak acilmamalidir. Sistem `book_profile`, `book_architecture`, onceki bolumler ve secili kitap turu presetinden alanlari onermelidir.

On doldurulabilecek alanlar:

- Bolum amaci.
- On kosullar.
- Ogrenme ciktilari.
- Zorunlu kavramlar.
- Kod ornegi adaylari.
- Bilerek hatali ornek adaylari.
- Mini uygulama fikri.
- Sik yapilan hata adaylari.
- Laboratuvar gorevi taslagi.
- Kapsam disi konu adaylari.

Kural:

- On doldurulan alanlar kullanici onayi almadan kesinlesmis sayilmaz.
- Sistem hangi alanin nereden on dolduruldugunu gostermelidir.

### Tek Tik Prompt Uretimi

Yazar prompt muhendisligi yapmak zorunda kalmamalidir.

Tek tik uretilecek promptlar:

- Outline promptu.
- Outline revizyon promptu.
- Tam metin promptu.
- Tam metin revizyon promptu.
- Kod repair promptu.
- Metadata repair promptu.
- Teknik hata repair promptu.

Prompt uretildiginde:

- Prompt surumlenir.
- Kopyalama eylemi kaydedilir.
- Promptun hangi artifact ve kurallardan uretildigi gorulebilir.

### Paste Sonrasi Otomatik Analiz

LLM ciktisi yapistirildigi anda sistem arka planda ilk kontrolleri calistirmalidir.

Otomatik kontroller:

- Baslik hiyerarsisi.
- Zorunlu bolum bloklari.
- Gorunur manuel numaralandirma.
- `CODE_META` varligi.
- `CODE_META` bloklarinin kod blogundan hemen once bulunmasi.
- `CODE_META` zorunlu alanlarinin dolu olmasi.
- `MERMAID_META` varligi.
- `intentional_mismatch` / `paired_with` tutarliligi.
- Kapsam disi konu sinyalleri.
- Eksik zorunlu kavramlar.

Sonuc:

- Hemen gorunen on skor.
- Issue listesi.
- "Normalize Et" onerisi.
- "Revizyon Paketi Olustur" onerisi.

### Metadata Formlari

Yazar `CODE_META`, `MERMAID_META` veya `SCREENSHOT_META` bloklarini elle yazmak zorunda kalmamalidir.

Kod bloklari otomatik algilanmali ve sag panelde form olarak duzenlenmelidir:

```text
code_id
kind
file
main_class
validation_mode
test
intentional_mismatch
mismatch_kind
paired_with
expected_stdout_contains
github
qr_policy
```

Kural:

- Form degisikligi Markdown metadata bloguna yansitilir.
- Hatalı ornek secildiginde `mismatch_*`, `expected_outcome`, `paired_with` alanlari zorunlu hale gelir.

### Guvenli Normalize

Normalize adimi yazar hizini ciddi artirir; ancak riskli degisiklikleri sessizce yapmamalidir.

Guvenli otomatik duzeltmeler:

- `Kod 1:` basligini `Kod:` bicimine cevirme.
- Fazla baslik bosluklarini temizleme.
- `DIAGRAM_META` icin `MERMAID_META` onerisi.
- Eksik front matter onerileri.
- Somut `code_id` uretme.
- `paired_with` adaylari onerme.
- `file` ve `main_class` uyumsuzluklarini isaretleme.

Kural:

- Mekanik ve dusuk riskli duzeltmeler tek tikla uygulanabilir.
- Icerik anlamini degistirecek duzeltmeler oneridir; kullanici onayi gerekir.

### Revizyon Paketi Otomasyonu

Dusuk skor veya eksik tespitinde sistem issue listesini otomatik gruplamali ve LLM'e tasinabilir revizyon paketine cevirmelidir.

Gruplama ornekleri:

- Eksik zorunlu kavramlar.
- Kapsam ihlalleri.
- Pedagojik akis sorunlari.
- Metadata eksikleri.
- Kod/test sorunlari.
- Asset/Mermaid sorunlari.

Revizyon promptu su ilkeyi izlemelidir:

```text
Dogru kisimlari koru.
Sadece belirtilen eksikleri hedefli olarak duzelt.
CHAPTER_SPEC kurallarini degistirme.
Kapsam disi konulari ekleme.
```

### Kisayol Is Akislari

Tekil butonlar yerine sik kullanilan is zincirleri sunulmalidir.

Onerilen is zinciri dugmeleri:

```text
Outline'i Degerlendir ve Revizyon Paketi Hazirla
Tam Metni Normalize Et ve Kontrol Et
Metadata Eksiklerini Bul ve Onar
Kavram Kapsami Kontrol Et
Teknik Kontrolleri Calistir
Onaya Hazirla
Surumleri Karsilastir
En Iyi Surumu Sec
```

### Klavye Kisayollari

Guc kullanicilari icin klavye kisayol katmani:

```text
Ctrl+Enter      → Aktif adimi calistir (evaluate / normalize / check)
Ctrl+K          → Promptu panoya kopyala
Ctrl+Shift+V    → LLM yanitini yapistir (Pano tespiti ile)
Ctrl+R          → Revizyon paketi uret
Ctrl+Shift+A    → Bolumu onayla
Ctrl+Z          → Bir onceki surum (version restore)
F11             → Odak (Zen) modu ac/kapat
← / →           → Issue'lar arasi gezinti (rapor paneli aktifken)
Ctrl+Tab        → Acik bolum sekmeleri arasi gecis
Ctrl+F          → Bolum ici arama
```

### Preset ve Sablon Sistemi

Kitap turune gore hazir presetler bulunmalidir.

Ilk preset adaylari:

- Java/programlama kitabi.
- Veri bilimi kitabi.
- Web gelistirme kitabi.
- Akademik ders kitabi.
- Laboratuvar kitabi.

Preset su alanlari belirleyebilir:

- Standart bolum yapisi.
- Zorunlu kalite kapilari.
- Kod test varsayilanlari.
- Asset/screenshot beklentileri.
- Varsayilan skor esikleri.
- Prompt sablonlari.

### Surum Karsilastirma Hizlandiricilari

Surum gecmisi sadece arsiv degil, karar destek araci olmalidir.

Arayuz sunlari gostermelidir:

- Skor degisimi.
- Cozulen issue sayisi.
- Yeni eklenen issue sayisi.
- Markdown diff.
- Teknik test durum degisimi.
- "Bu surum daha iyi gorunuyor" onerisi.

### Dashboard

Kitap duzeyinde hizli karar icin dashboard gereklidir.

Gosterilecek metrikler:

- Planlanan bolum sayisi.
- Tohumlanan bolum sayisi.
- Outline onayli bolum sayisi.
- Tam metin onayli bolum sayisi.
- Teknik kontrolden gecen bolum sayisi.
- Bloklu bolumler.
- Ortalama kalite skoru.
- En cok tekrar eden issue tipleri.

### LLM Saglayici Analizi

`manual_exchange` kayitlari kullanilarak saglayici bazinda kalite analizi dashboard'da sunulacak:

| Saglayici | Ort. Outline Skoru | Ort. Tam Metin Skoru | Ort. Revizyon Sayisi |
|-----------|--------------------|----------------------|----------------------|
| ChatGPT   | —                  | —                    | —                    |
| Claude    | —                  | —                    | —                    |
| Gemini    | —                  | —                    | —                    |

Bu tablo yazar icin hangi LLM'in bu kitap turu ve preset icin daha iyi sonuc verdigini gosterir. Dashboard'da isteğe bagli filtre olarak sunulur; veri birikmeden once bos goruntulenir.

## 6.2. Sonraki En Mantikli Is Kuralı

Arayuz her zaman tek bir ana onerilen eylem gostermelidir.

Ornekler:

| Durum | Onerilen ana eylem |
|---|---|
| `seeded` | `Outline Promptu Olustur` |
| `outline_prompt_ready` | `Promptu Kopyala` |
| `outline_pasted` | `Outline'i Degerlendir` |
| `outline_revision_required` | `Revizyon Paketi Olustur` |
| `outline_approved` | `Tam Metin Promptu Olustur` |
| `full_text_pasted` | `Normalize Et ve Kontrol Et` |
| `full_text_revision_required` | `Tam Metin Revizyon Paketi Olustur` |
| `technical_check_failed` | `Teknik Hata Paketini Olustur` |
| `technical_check_passed` | `Bolumu Onayla` |

## 7. CLI Karsiliklari

Ilk CLI komutlari:

```powershell
bookmaker chapter seed chapter_03
bookmaker chapter prompt outline chapter_03
bookmaker chapter paste outline chapter_03
bookmaker chapter evaluate outline chapter_03
bookmaker chapter revision outline chapter_03
bookmaker chapter approve outline chapter_03
bookmaker chapter prompt draft chapter_03
bookmaker chapter paste draft chapter_03
bookmaker chapter normalize chapter_03
bookmaker chapter evaluate draft chapter_03
bookmaker chapter check technical chapter_03
bookmaker chapter approve chapter_03
bookmaker version list chapter_03
bookmaker version diff chapter_03 draft_v001 draft_v002
bookmaker version restore chapter_03 draft_v001
```

Mevcut validator:

```powershell
python .\tools\chapter_semantic_validator.py .\sample\sample_chapter.md
```

## 8. Kalite Kapilari

| Gate | Minimum | Bloklayan durum |
|---|---:|---|
| Seed approval | manuel onay | amac veya zorunlu kavramlar yok |
| Outline quality | 80 | kapsam disi konu, eksik ana kavram |
| Full text quality | 85 | `CHAPTER_SPEC` hatasi, outline uyumsuzlugu |
| Code execution | 95% pass | runnable kod derlenmiyor |
| Mermaid/assets | 100% required pass | zorunlu diyagram/gorsel uretilemiyor |
| Final approval | kullanici onayi | teknik veya icerik kapisi bloklu |

Manual override:

- Bloklayan teknik hata override edilememeli.
- Icerik skoru override edilecekse gerekce zorunlu olmali.
- Override event olarak kaydedilmeli.

## 9. Acik Kararlar

1. Ilk runtime state dosya tabanli YAML/JSONL mi olacak, yoksa SQLite mi?
2. Diff ilk surumde satir bazli Markdown diff olarak mi kalacak?
3. Onayli surum kilitleme sadece uygulama seviyesinde mi olacak, yoksa dosya izinleriyle de desteklenecek mi?
4. Normalize adimi otomatik patch uygulayabilecek mi, yoksa ilk surumde sadece oneriler mi sunacak?
5. Outline ve full text semantik kalite skorunun ilk surumu tamamen deterministik mi olacak?
