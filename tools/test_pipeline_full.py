"""
Pipeline kapsamli test — tum prompt ve ciktilari kaydeder.

Kullanim: python tools/test_pipeline_full.py
"""
import sys, time, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)

from bookmaker.generation.pipeline import ChapterGenerator
from bookmaker.generation.prompts import (
    SYSTEM_AUTHOR, build_seed_prompt, build_enrich_deepen_prompt,
)
from bookmaker.generation.spec import build_spec_prompt, build_spec_validation_prompt
from bookmaker.core.config import load_config

# ---- Config -------------------------------------------------
config = load_config(book_name="java-temelleri")
gen = ChapterGenerator(config.project_root)
gen_dir = config.build_dir / "test_pipeline" / time.strftime("%Y%m%d_%H%M%S")
gen_dir.mkdir(parents=True, exist_ok=True)

# Save config snapshot
(gen_dir / "config.json").write_text(json.dumps({
    "model": gen.llm_config.model,
    "provider": gen.llm_config.provider,
    "project_root": str(config.project_root),
}, ensure_ascii=False, indent=2), encoding="utf-8")

# ---- Test Chapter -------------------------------------------
CHAPTER_ID = "test-ch"
TITLE = "String Isleme ve Metin Manipulasyonu"
CHAPTER_NO = 10
CONCEPTS = [
    "String sinifi ve immutable yapisi",
    "String havuzu (String Pool) ve bellek yonetimi",
    "Temel String metodlari: length(), charAt(), substring(), indexOf()",
    "String karsilastirma: equals() vs ==",
    "String birlestirme: concat(), StringBuilder ve StringBuffer",
    "Regular Expressions (Regex) temelleri",
    "StringTokenizer ve split() ile metin parcalama",
    "Metin formatlama: String.format() ve printf()",
]
ENRICH_TYPES = ["ozet", "sozluk", "soru", "alistirma", "hata", "kopru"]
NEXT_CHAPTER = "Dosya Isleme ve Kalici Veri Saklama"

# ---- Save inputs --------------------------------------------
(gen_dir / "input_chapter_id.txt").write_text(CHAPTER_ID)
(gen_dir / "input_title.txt").write_text(TITLE)
(gen_dir / "input_concepts.json").write_text(
    json.dumps(CONCEPTS, ensure_ascii=False, indent=2), encoding="utf-8")

print("=" * 70)
print(f"PIPELINE TEST: {CHAPTER_ID} — {TITLE}")
print(f"Model: {gen.llm_config.model}")
print(f"Output: {gen_dir}")
print(f"Ready: {gen.is_ready()}")
print("=" * 70)

if not gen.is_ready():
    print("FATAL: LLM API not configured!")
    sys.exit(1)

# ---- STEP 0: Save SYSTEM prompt -----------------------------
(gen_dir / "step0_SYSTEM_AUTHOR.txt").write_text(SYSTEM_AUTHOR, encoding="utf-8")
print(f"\nSYSTEM_AUTHOR saved: {len(SYSTEM_AUTHOR)} chars")

# ---- Run pipeline -------------------------------------------
t0 = time.time()

try:
    result = gen.generate_chapter_with_spec(
        chapter_id=CHAPTER_ID,
        title=TITLE,
        concepts=CONCEPTS,
        chapter_no=CHAPTER_NO,
        enrich_types=ENRICH_TYPES,
        next_chapter=NEXT_CHAPTER,
        save=True,
    )
    success = True
    error_msg = None
except Exception as e:
    success = False
    error_msg = str(e)
    import traceback
    error_trace = traceback.format_exc()
    (gen_dir / "ERROR.txt").write_text(error_trace, encoding="utf-8")
    print(f"\nPIPELINE FAILED: {e}")
    print(error_trace)

# ---- Collect generated files --------------------------------
gen_output = config.build_dir / "generation"
all_files = {}
if gen_output.exists():
    for f in sorted(gen_output.rglob("*")):
        if f.is_file():
            rel = str(f.relative_to(gen_output))
            size = f.stat().st_size
            all_files[rel] = size
            print(f"  {rel:50s} {size:>8,} bytes")

# ---- Final metrics ------------------------------------------
elapsed = time.time() - t0

if success:
    final_path = result.get("path", "")
    final_text = ""
    if final_path and Path(final_path).exists():
        final_text = Path(final_path).read_text(encoding="utf-8")
    elif all_files:
        # try to find final
        for fname in all_files:
            if fname.endswith("step4_final.md") or fname.endswith("final.md"):
                final_text = (gen_output / fname).read_text(encoding="utf-8")
                break

    wc = len(final_text.split()) if final_text else 0
    metrics = {
        "success": True,
        "chapter_id": CHAPTER_ID,
        "title": TITLE,
        "words": wc,
        "chars": len(final_text),
        "total_time_seconds": round(elapsed, 1),
        "model": gen.llm_config.model,
        "files_generated": len(all_files),
        "timings": result.get("timings", {}),
        "deepen_time": result.get("deepen_time", 0),
        "seed_time": result.get("seed_time", 0),
        "missing_count": len(result.get("missing", [])),
        "enriched_count": len(result.get("enriched", {})),
    }

    (gen_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{'='*70}")
    print(f"COMPLETE: {wc:,} words, {elapsed:.1f}s")
    print(f"Seed: {result.get('seed_time', '?')}s")
    print(f"Deepen: {result.get('deepen_time', 0)}s")
    print(f"Missing sections: {len(result.get('missing', []))}")
    print(f"Enriched: {len(result.get('enriched', {}))}")
    print(f"Output dir: {gen_dir}")
    print(f"Generation dir: {gen_output}")
    print(f"{'='*70}")
else:
    metrics = {
        "success": False,
        "error": error_msg,
        "total_time_seconds": round(elapsed, 1),
    }
    (gen_dir / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

sys.exit(0 if success else 1)
