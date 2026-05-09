"""CODE_META'dan kod bloklarını çıkarır ve build/code/ altına yazar."""

from __future__ import annotations

import re
from pathlib import Path

from bookmaker.chapter.parser import ParsedChapter


def _find_code_after_meta(text: str, meta_end: int) -> str | None:
    """CODE_META bitiminden sonraki ilk kod fence'ini bulur."""
    match = re.search(
        r"```(?P<lang>[A-Za-z0-9_+\-.]*)\s*\n(?P<code>.*?)(?:\n```)",
        text[meta_end:],
        re.DOTALL,
    )
    return match.group("code") if match else None


def extract_code(chapter: ParsedChapter, target_dir: Path) -> list[dict]:
    """CODE_META bloklarından kodları çıkarır ve dosyalara yazar."""
    results: list[dict] = []
    code_blocks = [b for b in chapter.meta_blocks if b.kind == "CODE_META"]

    for block in code_blocks:
        data = block.data
        code = _find_code_after_meta(chapter.text, block.end)

        code_id = data.get("code_id", "unknown")
        file_name = data.get("file", f"{code_id}.java")
        extract_val = data.get("extract", "true")
        test_val = data.get("test", "compile")
        kind = data.get("kind", "example")

        result = {
            "code_id": code_id,
            "file": file_name,
            "extract": extract_val,
            "test": test_val,
            "kind": kind,
            "status": "skipped",
            "path": None,
            "error": None,
        }

        if extract_val == "false" or test_val == "skip":
            results.append(result)
            continue

        if not code:
            result["status"] = "error"
            result["error"] = "No code fence found after CODE_META"
            results.append(result)
            continue

        out_dir = target_dir / code_id
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / file_name
        out_path.write_text(code, encoding="utf-8")

        result["status"] = "extracted"
        result["path"] = str(out_path)
        results.append(result)

    return results


def extract_and_report(chapter: ParsedChapter, build_root: Path) -> list[dict]:
    """Kod çıkarır ve build/code/ altına yazar."""
    code_dir = build_root / "code"
    code_dir.mkdir(parents=True, exist_ok=True)
    return extract_code(chapter, code_dir)
