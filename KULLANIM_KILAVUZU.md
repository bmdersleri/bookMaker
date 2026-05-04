# bookMaker — Kullanım Kılavuzu

**Sürüm:** 0.1.0 | **Branch:** deepseek | **Platform:** Windows + PowerShell 7.x

---

## 1. Giriş

bookMaker, akademik/teknik kitap üretimi için CLI + GUI stüdyosudur.
Temel akış: **seed → outline → draft → approve → build → production → export**

### 1.1 Ortam

```powershell
# Projeyi aktifleştir
cd D:\bookMaker_Deepseek
uv sync                    # bağımlılıkları yükle

# Hızlı test
just fast                  # lint + hızlı test (~3sn)
just test                  # tüm testler (~25sn)
```

### 1.2 Dosya Yapısı

```
src/bookmaker/
├── cli.py                 # Typer CLI (10 komut grubu)
├── authoring/             # seed -> outline -> draft -> approve
├── build/                 # kod çıkarma + Java derleme
├── chapter/               # parser, validator, scorer
├── commands/              # CLI komutları (init, check, build, ...)
├── core/                  # encoding, ids, time, paths
├── generation/            # LLM ile otomatik üretim
├── github/                # GitHub sync + Pages
├── llm/                   # LLM API entegrasyonu
├── manifest/              # book_manifest.yaml yönetimi
├── models/                # Pydantic veri modelleri
├── production/            # Mermaid, QR, Pandoc export
├── storage/               # SQLite + dosya sistemi
└── studio/                # FastAPI GUI
```

---

## 2. CLI Referansı

### 2.1 Genel

```bash
bookmaker --help           # tüm komutlar
bookmaker --version        # sürüm (0.1.0)
bookmaker init             # yeni proje oluştur
```

### 2.2 Kitap Yönetimi (`manifest`)

```bash
bookmaker manifest view                  # manifest görüntüle
bookmaker manifest list-chapters         # bölümleri listele
bookmaker manifest validate              # manifest doğrula
bookmaker manifest pipeline              # pipeline durumu
```

### 2.3 Bölüm Yazımı (`chapter`)

```bash
bookmaker chapter seed <id> --purpose "..."   # bölüm tohumu oluştur
bookmaker chapter outline <id> prompt         # outline promptu üret
bookmaker chapter outline <id> paste --text "..." # outline yapıştır
bookmaker chapter outline <id> review         # outline değerlendir
bookmaker chapter draft <id> prompt           # draft promptu üret
bookmaker chapter draft <id> paste --text "..."   # draft yapıştır
bookmaker chapter draft <id> review           # draft değerlendir
bookmaker chapter approve <id>                # bölümü onayla
```

### 2.4 Kalite Kontrol (`check`)

```bash
bookmaker check chapter <path>              # bölüm doğrula
bookmaker check chapter <path> --json       # JSON rapor
bookmaker check chapter <path> --final      # placeholder kontrolü
```

### 2.5 Derleme (`build`)

```bash
bookmaker build chapter <path>              # kod çıkar + derle
bookmaker build chapter <path> --json       # JSON rapor
```

### 2.6 Production (`production`)

```bash
bookmaker production full <path>            # derle + mermaid + qr + docx
bookmaker production mermaid <path>         # sadece mermaid render
bookmaker production docx <path>            # sadece docx export
```

### 2.7 GitHub (`github`)

```bash
bookmaker github status                     # repo durumu
bookmaker github sync-code [dizin]          # kodları push et
bookmaker github manifest                   # URL manifesti
```

### 2.8 LLM API (`llm`)

```bash
bookmaker llm configure --provider deepseek --key sk-... --model deepseek-chat
bookmaker llm test                          # bağlantı testi
bookmaker llm status                        # yapılandırma durumu
```

### 2.9 Otomatik Üretim (`generate`)

```bash
bookmaker generate outline <id> --topic "..."    # LLM ile outline
bookmaker generate chapter <id> --title "..."     # LLM ile bölüm
bookmaker generate book "Java Programlama"        # LLM ile kitap
```

---

## 3. LLM API Kurulumu

### 3.1 Desteklenen Sağlayıcılar

| Sağlayıcı | Base URL | Modeller |
|---|---|---|
| openai | https://api.openai.com/v1 | gpt-4o, gpt-4o-mini |
| deepseek | https://api.deepseek.com/v1 | deepseek-chat, deepseek-reasoner |
| anthropic | https://api.anthropic.com/v1 | claude-3-opus, claude-3-sonnet |

### 3.2 Kurulum

```bash
# 1. API anahtarını yapılandır
bookmaker llm configure --provider deepseek --key sk-xxxxxxxx --model deepseek-chat

# 2. Bağlantıyı test et
bookmaker llm test

# 3. Ortam değişkeni (opsiyonel — config dosyasına yazmaz)
$env:LLM_API_KEY = "sk-xxxxx"
$env:LLM_API_KEY_DEEPSEEK = "sk-xxxxx"
```

