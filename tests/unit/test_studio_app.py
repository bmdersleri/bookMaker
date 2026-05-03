"""Studio testleri."""


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
    assert data["version"] == "0.1.0"


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
