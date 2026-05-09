"""bookmaker.production.screenshot_engine
=======================================
Markdown içindeki işaretlenmiş kod bloklarını ekran görüntüsüne dönüştürür.

Fence sözdizimi (LLM'e SEED prompt'unda öğretilmeli):
    ```python plot      → matplotlib/plotly grafiği
    ```python console   → stdout terminal çıktısı
    ```jsx screenshot   → React bileşeni
    ```tsx screenshot   → React bileşeni (TypeScript)

Pipeline entegrasyonu — ASSEMBLE sonrasında çağrılır:
    engine = ScreenshotEngine.from_manifest(manifest)
    result = engine.process_markdown(
        md_content=draft_md,
        assets_dir=chapter_dir / "assets",
        chapter_alias="bolum-03",
    )
    updated_md = result.output_md
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from bookmaker.production.screenshot_strategies import (
    FlutterGoldenStrategy,
    FlutterWebStrategy,
    PythonConsoleStrategy,
    PythonPlotStrategy,
    ReactComponentStrategy,
    ScreenshotConfig,
    ScreenshotResult,
)
from bookmaker.production.screenshot_strategies.base import ScreenshotStrategy

logger = logging.getLogger(__name__)

# İşaretlenmiş kod bloklarını yakalayan regex
# Grup 1: dil etiketi (python, jsx, tsx, react)
# Grup 2: hint (plot, console, screenshot)
# Grup 3: kod içeriği
_TAGGED_BLOCK_RE = re.compile(
    r"```(python|jsx|tsx|javascript|react|dart)\s+(plot|console|screenshot|web-screenshot)\s*\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)

_CACHE_FILE = ".screenshot_cache.json"

# Dil etiketi → strateji hint eşlemesi
_LANG_HINT_TO_STRATEGY: dict[tuple[str, str], str] = {
    ("dart", "screenshot"): "flutter_golden",
    ("dart", "web-screenshot"): "flutter_web",
    ("javascript", "screenshot"): "screenshot",
    ("jsx", "screenshot"): "screenshot",
    ("python", "console"): "console",
    ("python", "plot"): "plot",
    ("react", "screenshot"): "screenshot",
    ("tsx", "screenshot"): "screenshot",
}


@dataclass
class ScreenshotProcessResult:
    """Bir Markdown dosyasının tüm screenshot işlemlerinin sonucu."""

    total: int
    rendered: int
    cached: int
    failed: int
    output_md: str
    results: list[ScreenshotResult] = field(default_factory=list)

    def log_summary(self, chapter_alias: str = "") -> None:
        prefix = f"[{chapter_alias}] " if chapter_alias else ""
        logger.info(
            f"{prefix}Screenshot tamamlandı — "
            f"toplam={self.total} çizildi={self.rendered} "
            f"cache={self.cached} hata={self.failed}"
        )
        for r in self.results:
            if not r.success:
                logger.warning(f"  ✗ {r.output_path.name}: {r.error}")


class ScreenshotEngine:
    """Markdown'daki işaretlenmiş kod bloklarını screenshot'a dönüştürür.

    Kullanım:
        engine = ScreenshotEngine(config)
        result = engine.process_markdown(md_content, assets_dir, chapter_alias)
        # result.output_md → güncellenmiş Markdown
    """

    def __init__(
        self,
        config: ScreenshotConfig | None = None,
        runner_dir: Path | None = None,
    ) -> None:
        self.config = config or ScreenshotConfig()
        self._strategies: dict[str, ScreenshotStrategy] = {
            "console": PythonConsoleStrategy(self.config),
            "flutter_golden": FlutterGoldenStrategy(self.config, runner_dir),
            "flutter_web": FlutterWebStrategy(self.config, runner_dir),
            "plot": PythonPlotStrategy(self.config),
            "screenshot": ReactComponentStrategy(self.config),
        }

    @classmethod
    def from_manifest(
        cls,
        manifest_screenshots: dict | None,
        runner_dir: Path | None = None,
    ) -> ScreenshotEngine:
        config = ScreenshotConfig.from_manifest(manifest_screenshots)
        return cls(config, runner_dir=runner_dir)

    # ------------------------------------------------------------------
    # Ana API
    # ------------------------------------------------------------------

    def process_markdown(
        self,
        md_content: str,
        assets_dir: Path,
        chapter_alias: str = "chapter",
    ) -> ScreenshotProcessResult:
        """Markdown içeriğindeki tüm işaretlenmiş kod bloklarını işler.

        Args:
            md_content: draft.md veya final.md içeriği
            assets_dir: PNG'lerin kaydedileceği klasör
            chapter_alias: Dosya adı öneki için bölüm takma adı

        Returns:
            ScreenshotProcessResult — güncellenmiş Markdown + istatistikler

        """
        if not self.config.enabled:
            return ScreenshotProcessResult(
                total=0, rendered=0, cached=0, failed=0, output_md=md_content,
            )

        assets_dir.mkdir(parents=True, exist_ok=True)
        cache = self._load_cache(assets_dir)

        matches = list(_TAGGED_BLOCK_RE.finditer(md_content))
        results: list[ScreenshotResult] = []
        replacements: list[tuple[str, str]] = []

        for i, match in enumerate(matches, start=1):
            lang = match.group(1).lower()
            hint = match.group(2).lower()
            code = match.group(3)
            original_block = match.group(0)

            strategy_key = _LANG_HINT_TO_STRATEGY.get((lang, hint))
            if not strategy_key or strategy_key not in self._strategies:
                logger.debug(f"Strateji bulunamadı: lang={lang} hint={hint} — atlanıyor")
                continue

            strategy = self._strategies[strategy_key]
            cache_key = strategy.cache_key(code, hint)
            fig_name = f"ss_{chapter_alias}_{i:02d}_{hint}.png"
            fig_path = assets_dir / fig_name

            # Cache kontrolü
            if cache.get(cache_key) == fig_name and fig_path.exists():
                logger.debug(f"Cache hit: {fig_name}")
                result = ScreenshotResult(
                    index=i, hint=hint, output_path=fig_path, was_cached=True,
                )
                results.append(result)
                replacement = self._md_block(
                    lang, code, fig_name, i, result.caption or f"Çıktı {i}"
                )
                replacements.append((original_block, replacement))
                continue

            # Render
            logger.info(f"Screenshot alınıyor: {fig_name} (strateji={strategy_key})")
            result = strategy.capture(code, fig_path, i)
            results.append(result)

            if result.success:
                cache[cache_key] = fig_name
                replacement = self._md_block(
                    lang, code, fig_name, i, result.caption or f"Çıktı {i}"
                )
            else:
                # Başarısız → orijinal bloğu yorum ekleyerek koru
                replacement = (
                    f"<!-- SCREENSHOT HATASI ({fig_name}): {result.error} -->\n\n"
                    f"```{lang}\n{code}```"
                )
            replacements.append((original_block, replacement))

        # Markdown'ı güncelle
        updated_md = md_content
        for original, replacement in replacements:
            updated_md = updated_md.replace(original, replacement, 1)

        self._save_cache(assets_dir, cache)

        process_result = ScreenshotProcessResult(
            total=len(matches),
            rendered=sum(1 for r in results if r.success and not r.was_cached),
            cached=sum(1 for r in results if r.was_cached),
            failed=sum(1 for r in results if not r.success),
            output_md=updated_md,
            results=results,
        )
        process_result.log_summary(chapter_alias)
        return process_result

    # ------------------------------------------------------------------
    # Yardımcılar
    # ------------------------------------------------------------------

    @staticmethod
    def _md_block(lang: str, code: str, fig_name: str, index: int, caption: str) -> str:
        """Kod bloğu + screenshot referansı içeren Markdown döner."""
        return (
            f"```{lang}\n{code}```\n\n"
            f"![{caption}](assets/{fig_name})\n"
        )

    @staticmethod
    def _load_cache(assets_dir: Path) -> dict[str, str]:
        p = assets_dir / _CACHE_FILE
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    @staticmethod
    def _save_cache(assets_dir: Path, cache: dict[str, str]) -> None:
        p = assets_dir / _CACHE_FILE
        p.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
