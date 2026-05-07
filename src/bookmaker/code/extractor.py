from __future__ import annotations

import re


def extract_fenced_blocks(text: str, languages: tuple[str, ...]) -> list[str]:
    blocks: list[str] = []
    for language in languages:
        pattern = rf"```{re.escape(language)}\s*\n(.*?)```"
        blocks.extend(re.findall(pattern, text, re.DOTALL | re.IGNORECASE))
    return blocks


def extract_blocks_tagged(
    text: str, languages: tuple[str, ...],
) -> list[tuple[str, str]]:
    """Extract fenced code blocks with their fence language tags.

    Returns list of (language, content) tuples in match order.
    """
    tagged: list[tuple[str, str]] = []
    for language in languages:
        pattern = rf"```{re.escape(language)}\s*\n(.*?)```"
        for match in re.finditer(pattern, text, re.DOTALL | re.IGNORECASE):
            tagged.append((language, match.group(1)))
    return tagged