### 3.3 Kullanım

```bash
# Outline üret
bookmaker generate outline bolum-1 --topic "Java'da Değişkenler"

# Bölüm üret
bookmaker generate chapter bolum-1 --title "Değişkenler ve Veri Tipleri"

# Kitap üret (outline + ilk 3 bölüm)
bookmaker generate book "Java'nın Temelleri"
```

---

## 4. Kitap Üretim Akışı

### 4.1 Manuel Akış (LLM copy/paste)

```bash
# 1. Proje oluştur
bookmaker init --preset java-temelleri --author "Adınız"

# 2. Bölüm tohumla
bookmaker chapter seed bolum-01 --purpose "Java giriş kavramları"

# 3. Outline promptu kopyala → LLM'e yapıştır → çıktıyı yapıştır
bookmaker chapter outline bolum-01 prompt              # kopyala
bookmaker chapter outline bolum-01 paste --text "..."  # yapıştır

# 4. Outline değerlendir
bookmaker chapter outline bolum-01 review

# 5. Draft üret
bookmaker chapter draft bolum-01 prompt                # kopyala
bookmaker chapter draft bolum-01 paste --text "..."    # yapıştır

# 6. Kalite kontrol
bookmaker check chapter chapters/bolum-01/draft_versions/v001.md

# 7. Onayla
bookmaker chapter approve bolum-01

# 8. Derle + Production
bookmaker build chapter chapters/bolum-01/approved/bolum-01_v001.md
bookmaker production full chapters/bolum-01/approved/bolum-01_v001.md
```

### 4.2 Otomatik Akış (LLM API ile)

```bash
# Tek adımda kitap
bookmaker generate book "Java'nın Temelleri" --lang tr-TR

# Veya adım adım
bookmaker generate outline bolum-01 --topic "Java Giriş"
bookmaker generate chapter bolum-01 --title "Java'ya Giriş"
```

---

## 5. Kalite Kontrol

### 5.1 Validasyon (CHAPTER_SPEC.md uyumluluğu)

```bash
bookmaker check chapter sample/sample_chapter.md
# Skor=100, Karar=pass, Hata=0, Uyari=0
```

6 validasyon grubu:
- Front matter (zorunlu/önerilen alanlar)
- Section meta (order, başlık, sıralama)
- CODE_META (zorunlu alanlar, broken_example kontrolü)
- MERMAID_META (⌀)
- Yasak işaretler (BÖLÜM SONU, DIAGRAM_META)
- Java kod uyumu (dosya adı ↔ class adı)

### 5.2 Derleme

```bash
bookmaker build chapter sample/sample_chapter.md
# 9 kod bloğu → 6 çıkarılan, 3 atlanan → 6/6 derlendi
```

### 5.3 Production Pipeline

```bash
bookmaker production full sample/sample_chapter.md
# Derleme + Mermaid render + QR üretimi + DOCX export
```

---

## 6. Studio GUI

### 6.1 Başlatma

```bash
just studio
# http://127.0.0.1:8765
```

### 6.2 API Endpointleri

| Endpoint | Açıklama |
|---|---|
| `/` | Dashboard |
| `/api/status` | Studio durumu |
| `/api/project` | Kitap bilgisi |
| `/api/chapters` | Bölüm listesi |
| `/api/check/<chapter_id>` | Validasyon çalıştır |
| `/api/build/<chapter_id>` | Derleme çalıştır |
| `/api/llm-status` | LLM yapılandırma |

---

## 7. Hızlı Test ve Optimizasyon

### 7.1 justfile Kısayolları

```bash
just          # komut listesi
just dev      # uv sync
just test     # tüm testler (~25sn)
just fast     # yavaş testleri atla (~3sn)
just lint     # ruff check
just fmt      # ruff format + fix
just ci       # lint + fast test
just studio   # GUI başlat
```

### 7.2 Fast Check

```bash
python tools/fast_check.py    # lint + fast test (~3sn)
```

### 7.3 Oturum Yönetimi

```bash
# Yeni oturumda önce bunları oku:
# SESSION.md   — aktif faz, test durumu, sıradaki görevler
# RESUME.md    — tüm kararların arşivi
```

---

## 8. Sık Kullanılan Komutlar (Hızlı Referans)

```bash
# Kurulum
uv sync

# Geliştirme döngüsü
just fast                                         # 3sn kalite kontrol
uv run python -m bookmaker check chapter <path>   # validasyon
uv run python -m bookmaker build chapter <path>   # derleme
uv run python -m bookmaker production full <path> # full pipeline

# LLM ile üretim
bookmaker llm configure --provider deepseek --key sk-xxx --model deepseek-chat
bookmaker generate book "Java'nın Temelleri" --lang tr-TR

# GitHub
git add -A && git commit -m "mesaj" && git push origin deepseek
```

---

*Son güncelleme: 2026-05-03 | bookMaker v0.1.0 | Branch: deepseek*
