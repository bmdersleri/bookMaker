"""
tests/production/test_flutter_screenshot.py
============================================
FlutterGoldenStrategy ve FlutterWebStrategy unit testleri.
Flutter SDK ve Playwright tamamen mock'lanır.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from bookmaker.production.screenshot_strategies.base import ScreenshotConfig
from bookmaker.production.screenshot_strategies.flutter_utils import (
    build_golden_test,
    build_web_main,
    extract_class_name,
    extract_imports,
    is_full_app,
    is_widget_class,
    is_widget_expression,
    strip_imports,
)
from bookmaker.production.screenshot_strategies.flutter_golden import FlutterGoldenStrategy
from bookmaker.production.screenshot_strategies.flutter_web import FlutterWebStrategy


# ---------------------------------------------------------------------------
# Örnek Dart kodları
# ---------------------------------------------------------------------------

EXPR = "ElevatedButton(onPressed: () {}, child: const Text('Tıkla'))"

CLASS = """\
class MerhabaWidget extends StatelessWidget {
  const MerhabaWidget({super.key});
  @override
  Widget build(BuildContext context) {
    return const Text('Merhaba Flutter!');
  }
}"""

FULL = """\
import 'package:flutter/material.dart';

void main() {
  runApp(const MaterialApp(home: Scaffold(body: Text('App'))));
}"""

WITH_IMPORTS = """\
import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';

