from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from bookmaker.code.adapters.base import CodeAdapter
from bookmaker.code.extractor import extract_blocks_tagged

_JS_LANGUAGES: frozenset[str] = frozenset({"javascript", "js"})


class ReactCodeAdapter(CodeAdapter):
    name = "react"
    language = "javascript"
    fence_languages = ("javascript", "js", "jsx", "tsx", "typescript", "ts")

    def extract_blocks(self, text: str) -> list[tuple[str, str]]:
        return extract_blocks_tagged(text, self.fence_languages)

    def run_tests(
        self, blocks: list[tuple[str, str]], workdir: Path,
    ) -> list[dict]:
        results: list[dict] = []
        node = shutil.which("node")

        for index, (lang, content) in enumerate(blocks, start=1):
            fpath = workdir / f"block_{index:03d}.js"
            fpath.write_text(content, encoding="utf-8")

            if lang not in _JS_LANGUAGES:
                results.append({
                    "block": index,
                    "status": "skipped",
                    "reason": f"dil_{lang}_review_only",
                    "command": [],
                })
                continue

            if not node:
                results.append({
                    "block": index,
                    "status": "skipped",
                    "reason": "node_bulunamadi",
                    "command": ["node", "--check", str(fpath)],
                })
                continue

            try:
                proc = subprocess.run(
                    [node, "--check", str(fpath)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(workdir),
                )
            except subprocess.TimeoutExpired:
                results.append({
                    "block": index,
                    "status": "error",
                    "errors": ["node --check timed out after 30s"],
                    "command": [node, "--check", str(fpath)],
                })
                continue

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
