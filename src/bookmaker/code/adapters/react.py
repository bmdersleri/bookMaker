from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from bookmaker.code.adapters.base import CodeAdapter


class ReactCodeAdapter(CodeAdapter):
    name = "react"
    language = "javascript"
    fence_languages = ("javascript", "js", "jsx", "tsx", "typescript", "ts")

    def run_tests(self, blocks: list[str], workdir: Path) -> list[dict]:
        results: list[dict] = []
        node = shutil.which("node")

        for index, block in enumerate(blocks, start=1):
            fpath = workdir / f"block_{index:03d}.js"
            fpath.write_text(block, encoding="utf-8")

            if not node:
                results.append({
                    "block": index,
                    "status": "skipped",
                    "reason": "node_bulunamadi",
                    "command": ["node", "--check", str(fpath)],
                })
                continue

            proc = subprocess.run(
                [node, "--check", str(fpath)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(workdir),
            )
            if proc.returncode == 0:
                results.append({
                    "block": index,
                    "status": "ok",
                    "command": [node, "--check", str(fpath)],
                })
            else:
                results.append({
                    "block": index,
                    "status": "error",
                    "errors": [proc.stderr.strip() or proc.stdout.strip()],
                    "command": [node, "--check", str(fpath)],
                })

        return results

