"""Ek C test sonuclariyla progress ve estimate'i guncelle."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. Progress guncelle
prog_path = ROOT / "build" / "reports" / "batch_progress.json"
data = json.loads(prog_path.read_text(encoding="utf-8"))
data["4"]["chapters"]["ek-c"] = {
    "title": "Mini Proje Fikirleri ve Rubrikler",
    "status": "OK",
    "chars": 30327,
    "elapsed_s": 107.9,
    "timestamp": "2026-05-04 08:15:00",
}
prog_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"[OK] Progress guncellendi: ek-c = 30,327 chars")

# 2. CHAPTER_SIZE_ESTIMATE guncelle
bv2_path = ROOT / "tools" / "batch_v2.py"
content = bv2_path.read_text(encoding="utf-8")
content = content.replace('"ek-c": 16000', '"ek-c": 30000')
bv2_path.write_text(content, encoding="utf-8")
print(f"[OK] CHAPTER_SIZE_ESTIMATE guncellendi: ek-c = 30,000 chars")

# 3. Yeni ek-c icerik analizi
text = (ROOT / "chapters" / "ek-c" / "draft_versions" / "v001.md").read_text(encoding="utf-8")
import re
mermaid = len(re.findall(r"```mermaid", text))
code_blocks = len(re.findall(r"```java", text))
meta = len(re.findall(r"<!-- CODE_META", text))
print(f"\n[OK] Yeni Ek C icerik analizi:")
print(f"    Toplam: {len(text):,} chars")
print(f"    Mermaid: {mermaid} diyagram")
print(f"    Java kodu: {code_blocks} blok")
print(f"    CODE_META: {meta} blok")
