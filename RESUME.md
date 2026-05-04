# RESUME

> **Yeni oturumda önce `SESSION.md` oku — 60 saniyede hazır olursun.**
> Bu dosya geçmiş kararların ve bağlamın arşividir; değişmez.

Bu dosya yeni bir sohbet veya sıfır bağlamla başlandığında `bookMaker` projesi hakkında bilinmesi gerekenleri özetler.

## Kullanıcı Hedefi

Kullanıcı, LLM modellerinden maksimum düzeyde faydalanarak bilimsel ve akademik temeli olan bilişim ve veri bilimi içerikli kitaplar hazırlamak istiyor.

İstenen sistem:
- CLI ile çalışmalı
- Güzel ve kullanışlı bir arayüzü de olmalı
- LLM sağlayıcısı olarak dış servisleri hedeflemeli
- Akademik kitap üretim sürecini sadece metin üretimi olarak değil, yapı, kaynak, kod, alıştırma, rubrik, çıktı ve kalite kontrol süreci olarak ele almalı

## Çalışma Dizini ve Repo

- Çalışma dizini: `D:\bookMaker_Deepseek`
- GitHub repo: `https://github.com/bmdersleri/bookMaker`
- Remote: `origin https://github.com/bmdersleri/bookMaker.git`
- Branch: `deepseek`

## Mevcut Durum

### Bölüm Üretimi — TAMAM ✅

| Batch | Bölümler | Durum | Boyut Aralığı |
|-------|----------|-------|---------------|
| 0 (önceden) | B1-B6 (6 bölüm) | ✅ | 11,535 — 13,783c |
| Batch 1 | B7-B11 (5 bölüm) | ✅ | 15,792 — 30,640c |
| Batch 2 | B12-B16 (5 bölüm) | ✅ | 17,761 — 28,907c |
| Batch 3 | B17-B21 (5 bölüm) | ✅ | 19,110 — 47,019c |
| Batch 4 | B22-B23 + Ek A-D (6 bölüm) | ✅ | 15,629 — 24,570c |

**Toplam: 23 bölüm + 4 ek = 27 dosya, ~552,232 karakter**

### Sıradaki Adımlar
- [ ] Commit + Push to GitHub
- [ ] DOCX/PDF çıktısı üret
- [ ] F-007: Mermaid diyagramları doğrula
- [ ] F-008: Bölüm uzunluğu tutarlılığı

### Aktif Hatalar (FAULT.md)

| ID | Sorun | Öncelik |
|----|-------|---------|
| F-007 | Görsel/Mermaid referansı yok | 🟡 Orta |
| F-008 | Bölüm uzunluğu dengesiz | 🟡 Orta |

### Çözülen Hatalar

| ID | Sorun | Çözüm |
|----|-------|-------|
| F-001 | Front matter eksik | postprocess.py: ensure_frontmatter |
| F-002 | Heading hiyerarşisi | postprocess.py: fix_heading_hierarchy |
| F-003 | CODE_META yok | postprocess.py: auto_code_meta |
| F-004 | API yanıt süresi (~95sn) | P12 combined prompt + P9 token opt. |
| F-005 | API timeout (120sn) | timeout=300 (pipeline) + 600 (batch) |
| F-006 | Eksik front matter alanları | 23 alan kontrolü |

### P1-P12 İyileştirmeleri

| # | İyileştirme | Durum |
|---|-------------|-------|
| P1 | Sıralı işlem | ✅ |
| P2 | requests streaming | ✅ |
| P3 | Retry (3 deneme, backoff) | ✅ |
| P4 | Atomik yazma (.tmp→rename) | ✅ |
| P5 | Progress göstergesi (5sn) | ✅ |
| P6/P12 | Combined prompt (varsayılan) | ✅ |
| P7 | Hata raporlama (JSON) | ✅ |
| P8 | Resume desteği | ✅ |
| P9 | Outline token 4096→2048 | ✅ |
| P10 | Büyük bölüm uyarısı | ✅ |
| P11 | Preflight API testi | ✅ |

## Kullanıcı Tercihleri

- Kodlamaya başlamadan önce problemi ve mimariyi tartışmak istiyor
- Tüm dosyalarda UTF-8 kullanılmalı
- Sistem Windows ve PowerShell 7.x üzerinde çalışıyor
- PowerShell sürümü: 7.6.1

## Ortam

- OS: Windows
- Shell: PowerShell
- Python: 3.14.0
- LLM: DeepSeek (deepseek-chat → deepseek-v4-flash)
- retry: 3 deneme, üstel backoff
- timeout: 600sn (batch), 300sn (pipeline)
- streaming: requests kütüphanesi

## Anahtar Dosyalar

- `SESSION.md` — oturum takibi (**önce bunu oku**)
- `KULLANIM_KILAVUZU.md` — tüm CLI komutları + batch_v2.py
- `FAULT.md` — hata listesi + P1-P12 iyileştirmeleri
- `MASTER_PLAN.md` — faz planı
- `TODO.md` — ürün hedefleri
- `src/bookmaker/generation/postprocess.py` — son düzeltmeler
- `tools/batch_v2.py` — optimize edilmiş batch üretim (P1-P12)

## Komut Kullanımı

```powershell
# Batch üretim (önerilen)
python tools/batch_v2.py --batch 3           # combined prompt (varsayılan)
python tools/batch_v2.py --two-step --batch 3 # iki aşamalı

# CLI ile tek bölüm
python -m bookmaker generate chapter bolum-17 --title "..."

# Test
python -m pytest tests/ -q -m "not slow"
```
