"""
bookmaker.production.mermaid_renderer
=======================================
Mermaid kod bloklarını temalı PNG'ye dönüştürür ve Markdown referanslarını günceller.

Pipeline entegrasyonu:
    NORMALIZE aşamasının sonunda `MermaidRenderer.process_markdown()` çağrılır.
    draft.md içindeki her ```mermaid bloğu:
      1. Hash hesaplanır → assets/ klasöründe PNG varsa skip edilir
      2. Profil teması uygulanır
      3. mmdc ile PNG render edilir
      4. Markdown'da blok → ![Şekil N](assets/fig_XX.png) ile değiştirilir

Idempotency:
    Her mermaid bloğunun MD5'i ve tema adı birleştirilerek cache key oluşturulur.
    PNG varsa ve kaynak değişmediyse yeniden render edilmez.
    assets/.mermaid_cache.json dosyasında hash→filename eşlemesi tutulur.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from bookmaker.production.mermaid_theme import MermaidTheme, MermaidThemeManager

logger = logging.getLogger(__name__)

# Markdown'daki mermaid bloklarını yakalayan regex
_MERMAID_BLOCK_RE = re.compile(
    r"```mermaid\s*\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)

_CACHE_FILE = ".mermaid_cache.json"


# ---------------------------------------------------------------------------
# Konfigürasyon
# ---------------------------------------------------------------------------

@dataclass
class MermaidRenderConfig:
    """
    Tek bir render operasyonunun ayarları.
    book_manifest.yaml → production.mermaid bölümünden yüklenir.

    Örnek manifest:
        production:
          mermaid:
            theme: flutter
            scale: 2
            background: white
            width: 900
            theme_overrides:
              themeVariables:
                fontSize: "16px"
    """

    theme: str = "default"
    scale: int = 2               # Retina (2x) için 2 önerilir
    background: str = "white"    # "white" veya "transparent"
    width: int = 900             # px cinsinden diyagram genişliği
    theme_overrides: dict = field(default_factory=dict)
    timeout_seconds: int = 30

    def cache_fingerprint(self) -> str:
        """Render çıktısını etkileyen tüm ayarların deterministik özeti.

        Cache key üretiminde kullanılır. width, scale, background, theme
        veya theme_overrides değiştiğinde fingerprint de değişir → cache
        invalidate olur.
        """
        payload = {
            "theme": self.theme,
            "scale": self.scale,
            "background": self.background,
            "width": self.width,
            "theme_overrides": self.theme_overrides,
        }
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_manifest(cls, manifest_mermaid: dict | None) -> MermaidRenderConfig:
        """book_manifest.yaml'ın production.mermaid bölümünden yükler."""
        if not manifest_mermaid:
            return cls()
        return cls(
            theme=manifest_mermaid.get("theme", "default"),
            scale=manifest_mermaid.get("scale", 2),
            background=manifest_mermaid.get("background", "white"),
            width=manifest_mermaid.get("width", 900),
            theme_overrides=manifest_mermaid.get("theme_overrides", {}),
            timeout_seconds=manifest_mermaid.get("timeout_seconds", 30),
        )

    def resolve_theme(self) -> MermaidTheme:
        """Profil adından MermaidTheme nesnesi üretir."""
        return MermaidThemeManager.for_profile(
            self.theme,
            overrides=self.theme_overrides or None,
        )


# ---------------------------------------------------------------------------
# Render sonucu
# ---------------------------------------------------------------------------

@dataclass
class RenderResult:
    """Tek bir mermaid bloğunun render sonucu."""

    index: int
    source_hash: str
    output_path: Path
    was_cached: bool = False
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None


@dataclass
class ProcessResult:
    """Bir Markdown dosyasının tüm mermaid bloklarının işlem sonucu."""

    total: int
    rendered: int
    cached: int
    failed: int
    output_md: str           # Güncellenmiş Markdown içeriği
    results: list[RenderResult] = field(default_factory=list)

    def log_summary(self, chapter_alias: str = "") -> None:
        prefix = f"[{chapter_alias}] " if chapter_alias else ""
        logger.info(
            f"{prefix}Mermaid render tamamlandı — "
            f"toplam={self.total} render={self.rendered} "
            f"cache={self.cached} hata={self.failed}"
        )
        for r in self.results:
            if not r.success:
                logger.warning(f"  ✗ fig_{r.index:02d}: {r.error}")


