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


def test_api_llm_status() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.get("/api/llm-status")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "configured" in data


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


def test_api_llm_configure() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.post("/api/llm-configure", json={
        "provider": "deepseek",
        "api_key": "sk-test-key-12345",
        "model": "deepseek-chat",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["provider"] == "deepseek"
    assert data["model"] == "deepseek-chat"


def test_api_llm_configure_missing_key() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.post("/api/llm-configure", json={
        "provider": "deepseek",
        "api_key": "",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


def test_api_generate_not_configured() -> None:
    if app is None:
        return
    from fastapi.testclient import TestClient
    client = TestClient(app)
    resp = client.post("/api/generate/bolum-03", json={})
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data or "final_words" in data or data.get("status") == "queued"


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
    assert "sortQuality('chapter_id')" in resp.text
    assert 'id="toast-container"' in resp.text
    assert 'id="wiz-author"' in resp.text
    assert 'id="wiz-book-type"' in resp.text
    assert 'id="wiz-chapter-count"' in resp.text
    assert 'onclick="nextWiz()"' in resp.text


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

        resp = client.get("/output/exports/md/sample.md")
        assert resp.status_code == 200
        assert resp.text.strip() == "# Sample"

        resp = client.get("/output/prompts/default_chapter.md")
        assert resp.status_code == 403
    finally:
        studio_app._active_book = previous
