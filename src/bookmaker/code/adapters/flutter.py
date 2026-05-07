from __future__ import annotations

from pathlib import Path

from bookmaker.code.adapters.base import CodeAdapter


class FlutterCodeAdapter(CodeAdapter):
    """Flutter/Dart adapter placeholder.

    Şimdilik skip davranışı korunur. Bu, profile-aware hattın Flutter
    projelerinde Java derlemesine düşmesini engelleyen güvenli ara basamaktır.
    Sonraki adımda `dart analyze` ve `flutter test` yürütülecektir.
    """

    name = "flutter"
    language = "dart"
    fence_languages = ("dart",)

    def run_tests(self, blocks: list[str], workdir: Path) -> list[dict]:
        return [
            {
                "block": index + 1,
                "status": "skipped",
                "reason": "flutter_adapter_ready_but_not_executed",
                "command": ["dart", "analyze"],
            }
            for index, _ in enumerate(blocks)
        ]
