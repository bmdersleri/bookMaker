# Java'nın Temelleri — Pipeline Kalite Kapıları v1.3

Bu belge, üretim hattında hangi aşamada hangi kontrollerin yapılacağını tanımlar.

---

## 1. Aşama tablosu

| Aşama | Ön kontrol | Son kontrol | Durdurucu hata örneği |
|---|---|---|---|
| `validate` | Kaynak dosyalar var mı? | YAML ve meta bloklar doğru mu? | `chapter_id` eksik |
| `merge` | Manifest sırası var mı? | Birleşik MD oluştu mu? | Aynı `chapter_id` iki kez var |
| `render-mermaid` | Mermaid CLI var mı? | PNG dosyaları oluştu mu? | Mermaid parse hatası |
| `extract-code` | `CODE_META` var mı? | Java dosyaları oluştu mu? | `file` alanı eksik |
| `test-code` | JDK var mı? | Kodlar derlendi mi? | Derlenmesi gereken kod hatalı |
| `push-github` | Git repo hazır mı? | URL manifesti oluştu mu? | Commit/push başarısız |
| `generate-qr` | URL'ler kesin mi? | QR dosyaları oluştu mu? | QR decode doğrulaması başarısız |
| `resolve-assets` | Auto/manual/locked klasörleri var mı? | Final görseller seçildi mi? | Gerekli final görsel yok |
| `build-docx` | Pandoc, reference docx, Lua filter var mı? | DOCX oluştu mu? | Pandoc çıkış kodu sıfır değil |
| `package` | Dist dosyaları var mı? | ZIP oluştu mu? | DOCX eksik |

---

## 2. Durdurucu hatalar

Aşağıdaki durumlarda üretim durmalıdır:

- YAML front matter yok.
- `chapter_id` yok veya yineleniyor.
- Kaynak Markdown'da manuel `# Bölüm X:` başlığı var.
- Alt başlıklarda manuel `X.1`, `X.2` numarası var.
- Derlenecek Java kodunda `file` ve `mainClass` uyumsuz.
- `kind: broken_example` olduğu hâlde `test: compile` verilmiş.
- Mermaid bloğu var ama `MERMAID_META` yok.
- Final görsel yolu eksik.
- GitHub URL boş olduğu hâlde QR üretilmeye çalışılmış.
- Pandoc reference DOCX veya Lua filter bulunamıyor.

---

## 3. Uyarılar

Aşağıdaki durumlarda üretim devam edebilir; ancak rapora uyarı yazılmalıdır:

- Bölümde Mermaid yok.
- Bölümde QR üretilecek kod yok.
- Bazı kod örnekleri `snippet` olduğu için test edilmedi.
- Manuel görsel otomatik görselden eski tarihli.
- Kod satırı 90 karakteri aşıyor.
- Tablo çok geniş olabilir.

---

## 4. Dry-run modu

Hiçbir dosya yazmadan doğrulama yapmak için:

```bash
python tools/book_pipeline.py validate --dry-run
```

---

## 5. Raporlama dosyaları

```text
build/reports/chapter_validation_report.md
build/reports/merge_report.md
build/reports/mermaid_report.md
build/reports/java_extract_report.md
build/reports/java_compile_report.md
build/reports/github_report.md
build/reports/qr_report.md
build/reports/asset_resolution_report.md
build/reports/pandoc_report.md
build/reports/final_build_report.md
```
