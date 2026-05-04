"""Generation pipeline post-processor — hata duzeltmeleri."""

from __future__ import annotations

import re
from pathlib import Path


def ensure_frontmatter(text: str, chapter_id: str, title: str) -> str:
    """F-001: Front matter yoksa veya eksikse yenile."""
    required_fields = [
        "title", "subtitle", "author", "date", "lang",
        "documentclass", "toc", "toc-depth", "numbersections",
        "repo", "project-alias", "chapter-alias", "chapter_id",
        "chapter_type", "automation_profile", "chapter_spec",
        "processing_stage", "numbering", "github_slug",
        "qr_policy", "asset_policy", "placeholder_policy",
        "snippet_policy",
    ]
    if text.lstrip().startswith("---"):
        # Mevcut front matter'i kontrol et, eksik alan varsa yenile
        end_idx = text.find("---", 3)
        if end_idx != -1:
            existing_fm = text[3:end_idx]
            missing = [f for f in required_fields if f not in existing_fm]
            if not missing:
                return text  # Tum alanlar mevcut
            # Eksik var -> yenile
    # Yeniden olustur
    fm = (
        "---\n"
        f'title: "{title}"\n'
        'subtitle: "Java\'nin Temelleri"\n'
        'author: "Ismail Kirbas"\n'
        'date: "2026"\n'
        "lang: tr-TR\n"
        "documentclass: report\n"
        "toc: true\n"
        "toc-depth: 3\n"
        "numbersections: true\n"
        "repo: bmdersleri\n"
        "project-alias: javanintemelleri\n"
        f"chapter-alias: {chapter_id}\n"
        f"chapter_id: {chapter_id}\n"
        "chapter_type: core\n"
        "automation_profile: academic_technical_book_v1\n"
        "chapter_spec: chapter_spec_v0_1\n"
        "processing_stage: authoring_source\n"
        "numbering: auto\n"
        f"github_slug: {chapter_id}\n"
        "qr_policy: dual_for_code_examples\n"
        "asset_policy: manual_override\n"
        "placeholder_policy: source_template\n"
        "snippet_policy: non_meta_code_is_explanatory\n"
        "---\n\n"
    )
    return fm + text


def fix_heading_hierarchy(text: str) -> str:
    """F-002: Ilk # H1 kalir, sonraki tum #'lar ## olur."""
    lines = text.splitlines()
    found_first_h1 = False
    result = []
    in_fm = text.lstrip().startswith("---")

    for line in lines:
        stripped = line.rstrip()

        # YAML front matter sonu
        if in_fm and stripped == "---":
            in_fm = False
            result.append(line)
            continue

        if not in_fm:
            match = re.match(r"^(#{1,6})\s+", stripped)
            if match:
                level = len(match.group(1))
                if level == 1:
                    if not found_first_h1:
                        found_first_h1 = True
                    else:
                        line = "##" + line[line.index("#") + 1:]

        result.append(line)

    return "\n".join(result)


def auto_code_meta(text: str, chapter_id: str) -> str:
    """F-003: Java kod bloklarina otomatik CODE_META ekle."""
    # Kod bloklarini bul
    pattern = re.compile(r"(```java\s*\n(.*?)```)", re.DOTALL)
    result = []
    last_end = 0
    counter = 0

    for match in pattern.finditer(text):
        start = match.start()
        code = match.group(2).strip()

        # CODE_META once eklenmis mi?
        before = text[max(0, start - 500):start]
        if "CODE_META" in before and before.rstrip().endswith("-->"):
            result.append(text[last_end:match.end()])
            last_end = match.end()
            continue

        # Dosya adini bul
        file_match = re.search(r"//\s*Dosya:\s*(\S+)", code)
        file_name = file_match.group(1) if file_match else f"Ornek{counter:02d}.java"
        main_class = Path(file_name).stem
        counter += 1

        code_id = f"{chapter_id}_kod{counter:02d}"
        meta = (
            f"<!-- CODE_META\n"
            f"id: {code_id}\n"
            f"chapter_id: {chapter_id}\n"
            f"kind: example\n"
            f'title: "Kod {counter}"\n'
            f'file: "{file_name}"\n'
            f"mainClass: {main_class}\n"
            f"extract: true\n"
            f"test: compile\n"
            f"github: true\n"
            f"qr: dual\n"
            f"-->\n\n"
        )
        result.append(text[last_end:start])
        result.append(meta)
        result.append(text[start:match.end()])
        last_end = match.end()

    result.append(text[last_end:])
    return "".join(result)


def process(text: str, chapter_id: str, title: str) -> str:
    """Tum duzeltmeleri sirayla uygula."""
    text = ensure_frontmatter(text, chapter_id, title)
    text = fix_heading_hierarchy(text)
    text = auto_code_meta(text, chapter_id)
    return text
