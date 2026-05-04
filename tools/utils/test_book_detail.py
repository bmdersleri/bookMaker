"""Detailed validation report."""
from pathlib import Path
from bookmaker.chapter.parser import parse
from bookmaker.chapter.book_validator import CHAPTER_ORDER, EXPECTED_NUMBERS
from collections import Counter

chapters_dir = Path("chapters")

# 1) Numbering değerlerini kontrol et
print("=== NUMBERING ANALYSIS ===")
for slug in CHAPTER_ORDER:
    path = chapters_dir / slug / "draft_versions" / "v001.md"
    if not path.exists():
        print(f"  {slug}: FILE MISSING")
        continue
    parsed = parse(path)
    expected = EXPECTED_NUMBERS.get(slug, "")
    actual = parsed.frontmatter.get("numbering", "")
    ok = "OK" if actual == expected else "MISMATCH"
    print(f"  [{ok}] {slug}: expected={expected!r}, actual={actual!r}")

# 2) Frontmatter alanları
print("\n=== FRONTMATTER FIELD COUNTS ===")
all_fields = Counter()
for slug in CHAPTER_ORDER:
    path = chapters_dir / slug / "draft_versions" / "v001.md"
    if not path.exists():
        continue
    parsed = parse(path)
    for k in parsed.frontmatter:
        all_fields[k] += 1
for field, count in sorted(all_fields.items(), key=lambda x: -x[1]):
    flag = "WARN" if count < 27 else "OK"
    print(f"  [{flag}] {field}: {count}/27")

# 3) Mermaid ID sayıları
print("\n=== MERMAID COUNTS ===")
total_mermaid = 0
for slug in CHAPTER_ORDER:
    path = chapters_dir / slug / "draft_versions" / "v001.md"
    if not path.exists():
        continue
    parsed = parse(path)
    count = sum(1 for mb in parsed.meta_blocks if mb.kind == "MERMAID_META")
    total_mermaid += count
    print(f"  {slug}: {count} mermaid blocks")
print(f"\n  TOTAL: {total_mermaid} mermaid blocks")

# 4) Chapter-level validation özeti
print("\n=== CHAPTER-LEVEL VALIDATION ===")
from bookmaker.chapter.validator import validate as validate_chapter
from bookmaker.chapter.scoring import make_report

error_counts = Counter()
warning_counts = Counter()
for slug in CHAPTER_ORDER:
    path = chapters_dir / slug / "draft_versions" / "v001.md"
    if not path.exists():
        continue
    parsed = parse(path)
    issues = validate_chapter(parsed)
    for iss in issues:
        cat = iss.category
        if iss.severity.value == "error":
            error_counts[cat] += 1
        elif iss.severity.value == "warning":
            warning_counts[cat] += 1

print("  Errors by category:")
for cat, count in error_counts.most_common():
    print(f"    [ERR] {cat}: {count}")
print("  Warnings by category:")
for cat, count in warning_counts.most_common():
    print(f"    [WARN] {cat}: {count}")
