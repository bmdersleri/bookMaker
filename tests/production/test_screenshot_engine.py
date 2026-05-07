"""
tests/production/test_screenshot_engine.py
===========================================
Screenshot motoru için unit testler.
Playwright ve subprocess tamamen mock'lanır — gerçek tarayıcı gerekmez.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from bookmaker.production.screenshot_engine import (
    _TAGGED_BLOCK_RE,
    ScreenshotEngine,
)
from bookmaker.production.screenshot_strategies.base import (
    ScreenshotConfig,
    ScreenshotStrategy,
)
from bookmaker.production.screenshot_strategies.python_console import PythonConsoleStrategy
from bookmaker.production.screenshot_strategies.python_plot import PythonPlotStrategy
from bookmaker.production.screenshot_strategies.react_component import (
    ReactComponentStrategy,
    _clean_exports,
    _detect_component_name,
)

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------

PLOT_CODE = """
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Test Grafik")
plt.show()
""".strip()

CONSOLE_CODE = """
for i in range(3):
    print(f"Satır {i+1}")
""".strip()

REACT_CODE = """
function Buton() {
  return <button style={{padding: 16}}>Tıkla</button>;
}
""".strip()

MD_WITH_ALL = f"""
# Bölüm

```python plot
{PLOT_CODE}
```

Açıklama metni.

```python console
{CONSOLE_CODE}
```

React örneği:

