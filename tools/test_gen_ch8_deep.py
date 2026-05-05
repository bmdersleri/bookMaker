"""Test: Chapter 8 deep mode — Arayuzler ve Soyut Siniflar (include_deepen=True)."""
import sys
sys.path.insert(0, "src")

from bookmaker.generation.pipeline import ChapterGenerator

gen = ChapterGenerator("book_projects/dummy-kitap")
print(f"Client ready: {gen.is_ready()}")

result = gen.generate_chapter_with_spec(
    chapter_id="bolum-08",
    title="Arayuzler ve Soyut Siniflar",
    concepts=["Interface", "Abstract Class", "Default Metot", "Static Metot",
              "Polymorphism", "Functional Interface"],
    include_deepen=True,
)

print(f"\n{'='*60}")
print(f"Done! Mode: spec+deepen")
print(f"Path: {result.get('path', 'N/A')}")
print(f"Seed time: {result.get('seed_time', 0)}s")
print(f"Deepen time: {result.get('deepen_time', 0)}s")
print(f"{'='*60}")
