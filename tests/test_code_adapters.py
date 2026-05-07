from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# select_code_adapter dispatch tests
# ---------------------------------------------------------------------------

def test_java_profile_returns_java_adapter() -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter("java", None)
    assert isinstance(adapter, JavaCodeAdapter)
    assert adapter.name == "java"


def test_flutter_profile_returns_flutter_adapter() -> None:
    from bookmaker.code.adapters.flutter import FlutterCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter("flutter", None)
    assert isinstance(adapter, FlutterCodeAdapter)
    assert adapter.name == "flutter"


def test_python_language_returns_python_adapter() -> None:
    from bookmaker.code.adapters.python import PythonCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter(None, "python")
    assert isinstance(adapter, PythonCodeAdapter)
    assert adapter.name == "python"


def test_python_profile_returns_python_adapter() -> None:
    from bookmaker.code.adapters.python import PythonCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter("python", None)
    assert isinstance(adapter, PythonCodeAdapter)
    assert adapter.name == "python"


def test_dart_language_returns_flutter_adapter() -> None:
    from bookmaker.code.adapters.flutter import FlutterCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter(None, "dart")
    assert isinstance(adapter, FlutterCodeAdapter)


def test_java_language_returns_java_adapter() -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter(None, "java")
    assert isinstance(adapter, JavaCodeAdapter)


def test_javascript_language_returns_react_adapter() -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter(None, "javascript")
    assert isinstance(adapter, ReactCodeAdapter)


def test_typescript_language_returns_react_adapter() -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter(None, "typescript")
    assert isinstance(adapter, ReactCodeAdapter)


def test_tsx_language_returns_react_adapter() -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter(None, "tsx")
    assert isinstance(adapter, ReactCodeAdapter)


def test_profile_takes_priority_over_language() -> None:
    from bookmaker.code.adapters.flutter import FlutterCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter("flutter", "java")
    assert isinstance(adapter, FlutterCodeAdapter)


def test_unknown_profile_unknown_language_returns_review_only() -> None:
    from bookmaker.code.adapters.base import ReviewOnlyAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter(None, None)
    assert isinstance(adapter, ReviewOnlyAdapter)


def test_unknown_profile_known_language_still_works() -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter("unknown-profile", "java")
    assert isinstance(adapter, JavaCodeAdapter)


def test_flutter_alias_profile_returns_flutter_adapter() -> None:
    from bookmaker.code.adapters.flutter import FlutterCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter("flutter-ile-mobil-uygulama-gelistirme", None)
    assert isinstance(adapter, FlutterCodeAdapter)


def test_java_alias_profile_returns_java_adapter() -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter("java-temelleri", None)
    assert isinstance(adapter, JavaCodeAdapter)


# ---------------------------------------------------------------------------
# JavaCodeAdapter run_tests tests
# ---------------------------------------------------------------------------

_JAVA_VALID = (
    "public class Main {\n"
    "    public static void main(String[] args) {\n"
    '        System.out.println("Hello");\n'
    "    }\n"
    "}\n"
)
_JAVA_NO_CLASS = "System.out.println(\"no class\");\n"


