"""Compare Pro vs Flash models for chapter generation quality."""
import sys, time, json
from pathlib import Path
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bookmaker.core.config import load_config
from bookmaker.generation.pipeline import ChapterGenerator
from bookmaker.llm.openai import OpenAICompatibleClient
from bookmaker.llm.config import LLMConfig
from bookmaker.generation.prompts import SYSTEM_AUTHOR

CONFIG = load_config(book_name="java-temelleri")
OUT_DIR = CONFIG.build_dir / "model_comparison"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODELS = {
    "pro": "deepseek-chat",      # deepseek-v4-pro
    "flash": "deepseek-chat",    # deepseek-v4-flash (same endpoint)
}

TITLE = "Java Programinin Temel Yapisi, Degiskenler ve Veri Tipleri"

# Use existing SPEC for consistency
SPEC = (CONFIG.build_dir / "generation" / "step0_spec.md").read_text(encoding="utf-8")

@dataclass
class ModelResult:
    model: str
    elapsed: float
    word_count: int
    char_count: int
    h2_count: int
    code_blocks: int
    output: str

def run_model(label: str, model_name: str, temperature: float = 0.7) -> ModelResult:
    """Run SEED generation with a specific model and measure."""
    from bookmaker.llm.openai import OpenAICompatibleClient
    from bookmaker.llm.config import LLMConfig
    from bookmaker.generation.spec import build_seed_from_spec_prompt

    client = OpenAICompatibleClient(
        base_url="https://api.deepseek.com/v1",
        api_key="sk-98a85ecced414d499d34caf73a09b80d",
        model=model_name,
    )

    prompt = build_seed_from_spec_prompt(SPEC, TITLE)
    
    print(f"[{label}] Generating with {model_name} (t={temperature})...", end=" ", flush=True)
    t0 = time.time()
    result = client.generate_text(SYSTEM_AUTHOR, prompt, temperature=temperature)
    elapsed = time.time() - t0
    
    import re
    h2_count = len(re.findall(r'^## ', result, re.MULTILINE))
    code_blocks = len(re.findall(r'```', result)) // 2
    
    mr = ModelResult(
        model=label,
        elapsed=elapsed,
        word_count=len(result.split()),
        char_count=len(result),
        h2_count=h2_count,
        code_blocks=code_blocks,
        output=result,
    )
    
    print(f"{mr.word_count} words, {mr.h2_count} H2, {mr.code_blocks} code, {elapsed:.1f}s")
    
    # Save
    out_path = OUT_DIR / f"seed_{label}_t{int(temperature*10)}.md"
    out_path.write_text(result, encoding="utf-8")
    
    return mr

def analyze_quality(text: str) -> dict:
    """Analyze chapter quality metrics."""
    import re
    
    metrics = {}
    metrics["words"] = len(text.split())
    metrics["chars"] = len(text)
    metrics["h2"] = len(re.findall(r'^## ', text, re.MULTILINE))
    metrics["h3"] = len(re.findall(r'^### ', text, re.MULTILINE))
    metrics["code_blocks"] = len(re.findall(r'```', text)) // 2
    metrics["mermaid"] = len(re.findall(r'```mermaid', text))
    metrics["inline_code"] = len(re.findall(r'`[^`]+`', text))
    metrics["bold"] = len(re.findall(r'\*\*[^*]+\*\*', text))
    metrics["lists"] = len(re.findall(r'^[\s]*[-*] ', text, re.MULTILINE))
    metrics["numbered"] = len(re.findall(r'^[\s]*\d+\. ', text, re.MULTILINE))
    metrics["tables"] = len(re.findall(r'^\|.*\|$', text, re.MULTILINE))
    
    # Java-specific checks
    metrics["has_main_method"] = "public static void main" in text
    metrics["has_class"] = "public class" in text
    metrics["has_println"] = "System.out.println" in text
    
    return metrics

print("=" * 70)
print("MODEL KARSILASTIRMASI: Pro vs Flash")
print("=" * 70)
print(f"Bolum: {TITLE}")
print(f"SPEC: {len(SPEC.split())} words")
print()

# Run both models
results = {}

# PRO model - creative temperature
results["pro_creative"] = run_model("pro_creative", MODELS["pro"], temperature=0.9)

# PRO model - precise temperature
results["pro_precise"] = run_model("pro_precise", MODELS["pro"], temperature=0.3)

# FLASH model - creative
results["flash_creative"] = run_model("flash_creative", MODELS["flash"], temperature=0.9)

# FLASH model - precise
results["flash_precise"] = run_model("flash_precise", MODELS["flash"], temperature=0.3)

# Analyze all
print()
print("=" * 70)
print("DETAYLI METRIK ANALIZI")
print("=" * 70)

header = f"{'Metrik':<25s}"
for name in results:
    header += f" {name:>16s}"
print(header)
print("-" * len(header))

all_metrics = {}
for name, mr in results.items():
    all_metrics[name] = analyze_quality(mr.output)

metric_names = ["words", "chars", "h2", "h3", "code_blocks", "mermaid", 
                "inline_code", "bold", "lists", "numbered", "tables",
                "has_main_method", "has_class", "has_println"]

for metric in metric_names:
    row = f"{metric:<25s}"
    for name in results:
        val = all_metrics[name].get(metric, "N/A")
        if isinstance(val, bool):
            val = "Evet" if val else "Hayir"
        elif isinstance(val, (int, float)):
            val = f"{val:,}"
        row += f" {str(val):>16s}"
    print(row)

# Timing comparison
print(f"\n{'Elapsed (s)':<25s}", end="")
for name, mr in results.items():
    print(f" {mr.elapsed:>16.1f}", end="")
print()

# Save comparison JSON
comparison = {
    "config": {
        "title": TITLE,
        "spec_words": len(SPEC.split()),
        "models": MODELS,
    },
    "results": {
        name: {
            "timing": {"elapsed_s": mr.elapsed},
            "metrics": all_metrics[name],
        }
        for name, mr in results.items()
    }
}
json_path = OUT_DIR / "comparison.json"
json_path.write_text(json.dumps(comparison, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"\nKarsilastirma kaydedildi: {json_path}")
print(f"Ciktilar: {OUT_DIR}")
for f in sorted(OUT_DIR.glob("*.md")):
    print(f"  {f.name} ({f.stat().st_size:,} bytes)")

print("\n" + "=" * 70)
print("TAMAMLANDI")
print("=" * 70)
