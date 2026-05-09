"""
bookmaker.production.screenshot_strategies.flutter_web
=======================================================
Flutter ekranlarını web build + Playwright ile PNG'ye dönüştürür.
Tam ekran görüntüleri, Scaffold düzenleri ve navigasyon akışları için.

Fence sözdizimi:
    ```dart web-screenshot
    class GirisEkrani extends StatelessWidget {
      const GirisEkrani({super.key});

      @override
      Widget build(BuildContext context) {
        return Scaffold(
          backgroundColor: Colors.indigo.shade50,
          appBar: AppBar(
            title: const Text('Hoş Geldiniz'),
            backgroundColor: Colors.indigo,
            foregroundColor: Colors.white,
          ),
          body: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.flutter_dash, size: 80, color: Colors.indigo),
                const SizedBox(height: 24),
                TextField(
                  decoration: const InputDecoration(
                    labelText: 'E-posta',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    minimumSize: const Size(double.infinity, 50),
                    backgroundColor: Colors.indigo,
                  ),
                  child: const Text('Giriş Yap',
                      style: TextStyle(color: Colors.white)),
                ),
              ],
            ),
          ),
        );
      }
    }
    ```

Nasıl çalışır:
    1. Kodu analiz et ve tools/flutter_screenshot_runner/lib/main.dart'a yaz
    2. flutter build web --release --web-renderer html
    3. Python http.server ile build/web/ klasörünü serve et
    4. Playwright ile mobil viewport (390×844) screenshot al
    5. Server'ı kapat, main.dart'ı placeholder'a geri döndür

Hız: ilk build ~40-60s, sonraki buildler ~10-20s (Dart önbelleği)
Windows: flutter.bat kullanılır, http.server platform-agnostic
"""

from __future__ import annotations

import http.server
import logging
import socket
import subprocess
import threading
import time
from pathlib import Path

from bookmaker.production.screenshot_strategies.base import (
    ScreenshotConfig,
    ScreenshotResult,
    ScreenshotStrategy,
)
from bookmaker.production.screenshot_strategies.flutter_utils import (
    build_web_main,
    check_flutter,
    find_runner_dir,
    flutter_cmd,
)

logger = logging.getLogger(__name__)

_MAIN_DART_REL = Path("lib") / "main.dart"
_BUILD_WEB_REL = Path("build") / "web"

# iPhone 14 Pro viewport — Flutter web tasarımları için standart
_MOBILE_VIEWPORT = {"width": 390, "height": 844}

_PLACEHOLDER_MAIN = """\
// bookMaker placeholder — bu dosya otomatik olarak yönetilir
import 'package:flutter/material.dart';

void main() {
  runApp(const MaterialApp(
    home: Scaffold(body: Center(child: Text('bookMaker placeholder'))),
  ));
}
"""


