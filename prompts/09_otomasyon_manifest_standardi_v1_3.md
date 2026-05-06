# Java'nın Temelleri — Otomasyon Manifest Standardı v1.3

Bu belge, v1.3 üretim hattında kullanılacak manifest dosyalarının amacını ve asgari alanlarını tanımlar.

---

## 1. Temel ilke

Üretim hattında tek otorite `book_manifest.yaml` olmalıdır. Bölüm sırası, görünen bölüm numarası ve çıktı üretim ayarları bu dosyadan okunur.

Kaynak Markdown dosyaları içerik ve meta varlık bilgisi taşır; nihai görünüm build sırasında belirlenir.

---

## 2. book_manifest.yaml

```yaml
book:
  title: "Java'nın Temelleri"
  subtitle: "Bilgisayar Mühendisliği Öğrencileri İçin Temel Programlama, Konsol ve GUI Uygulamaları"
  author: "İsmail Kırbaş"
  lang: "tr-TR"
  numbering_policy: "build_time"
  automation_profile: "java_book_v1_3"

paths:
  chapters_dir: "chapters"
  assets_auto: "assets/auto"
  assets_manual: "assets/manual"
  assets_locked: "assets/locked"
  assets_final: "assets/final"
  build_dir: "build"
  dist_dir: "dist"

pandoc:
  reference_doc: "templates/referenceV14_java_temelleri.docx"
  lua_filter: "filters/styles_revised_v14.lua"
  input_format: "markdown+tex_math_single_backslash"

repository:
  owner: "bmdersleri"
  repo: "javaninTemelleri"
  branch: "main"
  code_root: "kodlar"
  pages_root: "https://bmdersleri.github.io/javaninTemelleri"
  raw_root: "https://github.com/bmdersleri/javaninTemelleri/blob/main"

chapters:
  - order: 1
    chapter_id: "java-giris"
    source: "chapters/java-giris.md"
    title: "Java’ya Giriş ve Programlama Mantığı"
    github_slug: "java-giris"
```

---

## 3. code_manifest.json

Kod ayıklama aşamasında üretilir.

```json
{
  "code_id": "karar-yapilari_kod01",
  "chapter_id": "karar-yapilari",
  "display_chapter_no": 8,
  "display_code_no": "8.1",
  "kind": "example",
  "title": "Temel if kullanımı",
  "source_markdown": "chapters/karar-yapilari.md",
  "java_file": "build/code/kodlar/karar-yapilari/kod01/TemelIfKullanimi.java",
  "mainClass": "TemelIfKullanimi",
  "extract": true,
  "test": "compile",
  "compile_status": "passed",
  "github": true,
  "qr": "dual"
}
```

---

## 4. asset_manifest.json

Görsel çözümleme aşamasında üretilir.

```json
{
  "asset_id": "karar-yapilari_diyagram01",
  "chapter_id": "karar-yapilari",
  "type": "mermaid",
  "title": "Karar yapılarında program akışı",
  "auto_path": "assets/auto/mermaid/karar-yapilari_diyagram01.png",
  "manual_path": "assets/manual/mermaid/karar-yapilari_diyagram01.png",
  "locked_path": "assets/locked/mermaid/karar-yapilari_diyagram01.png",
  "final_path": "assets/final/mermaid/karar-yapilari_diyagram01.png",
  "selected_source": "manual",
  "manual_override": true,
  "width_cm": 12.5
}
```

---

## 5. qr_manifest.json

QR üretim aşamasında üretilir.

```json
{
  "code_id": "karar-yapilari_kod01",
  "chapter_id": "karar-yapilari",
  "source_url": "https://github.com/bmdersleri/javaninTemelleri/blob/main/kodlar/karar-yapilari/kod01/TemelIfKullanimi.java",
  "page_url": "https://bmdersleri.github.io/javaninTemelleri/kodlar/karar-yapilari/kod01/TemelIfKullanimi.html",
  "qr_source_path": "assets/final/qr/source/karar-yapilari_kod01.png",
  "qr_page_path": "assets/final/qr/page/karar-yapilari_kod01.png",
  "qr_policy": "dual",
  "status": "created"
}
```

---

## 6. Kimlik kuralları

- `chapter_id`: küçük harf, Türkçe karakter yok, boşluk yok, tire kullanılabilir.
- `code_id`: `{chapter_id}_kodNN`, `{chapter_id}_hataNN`, `{chapter_id}_miniuygulamaNN`.
- `asset_id`: `{chapter_id}_diyagramNN`, `{chapter_id}_screenshotNN`, `{chapter_id}_figureNN`.
- Dosya adlarında Türkçe karakter ve boşluk kullanılmamalıdır.
