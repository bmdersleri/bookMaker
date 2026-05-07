"""Java code adapter for bookMaker.

Compiles extracted Java code blocks with javac to verify syntax.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from bookmaker.code.adapters.base import CodeAdapter


class JavaCodeAdapter(CodeAdapter):
    """Code adapter for Java code blocks.

    Compiles each code block with javac to verify syntax correctness.
    """

    name = "java"
    language = "java"
    fence_languages = ("java",)

    def run_tests(self, blocks: list[str], workdir: Path) -> list[dict]:
        """Compile each Java code block with javac.

        Args:
            blocks: List of Java code block contents.
            workdir: Working directory for temporary files.

        Returns:
            List of test result dictionaries.

        """
        results: list[dict] = []
        javac = shutil.which("javac")

        for index, block in enumerate(blocks, start=1):
            class_match = re.search(r"public\s+class\s+(\w+)", block)
            class_name = class_match.group(1) if class_match else "unknown"
            if not class_match:
                results.append(
                    {
                        "block": index,
                        "status": "skipped",
                        "reason": "Sınıf adı bulunamadi",
                        "class_name": class_name,
                        "command": [],
                    }
                )
                continue

            fname = f"{class_name}.java"
            fpath = workdir / fname
            fpath.write_text(block, encoding="utf-8")

            if not javac:
                results.append(
                    {
                        "block": index,
                        "status": "skipped",
                        "reason": "javac bulunamadi",
                        "class_name": class_name,
                        "command": ["javac", str(fpath)],
                    }
                )
                continue

            try:
                proc = subprocess.run(
                    [javac, str(fpath)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(workdir),
                )
            except subprocess.TimeoutExpired:
                results.append(
                    {
                        "block": index,
                        "status": "error",
                        "class_name": class_name,
                        "errors": ["javac timed out after 30s"],
                        "command": [javac, str(fpath)],
                    }
                )
                continue

            if proc.returncode == 0:
                results.append(
                    {
                        "block": index,
                        "status": "ok",
                        "class_name": class_name,
                        "command": [javac, str(fpath)],
                    }
                )
                continue

            error_lines = [
                line.strip()
                for line in proc.stderr.splitlines()
                if line.strip()
            ][:5]
            results.append(
                {
                    "block": index,
                    "status": "error",
                    "class_name": class_name,
                    "errors": error_lines,
                    "command": [javac, str(fpath)],
                }
            )

        return results
