"""Studio testleri — API endpoint'leri."""


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
        assert data == [
            {
                "name": "flutter-demo",
                "path": str(project),
                "title": "Flutter Demo",
            }
        ]

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
