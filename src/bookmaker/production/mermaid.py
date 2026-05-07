"""Mermaid şema → PNG render (mmdc CLI via PowerShell).

Config kullanimi (book_manifest.yaml -> BookConfig -> mermaid_mmdc_cmd):
    config = BookConfig(project_root)
    cmd = config.mermaid_mmdc_cmd  # ['pwsh.exe', '-NoProfile', '-Command', 'mmdc']
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from bookmaker.core.config import BookConfig


def render_mermaid(
    code: str,
    output_path: Path,
    config: BookConfig | None = None,
    timeout: int | None = None,
) -> dict:
    """Tek bir Mermaid kodunu PNG'ye donusturur.

    Args:
        code: Mermaid diyagram kodu
        output_path: Cikis PNG yolu
        config: Kitap config (None = varsayilan ayarlar)
        timeout: Saniye cinsinden zaman asimi (None = config'den)

    Returns:
        {'status': 'passed'|'failed'|'timeout'|'error',
         'output': str, 'error': str, 'path': str|None}

    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    mmd_path = output_path.with_suffix(".mmd")
    mmd_path.write_text(code, encoding="utf-8")

    # mmdc komutunu config'den al
    if config:
        mmdc_cmd = config.mermaid_mmdc_cmd
        bg = config.mermaid_background
        timeout_val = timeout or config.mermaid_timeout
    else:
        mmdc_cmd = [
            "C:\\Program Files\\PowerShell\\7\\pwsh.exe",
            "-NoProfile", "-Command", "mmdc",
        ]
        bg = "white"
        timeout_val = timeout or 30

    cmd = mmdc_cmd + [
        "-i", str(mmd_path),
        "-o", str(output_path),
        "-f",
        "-b", bg,
    ]

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout_val,
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
    except Exception as e:
        return {"status": "error", "output": "", "error": str(e), "path": None}
    finally:
        if mmd_path.exists():
            mmd_path.unlink()


def extract_mermaid_blocks(text: str) -> list[dict]:
    """Markdown metninden Mermaid kod bloklarini cikarir."""
    pattern = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
    return [
        {
            "index": i,
            "code": match.group(1).strip(),
            "start": match.start(),
            "end": match.end(),
        }
        for i, match in enumerate(pattern.finditer(text))
    ]


def render_from_file(
    markdown_path: Path,
    output_dir: Path,
    config: BookConfig | None = None,
) -> list[dict]:
    """Markdown dosyasindaki tum Mermaid bloklarini render eder."""
    text = markdown_path.read_text(encoding="utf-8")
    blocks = extract_mermaid_blocks(text)
    results: list[dict] = []

    for i, block in enumerate(blocks):
        out = output_dir / f"mermaid_{i:03d}.png"
        result = render_mermaid(block["code"], out, config=config)
        result["index"] = i
        results.append(result)

    return results
