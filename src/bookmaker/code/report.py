from __future__ import annotations


def summarize_test_results(results: list[dict]) -> dict[str, int]:
    return {
        "compiled": sum(1 for item in results if item.get("status") == "ok"),
        "failed": sum(1 for item in results if item.get("status") == "error"),
        "skipped": sum(1 for item in results if item.get("status") == "skipped"),
    }

