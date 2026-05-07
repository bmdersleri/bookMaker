from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CodeBlock:
    code_id: str
    language: str
    file: str
    validation_mode: str
    content: str
    chapter_id: str
    test: str | None = None


@dataclass(slots=True)
class CodeTestResult:
    code_id: str
    file: str
    status: str
    command: list[str]
    stdout: str = ""
    stderr: str = ""
    elapsed_seconds: float = 0.0
    reason: str = ""