CupertinoButton(onPressed: () {}, child: const Text('iOS'))"""


# ---------------------------------------------------------------------------
# flutter_utils testleri
# ---------------------------------------------------------------------------

class TestFlutterUtils:
    def test_is_full_app(self):
        assert is_full_app(FULL)
        assert not is_full_app(CLASS)
        assert not is_full_app(EXPR)

    def test_is_widget_class(self):
        assert is_widget_class(CLASS)
        assert not is_widget_class(EXPR)
        assert not is_widget_class(FULL)

    def test_is_widget_expression(self):
        assert is_widget_expression(EXPR)
        assert not is_widget_expression(CLASS)
        assert not is_widget_expression(FULL)

    def test_extract_class_name(self):
        assert extract_class_name(CLASS) == "MerhabaWidget"
        assert extract_class_name(EXPR) is None

    def test_extract_imports(self):
        imports = extract_imports(WITH_IMPORTS)
        assert len(imports) == 2
        assert any("material" in i for i in imports)
        assert any("cupertino" in i for i in imports)

    def test_strip_imports(self):
        stripped = strip_imports(WITH_IMPORTS)
        assert "import" not in stripped
        assert "CupertinoButton" in stripped


class TestBuildGoldenTest:
    def test_expression_wrapped_in_scaffold(self):
        test = build_golden_test(EXPR)
        assert "testWidgets" in test
        assert "matchesGoldenFile" in test
        assert "ElevatedButton" in test
        assert "Center" in test
        assert "Scaffold" in test

    def test_class_uses_class_name(self):
        test = build_golden_test(CLASS)
        assert "MerhabaWidget" in test
        assert "matchesGoldenFile" in test

    def test_full_app_extracts_runapp_arg(self):
        test = build_golden_test(FULL)
        assert "testWidgets" in test
        assert "MaterialApp" in test

    def test_imports_preserved(self):
        test = build_golden_test(WITH_IMPORTS)
        assert "cupertino" in test.lower()


class TestBuildWebMain:
    def test_expression_wrapped(self):
        main = build_web_main(EXPR)
        assert "void main()" in main
        assert "runApp" in main
        assert "ElevatedButton" in main

    def test_class_used_as_home(self):
        main = build_web_main(CLASS)
        assert "MerhabaWidget" in main
        assert "void main()" in main

    def test_full_app_passthrough(self):
        main = build_web_main(FULL)
        assert "void main()" in main
        assert "runApp" in main


# ---------------------------------------------------------------------------
# FlutterGoldenStrategy testleri
# ---------------------------------------------------------------------------

@pytest.fixture
def runner(tmp_path) -> Path:
    """Sahte runner dizini oluşturur."""
    r = tmp_path / "tools" / "flutter_screenshot_runner"
    r.mkdir(parents=True)
    (r / "pubspec.yaml").write_text("name: runner\n")
    (r / "test").mkdir()
    (r / "test" / "screenshot_test.dart").write_text("void main() {}\n")
    (r / "lib").mkdir()
    (r / "lib" / "main.dart").write_text("// placeholder\n")
    return r


@pytest.fixture
def golden(runner) -> FlutterGoldenStrategy:
    with patch(
        "bookmaker.production.screenshot_strategies.flutter_golden.check_flutter",
        return_value="Flutter 3.27.0",
    ):
        return FlutterGoldenStrategy(ScreenshotConfig(python_timeout=30), runner_dir=runner)


class TestFlutterGoldenStrategy:
    def test_hint(self, golden):
        assert golden.hint == "screenshot"

    @patch("subprocess.run")
    def test_capture_success(self, mock_run, golden, runner, tmp_path):
        out = tmp_path / "out.png"

        def fake_run(cmd, **kwargs):
            golden_path = runner / "test" / "goldens" / "screenshot.png"
            golden_path.parent.mkdir(parents=True, exist_ok=True)
            golden_path.write_bytes(b"PNG_FAKE")
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_run.side_effect = fake_run
        with patch.object(golden, "_get_flutter_version", return_value="Flutter 3.x"):
            result = golden.capture(EXPR, out, 1)

        assert result.success
        assert out.exists()
        assert out.read_bytes() == b"PNG_FAKE"

    @patch("subprocess.run")
    def test_capture_test_failure(self, mock_run, golden, tmp_path):
        out = tmp_path / "out.png"
        mock_run.return_value = MagicMock(
            returncode=1, stderr="Compile error: undefined", stdout=""
        )
        with patch.object(golden, "_get_flutter_version", return_value="Flutter 3.x"):
            result = golden.capture("invalid dart code", out, 1)

        assert not result.success
        assert "başarısız" in result.error or "error" in result.error.lower()

    def test_flutter_not_found(self, golden, tmp_path):
        out = tmp_path / "out.png"
        with patch.object(golden, "_get_flutter_version", return_value=None):
            result = golden.capture(EXPR, out, 1)

        assert not result.success
        assert "Flutter SDK" in result.error

    @patch("subprocess.run")
    def test_test_file_restored_on_success(self, mock_run, golden, runner, tmp_path):
        """Başarılı render'dan sonra test dosyası placeholder'a geri dönmeli."""
        out = tmp_path / "out.png"

        def fake_run(cmd, **kwargs):
            (runner / "test" / "goldens").mkdir(parents=True, exist_ok=True)
            (runner / "test" / "goldens" / "screenshot.png").write_bytes(b"x")
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_run.side_effect = fake_run
        with patch.object(golden, "_get_flutter_version", return_value="Flutter 3.x"):
            golden.capture(EXPR, out, 1)

        content = (runner / "test" / "screenshot_test.dart").read_text()
        assert "bookMaker placeholder" in content

    @patch("subprocess.run")
    def test_test_file_restored_on_failure(self, mock_run, golden, runner, tmp_path):
        """Başarısız render'dan sonra da test dosyası temizlenmeli."""
        out = tmp_path / "out.png"
        mock_run.return_value = MagicMock(returncode=1, stderr="err", stdout="")

        with patch.object(golden, "_get_flutter_version", return_value="Flutter 3.x"):
            golden.capture(EXPR, out, 1)

        content = (runner / "test" / "screenshot_test.dart").read_text()
        assert "bookMaker placeholder" in content

    @patch("subprocess.run")
    def test_timeout_returns_error(self, mock_run, golden, tmp_path):
        out = tmp_path / "out.png"
        mock_run.side_effect = subprocess.TimeoutExpired("flutter", 30)
        with patch.object(golden, "_get_flutter_version", return_value="Flutter 3.x"):
            result = golden.capture(EXPR, out, 1)

        assert not result.success
        assert "aşımı" in result.error

    @patch("subprocess.run")
    def test_cmd_uses_update_goldens_flag(self, mock_run, golden, runner, tmp_path):
        out = tmp_path / "out.png"

        def fake_run(cmd, **kwargs):
            (runner / "test" / "goldens").mkdir(parents=True, exist_ok=True)
            (runner / "test" / "goldens" / "screenshot.png").write_bytes(b"x")
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_run.side_effect = fake_run
        with patch.object(golden, "_get_flutter_version", return_value="Flutter 3.x"):
            golden.capture(EXPR, out, 1)

        called_cmd = mock_run.call_args[0][0]
        assert "--update-goldens" in called_cmd

    def test_cache_key_stable(self, golden):
        k1 = FlutterGoldenStrategy.cache_key(EXPR, "screenshot")
        k2 = FlutterGoldenStrategy.cache_key(EXPR, "screenshot")
        assert k1 == k2

    def test_cache_key_differs_by_code(self, golden):
        k1 = FlutterGoldenStrategy.cache_key(EXPR, "screenshot")
        k2 = FlutterGoldenStrategy.cache_key(CLASS, "screenshot")
        assert k1 != k2


