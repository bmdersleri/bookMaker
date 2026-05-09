"""Diagnose all DOCX quality issues in approved files."""
from pathlib import Path
import re

root = Path("book_projects/java-temelleri")

print("="*60)
print("1. STRAY QUOTES IN CODE FENCES")
print("="*60)
total_bad = 0
for ap in sorted(root.glob("chapters/*/approved/*.md")):
    cid = ap.parent.parent.name
    text = ap.read_text("utf-8")
    # Check for ```java followed by unusual chars
    bad = list(re.finditer(r'```java[\u201c\u201d\"\u2018\u2019\u0022]', text))
    if bad:
        total_bad += len(bad)
        for b in bad[:3]:
            line = text[:b.start()].count("\n") + 1
            print(f"  {cid}: line {line} -> {repr(b.group())}")
        if len(bad) > 3:
            print(f"    ... and {len(bad)-3} more")

if total_bad == 0:
    print("  (none found)")
else:
    print(f"  TOTAL: {total_bad}")

print()
print("="*60)
print("2. UNCLOSED CODE FENCES (missing closing ```)")
print("="*60)
total_unclosed = 0
for ap in sorted(root.glob("chapters/*/approved/*.md")):
    cid = ap.parent.parent.name
    text = ap.read_text("utf-8")
    fences = list(re.finditer(r"```([A-Za-z0-9_+\-.]*)", text))
    last = fences[-1] if fences else None
    if last:
        # Check if there's a closing ``` after this opening
        after = text[last.start()+3:]
        close = re.search(r"\n```", after[100:])  # skip first 100 chars (the lang line)
        if not close:
            # The closing is MORE than 100 chars away OR doesn't exist
            # Let me check directly
            rest = text[last.start():]
            # Find the closing, but don't count the opening
            rest_after_start = rest[rest.index("\n")+1:]
            close2 = re.search(r"\n```", rest_after_start)
            if not close2:
                total_unclosed += 1
                print(f"  {cid}: last fence at end (lang={last.group(1)}) - NO closing ```")
            else:
                pass  # has closing
    
if total_unclosed == 0:
    print("  (none found)")
else:
    print(f"  TOTAL: {total_unclosed}")

print()
print("="*60)
print("3. MERMAID IMAGE FILES")
print("="*60)
mermaid_files = list(root.glob("**/mermaid_images/**/*.png")) + list(root.glob("**/mermaid/**/*.png"))
if mermaid_files:
    print(f"  Found {len(mermaid_files)} mermaid images:")
    for mf in mermaid_files[:5]:
        print(f"    {mf.relative_to(root)} ({mf.stat().st_size} bytes)")
else:
    print("  NO MERMAID IMAGES FOUND - they need to be generated!")
    # Check where mermaid code blocks exist
    mermaid_chapters = []
    for ap in sorted(root.glob("chapters/*/approved/*.md")):
        cid = ap.parent.parent.name
        text = ap.read_text("utf-8")
        mermaid_fences = list(re.finditer(r"```mermaid", text))
        if mermaid_fences:
            mermaid_chapters.append((cid, len(mermaid_fences)))
    if mermaid_chapters:
        print(f"  Chapters with mermaid code blocks ({len(mermaid_chapters)}):")
        for cid, count in mermaid_chapters:
            print(f"    {cid}: {count} mermaid fence(s)")
    else:
        print("  No mermaid code blocks in any chapter")

print()
print("="*60)
print("4. SUMMARY OF ALL ISSUES")
print("="*60)
print("  Stray quotes:     ", "FOUND" if total_bad > 0 else "CLEAN")
print("  Unclosed fences:  ", "FOUND" if total_unclosed > 0 else "CLEAN")
print("  Mermaid images:   ", f"{len(mermaid_files)} files" if mermaid_files else "MISSING!")
