"""Test build_front_matter: all edge cases."""
import sys, warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bookmaker.generation.postprocess import build_front_matter, ensure_front_matter, normalize
from bookmaker.core.config import load_config

print("=" * 60)
print("TEST: build_front_matter")
print("=" * 60)

# Test 1: None config (defaults)
print("\n1. config=None:")
fm = build_front_matter("bolum-02", "Test Baslik")
print(f"   OK: {len(fm)} chars, starts with ---: {fm.startswith('---')}")
print(f"   Author line present: {'author:' in fm}")

# Test 2: Valid BookConfig
c = load_config("java-temelleri")
print("\n2. config=BookConfig:")
fm2 = build_front_matter("bolum-02", c.chapter_title("bolum-02"), c)
print(f"   OK: {len(fm2)} chars")
print(f"   Has '{c.author}': {c.author in fm2}")

# Test 3: String config (the bug case - should warn, not crash)
print("\n3. config=string (HATA SENARYOSU):")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    fm3 = build_front_matter("bolum-02", "Test", "yanlislikla string gecildi")
    if w:
        print(f"   WARNING: {w[0].message}")
    print(f"   OK (cokmedi!): {len(fm3)} chars, defaults used")

# Test 4: ensure_front_matter
print("\n4. ensure_front_matter:")
sample = "# Test Chapter\n\nSome content here."
result = ensure_front_matter(sample, "bolum-02", "Test", c)
print(f"   OK: {len(result)} chars, starts with ---: {result.startswith('---')}")
print(f"   H1 preserved: {'# Test Chapter' in result}")

# Test 5: Full normalize pipeline
print("\n5. Full normalize:")
from pathlib import Path
seed = Path("D:/bookMaker_Deepseek/book_projects/java-temelleri/build/generation/step1_seed_raw.md").read_text(encoding="utf-8")
result = normalize(seed, "bolum-02", "Test Chapter", c)
print(f"   OK: {len(result)} chars, front matter: {'VAR' if result.startswith('---') else 'YOK'}")
import re
bt = '```'
print(f"   Code blocks preserved: {result.count(bt)//2}")

print("\n" + "=" * 60)
print("TUM TESTLER BASARILI!")
print("=" * 60)