def test_java_adapter_run_tests_valid_code(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter

    def fake_which(cmd):
        if cmd == "javac":
            return "/fake/javac"
        return None

    def fake_run(cmd, **kwargs):
        class Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.java.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.java.subprocess.run", fake_run)

    adapter = JavaCodeAdapter()
    results = adapter.run_tests([_JAVA_VALID], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "ok"
    assert results[0]["class_name"] == "Main"


def test_java_adapter_no_javac_skipped(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter

    monkeypatch.setattr("bookmaker.code.adapters.java.shutil.which", lambda cmd: None)

    adapter = JavaCodeAdapter()
    results = adapter.run_tests([_JAVA_VALID], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "skipped"
    assert "javac bulunamadi" == results[0]["reason"]


def test_java_adapter_no_public_class_skipped(tmp_path: Path) -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter

    adapter = JavaCodeAdapter()
    results = adapter.run_tests([_JAVA_NO_CLASS], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "skipped"
    assert "Sınıf adı bulunamadi" == results[0]["reason"]


def test_java_adapter_timeout_handled(tmp_path: Path, monkeypatch) -> None:
    import subprocess

    from bookmaker.code.adapters.java import JavaCodeAdapter

    def fake_which(cmd):
        if cmd == "javac":
            return "/fake/javac"
        return None

    def fake_run(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd, 30)

    monkeypatch.setattr("bookmaker.code.adapters.java.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.java.subprocess.run", fake_run)

    adapter = JavaCodeAdapter()
    results = adapter.run_tests([_JAVA_VALID], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "error"
    assert "timed out" in results[0]["errors"][0]


def test_java_adapter_compile_error(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter

    def fake_which(cmd):
        if cmd == "javac":
            return "/fake/javac"
        return None

    def fake_run(cmd, **kwargs):
        class Result:
            returncode = 1
            stdout = ""
            stderr = "error: ';' expected\n"
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.java.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.java.subprocess.run", fake_run)

    adapter = JavaCodeAdapter()
    results = adapter.run_tests([_JAVA_VALID], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "error"
    assert results[0]["errors"]


# ---------------------------------------------------------------------------
# PythonCodeAdapter run_tests tests
# ---------------------------------------------------------------------------

_PY_VALID = "def greet():\n    return 'hello'\n\nprint(greet())\n"
_PY_INVALID = "def greet(\n    return 'hello'\n"


def test_python_adapter_run_tests_valid_code(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.python import PythonCodeAdapter

    def fake_run(cmd, **kwargs):
        class Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.python.subprocess.run", fake_run)

    adapter = PythonCodeAdapter()
    results = adapter.run_tests([_PY_VALID], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "ok"
    assert "py_compile" in results[0]["command"][2]


def test_python_adapter_run_tests_timeout(tmp_path: Path, monkeypatch) -> None:
    import subprocess

    from bookmaker.code.adapters.python import PythonCodeAdapter

    def fake_run(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd, 30)

    monkeypatch.setattr("bookmaker.code.adapters.python.subprocess.run", fake_run)

    adapter = PythonCodeAdapter()
    results = adapter.run_tests([_PY_VALID], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "error"
    assert "timed out" in results[0]["errors"][0]


def test_python_adapter_run_tests_syntax_error(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.python import PythonCodeAdapter

    def fake_run(cmd, **kwargs):
        class Result:
            returncode = 1
            stdout = ""
            stderr = "SyntaxError: invalid syntax"
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.python.subprocess.run", fake_run)

    adapter = PythonCodeAdapter()
    results = adapter.run_tests([_PY_INVALID], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "error"
    assert results[0]["errors"]


def test_python_adapter_writes_file_and_runs(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.python import PythonCodeAdapter

    captured_cmd = []

    def fake_run(cmd, **kwargs):
        captured_cmd.append(cmd)
        class Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.python.subprocess.run", fake_run)

    adapter = PythonCodeAdapter()
    adapter.run_tests([_PY_VALID], tmp_path)

    assert len(captured_cmd) == 1
    written = Path(captured_cmd[0][3])
    assert written.exists()
    assert written.read_text(encoding="utf-8") == _PY_VALID
    assert written.suffix == ".py"


# ---------------------------------------------------------------------------
# ReactCodeAdapter run_tests tests
# ---------------------------------------------------------------------------

_JS_VALID = "const x = 42;\nconsole.log(x);\n"
_JS_INVALID = "const x = ;\n"


def test_react_adapter_javascript_syntax_ok(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter

    def fake_which(cmd):
        return "/fake/node" if cmd == "node" else None

    def fake_run(cmd, **kwargs):
        class Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.react.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.react.subprocess.run", fake_run)

    adapter = ReactCodeAdapter()
    tagged = [("javascript", _JS_VALID)]
    results = adapter.run_tests(tagged, tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "ok"


def test_react_adapter_javascript_syntax_error(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter

    def fake_which(cmd):
        return "/fake/node" if cmd == "node" else None

    err = "SyntaxError: Unexpected token ';'\n"

    def fake_run(cmd, **kwargs):
        class Result:
            returncode = 1
            stdout = ""
            stderr = err
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.react.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.react.subprocess.run", fake_run)

    adapter = ReactCodeAdapter()
    tagged = [("javascript", _JS_INVALID)]
    results = adapter.run_tests(tagged, tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "error"
    assert results[0]["errors"][0] == err.strip()


def test_react_adapter_skips_typescript_safely(tmp_path: Path) -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter

    adapter = ReactCodeAdapter()
    tagged = [("typescript", "const x: number = 1;\n")]
    results = adapter.run_tests(tagged, tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "skipped"
    assert "typescript" in results[0]["reason"]


def test_react_adapter_skips_tsx_safely(tmp_path: Path) -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter

    adapter = ReactCodeAdapter()
    tagged = [("tsx", "const App = () => <div>Hello</div>;\n")]
    results = adapter.run_tests(tagged, tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "skipped"
    assert "tsx" in results[0]["reason"]


def test_react_adapter_no_node_fallback(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter

    monkeypatch.setattr("bookmaker.code.adapters.react.shutil.which", lambda cmd: None)

    adapter = ReactCodeAdapter()
    tagged = [("javascript", _JS_VALID)]
    results = adapter.run_tests(tagged, tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "skipped"
    assert "node_bulunamadi" == results[0]["reason"]


def test_react_adapter_multiple_blocks(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter

    def fake_which(cmd):
        return "/fake/node" if cmd == "node" else None

    def fake_run(cmd, **kwargs):
        fpath = Path(cmd[2])
        content = fpath.read_text(encoding="utf-8")
        class Result:
            returncode = 0 if "const x = 42" in content else 1
            stdout = ""
            stderr = "" if "const x = 42" in content else "SyntaxError"
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.react.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.react.subprocess.run", fake_run)

    adapter = ReactCodeAdapter()
    tagged = [
        ("javascript", _JS_VALID),
        ("javascript", _JS_INVALID),
        ("javascript", _JS_VALID),
    ]
    results = adapter.run_tests(tagged, tmp_path)

    assert len(results) == 3
    assert [r["status"] for r in results] == ["ok", "error", "ok"]


def test_react_adapter_extract_returns_tagged() -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter

    md = "```javascript\nconst x = 1;\n```\n```typescript\nconst y: number = 2;\n```\n"
    adapter = ReactCodeAdapter()
    blocks = adapter.extract_blocks(md)

    assert len(blocks) == 2
    assert blocks[0] == ("javascript", "const x = 1;\n")
    assert blocks[1] == ("typescript", "const y: number = 2;\n")


def test_react_adapter_timeout_handled(tmp_path: Path, monkeypatch) -> None:
    import subprocess

    from bookmaker.code.adapters.react import ReactCodeAdapter

    def fake_which(cmd):
        return "/fake/node" if cmd == "node" else None

    def fake_run(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd, 30)

    monkeypatch.setattr("bookmaker.code.adapters.react.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.react.subprocess.run", fake_run)

    adapter = ReactCodeAdapter()
    tagged = [("javascript", _JS_VALID)]
    results = adapter.run_tests(tagged, tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "error"
    assert "timed out" in results[0]["errors"][0]


# ---------------------------------------------------------------------------
# FlutterCodeAdapter (placeholder) tests
# ---------------------------------------------------------------------------

def test_flutter_adapter_skips_when_dart_missing(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.flutter import FlutterCodeAdapter

    monkeypatch.setattr("bookmaker.code.adapters.flutter.shutil.which", lambda cmd: None)

    adapter = FlutterCodeAdapter()
    results = adapter.run_tests(["void main() { print('hello'); }"], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "skipped"
    assert "dart_bulunamadi" == results[0]["reason"]


def test_flutter_adapter_skips_when_pubspec_found(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.flutter import FlutterCodeAdapter

    monkeypatch.setattr(
        "bookmaker.code.adapters.flutter.shutil.which",
        lambda cmd: "/fake/dart" if cmd == "dart" else None,
    )
    (tmp_path / "pubspec.yaml").write_text("name: test_flutter\n")

    adapter = FlutterCodeAdapter()
    results = adapter.run_tests(["void main() {}"], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "skipped"
    assert "flutter_widget_pubspec_found" == results[0]["reason"]


def test_flutter_adapter_runs_dart_analyze_for_standalone_dart(
    tmp_path: Path, monkeypatch,
) -> None:
    from bookmaker.code.adapters.flutter import FlutterCodeAdapter

    def fake_which(cmd):
        return "/fake/dart" if cmd == "dart" else None

    def fake_run(cmd, **kwargs):
        class Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.flutter.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.flutter.subprocess.run", fake_run)

    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    adapter = FlutterCodeAdapter()
    results = adapter.run_tests(["void main() { print('hello'); }"], sub_dir)

    assert len(results) == 1
    assert results[0]["status"] == "ok"
    assert "dart" in results[0]["command"][0]
    assert "analyze" in results[0]["command"][1]


def test_flutter_adapter_dart_analyze_error(tmp_path: Path, monkeypatch) -> None:
    from bookmaker.code.adapters.flutter import FlutterCodeAdapter

    def fake_which(cmd):
        return "/fake/dart" if cmd == "dart" else None

    def fake_run(cmd, **kwargs):
        class Result:
            returncode = 2
            stdout = ""
            stderr = "error: Expected ';' after this.\n"
        return Result()

    monkeypatch.setattr("bookmaker.code.adapters.flutter.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.flutter.subprocess.run", fake_run)

    adapter = FlutterCodeAdapter()
    results = adapter.run_tests(["void main() { print('hello') }"], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "error"
    assert results[0]["errors"]


def test_flutter_adapter_timeout_handled(tmp_path: Path, monkeypatch) -> None:
    import subprocess

    from bookmaker.code.adapters.flutter import FlutterCodeAdapter

    def fake_which(cmd):
        return "/fake/dart" if cmd == "dart" else None

    def fake_run(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd, 60)

    monkeypatch.setattr("bookmaker.code.adapters.flutter.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.code.adapters.flutter.subprocess.run", fake_run)

    adapter = FlutterCodeAdapter()
    results = adapter.run_tests(["void main() {}"], tmp_path)

    assert len(results) == 1
    assert results[0]["status"] == "error"
    assert "timed out" in results[0]["errors"][0]


# ---------------------------------------------------------------------------
# ReviewOnlyAdapter tests
# ---------------------------------------------------------------------------

def test_review_only_adapter_skips_all(tmp_path: Path) -> None:
    from bookmaker.code.adapters.base import ReviewOnlyAdapter

    adapter = ReviewOnlyAdapter()
    results = adapter.run_tests(["code1", "code2", "code3"], tmp_path)

    assert len(results) == 3
    assert all(r["status"] == "skipped" for r in results)
    assert all(r["reason"] == "review_only" for r in results)


# ---------------------------------------------------------------------------
# extract_blocks tests (from base adapter)
# ---------------------------------------------------------------------------

_MD_WITH_CODE = """\
# Test

```java
public class Main {}
```

Some text.

```python
print("hello")
```

```javascript
const x = 1;
```
"""


def test_java_adapter_extract_blocks() -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter

    adapter = JavaCodeAdapter()
    blocks = adapter.extract_blocks(_MD_WITH_CODE)

    assert len(blocks) == 1
    assert "public class Main" in blocks[0]


def test_python_adapter_extract_blocks() -> None:
    from bookmaker.code.adapters.python import PythonCodeAdapter

    adapter = PythonCodeAdapter()
    blocks = adapter.extract_blocks(_MD_WITH_CODE)

    assert len(blocks) == 1
    assert 'print("hello")' in blocks[0]


def test_react_adapter_extract_multiple_languages() -> None:
    from bookmaker.code.adapters.react import ReactCodeAdapter

    adapter = ReactCodeAdapter()
    blocks = adapter.extract_blocks(_MD_WITH_CODE)

    assert len(blocks) == 1
    assert blocks[0][0] == "javascript"
    assert "const x = 1;" in blocks[0][1]


def test_extract_blocks_no_matches() -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter

    adapter = JavaCodeAdapter()
    blocks = adapter.extract_blocks("# No code here\n\nJust text.")

    assert blocks == []


def test_review_only_adapter_extract_no_blocks() -> None:
    from bookmaker.code.adapters.base import ReviewOnlyAdapter

    adapter = ReviewOnlyAdapter()
    blocks = adapter.extract_blocks(_MD_WITH_CODE)

    assert blocks == []


# ---------------------------------------------------------------------------
# summarize_test_results test (report.py)
# ---------------------------------------------------------------------------

def test_summarize_test_results_counts_correctly() -> None:
    from bookmaker.code.report import summarize_test_results

    results = [
        {"block": 1, "status": "ok"},
        {"block": 2, "status": "ok"},
        {"block": 3, "status": "error"},
        {"block": 4, "status": "skipped"},
        {"block": 5, "status": "ok"},
    ]
    summary = summarize_test_results(results)

    assert summary["compiled"] == 3
    assert summary["failed"] == 1
    assert summary["skipped"] == 1


# ---------------------------------------------------------------------------
# select_code_adapter edge cases
# ---------------------------------------------------------------------------

def test_empty_profile_returns_review_only() -> None:
    from bookmaker.code.adapters.base import ReviewOnlyAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter("", None)
    assert isinstance(adapter, ReviewOnlyAdapter)


def test_whitespace_language_normalized() -> None:
    from bookmaker.code.adapters.java import JavaCodeAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter(None, "  Java  ")
    assert isinstance(adapter, JavaCodeAdapter)


# ---------------------------------------------------------------------------
# summarize_test_results enriched output
# ---------------------------------------------------------------------------

def test_summarize_test_results_returns_ok_error_skipped_total() -> None:
    from bookmaker.code.report import summarize_test_results

    results = [
        {"block": 1, "status": "ok"},
        {"block": 2, "status": "ok"},
        {"block": 3, "status": "error"},
        {"block": 4, "status": "skipped"},
        {"block": 5, "status": "ok"},
    ]
    summary = summarize_test_results(results)

    assert summary["ok"] == 3
    assert summary["error"] == 1
    assert summary["skipped"] == 1
    assert summary["total"] == 5
    assert summary["compiled"] == 3  # backward compat
    assert summary["failed"] == 1   # backward compat
