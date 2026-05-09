"""Test: Bölüm 7 — Kalitim ve Polimorfizm (Deepen ile)."""
import sys
sys.path.insert(0, "src")

from bookmaker.generation.pipeline import ChapterGenerator

gen = ChapterGenerator("book_projects/dummy-kitap")
print(f"Client ready: {gen.is_ready()}")

result = gen.generate_chapter_with_spec(
    chapter_id="bolum-07",
    title="Kalitim ve Polimorfizm",
    concepts=[
        "Inheritance", "super anahtari", "Method Overriding",
        "Polymorphism", "Abstract Class vs Interface",
        "final anahtari", "Object sinifi", "Covariant Return Type",
    ],
    chapter_no=7,
    include_deepen=True,  # <-- COZUM B: Teorik derinlestirme acik
)

print(f"\n{'='*60}")
print(f"Done! Mode: spec+deepen")
print(f"Path: {result.get('path', 'N/A')}")
print(f"Seed time: {result.get('seed_time', 0)}s")
print(f"Deepen time: {result.get('deepen_time', 0)}s")
if 'steps' in result:
    print(f"Steps: {list(result['steps'].keys())}")
print(f"{'='*60}")
