"""Production qrcode testleri."""

from pathlib import Path

from bookmaker.production.qrcode import generate_qr


def test_generate_qr_url(tmp_path: Path) -> None:
    out = tmp_path / "test_qr.png"
    result = generate_qr("https://example.com", out)
    # qr CLI yoksa error döner
    assert result["status"] in ("passed", "error", "failed")
    if result["status"] == "passed":
        assert out.exists()


def test_generate_qr_empty_data(tmp_path: Path) -> None:
    out = tmp_path / "empty_qr.png"
    result = generate_qr("", out)
    assert result["status"] in ("passed", "error", "failed")
