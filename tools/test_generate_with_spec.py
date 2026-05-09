"""Test: Chapter generation with spec + intermediate file saving + comparison."""
import sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bookmaker.generation.pipeline import ChapterGenerator
from bookmaker.core.config import load_config

config = load_config(book_name="java-temelleri")
gen = ChapterGenerator(config.project_root)
gen_dir = config.build_dir / "generation"

print(f"Kitap: {config.title}")
print(f"Hazir: {gen.is_ready()}")
print(f"Model: {gen.llm_config.seed_model}")
print(f"Dizin: {gen_dir}")
print()

chapter_id = "bolum-02"
title = "Java Programinin Temel Yapisi, Degiskenler ve Veri Tipleri"
concepts = [
    "Java program yapisi (main metodu, sinif tanimi)",
    "Degisken tanimlama ve veri tipleri (int, double, boolean, char, String)",
    "Tip donusumleri (otomatik ve manuel)",
    "Operatorler (aritmetik, karsilastirma, mantiksal)",
    "Bellek yonetimi (stack, heap, reference tipleri)",
    "Sabitler (final keyword)",
    "Var anahtar kelimesi (local variable type inference)",
]

print("=" * 60)
print(f"SPEC TABANLI BOLUM URETIMI: {chapter_id}")
print("=" * 60)
print(f"Asamalar: SPEC -> DOGRULA -> SEED -> NORMALIZE -> ENRICH -> ASSEMBLE")
print(f"Ara dosyalar: {gen_dir}/")
print()

start_all = time.time()
result = gen.generate_chapter_with_spec(
    chapter_id=chapter_id,
    title=title,
    concepts=concepts,
    chapter_no=2,
    enrich_types=["ozet", "sozluk", "soru", "alistirma", "hata", "kopru"],
)

elapsed = time.time() - start_all
final_text = result.get("final", "")
wc = len(final_text.split()) if final_text else 0

print()
print("=" * 60)
print(f"TAMAMLANDI: {elapsed:.1f}s, {wc} kelime")
print("=" * 60)

# Ara dosyalari listele
print(f"\nUretilen dosyalar ({gen_dir}):")
for f in sorted(gen_dir.glob("*")):
    size = f.stat().st_size
    print(f"  {f.name:40s} {size:>8,} bytes")
