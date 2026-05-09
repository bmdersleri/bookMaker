"""GitHub pages testleri."""

from pathlib import Path

from bookmaker.github.pages import generate_code_page, generate_index_page


def test_generate_code_page(tmp_path: Path) -> None:
    out = generate_code_page("kod01", "Test.java", "public class Test {}", tmp_path)
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "kod01" in content
    assert "Test.java" in content


def test_generate_index(tmp_path: Path) -> None:
    entries = [
        {"code_id": "k1", "file": "f1.java", "github_url": "http://example.com/k1"},
        {"code_id": "k2", "file": "f2.java"},
    ]
    out = generate_index_page(entries, tmp_path)
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "k1" in content
    assert "k2" in content
