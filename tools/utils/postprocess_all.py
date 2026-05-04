"""Postprocess tum 27 bolumu toplu olarak duzeltir."""
from pathlib import Path

CHAPTER_ORDER = [
    "bolum-01","bolum-02","bolum-03","bolum-04","bolum-05","bolum-06",
    "bolum-07","bolum-08","bolum-09","bolum-10","bolum-11",
    "bolum-12","bolum-13","bolum-14","bolum-15","bolum-16",
    "bolum-17","bolum-18","bolum-19","bolum-20","bolum-21",
    "bolum-22","bolum-23",
    "ek-a","ek-b","ek-c","ek-d",
]

ROOT = Path(__file__).resolve().parent.parent.parent
chapters_dir = ROOT / "book_projects" / "java-temelleri" / "chapters"
total_fixed = 0

for slug in CHAPTER_ORDER:
    path = chapters_dir / slug / "draft_versions" / "v001.md"
    if not path.exists():
        print(f"[{slug}] FILE NOT FOUND")
        continue

    text = path.read_text(encoding="utf-8")
    
    temp = text.lstrip()
    if temp.startswith("---"):
        end_idx = temp.find("---", 3)
        if end_idx != -1:
            fm_text = temp[3:end_idx]
        else:
            fm_text = ""
    else:
        fm_text = ""

    import re
    cid_match = re.search(r'^chapter_id\s*:\s*(\S+)', fm_text, re.MULTILINE)
    title_match = re.search(r'^title\s*:\s*"(.+?)"', fm_text, re.MULTILINE)
    chapter_id = cid_match.group(1) if cid_match else slug
    title = title_match.group(1) if title_match else slug

    from bookmaker.generation.postprocess import ensure_frontmatter, auto_code_meta, fix_heading_hierarchy, process

    new_text = process(text, chapter_id, title)
    
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        added_code = new_text.count("<!-- CODE_META") - text.count("<!-- CODE_META")
        print(f"[{slug}] FIXED: +{added_code} CODE_META")
        total_fixed += 1
    else:
        print(f"[{slug}] OK (no changes)")

print(f"\nTotal chapters fixed: {total_fixed}/{len(CHAPTER_ORDER)}")
