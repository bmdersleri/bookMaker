"""Development toolchain readiness check."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class ToolResult:
    available: bool
    version: str | None = None
    path: str | None = None


def _check_tool(name: str, version_args: list[str] | None = None) -> ToolResult:
    """Check if a tool is available on PATH and optionally get its version."""
    exe_path = shutil.which(name)
    if exe_path is None:
        return ToolResult(available=False)
    if version_args is None:
        return ToolResult(available=True, path=exe_path)
    try:
        proc = subprocess.run(
            [exe_path, *version_args],
            capture_output=True, text=True, timeout=10,
        )
        version = (proc.stdout.strip() or proc.stderr.strip()).split("\n")[0]
        return ToolResult(available=True, version=version, path=exe_path)
    except Exception:
        return ToolResult(available=True, path=exe_path)


# Tools: (key, display_name, version_args, critical)
_TOOLS: list[tuple[str, str, list[str] | None, bool]] = [
    ("python", "python", ["--version"], True),
    ("uv", "uv", ["--version"], True),
    ("pandoc", "pandoc", ["--version"], False),
    ("node", "node", ["--version"], False),
    ("npm", "npm", ["--version"], False),
    ("java", "java", ["--version"], False),
    ("javac", "javac", ["--version"], False),
    ("dart", "dart", ["--version"], False),
    ("flutter", "flutter", ["--version"], False),
    ("mmdc", "mmdc", ["--version"], False),
]


def check_toolchain() -> dict:
    """Check development toolchain readiness.

    Returns a JSON-serializable dict with status, errors, warnings, and
    per-tool availability/version info.

    Critical tools (python, uv) → error if missing.
    All other tools → warning if missing.
    """
    errors: list[str] = []
    warnings: list[str] = []
    tools: dict[str, dict] = {}

    for key, display, version_args, critical in _TOOLS:
        result = _check_tool(key, version_args)
        tools[key] = {
            "available": result.available,
            "version": result.version,
        }
        if not result.available:
            msg = f"{display} bulunamadi"
            if critical:
                errors.append(msg)
            else:
                warnings.append(msg)

    if errors:
        status = "error"
    elif warnings:
        status = "warning"
    else:
        status = "ok"

    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "tools": tools,
    }
