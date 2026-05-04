# SESSION

Bu dosya her oturum sonunda güncellenir. Yeni oturumda **sadece bu dosyayı** oku.
Detaylı bağlam: `resume.md` | Optimizasyonlar: `fault.md` | Hedefler: `todo.md`

---

## SU AN

```
Aktif Faz       : Yapısal Ayrıştırma (Stüdyo ↔ Kitap Projeleri)
Son Değişiklik  : Kitap projeleri book_projects/ altına taşındı
Branch          : deepseek
PowerShell      : 7.6.1 (ZORUNLU — pwsh.exe)
PS7 Yolu        : C:\Program Files\PowerShell\7\pwsh.exe
PS5.1           : KULLANILMAYACAK
```

---

## YENİ MİMARİ

```
D:\bookMaker_Deepseek\              ← Otomasyon repom (bmdersleri/bookMaker)
├── src/bookmaker/                    ← Python otomasyon kodu
├── book_projects/                    ← Kitap projeleri (her biri ayrı repo)
│   └── java-temelleri/              ← İlk kitap (bmdersleri/java-temelleri)
│       ├── chapters/                ← 27 bölüm dosyası
│       ├── build/output/            ← DOCX, PDF, PNG çıktıları
│       ├── book_profile.yaml        ← Kitap profili
│       ├── llm_config.json          ← LLM API ayarları
│       ├── pipeline_state.yaml      ← Pipeline durumu
│       ├── book.ps1                 ← Kitap scriptleri
│       └── .git/                    ← AYRI repo
├── tools/                            ← Yardımcı araçlar
├── tests/                            ← Testler
└── docs/                             ← Ortak dokümantasyon
```

---

## KULLANIM

```powershell
# 1. Otomasyon kodunda calismak icin
cd D:\bookMaker_Deepseek

# 2. Kitap projesinde calismak icin
cd D:\bookMaker_Deepseek\book_projects\java-temelleri
.\book status

# 3. CLI ile kitap projesini belirtme
bookmaker --path book_projects/java-temelleri check book
bookmaker --path book_projects/java-temelleri production full build/output/java-programlamaya-giris.md
```

## KİTAP ÇIKTILARI

| Dosya | Boyut | İçerik |
|-------|-------|--------|
| `book_projects/java-temelleri/build/output/java-programlamaya-giris.docx` | 1.2 MB | 277 sayfa, TOC + 57 PNG |
| `book_projects/java-temelleri/build/output/java-programlamaya-giris.md` | 585 KB | Birleştirilmiş Markdown |
| `book_projects/java-temelleri/build/output/java-programlamaya-giris.pdf` | 1.9 MB | 347 sayfa, TOC + 57 PNG |
| `book_projects/java-temelleri/build/output/images/*.png` | ~1 MB | 58 Mermaid diyagramı |

## TAMAMLANANLAR (Bu Oturum)

### Yapısal Ayrıştırma ✅
- [x] `book_projects/java-temelleri/` oluşturuldu
- [x] 27 bölüm → `book_projects/java-temelleri/chapters/` taşındı
- [x] Build çıktıları → `book_projects/java-temelleri/build/` taşındı
- [x] Config dosyaları → `book_projects/java-temelleri/` taşındı
- [x] `book_profile.yaml` oluşturuldu
- [x] `core/paths.py` dual-root desteği kazandı
- [x] Tools scriptleri yeni path'lere güncellendi
- [x] `.gitignore` güncellendi
- [x] `book_projects/java-temelleri/` ayrı Git repo olarak init edildi
