from __future__ import annotations

import re


def extract_fenced_blocks(text: str, languages: tuple[str, ...]) -> list[str]:
    blocks: list[str] = []
    for language in languages:
        pattern = rf"```{re.escape(language)}\s*\n(.*?)```"
        blocks.extend(re.findall(pattern, text, re.DOTALL | re.IGNORECASE))
    return blocks

