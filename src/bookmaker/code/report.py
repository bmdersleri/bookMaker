from __future__ import annotations


def summarize_test_results(results: list[dict]) -> dict[str, int]:
    ok = sum(1 for item in results if item.get("status") == "ok")
    error = sum(1 for item in results if item.get("status") == "error")
    skipped = sum(1 for item in results if item.get("status") == "skipped")
    return {
        "ok": ok,
        "error": error,
        "skipped": skipped,
        "total": len(results),
        "compiled": ok,
        "failed": error,
    }

