"""Markdown chapter parser for bookMaker.

Provides data classes and parsing functions for extracting
frontmatter, headings, and meta blocks from markdown chapter files.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class MetaBlock:
    """Represents a meta block found in markdown content.

    Attributes:
        kind: Meta block kind (e.g. CODE_META, MERMAID_META).
        data: Key-value pairs parsed from the block body.
        line: Starting line number in the source text.
        end: Character offset (exclusive) in raw text.

    """

    kind: str
    data: dict[str, str]
    line: int
    end: int  # character offset (exclusive) in raw text


@dataclass
class Heading:
    """Represents a markdown heading.

    Attributes:
        level: Heading level (1-6).
        title: Heading title text.
        line: Line number in the source text.

    """

    level: int
    title: str
    line: int


@dataclass
class ParsedChapter:
    """Represents a fully parsed chapter with its structure.

    Attributes:
        path: Path to the source markdown file.
        text: Raw chapter text content.
        frontmatter: YAML front matter key-value pairs.
        headings: List of parsed headings.
        meta_blocks: List of parsed meta blocks.

    """

    path: Path
    text: str
    frontmatter: dict[str, str]
    headings: list[Heading] = field(default_factory=list)
    meta_blocks: list[MetaBlock] = field(default_factory=list)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_key_values(body: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*?)\s*$", stripped)
        if match:
            result[match.group(1)] = _parse_scalar(match.group(2))
    return result


def _parse_frontmatter(text: str) -> dict[str, str]:
    if text.startswith("﻿"):
        text = text[1:]
    if not text.startswith("---"):
        return {}
    match = re.match(r"(?s)^---\s*\n(.*?)\n---\s*(?:\n|$)", text)
    if not match:
        return {}
    return _parse_key_values(match.group(1))


def _parse_meta_blocks(text: str) -> list[MetaBlock]:
    blocks: list[MetaBlock] = []
    pattern = re.compile(r"<!--\s*(?P<kind>[A-Z_]+)\s*(?P<body>.*?)-->", re.DOTALL)
    for match in pattern.finditer(text):
        body = match.group("body")
        blocks.append(MetaBlock(
            kind=match.group("kind"),
            data=_parse_key_values(body),
            line=_line_number(text, match.start()),
            end=match.end(),
        ))
    return blocks


def _parse_headings(text: str) -> list[Heading]:
    headings = []
    for match in re.finditer(r"(?m)^(#{1,6})\s+(.+?)\s*$", text):
        headings.append(Heading(
            level=len(match.group(1)),
            title=match.group(2).strip(),
            line=_line_number(text, match.start()),
        ))
    return headings


def parse(path: Path) -> ParsedChapter:
    """Parse a markdown file into a ParsedChapter.

    Extracts frontmatter, headings, and meta blocks from the file.

    Args:
        path: Path to the markdown file.

    Returns:
        ParsedChapter containing all parsed elements.

    """
    text = path.read_text(encoding="utf-8")
    return ParsedChapter(
        path=path,
        text=text,
        frontmatter=_parse_frontmatter(text),
        headings=_parse_headings(text),
        meta_blocks=_parse_meta_blocks(text),
    )
