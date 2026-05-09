# bookMaker - Kullanım Kılavuzu

**bookMaker**, akademik/teknik kitap üretimi için CLI + GUI stüdyosudur.

## 1. Giriş

### 1.1 Ortam

```powershell
cd D:\bookMaker_clean
.\.venv\Scripts\python.exe -m bookmaker --help
```

Proje yapısı:

```
D:\bookMaker_Deepseek/
├── src/bookmaker/           # Ana kaynak kodu
├── chapters/                # Bölüm çalışma alanları
│   ├── bolum-XX/
│   │   ├── seed/            # Bölüm tohumu
│   │   ├── outline_versions/ # Outline versiyonları
│   │   ├── draft_versions/  # Taslak versiyonları
│   │   └── approved/        # Onaylanmış bölüm
├── tools/                   # Yardımcı scriptler
│   └── batch_v2.py          # Optimize edilmiş batch üretim (P1-P12)
├── build/                   # Yapı çıktıları
└── sample/                  # Referans kitap örnekleri
```

### 1.2 Dosya Yapısı

```
src/bookmaker/
├── cli.py                   # CLI giriş noktası
├── commands/                # CLI komut grupları
│   ├── init.py              # Proje başlatma
│   ├── chapter_commands.py  # Bölüm yönetimi
│   ├── check_commands.py    # Kalite kontrol
│   ├── build_commands.py    # Kod derleme
│   ├── llm_commands.py      # LLM API yönetimi
│   ├── generate_commands.py # Otomatik üretim
│   ├── manifest_commands.py # Manifest yönetimi
│   └── github_commands.py   # GitHub senkronizasyonu
├── llm/                     # LLM API entegrasyonu
├── generation/              # Otomatik içerik üretimi
├── authoring/               # Authoring pipeline
└── studio/                  # GUI stüdyosu
```

## 2. CLI Referansı

### 2.1 Genel

```powershell
bookmaker --help              # tüm komutlar
bookmaker --version           # sürüm (0.1.0)
bookmaker init                # yeni proje oluştur
```

### 2.2 Kitap Yönetimi (manifest)

```powershell
bookmaker manifest view                  # manifest görüntüle
bookmaker manifest list-chapters         # bölümleri listele
bookmaker manifest validate              # manifest doğrula
bookmaker manifest pipeline              # pipeline durumu
```

### 2.3 Bölüm Yazımı (chapter)

```powershell
bookmaker chapter seed <id> --purpose "..."   # bölüm tohumu oluştur
bookmaker chapter outline <id> prompt         # outline promptu üret
bookmaker chapter outline <id> paste --text "..." # outline yapıştır
bookmaker chapter outline <id> review         # outline değerlendir
bookmaker chapter draft <id> prompt           # draft promptu üret
bookmaker chapter draft <id> paste --text "..."   # draft yapıştır
bookmaker chapter draft <id> review           # draft değerlendir
bookmaker chapter approve <id>                # bölümü onayla
```

### 2.4 Kalite Kontrol (check)

```powershell
bookmaker check chapter <path>              # bölüm doğrula
bookmaker check chapter <path> --json       # JSON rapor
bookmaker check chapter <path> --final      # placeholder kontrolü
```

### 2.5 Derleme (build)

```powershell
bookmaker build chapter <path>              # kod çıkar + derle
bookmaker build chapter <path> --json       # JSON rapor
```

### 2.6 Production (production)

```powershell
bookmaker production full <path>            # derle + mermaid + qr + docx
bookmaker production mermaid <path>         # sadece mermaid render
bookmaker production docx <path>            # sadece docx export
```

### 2.7 GitHub (github)

```powershell
bookmaker github status                     # repo durumu
bookmaker github sync-code [dizin]          # kodları push et
bookmaker github manifest                   # URL manifesti
```

### 2.8 LLM API (llm)

```powershell
bookmaker llm configure --provider deepseek --key sk-... --model deepseek-chat
bookmaker llm test                          # bağlantı testi
bookmaker llm status                        # yapılandırma durumu
```

### 2.9 Otomatik Üretim (generate)

```powershell
bookmaker generate outline <id> --topic "..."    # LLM ile outline
bookmaker generate chapter <id> --title "..."     # LLM ile bölüm
bookmaker generate book "Java Programlama"        # LLM ile kitap
```

### 2.10 Optimize Edilmiş Batch Üretim (tools/batch_v2.py)

**En gelişmiş ve önerilen yöntem.** Tüm P1-P12 optimizasyonlarını içerir:

