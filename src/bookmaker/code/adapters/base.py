from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from bookmaker.code.extractor import extract_fenced_blocks


class CodeAdapter(ABC):
    name = "base"
    language = "generic"
    fence_languages: tuple[str, ...] = ()

    def extract_blocks(self, text: str) -> list[str]:
        return extract_fenced_blocks(text, self.fence_languages)

    @abstractmethod
    def run_tests(self, blocks: list[str], workdir: Path) -> list[dict]:
        raise NotImplementedError


class ReviewOnlyAdapter(CodeAdapter):
    name = "review"
    language = "generic"
    fence_languages: tuple[str, ...] = ()

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

