from __future__ import annotations

from pathlib import Path


def test_export_readiness_reports_ready_project(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.production.readiness import check_export_readiness

    project = tmp_path / "book_projects" / "readiness-ok"
    content_dir = project / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True)
    (project / "book_manifest.yaml").write_text(
        "book:\n"
        "  alias: readiness-ok\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    order: 1\n",
        encoding="utf-8",
    )
    (content_dir / "final.md").write_text("# Giriş\n\nFinal içerik.", encoding="utf-8")

    def fake_run(cmd, capture_output, text, timeout):  # noqa: ANN001
        class Result:
            returncode = 0
            stdout = "pandoc 3.x"
            stderr = ""

        return Result()

    monkeypatch.setattr("bookmaker.production.readiness.subprocess.run", fake_run)
    result = check_export_readiness(project, fmt="docx")

    assert result["ready"] is True
    assert result["errors"] == []
    assert result["chapters"][0]["source_kind"] == "final"


def test_export_readiness_fails_when_final_required_and_missing(
    tmp_path: Path, monkeypatch,
) -> None:
    from bookmaker.production.readiness import check_export_readiness

    project = tmp_path / "book_projects" / "readiness-fail"
    content_dir = project / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True)
    (project / "book_manifest.yaml").write_text(
        "book:\n"
        "  alias: readiness-fail\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    order: 1\n",
        encoding="utf-8",
    )
    (content_dir / "draft.md").write_text("# Giriş\n\nTaslak içerik.", encoding="utf-8")

    def fake_run(cmd, capture_output, text, timeout):  # noqa: ANN001
        class Result:
            returncode = 0
            stdout = "pandoc 3.x"
            stderr = ""

        return Result()

    monkeypatch.setattr("bookmaker.production.readiness.subprocess.run", fake_run)
    result = check_export_readiness(project, fmt="docx")

    assert result["ready"] is False
    assert any("final.md gerektiriyor" in item for item in result["errors"])

