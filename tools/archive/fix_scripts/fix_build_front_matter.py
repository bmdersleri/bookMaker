"""Fix build_front_matter: add string config protection."""
p = 'D:/bookMaker_Deepseek/src/bookmaker/generation/postprocess.py'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the function and its boundaries
start = content.find('def build_front_matter')
next_def = content.find('\ndef ', start + 1)
if next_def == -1:
    next_def = len(content)
old_func = content[start:next_def]

# Build the new function
new_func = '''def build_front_matter(chapter_id: str, title: str, config: Optional[BookConfig] = None) -> str:
    """book_profile.yaml'daki bilgileri kullanarak YAML front matter olusturur.

    Args:
        chapter_id: Bolum kimligi (orn. bolum-16)
        title: Bolum basligi
        config: Kitap config (None = varsayilan degerler, str = uyari + varsayilan)

    Returns:
        YAML front matter blogu (--- ile cevrili)

    Not: config yanlislikla string gecilirse uyari verir, varsayilan degerlerle
    devam eder (cokmez). normalize() fonksiyonu icinden dogru cagrilir:
        ensure_front_matter(text, chapter_id, title, config)
        -> build_front_matter(chapter_id, title, config)
    """
    # Saglamlik: yanlislikla string gecilmisse uyar
    if isinstance(config, str):
        import warnings
        warnings.warn(
            f"build_front_matter: 'config' parametresine BookConfig yerine "
            f"string gecildi ('{config[:50]}...'). Varsayilan degerler kullaniliyor. "
            f"Dogru kullanim: build_front_matter(chapter_id, title, config)",
            UserWarning, stacklevel=2,
        )
        config = None

    # Config'ten degerleri al (yoksa varsayilan)
    author = config.author if config else "Ismail Kirbas"
    year = config.year if config else 2026
    subtitle = f'"{config.title}"' if config else '"Java\'nin Temelleri"'
    repo = config.github_slug if config else "javanintemelleri"

    return f"""---
title: "{title}"
subtitle: {subtitle}
author: "{author}"
date: "{year}"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
repo: bmdersleri
project-alias: javanintemelleri
chapter-alias: {chapter_id}
chapter_id: {chapter_id}
chapter_type: core
automation_profile: academic_technical_book_v1
numbering: auto
github_slug: {chapter_id}
qr_policy: dual_for_code_examples
asset_policy: manual_override
---"""'''

content = content.replace(old_func, new_func)

with open(p, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Replaced: {len(old_func)} -> {len(new_func)} chars')
import py_compile
py_compile.compile(p, doraise=True)
print('Syntax OK')
