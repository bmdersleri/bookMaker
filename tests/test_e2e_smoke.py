"""End-to-end smoke tests — kitap kalite kontrolu, studio endpoint, code validation."""

from pathlib import Path

from bookmaker.studio.app import app

# ---------------------------------------------------------------------------
# Book Quality Smoke
# ---------------------------------------------------------------------------


def test_flutter_book_quality_smoke_passes() -> None:
    """Ornek Flutter kitap projesinde kalite kontrolunun gecmesi."""
    flutter_root = Path(
        "book_projects/flutter-ile-mobil-uygulama-gelistirme")
    if not flutter_root.exists():
        import pytest
        pytest.skip("Flutter kitap projesi bulunamadi")

    from bookmaker.studio.services import quality_service

    result = quality_service.get_book_quality_report(flutter_root)

    assert result["decision"] == "pass"
    assert result["errors"] == 0


# ---------------------------------------------------------------------------
# Studio Endpoint Smoke (TestClient)
# ---------------------------------------------------------------------------


def test_export_targets_endpoint_smoke() -> None:
    """GET /api/export/targets endpoint smoke testi."""
    if app is None:
        return
    from fastapi.testclient import TestClient

    client = TestClient(app)
    resp = client.get("/api/export/targets")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


def test_export_readiness_endpoint_smoke(monkeypatch) -> None:
    """GET /api/export/readiness smoke testi — pandoc mock'lu."""
    if app is None:
        return
    from fastapi.testclient import TestClient

    flutter_root = Path(
        "book_projects/flutter-ile-mobil-uygulama-gelistirme")
    if not flutter_root.exists():
        import pytest
        pytest.skip("Flutter kitap projesi bulunamadi")

    monkeypatch.setattr(
        "bookmaker.production.readiness._check_pandoc",
        lambda: (True, "pandoc 3.1.2"),
    )
    monkeypatch.setattr(
        "bookmaker.studio.app.get_active_book",
        lambda: flutter_root,
    )

    client = TestClient(app)
    resp = client.get("/api/export/readiness")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "checks" in data
    assert data["status"] in {"ok", "warning", "error"}


def test_quality_book_endpoint_smoke() -> None:
    """GET /api/quality/book endpoint smoke testi."""
    if app is None:
        return
    from fastapi.testclient import TestClient

    client = TestClient(app)
    resp = client.get("/api/quality/book")
    assert resp.status_code == 200
    data = resp.json()
    assert "decision" in data
    assert "score" in data
    assert "chapters" in data


# ---------------------------------------------------------------------------
# Code Validation Payload Smoke (service level)
# ---------------------------------------------------------------------------


def test_code_validate_payload_shape_smoke(tmp_path: Path) -> None:
    """compile_code ciktisinin UX semasina uygunlugu."""
    root = tmp_path / "smoke-book"
    root.mkdir(parents=True)
    (root / "book_manifest.yaml").write_text(
        "book:\n"
        "  title: Smoke Test\n"
        "  alias: smoke\n"
        "style:\n"
        "  code_language: python\n"
        "chapters:\n"
        "  - alias: giris\n"
        "    title: Giris\n",
        encoding="utf-8",
    )
    content_dir = root / "chapters" / "giris" / "content"
    content_dir.mkdir(parents=True)
    (content_dir / "final.md").write_text(
        "# Giris\n\n```python\nprint('hello')\n```\n",
        encoding="utf-8",
    )

    from bookmaker.studio.services import quality_service

    result = quality_service.compile_code(root, "giris")

    for field in (
        "chapter_id", "adapter", "language", "blocks",
        "summary", "status", "results",
    ):
        assert field in result, f"Missing field: {field}"
    assert isinstance(result["summary"], dict)
    assert "total" in result["summary"]
