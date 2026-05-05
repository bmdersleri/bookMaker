# bookMaker -- Yapilacaklar

> **Strateji:** Kartopu stratejisi -- kucuk basla, katman katman buyut.
> **Model:** DeepSeek Chat (tek model).

---

## Tamamlananlar

- [x] `book_profile.yaml` -- Kapsamli kitap anayasasi
- [x] `core/config.py` -- BookConfig okuyucu modul
- [x] `production/mermaid.py` -- mmdc CLI entegrasyonu
- [x] `production/pandoc.py` -- Pandoc DOCX export
- [x] `production/pipeline.py` -- Full production pipeline
- [x] `commands/production.py` -- CLI komutlari
- [x] `pipeline_state.yaml` -- Pipeline durum takibi
- [x] `generation/prompts.py` -- Prompt sablonlari
- [x] `generation/postprocess.py` -- Normalizasyon (heading fix, front matter, kod/mermaid)
- [x] `generation/pipeline.py` -- 4 asamali pipeline + 5 uretim stratejisi
- [x] `llm/config.py` -- LLM config yonetimi (tek model)
- [x] `llm_config.json` -- DeepSeek API yapilandirmasi
- [x] `generation/clean_text.py` -- TextCleaner (0 token, regex bazli)
- [x] `generation/mermaid_validator.py` -- MermaidValidator (syntax + auto-fix + compile + fallback, 0 token)
- [x] `openai.py` -- Retry + streaming + auto-resume mekanizmasi
- [x] **deepen theory pipeline** -- H2 bazinda teorik derinlestirme (genisletilmis prompt, +%50-100 icerik)
- [x] **tools/ temizligi** -- 94 -> 30 script, fix/check/verify/migration archive'e tasindi
- [x] **docstring/kod temizligi** -- Dual model referanslari, guncel olmayan yorumlar
- [x] **pipeline kod tekrari azaltma** -- `_spec_seed_normalize()` helper metodu cikarildi

---

## Oncelikli (Hemen)

- [ ] **`mermaid_validator.py` entegrasyonu** -- MermaidValidator `generate_chapter()`'a eklenecek
- [ ] **Gercek LLM ile test uretimi** -- `ChapterGenerator.generate_chapter()` calistir, token olc

---

## Orta Vadeli

- [ ] **ChapterTemplate** -- Template tabanli validasyon (sample_chapter.md yapisi)
- [ ] **bolum-02 baslik duzeltme** -- Front matter'da `title: "bolum-02"` -> gercek baslik
- [ ] **PDF ciktisi** -- `outputs.pdf: true`, pandoc xelatex
- [ ] **Paralel chapter generation** -- `generate_all_chapters()` ile 27 bolum

---

## Dusuk Oncelikli / Iyilestirme

- [ ] **README.md guncelleme** -- Yeni mimariyi yansit
- [ ] **GitHub Actions** -- DOCX build adimini guncelle
- [ ] **Bloke bolumler** -- bolum-14, 18, 21 icerik revizyonu
- [ ] **Studio Faz 1 kalanlar** -- app.js/styles.css ayristirma, /static/ mount

---

## Ilerleme

| Alan | Toplam | Bitmis | % |
|---|---|---|---|
| Config & Anayasa | 4 | 4 | 100% |
| Production Build | 2 | 2 | 100% |
| LLM Generation | 8 | 7 | 88% |
| Test & Validasyon | 3 | 1 | 33% |
| CI/CD & Dokumantasyon | 2 | 0 | 0% |
| Kod Kalitesi | 3 | 3 | 100% |
| **Toplam** | **22** | **17** | **77%** |
