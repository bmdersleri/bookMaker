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

## Yeni Makine Kurulumu

```bash
# 1. Repo'yu klonla
git clone https://github.com/bmdersleri/bookMaker.git
cd bookMaker

# 2. Sanal ortam ve bagimliliklar
uv venv --python 3.14
uv sync

# 3. LLM yapilandirmasi (makine-ozel, git'te yok!)
cp llm_config.example.json llm_config.json
# llm_config.json'u duzenle, kendi API anahtarini ekle

# 4. Kitap projesini ayri repodan klonla (submodule yok, manuel)
git clone https://github.com/bmdersleri/java-temelleri.git book_projects/java-temelleri
# VEYA var olan kitap projeni book_projects/ altina kopyala

# 5. Calistir
python -m bookmaker --help
python tools/validate_prompt_changes.py
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

# Tools scriptleri
python tools/build/book_build.py
python tools/build/book_pdf_v3.py

# Pipeline test
python tools/test_pipeline_full.py
```
