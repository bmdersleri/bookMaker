p = "src/bookmaker/generation/pipeline.py"
c = open(p, "r", encoding="utf-8").read()

# Replace escaped quotes in docstring
old = '\\"\\"Spec -> Validate -> Seed -> Normalize -> Enrich -> Assemble.'
new = '"""Spec -> Validate -> Seed -> Normalize -> Enrich -> Assemble.'
if old in c:
    c = c.replace(old, new)
    print("Fixed docstring start")
else:
    print("Docstring start not found")

old2 = 'kaydedilir.\\"\\"'
new2 = 'kaydedilir."""'
if old2 in c:
    c = c.replace(old2, new2)
    print("Fixed docstring end")
else:
    print("Docstring end not found")

open(p, "w", encoding="utf-8").write(c)
print(f"Done, length: {len(c)}")
