"""React/JavaScript code adapter for bookMaker.

Syntax-checks extracted JavaScript code blocks with node --check.
Other frontend languages (JSX, TSX, TypeScript) are skipped.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from bookmaker.code.adapters.base import CodeAdapter
from bookmaker.code.extractor import extract_blocks_tagged

_JS_LANGUAGES: frozenset[str] = frozenset({"javascript", "js"})


class ReactCodeAdapter(CodeAdapter):
    """Code adapter for React/JavaScript code blocks.

    Syntax-checks JavaScript blocks with node --check;
    other frontend fence languages are returned as skipped.
    """

    name = "react"
    language = "javascript"
    fence_languages = ("javascript", "js", "jsx", "tsx", "typescript", "ts")

    def extract_blocks(self, text: str) -> list[tuple[str, str]]:
        """Extract fenced code blocks with language tags.

        Args:
            text: Markdown text to extract blocks from.

        Returns:
            List of (language, content) tuples in match order.

        """
        return extract_blocks_tagged(text, self.fence_languages)

    def run_tests(
        self, blocks: list[tuple[str, str]], workdir: Path,
    ) -> list[dict]:
        """Syntax-check each JavaScript code block with node --check.

        Non-JavaScript blocks (JSX, TSX, TypeScript) are skipped.

        Args:
            blocks: List of (language, content) tuples.
            workdir: Working directory for temporary files.

        Returns:
            List of test result dictionaries.

        """
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
