"""Quick validation of all prompt changes."""
import sys
sys.path.insert(0, "src")
from bookmaker.generation.prompts import (
    SYSTEM_AUTHOR, build_seed_prompt, build_enrich_glossary_prompt,
    build_enrich_questions_prompt, build_enrich_exercises_prompt,
    build_enrich_summary_prompt, build_enrich_bridge_prompt,
    build_enrich_errors_prompt, build_enrich_deepen_prompt,
)
from bookmaker.generation.spec import build_seed_from_spec_prompt

PASS, FAIL = 0, 0
def check(name, condition):
    global PASS, FAIL
    if condition: PASS += 1; print(f"  [PASS] {name}")
    else: FAIL += 1; print(f"  [FAIL] {name}")

# 1. SYSTEM_AUTHOR has 6-step chain
print("=== SYSTEM_AUTHOR ===")
for step in ["TANIM", "NEDEN VAR?", "NASIL KULLANILIR",
             "NE ZAMAN TERCİH", "ALTERNATİFLERİ", "YAYGIN HATALAR"]:
    check(f"SYSTEM_AUTHOR: {step}", step in SYSTEM_AUTHOR)
check("SYSTEM_AUTHOR: Mermaid 5 dugum", "5 düğüm" in SYSTEM_AUTHOR)
check("SYSTEM_AUTHOR: Mermaid istege bagli", "isteğe bağlı" in SYSTEM_AUTHOR)
check("SYSTEM_AUTHOR: Mermaid sequence diagram", "sequence diagram" in SYSTEM_AUTHOR)

# 2. build_seed_prompt
print("\n=== build_seed_prompt ===")
p = build_seed_prompt("Test Bolum", ["k1", "k2", "k3"], chapter_no=5)
check("Seed: TANIM adimi", "TANIM" in p)
check("Seed: NEDEN VAR adimi", "NEDEN VAR?" in p)
check("Seed: NASIL KULLANILIR adimi", "NASIL KULLANILIR?" in p)
check("Seed: NE ZAMAN TERCİH adimi", "NE ZAMAN TERCİH" in p)
check("Seed: ALTERNATİFLERİ adimi", "ALTERNATİFLERİ" in p)
check("Seed: YAYGIN HATALAR adimi", "YAYGIN HATALAR" in p)
check("Seed: kod ZORUNLU DEGIL", "ZORUNLU DEĞİL" in p)
check("Seed: yol haritasi exempt", "yol haritası" in p)
check("Seed: mermaid istege bagli (zorunlu degil)", "mermaid" in p.lower() and "diyagramsız bölüm eksiktir" not in p.lower())
check("Seed: degisken isimleri Turkce", "anlamlı Türkçe" in p)
check("Seed: // Cikti gosterimi", "// Çıktı:" in p)

# 3. build_seed_from_spec_prompt
print("\n=== build_seed_from_spec_prompt ===")
p2 = build_seed_from_spec_prompt("spec content", "Test")
check("Spec: TANIM", "TANIM" in p2)
check("Spec: NEDEN VAR", "NEDEN VAR?" in p2)
check("Spec: kod ZORUNLU DEGIL", "ZORUNLU DEĞİL" in p2)

# 4. Enrichment prompts accept concepts
print("\n=== Enrichment prompts ===")
ctx = "X" * 2500
for name, fn in [
    ("glossary", build_enrich_glossary_prompt),
    ("questions", build_enrich_questions_prompt),
    ("exercises", build_enrich_exercises_prompt),
    ("summary", build_enrich_summary_prompt),
    ("errors", build_enrich_errors_prompt),
]:
    p3 = fn("Test", ["H1", "H2"], ctx, ["kavram1", "kavram2"])
    check(f"{name}: concepts section", "İşlenen kavramlar" in p3)
    check(f"{name}: kavram1 present", "kavram1" in p3)
    check(f"{name}: context 2000+", "XXXX" in p3)

p4 = build_enrich_bridge_prompt("Test", "Next", ["H1"], ctx, ["k1"])
check("bridge: concepts section", "İşlenen kavramlar" in p4)
check("bridge: next chapter", "Next" in p4)

print(f"\n===== {PASS}/{PASS+FAIL} PASSED =====")
sys.exit(0 if FAIL == 0 else 1)
