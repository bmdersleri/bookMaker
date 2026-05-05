# 📋 bookMaker — Yapılacaklar

> **Strateji:** Kartopu stratejisi — küçük başla, katman katman büyüt.
> **Model:** Seed = Pro, Enrich = Flash, Format = Kod (0 token).

---

## ✅ Tamamlananlar

- [x] `book_profile.yaml` — Kapsamlı kitap anayasası (schema, chapters, quality, outputs, pandoc, mermaid, stats)
- [x] `core/config.py` — BookConfig okuyucu modül (tüm ayarları property'lerle sunar)
- [x] `production/mermaid.py` — Config entegrasyonu (mmdc cmd, background, timeout)
- [x] `production/pandoc.py` — Config entegrasyonu (ref docx, lua filter, mermaid paths)
- [x] `production/pipeline.py` — Config entegrasyonu (build/exports/mermaid dirs)
- [x] `commands/production.py` — CLI: info, build-book, build-all, docx, mermaid
- [x] `tools/build_book_docx.py` — BookConfig kullanır (27 bölüm tek DOCX)
- [x] `pipeline_state.yaml` — Kapsamlı pipeline durumu (meta, milestones, chapters, stats)
- [x] `generation/prompts.py` — Temiz 3-prompt sistemi (system ~100 tok, seed ~170 tok, enrich ~50 tok)
- [x] `generation/postprocess.py` — Meta'sız normalizasyon (heading fix, front matter, kod/mermaid regex)
- [x] `generation/pipeline.py` — 2 aşamalı pipeline: seed(Pro) → normalize(Python) → enrich(Flash, paralel) → assemble(Python)
- [x] `llm/config.py` — Çift model desteği (seed_model + enrich_model)
- [x] `llm_config.json` — Yeni format (seed_model + enrich_model)
- [x] **`generation/clean_text.py`** — TextCleaner (tırnak/boşluk/yazım düzelt, 0 token, <10ms)
- [x] **`postprocess.py` entegrasyonu** — `normalize()` içinde TextCleaner çağrısı

---

## 🔴 Öncelikli (Hemen)

- [x] **`generation/clean_text.py`** — TextCleaner: tırnak, boşluk, başlık, kod blok düzeltme
- [x] **`postprocess.py` entegrasyonu** — TextCleaner normalize()'e eklendi
- [ ] **`generation/mermaid_validator.py`** — MermaidValidator (syntax + auto-fix + compile + fallback, 0 token)
- [ ] **`pipeline.py` entegrasyonu** — MermaidValidator `generate_chapter()`'a eklenecek
- [ ] **Gerçek LLM ile test üretimi** — `ChapterGenerator.generate_chapter()` çalıştır, token ölç

---

## 🟡 Orta Vadeli

- [ ] **ChapterTemplate** — Template tabanlı validasyon
  - Hedef şablon: `sample_chapter.md` yapısı
  - Her katmandan sonra template uyum kontrolü
- [ ] **bolum-02 başlık düzeltme** — Front matter'da `title: "bolum-02"` → gerçek başlık
- [ ] **PDF çıktısını aktifleştirme** — `outputs.pdf: true`, pandoc xelatex
- [ ] **Paralel chapter generation** — `generate_all_chapters()` ile 27 bölüm

---

## 🟢 Düşük Öncelikli / İyileştirme

- [ ] **tools/ temizliği** — Eski araçları archive'e taşı
- [ ] **README.md güncelleme** — Yeni mimariyi yansıt
- [ ] **Commit** — Tüm değişiklikleri toparla
- [ ] **GitHub Actions** — DOCX build adımını güncelle
- [ ] **Bloke bölümleri çöz** — bolum-14, 18, 21 içerik revizyonu

---

## 📊 İlerleme

| Alan | Toplam | Bitmiş | % |
|---|---|---|---|
| Config & Anayasa | 4 | 4 | 100% |
| Production Build | 2 | 2 | 100% |
| LLM Generation | 7 | 6 | 86% |
| Test & Validasyon | 3 | 0 | 0% |
| CI/CD | 2 | 0 | 0% |
| **Toplam** | **18** | **12** | **67%** |
