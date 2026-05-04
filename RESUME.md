# RESUME

> **Yeni oturumda once `session.md` oku — 30 saniyede hazir olursun.**
> Bu dosya gecmis kararlarin ve baglamin arsividir; degismez.

Bu dosya yeni bir sohbet veya sifir baglamla baslandiginda `bookMaker` projesi hakkinda bilinmesi gerekenleri ozetler.

## Kullanici Hedefi

Kullanici, LLM modellerinden maksimum duzeyde faydalanarak bilimsel ve akademik temeli olan bilisim ve veri bilimi icerikli kitaplar hazirlamak istiyor.

Istenen sistem:
- CLI ile calismali (`bookmaker <komut>`)
- GUI (FastAPI Studio) ile de calismali
- LLM saglayicisi olarak dis servisleri hedeflemeli (DeepSeek API)
- Akademik kitap uretim surecini yapi, kaynak, kod, alistirma, rubrik, cikti ve kalite kontrol sureci olarak ele almali
- Kitaplar ayri proje ve repo olarak yonetilmeli

## Calisma Dizini ve Repolar

### Ana Repo (Otomasyon)
- Dizin: `D:\bookMaker_Deepseek`
- GitHub: `github.com/bmdersleri/bookMaker`
- Branch: `deepseek`
- Icerik: `src/bookmaker/`, `tools/`, `tests/`, `docs/`, `prompts/`

### Kitap Repo (Java'nin Temelleri)
- Dizin: `D:\bookMaker_Deepseek\book_projects\java-temelleri`
- GitHub: `github.com/bmdersleri/java-temelleri`
- Branch: `main`
- Icerik: `chapters/` (27 bolum), `build/output/`, `book_profile.yaml`, `llm_config.json`

## Mimari Kararlar

1. CLI (Typer) + Studio (FastAPI) — iki arayuz
2. Pydantic v2 veri modelleri — kitap, bolum, kalite, versiyon
3. SQLite + dosya depolama — versiyon ve event log
4. Chapter Engine — parser, validator, normalizer, scorer
5. Authoring Pipeline — seed → outline → draft → approve
6. Production Pipeline — kod testi, Mermaid, QR, asset, export
7. Tum kitaplar `book_projects/<kitap-adi>/` altinda, ayri repo
8. `book_profile.yaml` kitap proje kokunu belirler
9. Otomasyon kodu `pyproject.toml` ile ayri repoda

## PS7 Zorunlu Kullanimi

- PowerShell 7.6.1 (`C:\Program Files\PowerShell\7\pwsh.exe`) ZORUNLU
- PS5.1 (`powershell.exe`) kullanilmayacak
- `&&` sadece PS7'de calisir
- `ps7-exec` skill'i yuklendi (C:\Users\ismai\.deepchat\skills\ps7-exec)
- Helper: `D:\bookMaker_Deepseek\tools\exec.ps1`
- PS7 profilde: `exec` ve `ps7` fonksiyonlari tanimli

## CLI Dogru Kullanim

```powershell
# Her zaman .venv kullan:
.venv\Scripts\python.exe -m bookmaker <komut>

# PS7 ile (&& calisir):
exec 'cd D:\bookMaker_Deepseek && .venv\Scripts\python.exe -m bookmaker check chapter "book_projects/java-temelleri/chapters/bolum-01/draft_versions/v001.md"'

# Kitap projesi icin --path veya dogrudan arguman:
# check chapter: positional PATH (bolum.md dosyasi)
# check book: positional CHAPTERS_DIR (proje dizini)
# manifest/lm/github: --path <proje_dizini>
# production full/mermaid/docx: positional PATH (bolum.md)
```

## Pinlenen Skill'ler (10 adet)

docx, pdf, code-review, frontend-design, git-commit, doc-coauthoring, xlsx, ps7-exec, skill-creator

## CLI Durumu

25 alt komuttan ~20'si calisiyor. 3 acik hata:
1. production full -> production/pipeline.py run() None donuyor
2. manifest pipeline -> PipelineManager bulk bulamiyor
3. build chapter -> javac PATH'te degil

## Sonraki Adim

1. Kalan CLI hatalarini duzelt
2. Studio GUI'yi baslat ve gelistir (FastAPI)
3. Kitap pipeline'ini tamamla (scoring -> approved -> ready_for_export)

## Ortam

- OS: Windows
- Python: 3.14.0 (.venv: 3.14)
- LLM: DeepSeek API (model: deepseek-chat, base: api.deepseek.com/v1)
- Pandoc: 3.9 + xelatex (MiKTeX Portable)
- Git: 2.44.0
- GitHub CLI: 2.92.0
- Ripgrep: 14.1.1 (+PCRE2)
- Node.js: v24.11.1 / npm: 11.13.0
