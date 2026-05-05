"""pipeline_state.yaml dogrulama scripti."""
import yaml
from pathlib import Path
from bookmaker.core.config import BookConfig

# 1. book_profile.yaml dogrulama
profile = Path("book_projects/java-temelleri/book_profile.yaml")
d = yaml.safe_load(profile.read_text("utf-8"))
ch = d.get("chapters", [])
print("=== book_profile.yaml ===")
print("Schema:", d.get("schema",{}).get("manifest_version"))
print("Book:", d["book"]["title"]["tr"])
print("Bolum:", len(ch))
approved = sum(1 for c in ch if c.get("status") == "approved")
print("Onayli:", approved)
print("DOCX:", d.get("statistics",{}).get("combined_docx_size_kb"), "KB")

# 2. pipeline_state.yaml dogrulama
state = Path("book_projects/java-temelleri/pipeline_state.yaml")
s = yaml.safe_load(state.read_text("utf-8"))
print()
print("=== pipeline_state.yaml ===")
print("Pipeline:", s.get("pipeline_id"))
print("Stage:", s.get("current_stage"))
chs = s.get("chapters", {})
print("Bolum:", len(chs))
blocked = [k for k,v in chs.items() if v.get("decision") == "blocked"]
print("Bloke:", len(blocked), blocked)
total_m = sum(v.get("mermaid_count",0) for v in chs.values())
print("Mermaid:", total_m)

# 3. Cross-check
profile_ids = {c["chapter_id"] for c in ch}
state_ids = set(chs.keys())
missing_in_state = profile_ids - state_ids
missing_in_profile = state_ids - profile_ids
if missing_in_state:
    print("\n[HATA] Profilde var ama state'te yok:", missing_in_state)
if missing_in_profile:
    print("\n[HATA] State'te var ama profilde yok:", missing_in_profile)
if not missing_in_state and not missing_in_profile:
    print("\n[OK] Her iki dosyadaki bolum listeleri eslesiyor")

# 4. BookConfig ile yukle
cfg = BookConfig(Path("book_projects/java-temelleri"))
print()
print("=== BookConfig ===")
print("book_id:", cfg.book_id)
print("DOCX name:", cfg.output_docx_path.name)
print("Total words: {:,}".format(cfg.total_words))

print()
print("TUM DOGRULAMALAR BASARILI!")
