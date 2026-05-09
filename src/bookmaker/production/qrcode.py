"""QR kod üretimi (qr CLI + pillow)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def generate_qr(data: str, output_path: Path) -> dict:
    """Bir URL/metin için QR kodu PNG olarak üretir."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        proc = subprocess.run(
            ["qr", "--output", str(output_path), data],
            capture_output=True, text=True, timeout=15,
        )
        success = proc.returncode == 0 and output_path.exists()
        return {
            "status": "passed" if success else "failed",
            "data": data,
            "path": str(output_path) if success else None,
            "error": proc.stderr if not success else "",
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "data": data, "path": None, "error": "Timeout"}
    except FileNotFoundError:
        return {"status": "error", "data": data, "path": None, "error": "qr CLI not found"}
    except Exception as e:
        return {"status": "error", "data": data, "path": None, "error": str(e)}


def generate_from_manifest(code_manifest: list[dict], output_dir: Path) -> list[dict]:
    """Code manifest'teki her kod için QR üretir."""
    results: list[dict] = []
    for item in code_manifest:
        url = item.get("github_url", "")
        code_id = item.get("code_id", "unknown")
        if not url:
            results.append({
                "code_id": code_id, "status": "skipped",
                "data": "", "path": None, "error": "No URL",
            })
            continue
        out = output_dir / f"{code_id}_qr.png"
        result = generate_qr(url, out)
        result["code_id"] = code_id
        results.append(result)
    return results
