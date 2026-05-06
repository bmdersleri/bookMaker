"""Test: Bolum 10 - Deep mode generation with include_deepen=True."""
import sys
sys.path.insert(0, "src")

from bookmaker.generation.pipeline import ChapterGenerator

gen = ChapterGenerator("book_projects/dummy-kitap")
print(f"Client ready: {gen.is_ready()}")

# Deep mode: generate_chapter_with_spec ile teorik derinlestirme acik
result = gen.generate_chapter_with_spec(
    chapter_id="bolum-10",
    title="Dosya Isleme ve Kalici Veri Saklama",
    concepts=["File", "FileReader", "FileWriter", "BufferedReader",
              "BufferedWriter", "Path", "Files", "Serializable"],
    include_deepen=True,  # <-- COZUM B: Teorik derinlestirme acik
)

print(f"\n{'='*60}")
print(f"Done! Mode: spec+deepen")
print(f"Path: {result.get('path', 'N/A')}")
print(f"Seed time: {result.get('seed_time', 0)}s")
print(f"Deepen time: {result.get('deepen_time', 0)}s")
if 'steps' in result:
    print(f"Steps: {list(result['steps'].keys())}")
print(f"Final length: {len(result.get('final', ''))}")
print(f"{'='*60}")
