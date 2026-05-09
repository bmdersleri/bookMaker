"""
Model / Sıcaklık Karşılaştırması — ANALİZ MODU

Mevcut dosyaları analiz eder, karşılaştırma tablosu üretir.
Varyantları yeniden ÇALIŞTIRMAZ.

Kullanım: python tools/compare_models.py
"""
import sys, time, json, re
from pathlib import Path
from dataclasses import dataclass, asdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.stdout.reconfigure(encoding='utf-8')

from bookmaker.core.config import load_config
from bookmaker.llm.config import LLMConfig

CONFIG = load_config(book_name="java-temelleri")
OUT_DIR = CONFIG.build_dir / "model_comparison"

# Varyantlar: (label, temperature, filename)
VARIANTS = [
    ("flash_precise",  0.3, "seed_flash_precise_t3.md"),
    ("flash_default",  0.7, "seed_flash_default_t7.md"),
    ("flash_creative", 0.9, "seed_flash_creative_t9.md"),
    ("pro_creative",   0.9, "seed_pro_creative_t9.md"),
]


@dataclass
class VariantResult:
    label: str
    temperature: float
    status: str
    word_count: int = 0
    char_count: int = 0
    h2: int = 0
    h3: int = 0
    code_blocks: int = 0
    mermaid: int = 0
    inline_code: int = 0
    bold: int = 0
    lists: int = 0
    numbered: int = 0
    tables: int = 0
    has_main: bool = False
    has_class: bool = False
    has_println: bool = False
    file_size: int = 0
    error: str = ""
    # Türetilmiş
    richness: int = 0


def analyze(text: str) -> dict:
    return {
        "words": len(text.split()),
        "chars": len(text),
        "h2": len(re.findall(r'^## ', text, re.MULTILINE)),
        "h3": len(re.findall(r'^### ', text, re.MULTILINE)),
        "code_blocks": len(re.findall(r'```', text)) // 2,
        "mermaid": len(re.findall(r'```mermaid', text)),
        "inline_code": len(re.findall(r'`[^`]+`', text)),
        "bold": len(re.findall(r'\*\*[^*]+\*\*', text)),
        "lists": len(re.findall(r'^[\s]*[-*+] ', text, re.MULTILINE)),
        "numbered": len(re.findall(r'^[\s]*\d+\. ', text, re.MULTILINE)),
        "tables": len(re.findall(r'^\|.*\|$', text, re.MULTILINE)),
        "has_main": "public static void main" in text,
        "has_class": "public class" in text,
        "has_println": "System.out.println" in text,
    }


def load_variant(label: str, temp: float, fname: str) -> VariantResult:
    path = OUT_DIR / fname
    if not path.exists():
        return VariantResult(label=label, temperature=temp, status="missing",
                             error=f"Dosya yok: {fname}")

    text = path.read_text(encoding='utf-8')
    m = analyze(text)
    richness = m["code_blocks"] * 5 + m["mermaid"] * 3 + m["lists"] + m["numbered"] + m["bold"] // 2

    return VariantResult(
        label=label,
        temperature=temp,
        status="ok",
        word_count=m["words"],
        char_count=m["chars"],
        h2=m["h2"],
        h3=m["h3"],
        code_blocks=m["code_blocks"],
        mermaid=m["mermaid"],
        inline_code=m["inline_code"],
        bold=m["bold"],
        lists=m["lists"],
        numbered=m["numbered"],
        tables=m["tables"],
        has_main=m["has_main"],
        has_class=m["has_class"],
        has_println=m["has_println"],
        file_size=path.stat().st_size,
        richness=richness,
    )


# ──────────────────────────────────────────────────────────
# ANA
# ──────────────────────────────────────────────────────────

print("=" * 70)
print("S I C A K L I K   K A R S I L A S T I R M A S I")
print("=" * 70)
print(f"Model:    deepseek-chat (v4 Flash)")
print(f"Dizin:    {OUT_DIR}")
print()

results: dict[str, VariantResult] = {}
for label, temp, fname in VARIANTS:
    vr = load_variant(label, temp, fname)
    results[label] = vr
    status_icon = "✅" if vr.status == "ok" else "❌"
    print(f"  {label:18s} t={temp} {status_icon} "
          f"{vr.word_count if vr.status=='ok' else 0:>5d} kel, "
          f"{vr.code_blocks} kod, "
          f"{vr.richness} zenginlik"
          + (f" — {vr.error}" if vr.error else ""))