```jsx screenshot
{REACT_CODE}
```
"""


# ---------------------------------------------------------------------------
# Config testleri
# ---------------------------------------------------------------------------

class TestScreenshotConfig:
    def test_defaults(self):
        c = ScreenshotConfig()
        assert c.enabled is True
        assert c.python_timeout == 15
        assert c.scale == 2
        assert c.terminal_theme == "dark"

    def test_from_manifest_full(self):
        c = ScreenshotConfig.from_manifest({
            "enabled": False,
            "python_timeout": 30,
            "scale": 3,
            "terminal_theme": "light",
        })
        assert c.enabled is False
        assert c.python_timeout == 30
        assert c.scale == 3
        assert c.terminal_theme == "light"

    def test_from_manifest_none(self):
        c = ScreenshotConfig.from_manifest(None)
        assert c.enabled is True

    def test_from_manifest_partial(self):
        c = ScreenshotConfig.from_manifest({"scale": 3})
        assert c.scale == 3
        assert c.python_timeout == 15  # varsayılan


# ---------------------------------------------------------------------------
# Regex testleri
# ---------------------------------------------------------------------------

class TestTaggedBlockRegex:
    def test_finds_python_plot(self):
        md = f"```python plot\n{PLOT_CODE}\n```"
        matches = _TAGGED_BLOCK_RE.findall(md)
        assert len(matches) == 1
        assert matches[0][0] == "python"
        assert matches[0][1] == "plot"

    def test_finds_python_console(self):
        md = f"```python console\n{CONSOLE_CODE}\n```"
        matches = _TAGGED_BLOCK_RE.findall(md)
        assert len(matches) == 1
        assert matches[0][1] == "console"

    def test_finds_jsx_screenshot(self):
        md = f"```jsx screenshot\n{REACT_CODE}\n```"
        matches = _TAGGED_BLOCK_RE.findall(md)
        assert len(matches) == 1
        assert matches[0][0] == "jsx"

    def test_finds_multiple(self):
        matches = list(_TAGGED_BLOCK_RE.finditer(MD_WITH_ALL))
        assert len(matches) == 3

    def test_no_match_for_plain_block(self):
        md = "```python\nprint('hello')\n```"
        matches = _TAGGED_BLOCK_RE.findall(md)
        assert len(matches) == 0

    def test_case_insensitive(self):
        md = "```Python Plot\nprint(1)\n```"
        matches = _TAGGED_BLOCK_RE.findall(md)
        assert len(matches) == 1


# ---------------------------------------------------------------------------
# PythonPlotStrategy testleri
# ---------------------------------------------------------------------------

class TestPythonPlotStrategy:
    @pytest.fixture
    def strategy(self):
        return PythonPlotStrategy(ScreenshotConfig())

    def test_hint(self, strategy):
        assert strategy.hint == "plot"

    def test_patch_code_replaces_show(self, strategy):
        code = "import matplotlib.pyplot as plt\nplt.plot([1,2])\nplt.show()"
        patched = strategy._patch_code(code, Path("/tmp/out.png"))
        assert "plt.show()" not in patched
        assert "plt.savefig" in patched
        assert "Agg" in patched  # non-interactive backend

    def test_patch_code_plotly(self, strategy):
        code = "import plotly.express as px\nfig = px.bar([1,2,3])\nfig.show()"
        patched = strategy._patch_code(code, Path("/tmp/out.png"))
        assert "fig.show()" not in patched
        assert "fig.write_image" in patched

    @patch("subprocess.run")
    def test_capture_success(self, mock_run, strategy, tmp_path):
        out = tmp_path / "out.png"

        def fake_run(cmd, **kwargs):
            out.write_bytes(b"fake_png")  # PNG oluştur
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_run.side_effect = fake_run
        result = strategy.capture(PLOT_CODE, out, 1)
        assert result.success
        assert not result.was_cached

    @patch("subprocess.run")
    def test_capture_no_png_created(self, mock_run, strategy, tmp_path):
        out = tmp_path / "out.png"
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        result = strategy.capture(PLOT_CODE, out, 1)
        assert not result.success
        assert "PNG" in result.error

    @patch("subprocess.run")
    def test_capture_runtime_error(self, mock_run, strategy, tmp_path):
        out = tmp_path / "out.png"
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "python", stderr="NameError: name 'plt' is not defined"
        )
        result = strategy.capture("plt.show()", out, 1)
        assert not result.success
        assert "hata" in result.error.lower() or "Error" in result.error

    @patch("subprocess.run")
    def test_capture_timeout(self, mock_run, strategy, tmp_path):
        out = tmp_path / "out.png"
        mock_run.side_effect = subprocess.TimeoutExpired("python", 15)
        result = strategy.capture(PLOT_CODE, out, 1)
        assert not result.success
        assert "aşımı" in result.error or "timeout" in result.error.lower()


# ---------------------------------------------------------------------------
# PythonConsoleStrategy testleri
# ---------------------------------------------------------------------------

class TestPythonConsoleStrategy:
    @pytest.fixture
    def strategy(self):
        return PythonConsoleStrategy(ScreenshotConfig())

    def test_hint(self, strategy):
        assert strategy.hint == "console"

    @patch("subprocess.run")
    def test_run_code_returns_stdout(self, mock_run, strategy):
        mock_run.return_value = MagicMock(
            stdout="Satır 1\nSatır 2", stderr="", returncode=0
        )
        stdout, stderr = strategy._run_code("print('test')")
        assert "Satır 1" in stdout
        assert stderr == ""

    def test_render_html_dark(self, strategy):
        html = strategy._render_html("Merhaba", "")
        assert "1e1e2e" in html  # dark background
        assert "Merhaba" in html

    def test_render_html_light(self):
        s = PythonConsoleStrategy(ScreenshotConfig(terminal_theme="light"))
        html = s._render_html("Merhaba", "")
        assert "#ffffff" in html  # light background

    def test_render_html_with_error(self, strategy):
        html = strategy._render_html("çıktı", "SyntaxError: ...")
        assert "SyntaxError" in html
        assert "error" in html.lower()

    def test_render_html_empty_output(self, strategy):
        html = strategy._render_html("", "")
        assert "(Çıktı yok)" in html


# ---------------------------------------------------------------------------
# ReactComponentStrategy testleri
# ---------------------------------------------------------------------------

class TestReactComponentStrategy:
    @pytest.fixture
    def strategy(self):
        return ReactComponentStrategy(ScreenshotConfig())

    def test_hint(self, strategy):
        assert strategy.hint == "screenshot"

    @pytest.mark.parametrize("code,expected", [
        ("function Buton() { return <div/>; }", "Buton"),
        ("const Kart = () => <div/>;", "Kart"),
        ("export default function App() {}", "App"),
        ("function kucuk() {}", "App"),  # küçük harf → fallback
    ])
    def test_detect_component_name(self, code, expected):
        assert _detect_component_name(code) == expected

    def test_clean_exports(self):
        code = "export default function App() {}\nexport const x = 1;"
        cleaned = _clean_exports(code)
        assert "export" not in cleaned
        assert "function App" in cleaned


# ---------------------------------------------------------------------------
# ScreenshotEngine entegrasyon testleri
# ---------------------------------------------------------------------------

class TestScreenshotEngine:
    @pytest.fixture
    def engine(self):
        return ScreenshotEngine(ScreenshotConfig())

    def test_disabled_engine_returns_unchanged(self, tmp_path):
        engine = ScreenshotEngine(ScreenshotConfig(enabled=False))
        md = f"```python plot\n{PLOT_CODE}\n```"
        result = engine.process_markdown(md, tmp_path / "assets", "ch")
        assert result.total == 0
        assert result.output_md == md

    def test_no_tagged_blocks_returns_unchanged(self, engine, tmp_path):
        md = "```python\nprint('hello')\n```"
        result = engine.process_markdown(md, tmp_path / "assets", "ch")
        assert result.total == 0
        assert result.output_md == md

    @patch.object(PythonPlotStrategy, "capture")
    def test_renders_plot_block(self, mock_capture, engine, tmp_path):
        assets = tmp_path / "assets"
        fig = assets / "ss_ch_01_plot.png"
        mock_capture.return_value = MagicMock(
            success=True, was_cached=False,
            output_path=fig, caption="Grafik 1", error=None,
        )
        fig.parent.mkdir(parents=True, exist_ok=True)
        fig.write_bytes(b"fake")

        md = f"```python plot\n{PLOT_CODE}\n```"
        result = engine.process_markdown(md, assets, "ch")

        assert result.rendered == 1
        assert "assets/ss_ch_01_plot.png" in result.output_md
        assert "```python" in result.output_md  # kod bloğu korunur

    @patch.object(PythonPlotStrategy, "capture")
    def test_failed_block_keeps_original(self, mock_capture, engine, tmp_path):
        assets = tmp_path / "assets"
        mock_capture.return_value = MagicMock(
            success=False, was_cached=False,
            output_path=assets / "x.png",
            error="test hatası",
        )
        md = f"```python plot\n{PLOT_CODE}\n```"
        result = engine.process_markdown(md, assets, "ch")

        assert result.failed == 1
        assert "SCREENSHOT HATASI" in result.output_md
        assert "```python" in result.output_md

    @patch.object(PythonPlotStrategy, "capture")
    def test_cache_hit_skips_render(self, mock_capture, engine, tmp_path):
        assets = tmp_path / "assets"
        assets.mkdir()
        fig_name = "ss_ch_01_plot.png"
        fig = assets / fig_name
        fig.write_bytes(b"fake")

        # Cache'e yaz
        code_for_key = PLOT_CODE
        cache_key = PythonPlotStrategy.cache_key(code_for_key, "plot")
        cache_file = assets / ".screenshot_cache.json"
        cache_file.write_text(
            json.dumps({cache_key: fig_name}), encoding="utf-8"
        )

        md = f"```python plot\n{PLOT_CODE}\n```"
        result = engine.process_markdown(md, assets, "ch")

        assert result.cached == 1
        assert result.rendered == 0
        mock_capture.assert_not_called()

    @patch.object(PythonPlotStrategy, "capture")
    @patch.object(PythonConsoleStrategy, "capture")
    @patch.object(ReactComponentStrategy, "capture")
    def test_processes_all_three_strategies(
        self, mock_react, mock_console, mock_plot, engine, tmp_path
    ):
        assets = tmp_path / "assets"
        assets.mkdir()

        def fake_capture(code, path, index):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"fake")
            return MagicMock(
                success=True, was_cached=False,
                output_path=path, caption=f"Çıktı {index}", error=None,
            )

        mock_plot.side_effect = fake_capture
        mock_console.side_effect = fake_capture
        mock_react.side_effect = fake_capture

        result = engine.process_markdown(MD_WITH_ALL, assets, "ch")

        assert result.total == 3
        assert result.rendered == 3
        assert result.failed == 0
        mock_plot.assert_called_once()
        mock_console.assert_called_once()
        mock_react.assert_called_once()

    def test_cache_key_stable(self):
        k1 = ScreenshotStrategy.cache_key(PLOT_CODE, "plot")
        k2 = ScreenshotStrategy.cache_key(PLOT_CODE, "plot")
        assert k1 == k2

    def test_cache_key_differs_by_hint(self):
        k1 = ScreenshotStrategy.cache_key(PLOT_CODE, "plot")
        k2 = ScreenshotStrategy.cache_key(PLOT_CODE, "console")
        assert k1 != k2