```powershell
# Varsayılan: combined prompt (outline+chapter tek API çağrısında)
python tools/batch_v2.py --batch 3

# İki aşamalı mod (outline+chapter ayrı)
python tools/batch_v2.py --two-step --batch 4

# Tüm batch'leri çalıştır
python tools/batch_v2.py
```

**P1-P12 Özellikleri:**

| # | Özellik | Açıklama |
|---|---------|----------|
| P1 | Sıralı işlem | Bir bölüm bitmeden diğerine geçmez |
| P2 | requests streaming | httpx yerine requests (daha kararlı) |
| P3 | Retry mekanizması | 3 deneme, üstel backoff (5sn, 15sn, 45sn) |
| P4 | Atomik yazma | Önce .tmp, sonra rename (veri bütünlüğü) |
| P5 | Progress göstergesi | Her 5sn'de chunk/chars/süre gösterimi |
| P6 | Combined prompt | Outline+chapter tek API çağrısında (P12) |
| P7 | Hata raporlama | batch_errors.json'a detaylı kayıt |
| P8 | Resume desteği | Kesintide kaldığı yerden devam (batch_progress.json) |
| P9 | Token optimizasyonu | Outline max_tokens=2048 (daha hızlı) |
| P10 | Büyük bölüm uyarısı | Outline >5000 chars ise uyarı |
| P11 | Preflight check | Batch başında API bağlantı testi |
| P12 | Combined prompt + BOLUM_METNI ayrıştırma | Varsayılan mod |

**Çıktılar:**
- Her bölüm: `chapters/bolum-XX/draft_versions/v001.md`
- Error log: `build/reports/batch_errors.json`
- Progress: `build/reports/batch_progress.json`

## 3. LLM API Kurulumu

### 3.1 Desteklenen Sağlayıcılar

- **DeepSeek** — `deepseek-chat`, `deepseek-reasoner`
- **OpenAI** — `gpt-4o`, `gpt-4o-mini`, `gpt-4`
- **Anthropic** — `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`

### 3.2 Kurulum

```powershell
bookmaker llm configure --provider deepseek --key sk-xxxxxxxx --model deepseek-chat
bookmaker llm test
```

Ortam değişkenleri:
```powershell
$env:LLM_API_KEY = "sk-xxxxx"
$env:LLM_API_KEY_DEEPSEEK = "sk-xxxxx"
```

### 3.3 Kullanım

```powershell
# CLS ile
bookmaker generate outline bolum-1 --topic "Java'da Değişkenler"
bookmaker generate chapter bolum-1 --title "Değişkenler ve Veri Tipleri"

# Optimize edilmiş batch ile (önerilen)
python tools/batch_v2.py --batch 2
```

## 4. Kitap Üretim Akışı

### 4.1 Manuel Akış (LLM copy/paste)

```powershell
# 1. Tohum oluştur
bookmaker chapter seed bolum-01 --purpose "..."

# 2. Outline promptu üret
bookmaker chapter outline bolum-01 prompt > outline_prompt.txt

# 3. LLM'e yapıştır → çıktıyı yapıştır
bookmaker chapter outline bolum-01 paste --text "$(Get-Content outline_prompt.txt -Raw)"

# 4. Draft promptu üret
bookmaker chapter draft bolum-01 prompt > draft_prompt.txt

# 5. LLM'e yapıştır → çıktıyı yapıştır
bookmaker chapter draft bolum-01 paste --text "$(Get-Content cevap.txt -Raw)"

# 6. Değerlendir ve onayla
bookmaker chapter draft bolum-01 review
bookmaker chapter approve bolum-01
```

### 4.2 Otomatik Akış (LLM API ile)

```powershell
# Tek kitap
bookmaker generate book "Java'nın Temelleri" --lang tr-TR

# Tek bölüm
bookmaker generate chapter bolum-01 --title "Java'ya Giriş"

# Batch üretim (önerilen)
python tools/batch_v2.py --batch 2     # Sadece 2. batch
python tools/batch_v2.py                # Tüm batch'ler
```

## 5. Kalite Kontrol

```powershell
bookmaker check chapter chapters/bolum-01/draft_versions/v001.md
bookmaker build chapter chapters/bolum-01/draft_versions/v001.md
```

## 6. Production Çıktısı

```powershell
bookmaker production full chapters/bolum-01/
bookmaker production docx chapters/bolum-01/
```

## 7. GitHub Entegrasyonu

```powershell
bookmaker github status
bookmaker github sync-code chapters/bolum-01/
bookmaker github manifest
```

## 8. Güvenlik Notları

- `api.txt` ve `llm_config.json` API anahtarları içerir — **git push edilmez**
- Bu dosyalar `.gitignore` ile korunmaktadır
- Hassas bilgiler için ortam değişkenleri kullanılabilir
