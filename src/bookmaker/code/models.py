from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CodeBlock:
    """Represents a single code block from a chapter with its metadata.

    Attributes:
        code_id: Unique identifier for the code block.
        language: Programming language of the block.
        file: Source file path.
        validation_mode: How this block should be validated.
        content: The actual code content.
        chapter_id: Identifier of the parent chapter.
        test: Optional test mode identifier.

    """

    code_id: str
    language: str
    file: str
    validation_mode: str
    content: str
    chapter_id: str
    test: str | None = None


@dataclass(slots=True)
class CodeTestResult:
    """Represents the result of testing a single code block.

    Attributes:
        code_id: Identifier of the tested code block.
        file: Source file path.
        status: Test outcome (ok, error, skipped).
        command: The command that was executed.
        stdout: Standard output from the command.
        stderr: Standard error from the command.
        elapsed_seconds: Time taken for the test.
        reason: Optional reason for skipped or failed status.

    """

    code_id: str
    file: str
    status: str
    command: list[str]
    stdout: str = ""
    stderr: str = ""
    elapsed_seconds: float = 0.0
    reason: str = ""
