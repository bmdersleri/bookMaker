"""bookmaker.production.screenshot_strategies.python_plot
=======================================================
matplotlib, plotly ve seaborn çıktılarını PNG'ye dönüştürür.

Fence sözdizimi:
    ```python plot
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.title("Örnek Grafik")
    plt.show()
    ```

Strateji:
    1. plt.show() → plt.savefig(output_path, ...) ile değiştir
    2. fig.show() → fig.write_image(output_path) ile değiştir
    3. Kodu sys.executable ile subprocess'te çalıştır
    4. PNG oluştu mu kontrol et
"""

from __future__ import annotations

import logging
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from bookmaker.production.screenshot_strategies.base import (
    ScreenshotResult,
    ScreenshotStrategy,
)

logger = logging.getLogger(__name__)

# matplotlib DPI — scale ile çarpılır (scale=2 → 300 DPI)
_BASE_DPI = 150


class PythonPlotStrategy(ScreenshotStrategy):
    """matplotlib / plotly / seaborn grafik screenshot stratejisi."""

    @property
    def hint(self) -> str:
        return "plot"

    def capture(
        self,
        code: str,
        output_path: Path,
        index: int,
    ) -> ScreenshotResult:
        try:
            patched = self._patch_code(code, output_path)
            self._run(patched)

            if not output_path.exists():
                return ScreenshotResult(
                    index=index, hint=self.hint, output_path=output_path,
                    error="Kod çalıştı ama PNG oluşturulmadı. plt.show() veya fig.show() var mı?",
                )

            logger.info(f"Plot screenshot kaydedildi: {output_path.name}")
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                caption=f"Çıktı {index}",
            )

        except subprocess.TimeoutExpired:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error=f"Zaman aşımı ({self.config.python_timeout}s).",
            )
        except Exception as e:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error=str(e)[:300],
            )

    # ------------------------------------------------------------------
    # Kod dönüşümü
    # ------------------------------------------------------------------

    def _patch_code(self, code: str, output_path: Path) -> str:
        """plt.show() ve fig.show() çağrılarını dosyaya kaydetme ile değiştirir.
        Matplotlib backend'ini non-interactive olarak ayarlar.
        """
        out = str(output_path).replace("\\", "/")
        dpi = _BASE_DPI * self.config.scale

        lines = []

        # Matplotlib non-interactive backend — ekran gerektirmez
        if "matplotlib" in code or "plt" in code or "seaborn" in code:
            lines.append("import matplotlib")
            lines.append("matplotlib.use('Agg')")

        lines.append(code)

        # plt.show() → savefig
        patched = "\n".join(lines)
        patched = re.sub(
            r"\bplt\.show\(\)",
            f"plt.savefig(r'{out}', dpi={dpi}, bbox_inches='tight', "
            f"facecolor='white', edgecolor='none')",
            patched,
        )

        # fig.show() → write_image (plotly)
        patched = re.sub(
            r"\bfig\.show\(\)",
            f"fig.write_image(r'{out}', scale={self.config.scale})",
            patched,
        )

        # plt.savefig() çağrısı zaten varsa da yakala
        if "plt.show()" not in code and "fig.show()" not in code:
            if "plt" in code and "plt.savefig" not in patched:
                patched += (
                    f"\nplt.savefig(r'{out}', dpi={dpi}, "
                    f"bbox_inches='tight', facecolor='white', edgecolor='none')"
                )

        return patched

    def _run(self, code: str) -> None:
        """Geçici dosyaya yazar ve Python interpreter ile çalıştırır."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False,
            encoding="utf-8",
        ) as f:
            f.write(code)
            tmp = Path(f.name)

        try:
            subprocess.run(
                [sys.executable, str(tmp)],
                capture_output=True,
                text=True,
                timeout=self.config.python_timeout,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            stderr = (e.stderr or "").strip()[:300]
            raise RuntimeError(f"Python çalıştırma hatası:\n{stderr}") from e
        finally:
            tmp.unlink(missing_ok=True)
