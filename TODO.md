# bookMaker -- Yapilacaklar

> **Model:** DeepSeek Chat (tek model) | **Branch:** main | **Test:** 294 passed

---

## Tamamlananlar

- [x] `book_manifest.yaml` tek konfigurasyon kaynagi (book_profile.yaml kaldirildi)
- [x] 6 asamali pipeline: SPEC → VALIDATE → SEED → NORMALIZE → ENRICH → ASSEMBLE
- [x] Multi-language destegi (Java, Python, Dart/Flutter, generic)
- [x] Studio GUI: 6 sekme, wizard, inline chapter edit, pipeline detail tracking
- [x] Export UI: referans DOCX, lua filter, TOC depth kontrolleri
- [x] Split-panel markdown editor (live preview + save)
- [x] Chapter validator: parser, semantic checks, scoring, profile-aware test modes
- [x] Profile-aware validation (Java, Flutter/Dart, Generic profilleri)
- [x] DeepSeek Chat entegrasyonu (retry, streaming, auto-resume)
- [x] 6 paralel enrichment: ozet, sozluk, soru, alistirma, hata, kopru
- [x] Production pipeline: Mermaid→PNG, Pandoc DOCX/PDF/EPUB/HTML
- [x] FAZ 6.3 Export readiness ve production export raporlari
- [x] FAZ 6.4 Profile-aware code adapter hatti (Java, Python, Flutter, React)
- [x] FAZ 6.5 Studio validation ve export UX payload'lari
- [x] FAZ 6.6 Studio frontend UX entegrasyonu (readiness, code validate)
- [x] FAZ 6.7 Uctan uca smoke testler, CI guclendirme, release checklist
- [x] GitHub Actions CI — Python 3.12/3.13 matrisi, ruff src/tests/, pytest

---

## Kisa Vadeli

- [ ] **GUI_ROADMAP.md Faz 7** — coklu kitap, kullanici rolleri, reader mode, Docker/PWA
- [ ] **Dokumantasyon revizyonu** — docs/ altindaki eski dosyalari guncelle veya arsivle
- [ ] **PDF ciktisi** — pandoc xelatex entegrasyonu
- [ ] **Otomatik screenshot** — Flutter/Dart kitaplar icin headless screenshot

---

## Orta Vadeli

- [ ] **Paralel chapter generation** — birden fazla bolumu ayni anda uretme
- [x] **GitHub Actions CI** — otomatik test + lint + build (tamamlandi FAZ 6.7)
- [ ] **Template tabanli validasyon** — chapter_spec.md ile otomatik kontrol
- [ ] **Docker imaji** — tek komutla calisan bookMaker ortami

---

## Dusuk Oncelikli

- [ ] **Reader mode** — salt okunur web kitap goruntuleyici
- [ ] **Multi-user rolleri** — editor, yazar, reviewer
- [ ] **Bildirimler** — pipeline tamamlaninca desktop/email bildirimi
- [ ] **PWA** — offline calisabilen Studio GUI
