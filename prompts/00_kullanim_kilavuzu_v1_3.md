# Java'nın Temelleri — v1.3 Otomasyon Uyumlu Prompt Paketi Kullanım Kılavuzu

**Sürüm:** 1.3  
**Durum:** Otomasyon uyumlu üretim paketi  
**Amaç:** Bölüm üretimi, birleştirme, Mermaid PNG üretimi, Java kod ayıklama, GitHub aktarımı, çift QR üretimi, manuel görsel önceliği ve Pandoc/DOCX üretimi için bölüm metinlerini baştan makine tarafından ayrıştırılabilir hâle getirmek.

---

## 1. v1.3 güncellemesinin amacı

v1.2 paketi, bölüm metinlerinin Pandoc/DOCX uyumlu ve pedagojik olarak tutarlı üretilmesini hedefliyordu. v1.3 ile bu yapıya aşağıdaki otomasyon ilkeleri eklenmiştir:

1. Bölüm, alt başlık, şekil, tablo, diyagram ve kod numaraları **Markdown üretimi sırasında elle verilmez**; üretim hattında `book_manifest.yaml` sırasına göre atanır.
2. Her bölüm değişmeyen bir `chapter_id` taşır.
3. Java kodları `CODE_META` bloklarıyla işaretlenir.
4. Mermaid diyagramları `MERMAID_META` bloklarıyla işaretlenir.
5. Ekran görüntüleri ve özel görseller `ASSET_META` bloklarıyla işaretlenebilir.
6. Kullanıcı tarafından elle düzenlenmiş görseller, otomatik üretilen görsellere göre önceliklidir.
7. Hatalı kod örnekleri derleme/test hattından açıkça hariç tutulabilir.
8. GitHub ve QR üretimi, tahmine dayalı dosya arama yerine manifest üzerinden yapılır.
9. Tüm üretim aşamaları raporlanabilir ve tekrar çalıştırılabilir olmalıdır.

---

## 2. Paket mantığı

v1.3 paketi dört katmanlıdır:

1. **İçerik üretim katmanı:** Ana sistem promptu, çıktı format standardı ve bölüm girdi şablonu.
2. **Otomasyon işaretleme katmanı:** `CODE_META`, `MERMAID_META`, `ASSET_META`, `TABLE_META` ve `QR` politikası.
3. **Manifest katmanı:** `book_manifest.yaml`, `code_manifest.json`, `asset_manifest.json`, `qr_manifest.json`.
4. **Yayın hattı katmanı:** doğrulama, birleştirme, görsel çözümleme, kod ayıklama, test, GitHub, QR, Pandoc ve ZIP paketleme.

---

## 3. Önerilen proje klasör yapısı

```text
java_temelleri_pipeline/
├── config/
│   ├── book_manifest.yaml
│   ├── pandoc_config.yaml
│   └── github_config.yaml
├── chapters/
├── assets/
│   ├── auto/
│   ├── manual/
│   ├── locked/
│   └── final/
├── build/
├── dist/
└── tools/
```

`assets/manual/` ve `assets/locked/` klasörleri hiçbir otomatik temizlik işleminde silinmemelidir.

---

## 4. Bölüm üretim sırası

1. `02_ana_sistem_promptu_java_temelleri_v1_3.md` modele verilir.
2. `03_cikti_format_standardi_v1_3.md` eklenir.
3. Gerekiyorsa `05_bolum_yapisi_standardi_v1_3.md` eklenir.
4. İlgili bölüm için v1.3 uyumlu bölüm girdi dosyası verilir.
5. Model önce ayrıntılı outline üretir.
6. Onay sonrası tam bölüm metni Markdown olarak üretilir.
7. Bölüm metni numarasız başlıklarla ve meta bloklarla kaydedilir.
8. Üretim hattı bölümün numarasını, kod numarasını, diyagram numarasını ve QR bağlantılarını build sırasında atar.

---

## 5. Markdown başlık ilkesi

Doğru:

```markdown
# Karar Yapıları: if, else-if ve switch

## Bölümün yol haritası
## Öğrenme çıktıları
```

Yanlış:

```markdown
# Bölüm 8: Karar Yapıları: if, else-if ve switch

## 8.1 Bölümün yol haritası
```

---

## 6. Manuel görsel önceliği

Öncelik sırası:

1. `assets/manual/`
2. `assets/locked/`
3. `assets/auto/`
4. kaynak Mermaid/görsel tanımı

Aynı ID ile manuel görsel varsa final DOCX üretiminde manuel sürüm kullanılmalıdır.

---

## 7. Tek komutla üretim

```bash
python tools/book_pipeline.py release --config config/book_manifest.yaml
```

Ara aşamalar ayrıca çalıştırılabilmelidir:

```bash
python tools/book_pipeline.py validate
python tools/book_pipeline.py merge
python tools/book_pipeline.py render-mermaid
python tools/book_pipeline.py extract-code
python tools/book_pipeline.py test-code
python tools/book_pipeline.py resolve-assets
python tools/book_pipeline.py generate-qr
python tools/book_pipeline.py build-docx
python tools/book_pipeline.py package
```
