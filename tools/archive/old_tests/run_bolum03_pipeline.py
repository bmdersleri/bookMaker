"""
bolum-03: Tip Dönüşümleri, Sayısal İşlemler ve Operatörler
Pipeline: SPEC → VALIDATE → SEED → NORMALIZE → ENRICH → ASSEMBLE

Usage: python tools/run_bolum03_pipeline.py
"""
import sys, time
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bookmaker.generation.pipeline import ChapterGenerator
from bookmaker.core.config import load_config

config = load_config(book_name="java-temelleri")
gen = ChapterGenerator(config.project_root)
gen_dir = config.build_dir / "generation"
gen_dir.mkdir(parents=True, exist_ok=True)

CHAPTER_ID = "bolum-03"
TITLE = "Tip Dönüşümleri, Sayısal İşlemler ve Operatörler"

CONCEPTS = [
    "Java veri tipleri (byte, short, int, long, float, double, char, boolean)",
    "Otomatik tip dönüşümü (widening casting)",
    "Manuel tip dönüşümü (narrowing casting)",
    "Dönüşüm fonksiyonları (Integer.parseInt, Double.parseDouble, String.valueOf)",
    "Sayısal tipler arası dönüşümler ve veri kaybı",
    "Metin ve sayı arası dönüşümler",
    "Temel aritmetik operatörler (+, -, *, /, %)",
    "İşlem önceliği kuralları",
    "Math sınıfı (pow, sqrt, abs, round, random)",
    "Farklı veri tiplerinde operatör davranışları",
    "String birleştirme ve sayısal toplama farkı",
]

print("=" * 60)
print(f"BOLUM URETIMI: {CHAPTER_ID} — {TITLE}")
print("=" * 60)
print(f"Model: {gen.llm_config.model}")
print(f"Hazir: {gen.is_ready()}")
print(f"Konsept sayisi: {len(CONCEPTS)}")
print()

start_all = time.time()

# Use generate_chapter_with_spec for full pipeline with intermediate saves
result = gen.generate_chapter_with_spec(
    chapter_id=CHAPTER_ID,
    title=TITLE,
    concepts=CONCEPTS,
    chapter_no=3,
    enrich_types=["ozet", "sozluk", "soru", "alistirma", "hata", "kopru"],
)

elapsed = time.time() - start_all
final_text = result.get("final", "")
final_text = final_text or (gen_dir / "step1_seed_raw.md").read_text(encoding="utf-8") if (gen_dir / "step1_seed_raw.md").exists() else ""
wc = len(final_text.split()) if final_text else 0

print()
print("=" * 60)
print(f"TAMAMLANDI: {elapsed:.1f}s, {wc} kelime")
print("=" * 60)

# List generated files
print(f"\nUretilen dosyalar ({gen_dir}):")
for f in sorted(gen_dir.glob("*")):
    size = f.stat().st_size
    age = time.time() - f.stat().st_mtime
    if age < 3600:  # only files from this run
        print(f"  {f.name:45s} {size:>8,} bytes  ({age:.0f}s ago)")

# Summary
print()
print("Timing summary:")
for step, t in result.get("timings", {}).items():
    print(f"  {step}: {t}s")
print(f"  TOTAL: {elapsed:.1f}s")
