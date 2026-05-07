"""
bookmaker.production.screenshot_strategies.python_console
==========================================================
Python kodunun konsol çıktısını stillendirilmiş terminal PNG'sine dönüştürür.

Fence sözdizimi:
    ```python console
    for i in range(1, 6):
        print(f"{i}. Merhaba Dünya!")
    ```

Strateji:
    1. Kodu subprocess'te çalıştır, stdout+stderr yakala
    2. Çıktıyı dark/light terminal HTML şablonuna yerleştir
    3. Playwright ile screenshot al
"""

from __future__ import annotations

import html
import logging
import subprocess
import sys
import tempfile
from pathlib import Path

from bookmaker.production.screenshot_strategies.base import (
    ScreenshotResult,
    ScreenshotStrategy,
)

logger = logging.getLogger(__name__)

# Terminal HTML şablonları
_DARK_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #1e1e2e;
    font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    font-size: 14px;
    line-height: 1.6;
    padding: 0;
  }}
  .terminal {{
    background: #1e1e2e;
    border-radius: 10px;
    overflow: hidden;
    min-width: 600px;
    max-width: 900px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  }}
  .titlebar {{
    background: #313244;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .dot {{ width: 13px; height: 13px; border-radius: 50%; }}
  .dot.red {{ background: #f38ba8; }}
  .dot.yellow {{ background: #f9e2af; }}
  .dot.green {{ background: #a6e3a1; }}
  .title {{
    flex: 1;
    text-align: center;
    color: #6c7086;
    font-size: 12px;
    font-family: inherit;
  }}
  .content {{
    padding: 20px 24px;
    color: #cdd6f4;
    white-space: pre-wrap;
    word-break: break-word;
  }}
  .prompt {{ color: #89b4fa; }}
  .output {{ color: #cdd6f4; }}
  .error {{ color: #f38ba8; }}
</style>
</head>
<body>
<div class="terminal">
  <div class="titlebar">
    <span class="dot red"></span>
    <span class="dot yellow"></span>
    <span class="dot green"></span>
    <span class="title">Python — Çıktı</span>
  </div>
  <div class="content"><span class="output">{output}</span>{error_block}</div>
</div>
</body>
</html>"""

_LIGHT_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #f5f5f5;
    font-family: 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace;
    font-size: 14px;
    line-height: 1.6;
    padding: 0;
  }}
  .terminal {{
    background: #ffffff;
    border-radius: 10px;
    overflow: hidden;
    min-width: 600px;
    max-width: 900px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.12);
  }}
  .titlebar {{
    background: #f0f0f0;
    border-bottom: 1px solid #e0e0e0;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .dot {{ width: 13px; height: 13px; border-radius: 50%; }}
  .dot.red {{ background: #ff5f57; }}
  .dot.yellow {{ background: #febc2e; }}
  .dot.green {{ background: #28c840; }}
  .title {{
    flex: 1;
    text-align: center;
    color: #999;
    font-size: 12px;
    font-family: inherit;
  }}
  .content {{
    padding: 20px 24px;
    color: #24292e;
    white-space: pre-wrap;
    word-break: break-word;
  }}
  .error {{ color: #d73a49; }}
</style>
</head>
<body>
<div class="terminal">
  <div class="titlebar">
    <span class="dot red"></span>
    <span class="dot yellow"></span>
    <span class="dot green"></span>
    <span class="title">Python — Çıktı</span>
  </div>
  <div class="content">{output}{error_block}</div>
</div>
</body>
</html>"""


class PythonConsoleStrategy(ScreenshotStrategy):
    """Python stdout/stderr çıktısını terminal ekran görüntüsüne dönüştürür."""

    @property
    def hint(self) -> str:
        return "console"

    def capture(
        self,
        code: str,
        output_path: Path,
        index: int,
    ) -> ScreenshotResult:
        try:
            stdout, stderr = self._run_code(code)

            if not stdout and not stderr:
                stdout = "(Çıktı yok)"

            html_content = self._render_html(stdout, stderr)
            self._screenshot(html_content, output_path)

            if not output_path.exists():
                return ScreenshotResult(
                    index=index, hint=self.hint, output_path=output_path,
                    error="Playwright screenshot oluşturulamadı.",
                )

            logger.info(f"Console screenshot kaydedildi: {output_path.name}")
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                caption=f"Program çıktısı {index}",
            )

        except Exception as e:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error=str(e)[:300],
            )

    # ------------------------------------------------------------------

    def _run_code(self, code: str) -> tuple[str, str]:
        """Kodu subprocess'te çalıştırır, stdout ve stderr döner."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            tmp = Path(f.name)

        try:
            result = subprocess.run(
                [sys.executable, str(tmp)],
                capture_output=True,
                text=True,
                timeout=self.config.python_timeout,
                encoding="utf-8",
                errors="replace",
            )
            return result.stdout.strip(), result.stderr.strip()
        finally:
            tmp.unlink(missing_ok=True)

    def _render_html(self, stdout: str, stderr: str) -> str:
        """Çıktıyı HTML terminal şablonuna yerleştirir."""
        escaped_out = html.escape(stdout) if stdout else "(Çıktı yok)"
        error_block = ""
        if stderr:
            escaped_err = html.escape(stderr)
            error_block = f'\n<span class="error">{escaped_err}</span>'

        template = (
            _DARK_TEMPLATE
            if self.config.terminal_theme == "dark"
            else _LIGHT_TEMPLATE
        )
        return template.format(output=escaped_out, error_block=error_block)

    def _screenshot(self, html_content: str, output_path: Path) -> None:
        """HTML içeriğini Playwright ile screenshot'lar."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise RuntimeError(
                "Playwright kurulu değil. "
                "Kurmak için: uv add playwright && uv run playwright install chromium"
            )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", delete=False, encoding="utf-8"
        ) as f:
            f.write(html_content)
            tmp_html = Path(f.name)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(
                    viewport={
                        "width": self.config.viewport_width,
                        "height": self.config.viewport_height,
                    },
                    device_scale_factor=self.config.scale,
                )
                page.goto(f"file:///{tmp_html.as_posix()}")
                page.wait_for_selector(".terminal")
                element = page.query_selector(".terminal")
                element.screenshot(path=str(output_path))
                browser.close()
        finally:
            tmp_html.unlink(missing_ok=True)
