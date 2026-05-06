"""Quick 2-model comparison: creative vs precise."""
import sys, time, json, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from bookmaker.llm.openai import OpenAICompatibleClient
from bookmaker.generation.spec import build_seed_from_spec_prompt
from bookmaker.generation.prompts import SYSTEM_AUTHOR

OUT_DIR = Path("D:/bookMaker_Deepseek/book_projects/java-temelleri/build/model_comparison")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SPEC = (Path("D:/bookMaker_Deepseek/book_projects/java-temelleri/build/generation/step0_spec.md")
        .read_text(encoding="utf-8"))
TITLE = "Java Programinin Temel Yapisi, Degiskenler ve Veri Tipleri"
prompt = build_seed_from_spec_prompt(SPEC, TITLE)

def analyze(text, label):
    m = {}
    m["label"] = label
    m["words"] = len(text.split())
    m["chars"] = len(text)
    m["h2"] = len(re.findall(r'^## ', text, re.MULTILINE))
    m["h3"] = len(re.findall(r'^### ', text, re.MULTILINE))
    m["code"] = len(re.findall(r'```', text)) // 2
    m["mermaid"] = len(re.findall(r'```mermaid', text))
    m["inline"] = len(re.findall(r'`[^`]+`', text))
    m["lists"] = len(re.findall(r'^[\s]*[-*] ', text, re.MULTILINE))
    return m

def run(label, temp):
    client = OpenAICompatibleClient(
        api_key="sk-98a85ecced414d499d34caf73a09b80d",
        model="deepseek-chat",
    )
    print(f"[{label}] t={temp} ...", end=" ", flush=True)
    t0 = time.time()
    try:
        result = client.generate_text(SYSTEM_AUTHOR, prompt, temperature=temp)
    except Exception as e:
        print(f"ERROR: {e}")
        return None
    elapsed = time.time() - t0
    metrics = analyze(result, label)
    metrics["elapsed"] = elapsed
    
    out = OUT_DIR / f"seed_{label}.md"
    out.write_text(result, encoding="utf-8")
    
    print(f"{metrics['words']}w, {metrics['h2']}H2, {metrics['code']}code, {elapsed:.1f}s")
    return metrics

print("=" * 60)
print("MODEL KARSILASTIRMASI: Creative vs Precise")
print("=" * 60)
print(f"SPEC: {len(SPEC.split())} words, prompt: {len(prompt.split())} words")
print()

results = {}
r1 = run("creative_t09", 0.9)
if r1: results["creative"] = r1

r2 = run("precise_t03", 0.3)
if r2: results["precise"] = r2

if len(results) >= 2:
    print()
    print("=" * 60)
    print("KARSILASTIRMA")
    print("=" * 60)
    header = f"{'Metrik':<15s}"
    for name in results:
        header += f" {name:>18s}"
    print(header)
    print("-" * len(header))
    
    for key in ["words", "chars", "h2", "h3", "code", "mermaid", "inline", "lists", "elapsed"]:
        row = f"{key:<15s}"
        for name in results:
            val = results[name].get(key, "N/A")
            if isinstance(val, float):
                row += f" {val:>17.1f}"
            else:
                row += f" {str(val):>18s}"
        print(row)

    # Save JSON
    json.dump(results, open(str(OUT_DIR / "comparison.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False, default=str)

print()
print("Done!")