# ---------------------------------------------------------------------------
# Ana renderer
# ---------------------------------------------------------------------------

class MermaidRenderer:
    """
    Markdown içindeki mermaid bloklarını temalı PNG'ye dönüştürür.

    Kullanım (NORMALIZE sonrasında):
        config = MermaidRenderConfig.from_manifest(manifest.production.mermaid)
        renderer = MermaidRenderer(config)
        result = renderer.process_markdown(
            md_content=draft_md,
            assets_dir=chapter_dir / "assets",
            chapter_alias="bolum-03",
        )
        # result.output_md → PNG referansları eklenmiş Markdown
        # result.rendered, result.cached → istatistikler

    Gereksinim:
        mmdc komut satırı aracının PATH'de kurulu olması gerekir.
        Kurulum: npm install -g @mermaid-js/mermaid-cli
    """

    def __init__(self, config: MermaidRenderConfig | None = None) -> None:
        self.config = config or MermaidRenderConfig()
        self._check_mmdc()

    # -----------------------------------------------------------------------
    # Genel API
    # -----------------------------------------------------------------------

    def process_markdown(
        self,
        md_content: str,
        assets_dir: Path,
        chapter_alias: str = "chapter",
    ) -> ProcessResult:
        """
        Markdown içeriğindeki tüm ```mermaid bloklarını işler.

        Args:
            md_content: draft.md veya normalized.md içeriği
            assets_dir: PNG'lerin kaydedileceği klasör (chapter/assets/)
            chapter_alias: Dosya adı öneki için bölüm takma adı

        Returns:
            ProcessResult — güncellenmiş Markdown + istatistikler
        """
        assets_dir.mkdir(parents=True, exist_ok=True)
        cache = self._load_cache(assets_dir)
        theme = self.config.resolve_theme()

        blocks = _MERMAID_BLOCK_RE.findall(md_content)
        results: list[RenderResult] = []
        replacements: list[tuple[str, str]] = []  # (original_block, replacement_md)

        for i, mermaid_src in enumerate(blocks, start=1):
            original_block = f"```mermaid\n{mermaid_src}```"
            cache_key = self._cache_key(mermaid_src, self.config.cache_fingerprint())
            fig_name = f"fig_{chapter_alias}_{i:02d}.png"
            fig_path = assets_dir / fig_name

            # Cache kontrolü
            if cache.get(cache_key) == fig_name and fig_path.exists():
                logger.debug(f"Cache hit: {fig_name}")
                result = RenderResult(
                    index=i,
                    source_hash=cache_key,
                    output_path=fig_path,
                    was_cached=True,
                )
                results.append(result)
                md_ref = self._md_reference(fig_name, i)
                replacements.append((original_block, md_ref))
                continue

            # Render
            result = self._render_single(
                mermaid_src=mermaid_src,
                output_path=fig_path,
                theme=theme,
                index=i,
                cache_key=cache_key,
            )
            results.append(result)

            if result.success:
                cache[cache_key] = fig_name
                md_ref = self._md_reference(fig_name, i)
            else:
                # Render başarısız → bloğu bir uyarı yorumuyla bırak
                md_ref = (
                    f"<!-- MERMAID RENDER HATASI (fig_{i:02d}): "
                    f"{result.error} -->\n\n"
                    f"```mermaid\n{mermaid_src}```"
                )
            replacements.append((original_block, md_ref))

        # Markdown'ı güncelle (tüm blokları aynı anda değiştir)
        updated_md = md_content
        for original, replacement in replacements:
            updated_md = updated_md.replace(original, replacement, 1)

        self._save_cache(assets_dir, cache)

        process_result = ProcessResult(
            total=len(blocks),
            rendered=sum(1 for r in results if r.success and not r.was_cached),
            cached=sum(1 for r in results if r.was_cached),
            failed=sum(1 for r in results if not r.success),
            output_md=updated_md,
            results=results,
        )
        process_result.log_summary(chapter_alias)
        return process_result

    def render_string(
        self,
        mermaid_src: str,
        output_path: Path,
    ) -> RenderResult:
        """
        Tek bir mermaid kaynak stringini PNG'ye render eder.
        Birim testleri ve doğrudan kullanım için.
        """
        theme = self.config.resolve_theme()
        cache_key = self._cache_key(mermaid_src, self.config.cache_fingerprint())
        return self._render_single(
            mermaid_src=mermaid_src,
            output_path=output_path,
            theme=theme,
            index=1,
            cache_key=cache_key,
        )

    # -----------------------------------------------------------------------
    # mmdc çağrısı
    # -----------------------------------------------------------------------

    def _render_single(
        self,
        mermaid_src: str,
        output_path: Path,
        theme: MermaidTheme,
        index: int,
        cache_key: str,
    ) -> RenderResult:
        """Tek bir mermaid bloğunu mmdc ile PNG'ye render eder."""
        src_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".mmd", delete=False, encoding="utf-8"
            ) as f:
                f.write(mermaid_src.strip())
                src_path = Path(f.name)

            with theme.config_file() as cfg_path:
                cmd = self._build_cmd(src_path, output_path, cfg_path)
                logger.debug(f"mmdc çalıştırılıyor: {' '.join(cmd)}")

                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.config.timeout_seconds,
                )

            if proc.returncode != 0:
                err = (proc.stderr or proc.stdout or "bilinmeyen hata").strip()
                logger.warning(f"mmdc hata döndürdü (fig_{index:02d}): {err[:200]}")
                return RenderResult(
                    index=index,
                    source_hash=cache_key,
                    output_path=output_path,
                    error=err[:200],
                )

            if not output_path.exists():
                return RenderResult(
                    index=index,
                    source_hash=cache_key,
                    output_path=output_path,
                    error="mmdc başarılı çıktı verdi ama PNG oluşturulmadı.",
                )

            logger.info(f"Mermaid PNG oluşturuldu: {output_path.name}")
            return RenderResult(
                index=index,
                source_hash=cache_key,
                output_path=output_path,
            )

        except subprocess.TimeoutExpired:
            return RenderResult(
                index=index,
                source_hash=cache_key,
                output_path=output_path,
                error=f"mmdc {self.config.timeout_seconds} saniye içinde tamamlanamadı (timeout).",
            )
        except Exception as e:
            return RenderResult(
                index=index,
                source_hash=cache_key,
                output_path=output_path,
                error=str(e),
            )
        finally:
            if src_path is not None:
                src_path.unlink(missing_ok=True)

    def _build_cmd(
        self,
        src: Path,
        out: Path,
        cfg: Path,
    ) -> list[str]:
        """mmdc komut satırını oluşturur."""
        return [
            "mmdc",
            "--input", str(src),
            "--output", str(out),
            "--configFile", str(cfg),
            "--scale", str(self.config.scale),
            "--backgroundColor", self.config.background,
            "--width", str(self.config.width),
            "--quiet",
        ]

    # -----------------------------------------------------------------------
    # Cache yönetimi
    # -----------------------------------------------------------------------

    @staticmethod
    def _cache_key(mermaid_src: str, config_fingerprint: str) -> str:
        """Mermaid kaynak + render konfigürasyon özetinden benzersiz hash üretir."""
        payload = f"{config_fingerprint}::{mermaid_src.strip()}"
        return hashlib.md5(payload.encode("utf-8")).hexdigest()

    @staticmethod
    def _load_cache(assets_dir: Path) -> dict[str, str]:
        cache_path = assets_dir / _CACHE_FILE
        if cache_path.exists():
            try:
                return json.loads(cache_path.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    @staticmethod
    def _save_cache(assets_dir: Path, cache: dict[str, str]) -> None:
        cache_path = assets_dir / _CACHE_FILE
        cache_path.write_text(
            json.dumps(cache, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # -----------------------------------------------------------------------
    # Yardımcılar
    # -----------------------------------------------------------------------

    @staticmethod
    def _md_reference(fig_name: str, index: int) -> str:
        """Pandoc uyumlu Markdown resim referansı oluşturur."""
        return f"![Şekil {index}](assets/{fig_name})\n"

    @staticmethod
    def _check_mmdc() -> None:
        """mmdc kurulu değilse uyarı log'lar (exception fırlatmaz)."""
        if shutil.which("mmdc") is None:
            logger.warning(
                "mmdc bulunamadı. Mermaid render devre dışı olacak.\n"
                "Kurulum: npm install -g @mermaid-js/mermaid-cli"
            )
