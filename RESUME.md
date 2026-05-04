# RESUME

> **Yeni oturumda once `session.md` oku — 60 saniyede hazir olursun.**
> Bu dosya gecmis kararlarin ve baglamin arsividir; degismez.

Bu dosya yeni bir sohbet veya sifir baglamla baslandiginda `bookMaker` projesi hakkinda bilinmesi gerekenleri ozetler.

## Kullanici Hedefi

Kullanici, LLM modellerinden maksimum duzeyde faydalanarak bilimsel ve akademik temeli olan bilisim ve veri bilimi icerikli kitaplar hazirlamak istiyor.

Istenen sistem:
- CLI ile calismali
- Guzel ve kullanisli bir arayuzu de olmali
- LLM saglayicisi olarak dis servisleri hedeflemeli
- Akademik kitap uretim surecini sadece metin uretimi olarak degil, yapi, kaynak, kod, alistirma, rubrik, cikti ve kalite kontrol sureci olarak ele almali

## Calisma Dizini ve Repo

- Calisma dizini: `D:\bookMaker_Deepseek`
- GitHub repo: `https://github.com/bmdersleri/bookMaker`
- Remote: `origin https://github.com/bmdersleri/bookMaker.git`
- Branch: `deepseek`

## Mevcut Durum

### Bolum Uretimi — TUMU TAMAM

| Batch | Bolumler | Durum | Boyut Araligi |
|-------|----------|-------|---------------|
| 0 (onceden) | B1-B6 (6 bolum) | TAMAM | 11,535 — 13,783c |
| Batch 1 | B7-B11 (5 bolum) | TAMAM | 15,792 — 30,640c |
| Batch 2 | B12-B16 (5 bolum) | TAMAM | 17,761 — 28,907c |
| Batch 3 | B17-B21 (5 bolum) | TAMAM | 19,110 — 47,019c |
| Batch 4 | B22-B23 + Ek A-D (6 bolum) | TAMAM | 15,629 — 24,570c |

**Toplam: 23 bolum + 4 ek = 27 dosya, ~585 KB**

### Production Ciktilar — TUMU TAMAM

| Cikti | Boyut | Detay |
|-------|-------|-------|
| `build/output/java-programlamaya-giris.md` | 585 KB | Birlestirilmis Markdown |
| `build/output/java-programlamaya-giris.docx` | 1.2 MB | TOC + 54 PNG Mermaid |
| `build/output/java-programlamaya-giris.pdf` | 1.8 MB | 339 sayfa, TOC + 54 PNG |
| `build/output/images/*.png` | ~971 KB | 54 Mermaid diyagrami |

### Siradaki Adimlar
- [ ] F-007: 4/58 Mermaid parse hatasini duzelt (manuel)
- [ ] F-008: Bolum uzunlugu tutarliligi
- [ ] GitHub push (deepseek branch)

### Aktif Hatalar (FAULT.md)

| ID | Sorun | Oncelik |
|----|-------|---------|
| F-007 | 4/58 Mermaid parse hatasi | Orta |
| F-008 | Bolum uzunlugu dengesiz | Orta |

### Cozulen Hatalar

| ID | Sorun | Cozum |
|----|-------|-------|
| F-001 | Front matter eksik | postprocess.py: ensure_frontmatter |
| F-002 | Heading hiyerarsisi | postprocess.py: fix_heading_hierarchy |
| F-003 | CODE_META yok | postprocess.py: auto_code_meta |
| F-004 | API yanit suresi (~95sn) | P12 combined prompt + P9 token opt. |
| F-005 | API timeout (120sn) | timeout=300 (pipeline) + 600 (batch) |
| F-006 | Eksik front matter alanlari | 23 alan kontrolu |

### P1-P13 Iyilestirmeleri

| # | Iyilestirme | Durum |
|---|-------------|-------|
| P1 | Sirali islem | TAMAM |
| P2 | requests streaming | TAMAM |
| P3 | Retry (3 deneme, backoff) | TAMAM |
| P4 | Atomik yazma (.tmp->rename) | TAMAM |
| P5 | Progress gostergesi (5sn) | TAMAM |
| P6/P12 | Combined prompt (varsayilan) | TAMAM |
| P7 | Hata raporlama (JSON) | TAMAM |
| P8 | Resume destegi | TAMAM |
| P9 | Outline token 4096->2048 | TAMAM |
| P10 | Buyuk bolum uyarisi | TAMAM |
| P11 | Preflight API testi | TAMAM |
| P13 | Token optimizasyonu (%60 kazanc) | TAMAM |

## Kullanici Tercihleri

- Kodlamaya baslamadan once problemi ve mimariyi tartismak istiyor
- Tum dosyalarda UTF-8 kullanilmali
- Sistem Windows ve PowerShell 7 **ZORUNLU**
- PowerShell surumu: 7.6.1 (`C:\Program Files\PowerShell\7\pwsh.exe`)
- **Windows PowerShell 5.1 (powershell.exe) kullanilmayacak**
- Tum `exec` komutlari PS7 ile calistirilir

## Ortam

- OS: Windows
- Shell: PowerShell 7 (pwsh.exe — tercih edilen shell)
- Python: 3.14.0
- LLM: DeepSeek (deepseek-chat -> deepseek-v4-flash)
- retry: 3 deneme, ustel backoff
- timeout: 600sn (batch), 300sn (pipeline)
- streaming: requests kutuphanesi
- PDF: pandoc 3.9 + xelatex (MiKTeX Portable)

## Anahtar Dosyalar

- `session.md` — oturum takibi (**once bunu oku**)
- `kullanim_kilavuzu.md` — tum CLI komutlari + batch_v2.py
- `fault.md` — hata listesi + P1-P12 iyilestirmeleri
- `master_plan.md` — faz plani
- `todo.md` — urun hedefleri
- `src/bookmaker/generation/postprocess.py` — son duzeltmeler
- `tools/batch_v2.py` — optimize edilmis batch uretim (P1-P12)
- `tools/book_pdf_v3.py` — PDF uretimi (pandoc + xelatex)

## Komut Kullanimi

```powershell
# PDF uretimi (yeni)
.\book pdf
# veya
python tools/book_pdf_v3.py

# Batch uretim (on
python tools/batch_v2.py --batch 3
python tools/batch_v2.py --two-step --batch 3

# Kitap birlestir
python tools/book_build.py --format both

# Test
python -m pytest tests/ -q -m "not slow"
```
