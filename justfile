# bookMaker — Justfile
# Kullanim: just <recipe>
# Kurulum: winget install casey.just  veya  scoop install just

dev:
    uv sync

test:
    uv run pytest tests/ -q --tb=short

fast:
    uv run pytest tests/ -q --tb=short -m "not slow"

all:
    uv run pytest tests/

lint:
    uv run ruff check src/ tests/

fmt:
    uv run ruff format src/ tests/

check:
    uv run ruff check src/ tests/
    uv run pytest tests/ -q --tb=short -m "not slow"

ci:
    uv run ruff check src/ tests/ --fix
    uv run pytest tests/ -q --tb=short -m "not slow"
    echo "CI OK"

version:
    uv run python -m bookmaker --version

studio:
    uv run python -c "from bookmaker.studio.app import run_studio; run_studio()"

help:
    uv run python -m bookmaker --help

# === bookMaker Ek Recipes ===

# Kitap birleştir + DOCX
build-book:
    uv run python tools/book_build.py --format both

# Batch üretim (combined prompt, varsayılan)
batch n:
    uv run python tools/batch_v2.py --batch {{n}}

# Batch üretim (iki aşamalı)
batch-two-step n:
    uv run python tools/batch_v2.py --two-step --batch {{n}}

# Git durumu
status:
    git status --short

# Git log (son N)
log n=10:
    git log --oneline -{{n}}

# Kitap bütünlük kontrolü
check-book:
    uv run python tools/book_build.py --format md 2>&1 | findstr "chars"

# PDF çıktısı (pandoc + xelatex, 54 Mermaid PNG)
pdf:
    uv run python tools/book_pdf_v3.py

# Tüm dosyaları stage'le
stage:
    git add -A

# Stage + commit + push
push m="auto":
    git add -A
    git commit -m {{m}}
    git push origin deepseek

# Branch bilgisi
branch:
    git branch -a
