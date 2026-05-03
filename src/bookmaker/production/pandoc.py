"""Pandoc ile Markdown → DOCX dönüşümü."""

from __future__ import annotations

import subprocess
from pathlib import Path


def pandoc_available() -> bool:
    """Pandoc CLI erişilebilir mi?"""
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def export_docx(
    markdown_path: Path,
    output_path: Path,
    reference_doc: Path | None = None,
    lua_filter: Path | None = None,
) -> dict:
    """Markdown dosyasını Pandoc ile DOCX'e dönüştürür."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["pandoc", "-f", "markdown+tex_math_single_backslash",
           "-o", str(output_path), str(markdown_path)]

    if reference_doc and reference_doc.exists():
        cmd.extend(["--reference-doc", str(reference_doc)])
    if lua_filter and lua_filter.exists():
        cmd.extend(["--lua-filter", str(lua_filter)])

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        success = proc.returncode == 0 and output_path.exists()
        return {
            "status": "passed" if success else "failed",
            "output": proc.stdout,
            "error": proc.stderr,
            "path": str(output_path) if success else None,
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "output": "", "error": "Pandoc timed out (60s)", "path": None}
    except FileNotFoundError:
        return {"status": "error", "output": "", "error": "pandoc not found in PATH", "path": None}
    except Exception as e:
        return {"status": "error", "output": "", "error": str(e), "path": None}
