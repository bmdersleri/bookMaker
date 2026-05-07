"""Base code adapter with abstract interface.

Defines CodeAdapter (abstract) and ReviewOnlyAdapter (no-op)
for testing code blocks extracted from book chapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from bookmaker.code.extractor import extract_fenced_blocks


class CodeAdapter(ABC):
    """Abstract base class for language-specific code adapters.

    Attributes:
        name: Adapter identifier string.
        language: Primary programming language name.
        fence_languages: Tuple of markdown fence languages to extract.

    """

    name = "base"
    language = "generic"
    fence_languages: tuple[str, ...] = ()

    def extract_blocks(self, text: str) -> list[str]:
        """Extract fenced code blocks matching this adapter's languages.

        Args:
            text: Markdown text to extract blocks from.

        Returns:
            List of extracted code block contents.

        """
        return extract_fenced_blocks(text, self.fence_languages)

    @abstractmethod
    def run_tests(self, blocks: list[str], workdir: Path) -> list[dict]:
        """Run tests on extracted code blocks.

        Args:
            blocks: List of code block contents to test.
            workdir: Working directory for test execution.

        Returns:
            List of test result dictionaries per block.

        """
        raise NotImplementedError


class ReviewOnlyAdapter(CodeAdapter):
    """Adapter that skips all code execution.

    Used when no matching language-specific adapter is found.
    Returns all blocks as skipped.
    """

    name = "review"
    language = "generic"
    fence_languages: tuple[str, ...] = ()

    def run_tests(self, blocks: list[str], workdir: Path) -> list[dict]:
        """Skip all code blocks (review-only mode).

        Args:
            blocks: List of code block contents.
            workdir: Working directory (unused).

        Returns:
            List of skipped result dictionaries.

        """
        return [
            {
                "block": index + 1,
                "status": "skipped",
                "reason": "review_only",
                "command": [],
            }
            for index, _ in enumerate(blocks)
        ]

