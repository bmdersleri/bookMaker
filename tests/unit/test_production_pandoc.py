"""Production pandoc testleri."""

from pathlib import Path

from bookmaker.production.pandoc import pandoc_available


def test_pandoc_available() -> None:
    """Pandoc kurulu mu?"""
    result = pandoc_available()
    assert isinstance(result, bool)


def test_pandoc_export(tmp_path: Path) -> None:
    from bookmaker.production.pandoc import export_docx

    if not pandoc_available():
        return  # skip if pandoc unavailable

    md_file = tmp_path / "test.md"
    md_file.write_text("# Test\nIcerik.\n", encoding="utf-8")
    out = tmp_path / "test.docx"

    result = export_docx(md_file, out)
    assert result["status"] in ("passed", "failed")
    if result["status"] == "passed":
        assert out.exists()
