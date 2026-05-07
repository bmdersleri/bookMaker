"""Flutter/Dart code adapter for bookMaker.

Runs dart analyze on extracted Dart code blocks to verify syntax.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from bookmaker.code.adapters.base import CodeAdapter


def _find_pubspec(workdir: Path) -> Path | None:
    """Search upward from workdir for pubspec.yaml."""
    current = workdir.resolve()
    for _ in range(6):
        candidate = current / "pubspec.yaml"
        if candidate.exists():
            return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


class FlutterCodeAdapter(CodeAdapter):
    """Code adapter for Flutter/Dart code blocks.

    Runs dart analyze on extracted Dart code snippets to verify syntax.
    """

    name = "flutter"
    language = "dart"
    fence_languages = ("dart",)

    def run_tests(self, blocks: list[str], workdir: Path) -> list[dict]:
        """Run dart analyze on each code block.

        Args:
            blocks: List of Dart code block contents.
            workdir: Working directory for temporary files.

        Returns:
            List of test result dictionaries.

        """
        results: list[dict] = []
        dart = shutil.which("dart")
        pubspec = _find_pubspec(workdir)

        for index, block in enumerate(blocks, start=1):
            fpath = workdir / f"block_{index:03d}.dart"
            fpath.write_text(block, encoding="utf-8")

            if not dart:
                results.append({
                    "block": index,
                    "status": "skipped",
                    "reason": "dart_bulunamadi",
                    "command": ["dart", "analyze", str(fpath)],
                })
                continue

            if pubspec:
                results.append({
                    "block": index,
                    "status": "skipped",
                    "reason": "flutter_widget_pubspec_found",
                    "command": ["dart", "analyze", str(fpath)],
                })
                continue

            try:
                proc = subprocess.run(
                    [dart, "analyze", str(fpath)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(workdir),
                )
            except subprocess.TimeoutExpired:
                results.append({
                    "block": index,
                    "status": "error",
                    "errors": ["dart analyze timed out after 60s"],
                    "command": [dart, "analyze", str(fpath)],
                })
                continue

            if proc.returncode == 0:
                results.append({
                    "block": index,
                    "status": "ok",
                    "command": [dart, "analyze", str(fpath)],
                })
            else:
                err_text = proc.stderr.strip() or proc.stdout.strip()
                results.append({
                    "block": index,
                    "status": "error",
                    "errors": [err_text] if err_text else [],
                    "command": [dart, "analyze", str(fpath)],
                })

        return results
