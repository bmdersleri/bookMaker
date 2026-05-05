"""Find and diagnose problematic mermaid blocks."""
import re
from pathlib import Path

root = Path("book_projects/java-temelleri")

# Check bolum-14 (0/1 failed) and bolum-17 (1/2 failed)
for cid in ["bolum-14", "bolum-17"]:
    ap = root / "chapters" / cid / "approved" / f"{cid}_v001.md"
    text = ap.read_text("utf-8")
    
    blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text, re.DOTALL))
    print(f"\n=== {cid}: {len(blocks)} mermaid bloklari ===")
    
    for i, b in enumerate(blocks):
        code = b.group(1).strip()
        lines = code.splitlines()
        
        # Check if it looks like valid mermaid
        first_line = lines[0] if lines else "(empty)"
        has_flowchart = "flowchart" in first_line.lower() or "graph" in first_line.lower()
        has_class = "classDiagram" in first_line or "class" in first_line.lower()
        has_sequence = "sequenceDiagram" in first_line.lower()
        
        print(f"\n  Blok #{i+1}:")
        print(f"    Type: {'flowchart' if has_flowchart else 'classDiagram' if has_class else 'sequence' if has_sequence else 'unknown'}")
        print(f"    Lines: {len(lines)}")
        print(f"    First: {first_line[:80]}")
        
        # Check for common issues
        issues = []
        if "```" in code:
            issues.append("Nested backticks!")
        if "&lt;" in code or "&gt;" in code:
            issues.append("HTML entities!")
        lines_with_issues = [j+1 for j, l in enumerate(lines) if len(l) > 200]
        if lines_with_issues:
            issues.append(f"Very long lines: {lines_with_issues}")
        
        if issues:
            print(f"    ISSUES: {', '.join(issues)}")
            # Print the full code
            print(f"    Full code ({len(code)} chars):")
            for j, l in enumerate(lines):
                print(f"      {j+1}: {l[:120]}")
        else:
            print(f"    (looks OK)")
        
        # Check if PNG exists
        png_path = ap.parent / "mermaid_images" / f"diagram_{i+1:03d}.png"
        if png_path.exists():
            print(f"    PNG: {png_path.name} ({png_path.stat().st_size} bytes) OK")
        else:
            print(f"    PNG: MISSING")
