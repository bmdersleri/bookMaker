"""bolum-06: Nesne Yonelimli Programlama — pipeline ile uret."""
import os
import sys
from pathlib import Path

os.environ["PYTHONIOENCODING"] = "utf-8"

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bookmaker.generation.pipeline import ChapterGenerator

PROJECT = Path(__file__).resolve().parents[1] / "book_projects" / "dummy-kitap"

gen = ChapterGenerator(PROJECT)

if not gen.is_ready():
    print("HATA: LLM API yapilandirilmamis!")
    sys.exit(1)

print(f"Model: {gen.llm_config.model}")
print(f"Provider: {gen.llm_config.provider}")
print()

result = gen.generate_chapter_with_spec(
    chapter_id="bolum-06",
    title="Nesne Yonelimli Programlama",
    concepts=[
        "Sinif (Class)",
        "Nesne (Object)",
        "Constructor",
        "Encapsulation (Kapsulleme)",
        "Access Modifiers (public, private, protected)",
        "this anahtar kelimesi",
        "static uyeler",
        "Get/Set metotlari",
        "final degiskenler",
        "Method Overloading",
    ],
    chapter_no=6,
    enrich_types=["ozet", "sozluk", "soru", "alistirma", "hata", "kopru"],
    next_chapter="Kalitim ve Polimorfizm",
    save=True,
)

print("\n=== SONUC ===")
print(f"Kelime: {len(result.get('final', '').split())}")
print(f"Sure: {result.get('total_time', '?')}s")
print(f"Dosya: {result.get('path', '?')}")
