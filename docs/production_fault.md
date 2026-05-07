# PRODUCTION_FAULT.md — Production Pipeline Hata ve Problem Kaydı

> **TARIHI KAYIT.** Tum sorunlar cozuldu. Eski `tools/book_pdf_v3.py`, `book_production.py` script'leri ve deepseek branch donemine aittir.

**Proje:** bookMaker | **Tarih:** 2026-05-04 | **Branch:** deepseek (tarihi)
**Durum:** Güncel — PDF çıktısı başarılı (339 sayfa), 4 açık hata, 10 çözülmüş hata

---

## Genel Bakış

Production pipeline üç aşamalıdır:
1. **Mermaid → PNG** (book_production.py) — 58 Mermaid diyagramı işlenir
2. **MD + DOCX** (book_build.py) — 27 bölüm birleştirilir, pandoc ile DOCX
3. **PDF** (book_pdf_v3.py) — Placeholder temizleme + Mermaid → PNG + pandoc/xelatex

---

## AÇIK HATALAR

### PF-001: ✅ 4/58 Mermaid PNG Eksik (ÇÖZÜLDÜ — bkz: FAULT.md F-007)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟡 Orta |
| **Çözüm tarihi** | 2026-05-04 |
| **Çözüm detayı** | `fault.md` → F-007 |

**Sorun:** 4 Mermaid bloğu mmdc ile render edilemedi (mermaid-008, 021, 026, 031). Sebepler: Mermaid'de özel anlamlı karakterler (`()`, `"`, `<br/>`).