# ---------------------------------------------------------------------------
# FlutterWebStrategy testleri
# ---------------------------------------------------------------------------

@pytest.fixture
def web(runner) -> FlutterWebStrategy:
    with patch(
        "bookmaker.production.screenshot_strategies.flutter_web.check_flutter",
        return_value="Flutter 3.27.0",
    ):
        return FlutterWebStrategy(ScreenshotConfig(react_timeout=10), runner_dir=runner)


class TestFlutterWebStrategy:
    def test_hint(self, web):
        assert web.hint == "web-screenshot"

    def test_flutter_not_found(self, web, tmp_path):
        out = tmp_path / "out.png"
        with patch.object(web, "_get_flutter_version", return_value=None):
            result = web.capture(CLASS, out, 1)

        assert not result.success
        assert "Flutter SDK" in result.error

    @patch("subprocess.run")
    def test_main_dart_written_before_build(self, mock_run, web, runner, tmp_path):
        """_build_web() çağrılmadan önce main.dart doğru içerikle yazılmış olmalı."""
        out = tmp_path / "out.png"
        main_written = []

        def fake_run(cmd, **kwargs):
            content = (runner / "lib" / "main.dart").read_text()
            main_written.append(content)
            raise RuntimeError("test stop")

        mock_run.side_effect = fake_run
        with patch.object(web, "_get_flutter_version", return_value="Flutter 3.x"):
            web.capture(CLASS, out, 1)

        assert main_written, "main.dart yazılmadan build tetiklendi"
        assert "MerhabaWidget" in main_written[0]

    @patch("subprocess.run")
    def test_main_dart_restored_after_capture(self, mock_run, web, runner, tmp_path):
        """Başarılı veya başarısız olsun main.dart placeholder'a döndürülmeli."""
        out = tmp_path / "out.png"
        mock_run.side_effect = RuntimeError("build failed")

        with patch.object(web, "_get_flutter_version", return_value="Flutter 3.x"):
            web.capture(CLASS, out, 1)

        content = (runner / "lib" / "main.dart").read_text()
        assert "bookMaker placeholder" in content

    @patch("subprocess.run")
    def test_build_web_timeout(self, mock_run, web, tmp_path):
        out = tmp_path / "out.png"
        mock_run.side_effect = subprocess.TimeoutExpired("flutter", 120)
        with patch.object(web, "_get_flutter_version", return_value="Flutter 3.x"):
            result = web.capture(CLASS, out, 1)

        assert not result.success
        assert "aşımı" in result.error

    @patch("subprocess.run")
    def test_build_failure_returns_error(self, mock_run, web, tmp_path):
        out = tmp_path / "out.png"
        mock_run.return_value = MagicMock(
            returncode=1, stderr="Error: file not found", stdout=""
        )
        with patch.object(web, "_get_flutter_version", return_value="Flutter 3.x"):
            result = web.capture(CLASS, out, 1)

        assert not result.success
        assert "başarısız" in result.error
