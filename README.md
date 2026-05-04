# bookMaker

Akademik ve teknik kitap üretim stüdyosu.

## Mimari

```
D:\bookMaker_Deepseek\              ← Otomasyon repom (bmdersleri/bookMaker)
├── src/bookmaker/                    ← Python otomasyon kodu
├── book_projects/                    ← Kitap projeleri (her biri ayrı repo)
│   └── java-temelleri/               ← Java'nin Temelleri kitabı
│       ├── chapters/                 ← 27 bölüm dosyası
│       ├── build/                    ← Çıktılar (DOCX, PDF, PNG)
│       ├── book_profile.yaml         ← Kitap profili
│       ├── llm_config.json           ← LLM API ayarları
│       ├── pipeline_state.yaml       ← Pipeline durumu
│       └── .git/                     ← AYRI repo
├── tools/                            ← Yardımcı araçlar
├── tests/                            ← Testler
└── docs/                             ← Dokümantasyon
```

## Kullanım

```powershell
# Otomasyon ortamı
cd D:\bookMaker_Deepseek
.\venv\Scripts\activate

# Kitap projesinde çalışma
bookmaker --path book_projects/java-temelleri check book

# Production build
bookmaker --project java-temelleri production full build/output/java-programlamaya-giris.md

# Tools scriptleri (güncellenmiş path'lerle)
python tools/build/book_build.py
python tools/build/book_pdf_v3.py
```
