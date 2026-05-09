"""Build runner testleri."""

from pathlib import Path

from bookmaker.build.runner import compile_java


def test_compile_valid_java(tmp_path: Path) -> None:
    src = tmp_path / "Merhaba.java"
    src.write_text(
        "public class Merhaba {\n"
        "    public static void main(String[] args) {\n"
        '        System.out.println("Merhaba");\n'
        "    }\n"
        "}\n",
        encoding="utf-8",
    )
    result = compile_java(src, tmp_path)
    assert result["compile_status"] == "passed"
    assert result["class_path"] is not None
    assert Path(result["class_path"]).exists()


def test_compile_invalid_java(tmp_path: Path) -> None:
    src = tmp_path / "Hatali.java"
    src.write_text("public class Hatali {\n  invalid syntax\n", encoding="utf-8")
    result = compile_java(src, tmp_path)
    assert result["compile_status"] == "failed"


def test_compile_nonexistent_file(tmp_path: Path) -> None:
    src = tmp_path / "yok.java"
    result = compile_java(src, tmp_path)
    assert result["compile_status"] == "error"


def test_compile_no_main(tmp_path: Path) -> None:
    """main()'siz class derlenebilir."""
    src = tmp_path / "Utility.java"
    code = (
        "public class Utility {\n"
        "  public static int topla(int a, int b) { return a + b; }\n"
        "}\n"
    )
    src.write_text(code, encoding="utf-8")
    result = compile_java(src, tmp_path)
    assert result["compile_status"] == "passed"
