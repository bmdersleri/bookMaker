"""Quick rebuild: only chapters with mermaid blocks."""
import time
from pathlib import Path
from bookmaker.production.pandoc import export_docx

root = Path("book_projects/java-temelleri")
out_dir = root / "build" / "exports"
out_dir.mkdir(parents=True, exist_ok=True)

# Get all approved files
chapters = list(root.glob("chapters/*/approved/*.md"))
print(f"Rebuilding {len(chapters)} chapters with mermaid images...\n")

for md in chapters:
    cid = md.parent.parent.name
    out = out_dir / f"{cid}.docx"
    
    start = time.time()
    result = export_docx(md, out, render_mermaid=True)
    elapsed = time.time() - start
    
    if result["status"] == "passed":
        kb = result["size"] / 1024
        m_ok = sum(1 for r in result.get("mermaid_results", []) if r["status"] == "passed")
        m_tot = len(result.get("mermaid_results", []))
        m_str = f", mermaid {m_ok}/{m_tot}" if m_tot > 0 else ""
        print(f"  OK {cid}: {kb:.0f}KB ({elapsed:.1f}s){m_str}")
    else:
        print(f"  FAIL {cid}: {result.get('error','')[:80]}")

print(f"\nDone! All chapters rebuilt.")