# ──────────────────────────────────────────────────────────
# TABLO
# ──────────────────────────────────────────────────────────

print()
print("=" * 70)
print("K A R S I L A S T I R M A   T A B L O S U")
print("=" * 70)

METRIC_LABELS = [
    ("word_count",  "Kelime",     "{:>6d}"),
    ("code_blocks", "Kod Blogu",  "{:>6d}"),
    ("inline_code", "Inline Kod", "{:>6d}"),
    ("bold",        "Bold",       "{:>6d}"),
    ("lists",       "Liste",      "{:>6d}"),
    ("numbered",    "Numarali",   "{:>6d}"),
    ("tables",      "Tablo",      "{:>6d}"),
    ("mermaid",     "Mermaid",    "{:>6d}"),
    ("h2",          "H2",         "{:>6d}"),
    ("h3",          "H3",         "{:>6d}"),
    ("richness",    "Zenginlik",  "{:>6d}  "),
]

# Header
hdr = f"{'Metrik':<20s}"
for label, _, _ in VARIANTS:
    hdr += f" {label:>20s}"
print(hdr)
print("-" * len(hdr))

for key, mlabel, fmt in METRIC_LABELS:
    row = f"{mlabel:<20s}"
    for label, _, _ in VARIANTS:
        vr = results[label]
        val = fmt.format(getattr(vr, key, 0)) if vr.status == "ok" else "  HATA "
        row += f" {val:>20s}"
    print(row)

# Boolean metrics
print()
for bool_key, blabel in [("has_main", "main()"), ("has_class", "class"), ("has_println", "println()")]:
    row = f"{blabel:<20s}"
    for label, _, _ in VARIANTS:
        vr = results[label]
        val = "✅" if vr.status == "ok" and getattr(vr, bool_key) else "❌"
        row += f" {val:>20s}"
    print(row)

# File size
row = f"{'Dosya Boyutu':<20s}"
for label, _, _ in VARIANTS:
    vr = results[label]
    val = f"{vr.file_size:,}b" if vr.status == "ok" else "  HATA "
    row += f" {val:>20s}"
print(row)

# ──────────────────────────────────────────────────────────
# ÖZET
# ──────────────────────────────────────────────────────────

print()
print("=" * 70)
print("Ö Z E T")
print("=" * 70)

oks = [k for k, v in results.items() if v.status == "ok"]
errs = [k for k, v in results.items() if v.status != "ok"]
print(f"\nBaşarılı: {len(oks)}/{len(VARIANTS)}")
if errs:
    print(f"Hatalı: {', '.join(errs)}")

# En iyi ve en kötü
if oks:
    best = max(oks, key=lambda k: results[k].richness)
    worst = min(oks, key=lambda k: results[k].richness)
    print(f"\nEn yüksek zenginlik: {best} ({results[best].richness})")
    print(f"En düşük zenginlik:  {worst} ({results[worst].richness})")

# En uzun/kısa
if oks:
    longest = max(oks, key=lambda k: results[k].word_count)
    shortest = min(oks, key=lambda k: results[k].word_count)
    print(f"En uzun:  {longest} ({results[longest].word_count} kelime)")
    print(f"En kısa:  {shortest} ({results[shortest].word_count} kelime)")

# ──────────────────────────────────────────────────────────
# JSON KAYDI
# ──────────────────────────────────────────────────────────

comparison = {
    "config": {
        "model": "deepseek-chat (v4 Flash)",
        "description": "Sıcaklık karşılaştırması: t=0.3, t=0.7, t=0.9",
    },
    "variants": {k: asdict(v) for k, v in results.items()},
}
json_path = OUT_DIR / "comparison.json"
json_path.write_text(json.dumps(comparison, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nJSON: {json_path}")

# Dosya listesi
print(f"\nDosyalar:")
for f in sorted(OUT_DIR.glob("*")):
    print(f"  {f.name:45s} {f.stat().st_size:>8,} bytes")

print()
print("=" * 70)
print("T A M A M L A N D I")
print("=" * 70)
