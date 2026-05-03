"""Mermaid şema → PNG render (mmdc CLI)."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


def extract_mermaid_blocks(text: str) -> list[dict]:
    """Markdown metninden Mermaid kod bloklarını çıkarır."""
    blocks: list[dict] = []
    pattern = re.compile(
        r"```mermaid\s*\n(.*?)```", re.DOTALL
    )
    for i, match in enumerate(pattern.finditer(text)):
        blocks.append({
            "index": i,
            "code": match.group(1).strip(),
            "start": match.start(),
            "end": match.end(),
        })
    return blocks


def render_mermaid(code: str, output_path: Path, timeout: int = 30) -> dict:
    """Tek bir Mermaid kodunu PNG'ye dönüştürür."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Geçici .mmd dosyası yaz
    mmd_path = output_path.with_suffix(".mmd")
    mmd_path.write_text(code, encoding="utf-8")

    try:
        proc = subprocess.run(
            ["mmdc", "-i", str(mmd_path), "-o", str(output_path), "-f"],
            capture_output=True, text=True, timeout=timeout,
        )
        success = proc.returncode == 0 and output_path.exists()
        return {
            "status": "passed" if success else "failed",
            "output": proc.stdout,
            "error": proc.stderr,
            "path": str(output_path) if success else None,
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "output": "", "error": "Timed out", "path": None}
    except FileNotFoundError:
        return {"status": "error", "output": "", "error": "mmdc not found", "path": None}
    except Exception as e:
        return {"status": "error", "output": "", "error": str(e), "path": None}
    finally:
        if mmd_path.exists():
            mmd_path.unlink()


def render_from_file(markdown_path: Path, output_dir: Path) -> list[dict]:
    """Markdown dosyasındaki tüm Mermaid bloklarını render eder."""
    text = markdown_path.read_text(encoding="utf-8")
    blocks = extract_mermaid_blocks(text)
    results: list[dict] = []

    for i, block in enumerate(blocks):
        out = output_dir / f"mermaid_{i:03d}.png"
        result = render_mermaid(block["code"], out)
        result["index"] = i
        results.append(result)

    return results
