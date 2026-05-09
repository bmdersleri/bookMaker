p = "src/bookmaker/generation/pipeline.py"
c = open(p, "r", encoding="utf-8").read()

# Fix line 414: \""""Spec -> """Spec
bad = "\\\"\"\"\"Spec -> Validate -> Seed -> Normalize -> Enrich -> Assemble."
good = "\"\"\"Spec -> Validate -> Seed -> Normalize -> Enrich -> Assemble."
if bad in c:
    c = c.replace(bad, good)
    print("Fixed line 414")
else:
    print("Line 414 pattern not found, searching...")
    # Find any remaining backslash+quote patterns
    import re
    for m in re.finditer(r'\\"+"', c):
        start = max(0, m.start()-10)
        end = min(len(c), m.end()+10)
        print(f"  Found at pos {m.start()}: ...{c[start:end]}...")

# Fix trailing: """\ → """
trail_bad = '.\"\"\"\\\"'
trail_good = '.\"\"\"'
if trail_bad in c:
    c = c.replace(trail_bad, trail_good)
    print("Fixed trailing quote")
else:
    print("Trailing pattern not found")

open(p, "w", encoding="utf-8").write(c)
print(f"Done, length: {len(c)}")