**Çözüm (3 aşamalı):**
1. `.mmd` dosyaları manuel düzeltildi → geçerli Mermaid sözdizimi (quote'lanmış düğüm metinleri)
2. Tüm 4 blok `mmdc` ile yeniden render edildi → 58/58 PNG başarılı
3. Kaynak bölüm dosyaları (`draft_versions/v001.md`) kalıcı olarak düzeltildi

**Sonuç:** 58/58 Mermaid diyagramı başarıyla render edildi. Toplam PNG: ~1,060 KB.

---

### PF-002: Placeholder Resimler (5 Adet)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟢 Düşük |
| **Etkilediği** | PDF (çözüldü), orijinal markdown |
| **Kaynak** | LLM üretimi — `via.placeholder.com` URL'leri |

**Belirti:** Markdown'da 5 adet `via.placeholder.com` resim referansı:
- `![Başlangıç/Bitiş](https://via.placeholder.com/50x30/4CAF50/FFFFFF?text=Oval)`
- `![İşlem](https://via.placeholder.com/50x30/2196F3/FFFFFF?text=Dikdörtgen)`
- `![Karar](https://via.placeholder.com/50x30/FF5722/FFFFFF?text=EşkenarDörtgen)`
- `![Girdi/Çıktı](https://via.placeholder.com/50x30/9C27B0/FFFFFF?text=Paralelkenar)`
- `![Ok](https://via.placeholder.com/50x30/FFC107/000000?text=→)`

**Etki:** Pandoc bu URL'leri fetch etmeye çalışır, başarısız olur ve PDF'te "image with description" yazar. DOCX'te de aynı sorun.

**Çözüm (PDF):** `book_pdf_v3.py`'de regex ile temizlenir:
```python
pattern = re.compile(r'!\[.*?\]\(https?://[^)]*placeholder[^)]*\)')
content, count = pattern.subn('', content)
```

**Öneri:** Bu placeholder'ları gerçek Mermaid diyagramları veya görsellerle değiştir.

---

### PF-003: Bölüm Uzunluğu Dengesiz (F-008 ile aynı)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟡 Orta |
| **Etkilediği** | PDF sayfa dağılımı, okuma deneyimi |

**Ölçüm:** Bölüm başına karakter sayısı 11,535 — 47,019 arasında değişiyor. En kısa (B6: 11,535c) ile en uzun (B19: 47,019c) arasında **4 kat fark**.

**PDF Etkisi:** 339 sayfada bölümler arası sayfa dağılımı dengesiz — bazı bölümler 5 sayfa, bazıları 20+ sayfa.

---

### PF-004: PDF Sayfa Sayısı Tespit Edilemiyor (Binary PDF)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟢 Düşük |
| **Etkilediği** | Sadece otomatik doğrulama |

**Belirti:** XeLaTeX üretilen PDF'de `\Type \Page` entry'leri binary (object stream) içinde sıkıştırılmış. Basit regex ile sayfa sayısı bulunamıyor. `pdfinfo` gibi harici araçlar gerekiyor.

**Mevcut Çözüm:** `pdfinfo.exe` kullanarak sayfa sayısı alınıyor:
```powershell
pdfinfo D:\path\to\file.pdf | Select-String "Pages:"
# Çıktı: Pages: 339
```

---

## ÇÖZÜLEN HATALAR

### PF-101: ✅ LaTeX `\n` Kontrol Karakteri Hatası (ÇÖZÜLDÜ)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🔴 Kritik |
| **Çözüm tarihi** | 2026-05-04 |
| **İlgili dosya** | `tools/book_pdf_v3.py` — `sanitize_for_latex()` |

**Belirti:** Pandoc + xelatex ile PDF üretirken:
```
! Undefined control sequence.
l.1134 ... & 16 bit & Tek karakter & 'A', '5', '\n
```

**Sebep:** Markdown içinde tablo hücrelerinde `\n` karakteri geçiyor. LaTeX bunu kontrol dizisi olarak algılıyor.

**Çözüm:** `sanitize_for_latex()` fonksiyonu eklendi. Kod blokları dışındaki `\n` karakterleri `\\textbackslash{}n` ile değiştirilir (veya `\\n` olarak escape edilir).

**Kritik Detay:** 
- Kod blokları (` ``` `) içindeki `\n`'lere dokunulmaz
- Inline code (`` ` ` ``) içindekilere dokunulmaz
- Sadece düz metindeki `\n`'ler temizlenir (tablolar, paragraflar)

---

### PF-102: ✅ Font "Arial Mono" Bulunamadı (ÇÖZÜLDÜ)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟠 Önemli |
| **Çözüm tarihi** | 2026-05-04 |
| **İlgili dosya** | `tools/book_pdf_v3.py` — `generate_pdf()` |

**Belirti:**
```
! Package fontspec Error: The font "Arial Mono" cannot be found
```

**Sebep:** PowerShell ile script düzenlenirken PANDOC_OPTS satırı bozuldu:
```python
# HATALI (PowerShell replace sonucu):
"mainfont=Arial" -V "monofont="
"-V", "monofont=Arial Mono",
```

**Çözüm:** Monofont tamamen kaldırıldı, sadece mainfont kullanıldı:
```python
"-V", "mainfont=Arial",
```

**Ders:** PowerShell'de Python dosyası düzenlerken her satırı ayrı ayrı kontrol et. Script bozulabilir.

---

### PF-103: ✅ Python cp1254 Encoding Hatası (ÇÖZÜLDÜ)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟠 Önemli |
| **Çözüm tarihi** | 2026-05-04 |
| **Etkilediği** | Tüm Python -> PowerShell stdout |

**Belirti:**
```
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 2705
```

**Sebep:** Windows varsayılan kodlaması cp1254 (Turkish). Python'un subprocess `_readerthread`'i stdout'u cp1254 ile decode etmeye çalışır, ancak PDF binary çıktısı veya UTF-8 karakterleri cp1254'te tanımlı değil.

**Etkisi:**
- `subprocess.run(capture_output=True, text=True)` hata fırlatır
- Özellikle pandoc/xelatex çıktılarında görülür
- PDF binary stream'leri okunamaz

**Çözümler:**
1. `capture_output=True, text=True` yerine `capture_output=True` (bytes) kullan
2. veya `PYTHONIOENCODING=utf-8` ortam değişkeni
3. veya `subprocess.PIPE` ile elle kontrol

**Geçici:** `process` tool ile poll yaparak hata bastırılabilir (thread exception, process devam eder).

---

### PF-104: ✅ WeasyPrint GTK Bağımlılığı (ÇÖZÜLDÜ - Alternatif Kullanıldı)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟠 Önemli |
| **Çözüm tarihi** | 2026-05-04 |
| **İlgili** | `tools/book_pdf_v2.py` (iptal edildi) |

**Belirti:**
```
OSError: cannot load library 'libgobject-2.0-0': error 0x7e
```

**Sebep:** WeasyPrint Windows'ta GTK (GLib/GObject/Pango/Cairo) kütüphanelerine ihtiyaç duyar. GTK kurulumu olmadan çalışmaz.

**Çözüm:** WeasyPrint yaklaşımı tamamen terk edildi. Bunun yerine **pandoc + xelatex** kullanıldı.

**Not:** WeasyPrint Linux/macOS'te sorunsuz çalışır. Windows'ta GTK kurulumu mümkün ama zahmetli:
1. GTK3 runtime indir (https://github.com/tschoonj/GTK-for-Windows)
2. PATH'e ekle
3. DLL'leri manuel kopyala

---

### PF-105: ✅ Markdown'da Mermaid Blokları PNG'ye Dönüşmemiş (ÇÖZÜLDÜ)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🔴 Kritik |
| **Çözüm tarihi** | 2026-05-04 |

**Belirti:** `build/output/java-programlamaya-giris.md` dosyasında 58 Mermaid kodu bloğu var, ancak **hiçbiri PNG referansına dönüşmemiş**. 54 PNG dosyası `images/` klasöründe hazır duruyor ama kullanılmamış.

**Sebep:** `book_production.py` (eski adı: book_build.py) sadece Mermaid PNG'leri üretiyor, ama birleştirilmiş markdown'da Mermaid bloklarını PNG'ye çevirmiyor.

**Çözüm:** `book_pdf_v3.py`'de preprocessing aşaması eklendi:
1. Markdown'ı oku
2. Her ` ```mermaid ` bloğunu bul
3. Karşılık gelen PNG varsa, `![Mermaid Diyagramı N](abs_path)` ile değiştir
4. PNG yoksa (4 adet - PF-001), blok olarak bırak

```python
while i < len(lines):
    if line.strip().startswith('```') and 'mermaid' in line.strip().lower():
        png_path = IMAGES_DIR / f"mermaid-{block_num:03d}.png"
        if png_path.exists():
            abs_path = str(png_path.resolve())
            new_lines.append(f'![Mermaid Diyagramı {block_num}]({abs_path})')
            converted_count += 1
        else:
            # Blok olarak bırak
    i += 1
```

---

### PF-106: ✅ Pandoc +raw_tex Uzantısı Sorunu (ÇÖZÜLDÜ)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟠 Önemli |
| **Çözüm tarihi** | 2026-05-04 |

**Belirti:** `-f markdown+raw_tex` kullanıldığında, markdown içindeki `\n` geçişleri LaTeX'e ham olarak aktarılıyor.

**Çözüm:** `+raw_tex` kaldırıldı, sadece `-f markdown` kullanıldı. Bu sayede pandoc tüm özel karakterleri otomatik escape ediyor.

---

### PF-107: ✅ Resim Yolları Relative/Absolute Karışıklığı (ÇÖZÜLDÜ)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟠 Önemli |
| **Çözüm tarihi** | 2026-05-04 |

**Belirti:** İlk denemede `os.path.relpath(png_path, OUTPUT_DIR)` kullanıldı, pandoc farklı bir dizinden çalıştırılınca resimler bulunamadı:
```
[WARNING] Could not fetch resource images\mermaid-054.png
```

**Çözüm:** Absolute path kullanıldı:
```python
abs_path = str(png_path.resolve())  # D:\bookMaker_Deepseek\build\output\images\mermaid-001.png
```

Bu sayede pandoc hangi dizinden çalıştırılırsa çalıştırılsın resimler bulunur.

---

### PF-108: ✅ Python Subprocess Çıktı Tamponlaması (ÇÖZÜLDÜ)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟢 Düşük |
| **Çözüm tarihi** | 2026-05-04 |

**Belirti:** Uzun süren pandoc işlemlerinde (3-5 dk) `subprocess.run()` hiç çıktı üretmez, sonra aniden tüm çıktı gelir. Kullanıcı işlemin canlı olup olmadığını anlayamaz.

**Sebep:** Python'un stdout tamponlaması. Pandoc/xelatex stderr'e yazdığı için `capture_output=True` ile toplanan çıktı işlem bitene kadar gelmez.

**Çözüm:**
1. `PYTHONUNBUFFERED=1` ortam değişkeni
2. veya `python -u` flag'i
3. veya `subprocess.PIPE` ile canlı okuma (thread)

**Not:** Batch/Pipeline script'lerinde 600sn timeout kullanılır. Çıktı gelmese bile işlem devam eder.

---

### PF-109: ✅ book.ps1 PowerShell String Manipülasyonu (ÇÖZÜLDÜ)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟢 Düşük |
| **Çözüm tarihi** | 2026-05-04 |

**Belirti:** PowerShell ile Python dosyasında `Replace()` yaparken `"` ve `$` karakterleri düzgün escape edilmezse dosya bozulur.

**Örnek:** `book.ps1` ile `book_pdf_v3.py`'de font ayarları değiştirilirken satır bozuldu:
```python
# Olması gereken:
"-V", "mainfont=Arial",
# PowerShell replace sonrası:
"mainfont=Arial" -V "monofont="
"-V", "monofont=Arial Mono",  # Geçersiz Python!
```

**Çözüm:** Python içinden Python dosyası düzenle:
```python
# Güvenli yöntem
with open('script.py', 'r') as f:
    content = f.read()
content = content.replace('old_text', 'new_text')
with open('script.py', 'w') as f:
    f.write(content)
```

**Ders:** Python dosyalarını düzenlemek için her zaman Python kullan. PowerShell string manipulation güvenilir değil.

---

### PF-110: ✅ DOCX'te Mermaid PNG'ler ve TOC (ÇÖZÜLDÜ)

| Alan | Değer |
|------|-------|
| **Öncelik** | 🟠 Önemli |
| **Çözüm tarihi** | 2026-05-04 |
| **İlgili** | `book_production.py` |

**Durum:** DOCX çıktısı başarılı:
- 1.2 MB boyut
- TOC (Table of Contents) dahil
- 54 Mermaid PNG gömülü
- 27 bölümün tamamı dahil

**Not:** Bu pipeline daha önce tamamlanmıştı, PDF üretimi sırasında sorun yaşanmadı.

---

## PANDOC/XELATEX PDF ÜRETİM SÜRECİ

### Başarılı Komut

```powershell
pandoc D:\bookMaker_Deepseek\build\output\java-programlamaya-giris-latex-ready.md `
  -o D:\bookMaker_Deepseek\build\output\java-programlamaya-giris.pdf `
  --pdf-engine=xelatex `
  -V geometry:margin=2cm `
  -V geometry:top=2.5cm `
  -V geometry:bottom=2.5cm `
  -V mainfont=Arial `
  -V fontsize=11pt `
  --toc --toc-depth=2 `
  --metadata title="Java Programlamaya Giris" `
  -f markdown
```

### Pipeline Akışı

```
INPUT: java-programlamaya-giris.md (585 KB, 552,844 karakter)
    │
    ├─ [1] Placeholder Temizleme (5 adet)
    │   regex: !\[.*?\]\(https?://[^)]*placeholder[^)]*\)
    │
    ├─ [2] Mermaid → PNG Dönüşümü (54/58)
    │   Her ```mermaid bloğu için:
    │     - PNG varsa → ![Mermaid Diyagramı N](abs_path)
    │     - PNG yoksa → blok olduğu gibi bırak
    │
    ├─ [3] LaTeX Güvenli Hale Getirme
    │   - Kod blokları dışındaki \n → \\textbackslash{}n
    │   - Inline code içindekiler korunur
    │
    ├─ [4] Geçici Markdown Yazma (568 KB)
    │
    └─ [5] Pandoc + XeLaTeX PDF Üretimi
       - ~3-5 dakika
       - 339 sayfa
       - 1.8 MB
       - TOC + 54 PNG gömülü
```

### PDF Çıktı Özellikleri

| Özellik | Değer |
|---------|-------|
| Sayfa sayısı | 339 |
| Boyut | 1.8 MB (1,894,205 bytes) |
| PDF versiyonu | 1.7 |
| Sayfa boyutu | 612 × 792 pts (Letter) |
| Font | Arial 11pt |
| İçindekiler | Evet (--toc, depth 2) |
| Başlık | Java Programlamaya Giris |
| Yazar | Teknik Kitap Ekibi |
| Üreten | LaTeX via pandoc → MiKTeX-dvipdfmx |
| Görseller | 54 Mermaid PNG gömülü |
| Placeholder (eksik) | 4 Mermaid bloğu kod olarak kaldı |

---

## METRİKLER

### Süreler

| Aşama | Süre | Not |
|-------|------|-----|
| Placeholder temizleme | < 1sn | Regex |
| Mermaid → PNG | ~5sn | 58 blok, dosya kontrolü |
| LaTeX sanitize | ~2sn | 17,455 satır |
| **Pandoc + XeLaTeX** | **~3-5 dk** | En uzun aşama |
| **Toplam** | **~5 dk** | |

### Boyutlar

| Aşama | Giriş | Çıkış |
|-------|-------|-------|
| Markdown | 585 KB | 568 KB |
| PDF | - | 1.8 MB |
| PNG görseller | - | 971 KB (54 dosya) |

### Hata Oranı

| Ölçüt | Değer |
|-------|-------|
| Mermaid bloğu | 58 |
| Başarılı PNG | 54 (%93.1) |
| Başarısız PNG | 4 (%6.9) |
| Placeholder | 5 (temizlendi) |
| PDF sayfası | 339 (hepsi geçerli) |

---

## ÖNERİLEN İYİLEŞTİRMELER

### Kısa Vade
- [ ] PF-001: 4 Mermaid `.mmd` dosyasını manuel düzelt ve PNG'leri yeniden üret
- [ ] PF-002: Placeholder resimleri gerçek Mermaid veya metin diyagramlarıyla değiştir
- [ ] PF-003: Bölüm uzunluğu için max_tokens hedefi belirle (örn: 15,000-25,000c)

### Orta Vade
- [ ] Mermaid PNG üretimini `book_build.py`'ye entegre et (PDF script'ine bağımlılığı kaldır)
- [ ] PyMuPDF (fitz) kurarak PDF doğrulamayı otomatikleştir
- [ ] PDF üretim süresini azalt: `--pdf-engine-opt=-draftmode` ile hızlı önizleme

### Uzun Vade
- [ ] LaTeX template'i özelleştir (kitap görünümü, başlık sayfası, footer)
- [ ] Alternatif PDF engine: lualatex (Unicode desteği daha iyi)
- [ ] Windows'ta WeasyPrint için GTK kurulum scripti

---

## KOMUT REFERANSI

```powershell
# Kitap birleştir (MD + DOCX)
.\book build

# PDF üret (tüm preprocessing dahil)
.\book pdf
# veya direkt:
python tools/book_pdf_v3.py

# Production pipeline (Mermaid PNG + DOCX TOC)
.\book production
# veya:
python tools/book_production.py

# PDF doğrulama
pdfinfo build/output/java-programlamaya-giris.pdf | Select-String "Pages:"
pdftotext build/output/java-programlamaya-giris.pdf - -l 1 | Select-Object -First 20

# Git durumu
.\book status
git log --oneline -5
```
