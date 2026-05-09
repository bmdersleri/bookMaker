"""
bookmaker.production.screenshot_strategies.flutter_golden
===========================================================
Flutter widget'larını headless golden test ile PNG'ye dönüştürür.
Emülatör veya fiziksel cihaz gerektirmez — Dart VM üzerinde çalışır.

Fence sözdizimi:
    ```dart screenshot
    ElevatedButton(
      onPressed: () {},
      style: ElevatedButton.styleFrom(backgroundColor: Colors.indigo),
      child: const Text('Kaydet', style: TextStyle(color: Colors.white)),
    )
    ```

    ```dart screenshot
    class UrunKarti extends StatelessWidget {
      const UrunKarti({super.key});
      @override
      Widget build(BuildContext context) {
        return Card(
          elevation: 4,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: const [
                Icon(Icons.shopping_bag, size: 48, color: Colors.indigo),
                SizedBox(height: 8),
                Text('Ürün Adı', style: TextStyle(fontSize: 18)),
              ],
            ),
          ),
        );
      }
    }
    ```

Nasıl çalışır:
    1. Widget kodunu analiz et (ifade / sınıf / tam uygulama)
    2. tools/flutter_screenshot_runner/test/screenshot_test.dart'a yaz
    3. flutter test --update-goldens çalıştır (headless, Dart VM)
    4. Üretilen golden PNG'yi assets/ klasörüne kopyala
    5. Test dosyasını placeholder'a geri döndür

Hız: ~3-8 saniye/widget (ilk çalıştırma: flutter pub get ~20s)
Windows: flutter.bat kullanılır, sorunsuz çalışır
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

from bookmaker.production.screenshot_strategies.base import (
    ScreenshotConfig,
    ScreenshotResult,
    ScreenshotStrategy,
)
from bookmaker.production.screenshot_strategies.flutter_utils import (
    build_golden_test,
    check_flutter,
    find_runner_dir,
    flutter_cmd,
)

logger = logging.getLogger(__name__)

_TEST_FILE_REL = Path("test") / "screenshot_test.dart"
_GOLDEN_REL = Path("test") / "goldens" / "screenshot.png"

_PLACEHOLDER = (
    "// bookMaker placeholder — bu dosya otomatik olarak yönetilir\n"
    "void main() {}\n"
)


class FlutterGoldenStrategy(ScreenshotStrategy):
    """
    Flutter Widget → headless golden test → PNG.

    Emülatör gerektirmez. flutter test Dart VM üzerinde çalışır.
    Windows'ta flutter.bat ile sorunsuz çalışır.
    """

    def __init__(
        self,
        config: ScreenshotConfig,
        runner_dir: Path | None = None,
    ) -> None:
        super().__init__(config)
        self._runner_dir = runner_dir
        self._flutter_version: str | None | bool = None  # None=kontrol edilmedi

    @property
    def hint(self) -> str:
        return "screenshot"

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
        code: str,
        output_path: Path,
        index: int,
    ) -> ScreenshotResult:
        flutter_ver = self._get_flutter_version()
        if flutter_ver is None:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error=(
                    "Flutter SDK bulunamadı. PATH'e flutter ekleyin ya da "
                    "https://flutter.dev/docs/get-started/install adresinden kurun."
                ),
            )

        logger.debug(f"Flutter golden render başlıyor [{flutter_ver}]")
        test_path = self.runner_dir / _TEST_FILE_REL
        golden_path = self.runner_dir / _GOLDEN_REL

        try:
            # 1. Test dosyasını yaz
            test_code = build_golden_test(code)
            test_path.write_text(test_code, encoding="utf-8")

            # 2. Goldens klasörünü oluştur
            golden_path.parent.mkdir(parents=True, exist_ok=True)

            # 3. flutter test --update-goldens
            self._run_test()

            # 4. PNG kontrolü
            if not golden_path.exists():
                return ScreenshotResult(
                    index=index, hint=self.hint, output_path=output_path,
                    error="flutter test başarılı çıktı ama golden PNG oluşturulmadı.",
                )

            # 5. output_path'e kopyala
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(golden_path, output_path)
            logger.info(f"Flutter golden screenshot kaydedildi: {output_path.name}")

            return ScreenshotResult(
                index=index,
                hint=self.hint,
                output_path=output_path,
                caption=f"Widget görünümü {index}",
            )

        except subprocess.TimeoutExpired:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error=f"flutter test zaman aşımı ({self.config.python_timeout * 4}s).",
            )
        except RuntimeError as e:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error=str(e)[:300],
            )
        except Exception as e:
            return ScreenshotResult(
                index=index, hint=self.hint, output_path=output_path,
                error=f"Beklenmeyen hata: {e!s:.200}",
            )
        finally:
            # Test dosyasını her zaman placeholder'a geri döndür
            if test_path.exists():
                test_path.write_text(_PLACEHOLDER, encoding="utf-8")

    # ------------------------------------------------------------------
    # İç yardımcılar
    # ------------------------------------------------------------------

    def _run_test(self) -> None:
        cmd = [
            flutter_cmd(),
            "test",
            str(_TEST_FILE_REL),
            "--update-goldens",
            "--reporter=compact",
        ]
        result = subprocess.run(
            cmd,
            cwd=str(self.runner_dir),
            capture_output=True,
            text=True,
            timeout=self.config.python_timeout * 4,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            details = (result.stderr or result.stdout or "").strip()[:400]
            raise RuntimeError(f"flutter test başarısız:\n{details}")

    def _get_flutter_version(self) -> str | None:
        """Flutter SDK varlığını kontrol eder; sonucu önbelleğe alır."""
        if self._flutter_version is None:
            self._flutter_version = check_flutter()
        return self._flutter_version  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Sınıf yardımcısı
    # ------------------------------------------------------------------

    @classmethod
    def setup_runner(cls, project_root: Path) -> None:
        """
        Runner projesinde flutter pub get çalıştırır.
        İlk kurulumda veya pubspec.yaml değiştiğinde çağrılır.
        """
        runner = project_root / "tools" / "flutter_screenshot_runner"
        if not (runner / "pubspec.yaml").exists():
            raise FileNotFoundError(
                f"Runner projesi bulunamadı: {runner}\n"
                "tools/flutter_screenshot_runner/pubspec.yaml eksik."
            )
        logger.info("flutter pub get çalıştırılıyor...")
        result = subprocess.run(
            [flutter_cmd(), "pub", "get"],
            cwd=str(runner),
            capture_output=True,
            text=True,
            timeout=120,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"flutter pub get başarısız:\n{result.stderr[:300]}"
            )
        logger.info("Flutter runner kurulumu tamamlandı.")
