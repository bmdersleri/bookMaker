"""Bölüm başlık hiyerarşisini düzeltir: ilk # H1 kalır, diğer #'lar ## olur."""

import re
import sys
from pathlib import Path

BASE = Path("chapters")


def fix_heading_hierarchy(text: str) -> str:
    """İlk # H1 kalır, sonraki tüm #'lar ## olur."""
    lines = text.splitlines()
    found_first_h1 = False
    result = []

    for line in lines:
        stripped = line.lstrip()
        # YAML front matter içinde değilsek ve # heading varsa
        if re.match(r"^#{1,6}\s+", stripped):
            current_level = len(stripped) - len(stripped.lstrip("#"))
            actual_level = current_level

            if actual_level == 1:
                if not found_first_h1:
                    found_first_h1 = True
                    # İlk H1 olduğu gibi kalır
                else:
                    # Sonraki tüm #'lar ## olur
                    line = "##" + line[line.index("#") + 1:]
            # Diğer seviyeler (##, ###) olduğu gibi kalır

        result.append(line)

    return "\n".join(result)


def process_chapter(chapter_id: str) -> bool:
    dp = BASE / chapter_id / "draft_versions" / "v001.md"
    if not dp.exists():
        print(f"  [YOK] {chapter_id}")
        return False

    text = dp.read_text(encoding="utf-8")
    # Sadece YAML front matter'dan sonraki kısmı işle
    parts = text.split("---\n", 2)
    if len(parts) >= 3:
        body = fix_heading_hierarchy(parts[2])
        text = parts[0] + "---\n" + parts[1] + "---\n" + body
    else:
        text = fix_heading_hierarchy(text)

    dp.write_text(text, encoding="utf-8")
    print(f"  [OK] {chapter_id}")
    return True


if __name__ == "__main__":
    chapters = sys.argv[1:] if len(sys.argv) > 1 else [
        f"bolum-{i:02d}" for i in range(1, 6)
    ]
    print(f"Baslik hiyerarsisi duzeltiliyor: {len(chapters)} bolum")
    for cid in chapters:
        process_chapter(cid)
    print("Tamam.")
