from __future__ import annotations

from pathlib import Path


def test_export_uses_manifest_from_format_and_toc_settings(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.studio.services import export_service

    project = tmp_path / "book_projects" / "export-demo"
    content_dir = project / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True)
    (project / "book_manifest.yaml").write_text(
        "book:\n"
        "  alias: export-demo\n"
        "style:\n"
        "  code_language: dart\n"
        "pandoc:\n"
        "  from_format: markdown+fenced_divs\n"
        "  toc: false\n"
        "  toc_depth: 1\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    order: 1\n",
        encoding="utf-8",
    )
    (content_dir / "final.md").write_text(
        "# Giriş\n\n```dart\nvoid main() {}\n```\n",
        encoding="utf-8",
    )

    captured: dict[str, list[str]] = {}

    def fake_run(cmd, capture_output, text, timeout):  # noqa: ANN001
        captured["cmd"] = cmd
        out_index = cmd.index("-o") + 1
        Path(cmd[out_index]).write_text("dummy docx", encoding="utf-8")

        class Result:
            returncode = 0
            stdout = ""
            stderr = ""

        return Result()

    monkeypatch.setattr(export_service.subprocess, "run", fake_run)

    result = export_service.export_to_format(project, "docx")

    assert result["format"] == "docx"
    assert captured["cmd"][captured["cmd"].index("-f") + 1] == "markdown+fenced_divs"
    assert "--toc" not in captured["cmd"]
    assert result["path"].replace("\\", "/") == "exports/docx/kitap.docx"
