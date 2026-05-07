from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from bookmaker.code.adapters.base import CodeAdapter


class PythonCodeAdapter(CodeAdapter):
    name = "python"
    language = "python"
    fence_languages = ("python",)

    def run_tests(self, blocks: list[str], workdir: Path) -> list[dict]:
        results: list[dict] = []
        for index, block in enumerate(blocks, start=1):
            fpath = workdir / f"block_{index:03d}.py"
            fpath.write_text(block, encoding="utf-8")
            try:
                proc = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(fpath)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(workdir),
                )
            except subprocess.TimeoutExpired:
                results.append({
                    "block": index,
                    "status": "error",
                    "errors": ["py_compile timed out after 30s"],
                    "command": [sys.executable, "-m", "py_compile", str(fpath)],
                })
                continue
            if proc.returncode == 0:
                results.append(
                    {
                        "block": index,
                        "status": "ok",
                        "command": [sys.executable, "-m", "py_compile", str(fpath)],
                    }
                )
            else:
                results.append(
                    {
                        "block": index,
                        "status": "error",
                        "errors": [proc.stderr.strip() or proc.stdout.strip()],
                        "command": [sys.executable, "-m", "py_compile", str(fpath)],
                    }
                )
        return results

