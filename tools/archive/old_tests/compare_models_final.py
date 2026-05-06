"""Compare original (t=0.7) vs creative (t=0.9) SEED outputs."""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def analyze(path, label):
    text = Path(path).read_text(encoding='utf-8')
    return {
        "label": label,
        "words": len(text.split()),
        "chars": len(text),
        "h2": len(re.findall(r'^## ', text, re.MULTILINE)),
        "h3": len(re.findall(r'^### ', text, re.MULTILINE)),
        "code": len(re.findall(r'```', text)) // 2,
        "mermaid": len(re.findall(r'```mermaid', text)),
        "inline": len(re.findall(r'`[^`]+`', text)),
        "bold": len(re.findall(r'\*\*[^*]+\*\*', text)),
        "lists": len(re.findall(r'^[\s]*[-*] ', text, re.MULTILINE)),
        "numbered": len(re.findall(r'^[\s]*\d+\. ', text, re.MULTILINE)),
        "tables": len(re.findall(r'^\|.*\|$', text, re.MULTILINE)),
        "has_main": "public static void main" in text,
        "has_class": "public class" in text,
        "has_sout": "System.out.println" in text,
    }

base = Path("D:/bookMaker_Deepseek/book_projects/java-temelleri/build")
r1 = analyze(base / "generation/step1_seed_raw.md", "Original (t=0.7)")
r2 = analyze(base / "model_comparison/seed_pro_creative_t9.md", "Creative (t=0.9)")

print("=" * 70)
print("MODEL KARSILASTIRMASI: t=0.7 vs t=0.9")
print("=" * 70)
print()

header = f"{'Metrik':<20s} {'Orijinal (t=0.7)':>18s} {'Creative (t=0.9)':>18s} {'Fark':>10s}"
print(header)
print("-" * len(header))

for key in ["words", "chars", "h2", "h3", "code", "mermaid", "inline", "bold", "lists", "numbered", "tables"]:
    v1 = r1[key]
    v2 = r2[key]
    diff = v2 - v1
    sign = "+" if diff > 0 else ""
    print(f"{key:<20s} {str(v1):>18s} {str(v2):>18s} {sign}{diff:>9d}")

print()
print("Java-specific:")
for key in ["has_main", "has_class", "has_sout"]:
    print(f"  {key:<20s} {'Evet' if r1[key] else 'Hayir':>18s} {'Evet' if r2[key] else 'Hayir':>18s}")

# Sample comparison
print()
print("=" * 70)
print("ORNEK KARSILASTIRMA (ilk 300 karakter)")
print("=" * 70)

t1 = Path(base / "generation/step1_seed_raw.md").read_text(encoding='utf-8')
t2 = Path(base / "model_comparison/seed_pro_creative_t9.md").read_text(encoding='utf-8')

print(f"\n[Original t=0.7]")
print(t1[:300])
print(f"\n[Creative t=0.9]")
print(t2[:300])

# Code block comparison
def count_code_lines(text):
    blocks = re.findall(r'```(?:\w+)?\n(.*?)```', text, re.DOTALL)
    total = 0
    for b in blocks:
        total += len(b.strip().split('\n'))
    return total

print()
print("=" * 70)
print("KOD KARMASIKLIGI")
print("=" * 70)
print(f"  Original: {count_code_lines(t1)} satir kod")
print(f"  Creative: {count_code_lines(t2)} satir kod")
