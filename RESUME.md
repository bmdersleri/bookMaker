# RESUME

> **Yeni oturumda once `SESSION.md` oku — 30 saniyede hazir olursun.**

Bu dosya projenin gecmis kararlarinin ve kalici baglaminin ozetidir.

## Kullanici Hedefi

LLM modellerinden faydalanarak akademik temelli bilisim, veri bilimi ve programlama kitaplari hazirlamak.

## Calisma Alani

```text
Repo: D:\bookMaker_clean
Branch: main (tek branch)
Remote: https://github.com/bmdersleri/bookMaker.git
```

## Mimari Ozet

```text
src/bookmaker/
├── cli.py                    # Typer CLI
├── generation/               # LLM pipeline (spec, seed, enrich, assemble)
├── chapter/                  # Parser, validator, scoring
├── production/               # Mermaid, Pandoc, export
├── manifest/                 # BookManifest, PipelineState modelleri
├── studio/                   # FastAPI GUI (localhost:8765)
├── llm/                      # DeepSeek API client
└── core/                     # BookConfig, paths, errors
```

## Kilit Mimari Kararlar

1. **Tek konfigurasyon kaynagi:** `book_manifest.yaml` (her kitap projesinin kokunde)
2. **Pipeline:** SPEC → VALIDATE → SEED → NORMALIZE → ENRICH → ASSEMBLE
3. **LLM:** DeepSeek Chat (tek model, global `llm_config.json`)
4. **GUI:** FastAPI + vanilla JS (localhost:8765, 6 sekme)
5. **Kitap projeleri:** `book_projects/<kitap-adi>/` altinda bagimsiz dizinler
6. **Validation profilleri:** Java, Flutter/Dart, Generic (manifest.style.code_language uzerinden)
7. **Encoding:** UTF-8 her yerde, `pathlib.Path`, LF line endings

## Kritik Dosyalar

| Dosya | Amac |
|-------|------|
| `SESSION.md` | Oturum günlügü — her oturum sonu güncellenir |
| `CLAUDE.md` | Agent talimatlari |
| `CHAPTER_PRODUCTION.md` | 6 asamali pipeline dokumantasyonu |
| `GUI_ROADMAP.md` | Studio GUI gelistirme yol haritasi |
| `MIGRATION.md` | project-based mimariye gecis kaydi (tamamlandi) |
| `CHANGELOG.md` | Surum gecmisi |

## Calisma Komutlari

```bash
uv sync                                           # bagimliliklari kur
uv run ruff check src/                            # lint
uv run pytest tests/ -q --tb=short                # test (218 passed)
uv run python -m bookmaker.studio.app             # GUI baslat (port 8765)
```

## Dikkat Edilecekler

- `llm_config.json` ve `.claude/settings.local.json` asla commit edilmez
- `book_projects/` altindaki kitap icerikleri ayri repolarda olabilir
- `.playwright-mcp/`, `build/`, `exports/` gibi generated dizinler commit disi
- `book_profile.yaml` artik kullanilmiyor — tek kaynak `book_manifest.yaml`
