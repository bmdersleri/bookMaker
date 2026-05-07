"""Studio testleri — API endpoint'leri."""

from pathlib import Path

from bookmaker.studio.app import app


def test_app_created() -> None:
    assert app is not None


def test_api_status() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/api/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "running"
    assert data["version"] == "0.2.0"


def test_api_project() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/api/project")
    assert resp.status_code == 200
    data = resp.json()
    assert "title" in data
    assert "chapters" in data


def test_api_chapters() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/api/chapters")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_api_pipeline_state() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/api/pipeline-state")
    assert resp.status_code == 200
    data = resp.json()
    assert "pipeline_id" in data
    assert "chapters" in data


def test_api_view_not_found() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/api/view/bolum-99")
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


def test_api_check_not_found() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/api/check/bolum-99")
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


def test_api_build_not_found() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/api/build/bolum-99")
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


def test_api_generate_not_configured(tmp_path) -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app

    project = tmp_path / "book_projects" / "no-llm"
    project.mkdir(parents=True)
    (project / "book_manifest.yaml").write_text(
        "book:\n  alias: no-llm\nchapters: []\n",
        encoding="utf-8",
    )
    previous = studio_app._active_book
    studio_app._active_book = str(project)
    client = TestClient(app)
    try:
        resp = client.post("/api/generate/bolum-03", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert data["error"] == "LLM yapılandırılmamış"
        assert not (project / "logs" / "studio_jobs").exists()
    finally:
        studio_app._active_book = previous


def test_index_page() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert "bookMaker" in resp.text
    assert "Bölüm" in resp.text
    assert 'data-tab="quality"' in resp.text
    assert 'data-tab="build"' in resp.text
    assert 'data-tab="prompts"' in resp.text
    assert 'id="stat-screenshot"' in resp.text
    assert 'id="stat-qr"' in resp.text
    assert 'id="build-targets"' in resp.text
    assert 'id="quality-book-summary"' in resp.text
    assert 'id="jobs-body"' in resp.text
    assert "logs/studio_jobs" in resp.text
    assert "sortQuality('chapter_id')" in resp.text
    assert 'id="toast-container"' in resp.text
    assert 'id="wiz-author"' in resp.text
    assert 'id="wiz-book-type"' in resp.text
    assert 'id="wiz-chapter-count"' in resp.text
    assert 'onclick="nextWiz()"' in resp.text
    # FAZ 6.6: export readiness, code validation, export link hooks
    assert 'id="readiness-result"' in resp.text
    assert 'id="readiness-badge"' in resp.text
    assert 'id="code-validate-result"' in resp.text
    assert 'id="code-validate-chapter"' in resp.text
    assert 'onclick="loadExportReadiness()"' in resp.text
    assert 'onclick="runCodeValidate()"' in resp.text


def test_studio_template_contains_export_readiness_ui_hooks() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert 'id="readiness-result"' in resp.text
    assert 'id="readiness-badge"' in resp.text
    assert 'id="readiness-fmt"' in resp.text
    assert 'onclick="loadExportReadiness()"' in resp.text


def test_studio_template_contains_code_validation_summary_hooks() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert 'id="code-validate-result"' in resp.text
    assert 'id="code-validate-chapter"' in resp.text
    assert 'onclick="runCodeValidate()"' in resp.text


def test_studio_template_contains_export_report_link_hooks() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    # Export result div exists (where links appear after export)
    assert 'id="export-result"' in resp.text
    # Export button triggers link rendering in runExport()
    assert 'onclick="runExport()"' in resp.text


def test_api_projects_uses_book_manifest(tmp_path) -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app

    workspace = tmp_path / "workspace"
    project = workspace / "book_projects" / "flutter-demo"
    legacy = workspace / "book_projects" / "legacy-only"
    project.mkdir(parents=True)
    legacy.mkdir(parents=True)
    (project / "book_manifest.yaml").write_text(
        "book:\n"
        "  title: Flutter Demo\n"
        "  alias: flutter-demo\n"
        "  author: Test Yazar\n"
        "chapters: []\n",
        encoding="utf-8",
    )
    (legacy / "book_profile.yaml").write_text(
        "book:\n  title: Legacy Only\n",
        encoding="utf-8",
    )

    previous = studio_app._active_book
    studio_app._active_book = str(workspace)
    try:
        client = TestClient(app)
        resp = client.get("/api/projects")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "flutter-demo"
        assert data[0]["title"] == "Flutter Demo"
        assert Path(data[0]["path"]).resolve() == project.resolve()

        resp = client.post("/api/active-book", json={"path": str(project)})
        assert resp.status_code == 200
        assert resp.json()["name"] == "flutter-demo"

        resp = client.get("/api/active-book")
        assert resp.status_code == 200
        active = resp.json()
        assert active["name"] == "flutter-demo"
        assert active["title"] == "Flutter Demo"
    finally:
        studio_app._active_book = previous


def test_api_chapters_reorder_route_precedes_dynamic_update(tmp_path) -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app
    from bookmaker.studio.services import wizard_service

    result = wizard_service.create_book(
        tmp_path,
        {
            "project_name": "reorder-demo",
            "title": "Reorder Demo",
            "author": "Test Yazar",
            "chapters": ["bir", "iki", "uc"],
        },
    )
    assert "error" not in result
    project = tmp_path / "book_projects" / "reorder-demo"

    previous = studio_app._active_book
    studio_app._active_book = str(project)
    try:
        client = TestClient(app)
        resp = client.put("/api/chapters/reorder", json={"chapter_ids": ["iki", "bir", "uc"]})
        assert resp.status_code == 200
        assert resp.json()["reordered"] is True

        chapters = client.get("/api/chapters").json()
        assert [chapter["chapter_id"] for chapter in chapters] == ["iki", "bir", "uc"]
    finally:
        studio_app._active_book = previous


def test_api_prompt_endpoints_roundtrip(tmp_path) -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app
    from bookmaker.studio.services import wizard_service

    result = wizard_service.create_book(
        tmp_path,
        {
            "project_name": "prompt-demo",
            "title": "Prompt Demo",
            "author": "Test Yazar",
            "chapters": ["giris"],
        },
    )
    assert "error" not in result
    project = tmp_path / "book_projects" / "prompt-demo"

    previous = studio_app._active_book
    studio_app._active_book = str(project)
    try:
        client = TestClient(app)

        resp = client.get("/api/prompts/default/chapter")
        assert resp.status_code == 200
        assert resp.json()["path"].replace("\\", "/") == "prompts/default_chapter.md"

        resp = client.put(
            "/api/prompts/default/chapter",
            json={"content": "Updated default chapter prompt"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
        assert (project / "prompts" / "default_chapter.md").read_text(
            encoding="utf-8",
        ) == "Updated default chapter prompt"

        resp = client.get("/api/prompts/default/review")
        assert resp.status_code == 200
        assert resp.json()["path"].replace("\\", "/") == "prompts/default_review.md"

        resp = client.put(
            "/api/prompts/chapter/giris",
            json={"content": "Updated chapter prompt"},
        )
        assert resp.status_code == 200
        assert resp.json()["path"].replace("\\", "/") == "chapters/giris/prompt.md"

        resp = client.get("/api/prompts/chapter/giris")
        assert resp.status_code == 200
        assert resp.json()["content"] == "Updated chapter prompt"
    finally:
        studio_app._active_book = previous


def test_api_quality_book_summary(tmp_path) -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app
    from bookmaker.studio.services import wizard_service

    result = wizard_service.create_book(
        tmp_path,
        {
            "project_name": "quality-api-demo",
            "title": "Quality API Demo",
            "author": "Test Yazar",
            "chapters": ["giris"],
        },
    )
    assert "error" not in result
    project = tmp_path / "book_projects" / "quality-api-demo"

    previous = studio_app._active_book
    studio_app._active_book = str(project)
    try:
        client = TestClient(app)
        resp = client.get("/api/quality/book")
        assert resp.status_code == 200
        data = resp.json()
        assert data["score"] == 100
        assert data["decision"] == "pass"
        assert data["chapters"][0]["chapter_id"] == "giris"
        assert data["report_path"].replace("\\", "/") == "logs/reviews/book_quality_report.json"

        resp = client.get("/api/check/giris")
        assert resp.status_code == 200
        chapter = resp.json()
        assert chapter["chapter_id"] == "giris"
        assert "report_path" in chapter
        assert "issues" in chapter
    finally:
        studio_app._active_book = previous


def test_export_targets_and_output_serving_are_project_based(tmp_path) -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app

    project = tmp_path / "book_projects" / "export-demo"
    project.mkdir(parents=True)
    (project / "book_manifest.yaml").write_text(
        "book:\n"
        "  alias: export-demo\n"
        "style:\n"
        "  code_language: dart\n"
        "chapters: []\n",
        encoding="utf-8",
    )
    output = project / "exports" / "md" / "sample.md"
    output.parent.mkdir(parents=True)
    output.write_text("# Sample\n", encoding="utf-8")

    previous = studio_app._active_book
    studio_app._active_book = str(project)
    try:
        client = TestClient(app)

        resp = client.get("/api/export/targets")
        assert resp.status_code == 200
        data = resp.json()
        assert data["root"] == "exports"
        assert data["code_language"] == "dart"
        assert data["targets"]["markdown"].replace("\\", "/") == "exports/md"

        resp = client.get("/api/export/readiness?fmt=docx")
        assert resp.status_code == 200
        readiness = resp.json()
        assert readiness["format"] == "docx"
        assert "ready" in readiness

        resp = client.get("/output/exports/md/sample.md")
        assert resp.status_code == 200
        assert resp.text.strip() == "# Sample"

        resp = client.get("/output/prompts/default_chapter.md")
        assert resp.status_code == 403
    finally:
        studio_app._active_book = previous


def test_api_jobs_create_list_cancel_use_project_logs(tmp_path) -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app
    from bookmaker.studio import jobs

    project = tmp_path / "book_projects" / "jobs-demo"
    project.mkdir(parents=True)
    (project / "book_manifest.yaml").write_text(
        "book:\n  alias: jobs-demo\nchapters: []\n",
        encoding="utf-8",
    )

    previous = studio_app._active_book
    previous_jobs = dict(jobs._JOBS)
    studio_app._active_book = str(project)
    try:
        with jobs._LOCK:
            jobs._JOBS.clear()

        client = TestClient(app)
        resp = client.post(
            "/api/jobs",
            json={"step": "build", "chapter_id": "giris", "params": {}},
        )
        assert resp.status_code == 200
        job = resp.json()
        assert job["status"] == "queued"

        job_file = project / "logs" / "studio_jobs" / f"{job['id']}.json"
        assert job_file.exists()
        assert not (project / "build" / "studio_jobs").exists()

        resp = client.get("/api/jobs")
        assert resp.status_code == 200
        assert any(item["id"] == job["id"] for item in resp.json())

        resp = client.post(f"/api/jobs/{job['id']}/cancel")
        assert resp.status_code == 200
        assert resp.json()["status"] == "cancelled"
    finally:
        studio_app._active_book = previous
        with jobs._LOCK:
            jobs._JOBS.clear()
            jobs._JOBS.update(previous_jobs)


# ---------------------------------------------------------------------------
# Export readiness and report URL tests (FAZ 6.5)
# ---------------------------------------------------------------------------

def test_export_readiness_includes_status_and_checks(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app

    manifest = tmp_path / "book_manifest.yaml"
    manifest.write_text(
        "book:\n"
        "  title: Test Readiness\n"
        "  alias: test-readiness\n"
        "style:\n"
        "  code_language: java\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    title: Giriş\n",
        encoding="utf-8",
    )
    content_dir = tmp_path / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    (content_dir / "final.md").write_text("# Giriş\n\nTest.\n", encoding="utf-8")

    previous = getattr(studio_app, "_active_book", None)
    studio_app._active_book = str(tmp_path)
    try:
        client = TestClient(studio_app.app)
        resp = client.get("/api/export/readiness?fmt=docx")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
        assert data["status"] in {"ok", "warning", "error"}
        assert "checks" in data
        assert isinstance(data["checks"], list)
        assert len(data["checks"]) >= 2  # book_manifest + chapters
        assert all("name" in c and "status" in c for c in data["checks"])
    finally:
        studio_app._active_book = previous


def test_export_to_format_returns_report_url(
    tmp_path: Path, monkeypatch,
) -> None:
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app

    manifest = tmp_path / "book_manifest.yaml"
    manifest.write_text(
        "book:\n"
        "  title: Report URL Test\n"
        "  alias: report-url-test\n"
        "style:\n"
        "  code_language: java\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    title: Giriş\n",
        encoding="utf-8",
    )
    content_dir = tmp_path / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    (content_dir / "final.md").write_text(
        "# Giriş\n\nTest içeriği.\n", encoding="utf-8",
    )
    (tmp_path / "exports" / "md").mkdir(parents=True, exist_ok=True)
    (tmp_path / "exports" / "docx").mkdir(parents=True, exist_ok=True)
    md_path = tmp_path / "exports" / "md" / "kitap_birlestirilmis.md"
    md_path.write_text("# Test\n\nContent.\n", encoding="utf-8")
    (tmp_path / "logs" / "production").mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(
        "bookmaker.studio.services.export_service.check_export_readiness",
        lambda root, fmt=None, chapter_ids=None: {
            "ready": True,
            "status": "ok",
            "format": fmt or "docx",
            "errors": [],
            "warnings": [],
            "checks": [
                {"name": "book_manifest", "status": "ok", "message": "ok"},
                {"name": "chapters", "status": "ok", "message": "1 bölüm"},
            ],
            "chapters": [
                {
                    "chapter_id": "giris",
                    "ready": True,
                    "source": "chapters/giris/content/final.md",
                    "source_kind": "final",
                },
            ],
        },
    )

    def fake_run(cmd, **kwargs):
        out = cmd[cmd.index("-o") + 1]
        Path(out).write_text("dummy", encoding="utf-8")

        class R:
            returncode = 0
            stdout = ""
            stderr = ""
        return R()

    monkeypatch.setattr(
        "bookmaker.studio.services.export_service.subprocess.run", fake_run,
    )

    previous = getattr(studio_app, "_active_book", None)
    studio_app._active_book = str(tmp_path)
    try:
        client = TestClient(studio_app.app)
        resp = client.post("/api/export/docx")
        assert resp.status_code == 200
        data = resp.json()
        assert "report_url" in data
        assert data["report_url"].startswith("/output/logs/production/")
    finally:
        studio_app._active_book = previous


def test_export_to_format_returns_output_url_on_success(
    tmp_path: Path, monkeypatch,
) -> None:
    from fastapi.testclient import TestClient

    from bookmaker.studio import app as studio_app

    manifest = tmp_path / "book_manifest.yaml"
    manifest.write_text(
        "book:\n"
        "  title: Output URL Test\n"
        "  alias: output-url-test\n"
        "style:\n"
        "  code_language: java\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    title: Giriş\n",
        encoding="utf-8",
    )
    content_dir = tmp_path / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    (content_dir / "final.md").write_text(
        "# Giriş\n\nTest içeriği.\n", encoding="utf-8",
    )
    (tmp_path / "exports" / "md").mkdir(parents=True, exist_ok=True)
    (tmp_path / "exports" / "docx").mkdir(parents=True, exist_ok=True)
    md_path = tmp_path / "exports" / "md" / "kitap_birlestirilmis.md"
    md_path.write_text("# Test\n\nContent.\n", encoding="utf-8")
    (tmp_path / "logs" / "production").mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(
        "bookmaker.studio.services.export_service.check_export_readiness",
        lambda root, fmt=None, chapter_ids=None: {
            "ready": True,
            "status": "ok",
            "format": fmt or "docx",
            "errors": [],
            "warnings": [],
            "checks": [
                {"name": "book_manifest", "status": "ok", "message": "ok"},
                {"name": "chapters", "status": "ok", "message": "1 bölüm"},
            ],
            "chapters": [
                {
                    "chapter_id": "giris",
                    "ready": True,
                    "source": "chapters/giris/content/final.md",
                    "source_kind": "final",
                },
            ],
        },
    )

    def fake_run(cmd, **kwargs):
        out = cmd[cmd.index("-o") + 1]
        Path(out).write_text("dummy docx content", encoding="utf-8")

        class R:
            returncode = 0
            stdout = ""
            stderr = ""
        return R()

    monkeypatch.setattr(
        "bookmaker.studio.services.export_service.subprocess.run", fake_run,
    )

    previous = getattr(studio_app, "_active_book", None)
    studio_app._active_book = str(tmp_path)
    try:
        client = TestClient(studio_app.app)
        resp = client.post("/api/export/docx")
        assert resp.status_code == 200
        data = resp.json()
        assert "output_url" in data
        assert data["output_url"].startswith("/output/exports/docx/")
        assert "path" in data
        assert "report_url" in data
    finally:
        studio_app._active_book = previous
