from __future__ import annotations

from pathlib import Path

from bookmaker.code.adapters.base import CodeAdapter


class ReactCodeAdapter(CodeAdapter):
    name = "react"
    language = "javascript"
    fence_languages = ("javascript", "js", "jsx", "tsx", "typescript", "ts")

    def run_tests(self, blocks: list[str], workdir: Path) -> list[dict]:
        return [
            {
                "block": index + 1,
                "status": "skipped",
                "reason": "review_only",
                "command": [],
            }
            for index, _ in enumerate(blocks)
        ]

