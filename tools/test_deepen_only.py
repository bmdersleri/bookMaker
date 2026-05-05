"""Test: Sadece DEEPEN adimi — mevcut SEED ciktisina uygula.

Bu test:
1. Mevcut step2_normalized.md (41KB, 3747 kelime) dosyasini okur
2. Sadece _deepen_sections metodunu calistirir
3. Sonucu gosterir

Hedef: ~2x buyume (7500-8000 kelime), max 3x sinir.
"""
import sys
import time
sys.path.insert(0, "src")

from bookmaker.generation.pipeline import ChapterGenerator
from pathlib import Path

gen = ChapterGenerator("book_projects/dummy-kitap")
print(f"Client ready: {gen.is_ready()}")

# Mevcut normalized ciktiyi oku
gen_dir = Path("book_projects/dummy-kitap/build/generation")
norm_path = gen_dir / "step2_normalized.md"
if not norm_path.exists():
    print(f"HATA: {norm_path} bulunamadi!")
    sys.exit(1)

normalized_text = norm_path.read_text(encoding="utf-8")
old_wc = len(normalized_text.split())
print(f"\nMevcut normalized metin: {old_wc} kelime, {len(normalized_text)} karakter")
print(f"{'='*60}")

# Sadece DEEPEN adimini calistir
t0 = time.time()
deepened = gen._deepen_sections(
    text=normalized_text,
    chapter_title="Dosya Isleme ve Kalici Veri Saklama",
    gen_dir=gen_dir,
)
elapsed = time.time() - t0

new_wc = len(deepened.split())
growth = round((new_wc - old_wc) / old_wc * 100)

print(f"\n{'='*60}")
print(f"SONUC:")
print(f"  Once: {old_wc} kelime")
print(f"  Sonra: {new_wc} kelime")
print(f"  Buyume: %{growth} (hedef: ~%100)")
print(f"  Sure: {elapsed:.1f}s")
print(f"{'='*60}")