class FlutterWebStrategy(ScreenshotStrategy):
    """
    Flutter App/Widget → Web Build → Playwright → PNG.

    Playwright bookMaker'ın dev bağımlılığından production'a taşınmış olmalıdır.
    (pyproject.toml güncellenmesi gerekiyor — entegrasyon adım 2'ye bakın)
    """

    def __init__(
        self,
        config: ScreenshotConfig,
        runner_dir: Path | None = None,
    ) -> None:
        super().__init__(config)
        self._runner_dir = runner_dir
        self._flutter_version: str | None | bool = None

    @property
    def hint(self) -> str:
        return "web-screenshot"

    @property
    def runner_dir(self) -> Path:
        if self._runner_dir is None:
            self._runner_dir = find_runner_dir()
        return self._runner_dir

    # ------------------------------------------------------------------
    # Ana metot
    # ------------------------------------------------------------------

    def capture(
        self,
        output_path: Path,
        code: str,
        index: int,
    ) -> ScreenshotResult:
        # Parametre sırası base class ile aynı: (code, output_path, index)
        # Bu imzayı override etmiyoruz — base'den devralıyoruz.
        # (Aşağıda doğru sırayla çağrılıyor)
        raise NotImplementedError("capture(code, output_path, index) kullanın")

    def capture(  # type: ignore[misc]  # noqa: F811
        self,
        code: str,
        output_path: Path,
        index: int,
    ) -> ScreenshotResult:
        flutter_ver = self._get_flutter_version()
        if flutter_ver is None:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error="Flutter SDK bulunamadı.",
            )

        main_path = self.runner_dir / _MAIN_DART_REL
        try:
            # 1. main.dart'ı yaz
            main_code = build_web_main(code)
            main_path.write_text(main_code, encoding="utf-8")

            # 2. Web build
            logger.info("Flutter web build başlıyor...")
            self._build_web()

            build_dir = self.runner_dir / _BUILD_WEB_REL
            if not build_dir.exists():
                return ScreenshotResult(
                    index=index, hint=self.hint, output_path=output_path,
                    error="flutter build web başarısız — build/web/ oluşturulmadı.",
                )

            # 3. Playwright screenshot
            output_path.parent.mkdir(parents=True, exist_ok=True)
            self._screenshot_via_playwright(build_dir, output_path)

            if not output_path.exists():
                return ScreenshotResult(
                    index=index, hint=self.hint, output_path=output_path,
                    error="Playwright screenshot oluşturulamadı.",
                )

            logger.info(f"Flutter web screenshot kaydedildi: {output_path.name}")
            return ScreenshotResult(
                index=index,
                hint=self.hint,
                output_path=output_path,
                caption=f"Uygulama ekranı {index}",
            )

        except subprocess.TimeoutExpired:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error="flutter build web zaman aşımı (120s). Büyük projeler daha uzun sürebilir.",
            )
        except Exception as e:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error=str(e)[:300],
            )
        finally:
            # main.dart'ı placeholder'a geri döndür
            if main_path.exists():
                main_path.write_text(_PLACEHOLDER_MAIN, encoding="utf-8")

    # ------------------------------------------------------------------
    # Flutter web build
    # ------------------------------------------------------------------

    def _build_web(self) -> None:
        cmd = [
            flutter_cmd(),
            "build", "web",
            "--release",
            "--no-pub",          # pub get zaten yapıldı
            "--web-renderer", "html",  # canvaskit'ten daha hızlı build
        ]
        result = subprocess.run(
            cmd,
            cwd=str(self.runner_dir),
            capture_output=True,
            text=True,
            timeout=120,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            details = (result.stderr or result.stdout or "").strip()[:400]
            raise RuntimeError(f"flutter build web başarısız:\n{details}")
        logger.debug("Flutter web build tamamlandı.")

    # ------------------------------------------------------------------
    # HTTP server + Playwright
    # ------------------------------------------------------------------

    def _screenshot_via_playwright(
        self,
        build_dir: Path,
        output_path: Path,
    ) -> None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise RuntimeError(
                "playwright import edilemiyor. "
                "Kurulum: uv add playwright && uv run playwright install chromium\n"
                "pyproject.toml'da playwright production dependencies'e taşınmış olmalı."
            )

        port = self._find_free_port()
        server, thread = self._start_http_server(build_dir, port)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                context = browser.new_context(
                    viewport=_MOBILE_VIEWPORT,
                    device_scale_factor=self.config.scale,
                )
                page = context.new_page()
                page.goto(
                    f"http://localhost:{port}",
                    wait_until="networkidle",
                    timeout=self.config.react_timeout * 1000,
                )
                # Flutter canvas render için ek bekleme
                page.wait_for_timeout(1500)
                page.screenshot(
                    path=str(output_path),
                    clip={
                        "x": 0, "y": 0,
                        "width": _MOBILE_VIEWPORT["width"],
                        "height": _MOBILE_VIEWPORT["height"],
                    },
                )
                browser.close()
        finally:
            server.shutdown()
            thread.join(timeout=3)

    @staticmethod
    def _find_free_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            return s.getsockname()[1]

    @staticmethod
    def _start_http_server(
        directory: Path, port: int
    ) -> tuple[http.server.HTTPServer, threading.Thread]:
        dir_str = str(directory)

        class _Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=dir_str, **kwargs)

            def log_message(self, fmt, *args):
                pass  # Server loglarını sustur

        server = http.server.HTTPServer(("localhost", port), _Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        time.sleep(0.3)  # Server'ın hazır olmasını bekle
        return server, thread

    def _get_flutter_version(self) -> str | None:
        if self._flutter_version is None:
            self._flutter_version = check_flutter()
        return self._flutter_version  # type: ignore[return-value]
