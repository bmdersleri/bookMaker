from __future__ import annotations

import json
from pathlib import Path


def test_export_to_format_writes_production_export_report(
    tmp_path: Path,
    monkeypatch,
) -> None:
    from bookmaker.studio.services import export_service

    project = tmp_path / "book_projects" / "report-demo"
    content_dir = project / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True)
    (project / "book_manifest.yaml").write_text(
        "book:\n"
        "  alias: report-demo\n"
        "style:\n"
        "  code_language: java\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    order: 1\n",
        encoding="utf-8",
    )
    (content_dir / "final.md").write_text(
        "# Giriş\n\n```java\nclass Demo {}\n```\n",
        encoding="utf-8",
    )

    def fake_run(cmd, capture_output, text, timeout):  # noqa: ANN001
        if "--version" in cmd:
            class VersionResult:
                returncode = 0
                stdout = "pandoc 3.x"
                stderr = ""

            return VersionResult()

        out_index = cmd.index("-o") + 1
        Path(cmd[out_index]).write_text("dummy docx", encoding="utf-8")

        class ExportResult:
            returncode = 0
            stdout = ""
            stderr = ""

        return ExportResult()

    monkeypatch.setattr(export_service.subprocess, "run", fake_run)

    result = export_service.export_to_format(project, "docx")

    assert result["format"] == "docx"
    assert result["path"].replace("\\", "/") == "exports/docx/kitap.docx"
    assert result["report_path"].replace("\\", "/").startswith(
        "logs/production/export_"
    )

    report_path = project / result["report_path"]
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["status"] == "success"
    assert data["format"] == "docx"
    assert data["readiness"]["ready"] is True


def test_export_to_format_stops_on_readiness_failure_and_reports(
    tmp_path: Path,
    monkeypatch,
) -> None:
    from bookmaker.studio.services import export_service

    project = tmp_path / "book_projects" / "report-fail"
    content_dir = project / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True)
    (project / "book_manifest.yaml").write_text(
        "book:\n"
        "  alias: report-fail\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    order: 1\n",
        encoding="utf-8",
    )
    (content_dir / "draft.md").write_text("# Taslak\n", encoding="utf-8")

    called = {"count": 0}

    def fake_run(cmd, capture_output, text, timeout):  # noqa: ANN001
        called["count"] += 1

        class VersionResult:
            returncode = 0
            stdout = "pandoc 3.x"
            stderr = ""

        return VersionResult()

    monkeypatch.setattr(export_service.subprocess, "run", fake_run)

    result = export_service.export_to_format(project, "docx")

    assert "error" in result
    assert "readiness" in result
    assert result["readiness"]["ready"] is False
    assert called["count"] == 1

    report_path = project / result["report_path"]
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["status"] == "failed"
    assert data["reason"] == "readiness"
