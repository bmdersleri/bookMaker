"""Fix front matter for chapter 1."""
from pathlib import Path
p = Path("chapters/bolum-01/draft_versions/v001.md")
text = p.read_text(encoding="utf-8")
if not text.startswith("---"):
    fm = '''---
title: "Java'ya Giris, Calisma Modeli ve Gelistirme Ortami"
subtitle: "Java'nin Temelleri"
author: "Ismail Kirbas"
date: "2026"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
repo: bmdersleri
project-alias: javanintemelleri
chapter-alias: bolum-01
chapter_id: bolum-01
chapter_type: core
automation_profile: academic_technical_book_v1
numbering: auto
github_slug: bolum-01
qr_policy: dual_for_code_examples
asset_policy: manual_override
---

'''
    p.write_text(fm + text, encoding="utf-8")
    print("Front matter eklendi")
else:
    print("Zaten var")
