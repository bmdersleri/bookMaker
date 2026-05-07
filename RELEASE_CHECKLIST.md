# bookMaker Release Checklist

## 1. Pre-flight

- [ ] `git status --short` kontrol edildi
- [ ] Generated/local dosyalar commit'e dahil edilmedi
- [ ] `uv run ruff check src/ tests/` gecti
- [ ] `uv run pytest tests/ -q --tb=short` gecti
- [ ] Ornek kitap kalite kontrolu gecti

## 2. Studio Smoke

- [ ] Studio aciliyor
- [ ] Aktif kitap secilebiliyor
- [ ] Bolum listesi geliyor
- [ ] Code validation summary gorunuyor
- [ ] Export readiness checks gorunuyor
- [ ] Export rapor linki calisiyor

## 3. Documentation

- [ ] README guncel
- [ ] LLM_EXPLANATION guncel
- [ ] CHANGELOG guncel
- [ ] TODO guncel

## 4. Git

- [ ] Commit mesaji anlamli
- [ ] Push tamamlandi
- [ ] GitHub Actions gecti
