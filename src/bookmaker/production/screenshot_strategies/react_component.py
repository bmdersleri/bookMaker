"""bookmaker.production.screenshot_strategies.react_component
===========================================================
React/JSX bileşenlerini tarayıcıda render edip PNG'ye dönüştürür.
Vite veya build adımı gerektirmez — CDN React + Babel kullanır.

Fence sözdizimi:
    ```jsx screenshot
    function Sayac() {
      const [n, setN] = React.useState(0);
      return (
        <div style={{padding: 24, fontFamily: 'sans-serif'}}>
          <h2>Sayaç: {n}</h2>
          <button onClick={() => setN(n + 1)}>Artır</button>
        </div>
      );
    }
    ```

Desteklenen dil etiketleri: jsx, tsx, react (hepsi "screenshot" hint'i ile)

Strateji:
    1. Bileşen kodunu React CDN + Babel standalone HTML'e yerleştir
    2. Playwright headless Chromium ile yükle
    3. #root içeriği render olunca screenshot al
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from bookmaker.production.screenshot_strategies.base import (
    ScreenshotResult,
    ScreenshotStrategy,
)

logger = logging.getLogger(__name__)

_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: {bg_color};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    padding: 24px;
    min-height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
  }}
  #root {{
    width: 100%;
  }}
  /* Temel stil sıfırlaması — bileşen kendi stilini getirir */
  button {{
    cursor: pointer;
    font-family: inherit;
  }}
</style>
</head>
<body>
<div id="root"></div>
<script src="https://unpkg.com/react@18/umd/react.development.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script type="text/babel">
const {{ useState, useEffect, useRef, useCallback, useMemo }} = React;

{component_code}

// Bileşen adını tespit et ve render et
(function() {{
  const rootEl = document.getElementById('root');
  const root = ReactDOM.createRoot(rootEl);

  // Son tanımlanan function/const bileşeni bul
  const componentName = '{component_name}';
  const Component = eval(componentName);
  root.render(React.createElement(Component));
  document.title = 'ready';
}})();
</script>
</body>
</html>"""


def _detect_component_name(code: str) -> str:
    """Koddan bileşen adını çıkarır.
    Önce 'export default X' veya 'function X' formatına bakar.
    Bulamazsa 'App' döner.
    """
    import re

    # export default function ComponentName
    m = re.search(r"export\s+default\s+function\s+(\w+)", code)
    if m:
        return m.group(1)

    # function ComponentName( — büyük harfle başlayan
    m = re.search(r"function\s+([A-Z]\w+)\s*\(", code)
    if m:
        return m.group(1)

    # const ComponentName = (
    m = re.search(r"const\s+([A-Z]\w+)\s*=", code)
    if m:
        return m.group(1)

    return "App"


def _clean_exports(code: str) -> str:
    """Export default/export deyimlerini kaldırır — CDN ortamında çalışmaz."""
    import re
    code = re.sub(r"\bexport\s+default\s+", "", code)
    code = re.sub(r"\bexport\s+", "", code)
    return code


class ReactComponentStrategy(ScreenshotStrategy):
    """JSX/TSX React bileşenlerini Playwright ile screenshot'lar."""

    @property
    def hint(self) -> str:
        return "screenshot"

    def capture(
        self,
        code: str,
        output_path: Path,
        index: int,
    ) -> ScreenshotResult:
        try:
            component_name = _detect_component_name(code)
            cleaned_code = _clean_exports(code)
            bg = "#ffffff" if self.config.terminal_theme == "light" else "#f8f9fa"
            html_content = _HTML_TEMPLATE.format(
                component_code=cleaned_code,
                component_name=component_name,
                bg_color=bg,
            )
            self._screenshot(html_content, output_path)

            if not output_path.exists():
                return ScreenshotResult(
                    index=index, hint=self.hint, output_path=output_path,
                    error="Playwright screenshot oluşturulamadı.",
                )

            logger.info(f"React screenshot kaydedildi: {output_path.name}")
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                caption=f"Bileşen çıktısı {index}",
            )

        except Exception as e:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error=str(e)[:300],
            )

    # ------------------------------------------------------------------

    def _screenshot(self, html_content: str, output_path: Path) -> None:
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
                page.goto(
                    f"file:///{tmp_html.as_posix()}",
                    wait_until="domcontentloaded",
                )
                # React render'ını bekle
                page.wait_for_function(
                    "document.title === 'ready'",
                    timeout=self.config.react_timeout * 1000,
                )
                page.wait_for_timeout(300)  # animasyonlar için bekleme

                element = page.query_selector("#root")
                if element:
                    element.screenshot(path=str(output_path))
                else:
                    page.screenshot(path=str(output_path), full_page=True)

                browser.close()
        finally:
            tmp_html.unlink(missing_ok=True)
