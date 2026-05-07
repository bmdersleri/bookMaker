"""
bookmaker.production.mermaid_theme
===================================
Kitap profiline göre Mermaid tema seçimi ve mmdc konfigürasyon yönetimi.

Her kitap profili (flutter, java, python, react, generic) için ayrı
bir JSON tema dosyası bulunur. Tema, mmdc'ye --configFile argümanıyla
geçilen geçici bir JSON dosyasına yazılır.

Kullanım:
    theme = MermaidThemeManager.for_profile("flutter")
    with theme.config_file() as cfg_path:
        subprocess.run(["mmdc", "-i", src, "-o", out, "--configFile", cfg_path])
"""

from __future__ import annotations

import contextlib
import json
import logging
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

# Tema dosyalarının bulunduğu dizin (bu modülle aynı pakette)
_THEMES_DIR = Path(__file__).parent / "themes"

# Profil adından tema dosyasına eşleme
# bookMaker profil isimleri: flutter, java, python, react, generic
_PROFILE_MAP: dict[str, str] = {
    "flutter": "flutter",
    "dart": "flutter",
    "java": "java",
    "python": "python",
    "react": "react",
    "javascript": "react",
    "typescript": "react",
    "generic": "default",
    "default": "default",
}


@dataclass
class MermaidTheme:
    """
    Tek bir Mermaid tema konfigürasyonu.

    Attributes:
        name: Tema adı (dosya adıyla aynı, uzantısız)
        config: mmdc'ye geçilecek tam JSON nesnesi
    """

    name: str
    config: dict = field(default_factory=dict)

    @classmethod
    def load(cls, theme_name: str) -> MermaidTheme:
        """
        Tema dosyasını yükler. Bulunamazsa 'default' temaya düşer.

        Args:
            theme_name: Tema dosyasının adı (uzantısız, örn. 'flutter')
        """
        theme_path = _THEMES_DIR / f"{theme_name}.json"

        if not theme_path.exists():
            logger.warning(
                f"Tema bulunamadı: {theme_path}. 'default' kullanılıyor."
            )
            theme_path = _THEMES_DIR / "default.json"

        if not theme_path.exists():
            logger.error("default.json da bulunamadı — boş tema kullanılıyor.")
            return cls(name="empty", config={})

        config = json.loads(theme_path.read_text(encoding="utf-8"))
        logger.debug(f"Mermaid teması yüklendi: {theme_path.name}")
        return cls(name=theme_path.stem, config=config)

    def merge(self, overrides: dict) -> MermaidTheme:
        """
        Mevcut temaya kullanıcı override'larını uygular.
        book_manifest.yaml'dan gelen özel ayarlar için kullanılır.

        Args:
            overrides: {"themeVariables": {...}} formatında ek ayarlar
        """
        import copy

        merged = copy.deepcopy(self.config)
        for key, value in overrides.items():
            if key == "themeVariables" and isinstance(value, dict):
                merged.setdefault("themeVariables", {}).update(value)
            else:
                merged[key] = value
        return MermaidTheme(name=f"{self.name}+override", config=merged)

    @contextlib.contextmanager
    def config_file(self) -> Iterator[Path]:
        """
        Geçici bir JSON konfigürasyon dosyası oluşturur ve path'ini yield eder.
        Context manager bitince dosya silinir.

        Kullanım:
            with theme.config_file() as cfg_path:
                subprocess.run(["mmdc", "--configFile", str(cfg_path)])
        """
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            encoding="utf-8",
        ) as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
            tmp_path = Path(f.name)

        try:
            yield tmp_path
        finally:
            tmp_path.unlink(missing_ok=True)


class MermaidThemeManager:
    """
    Profil adından tema yükleyen statik yardımcı.
    """

    @staticmethod
    def for_profile(
        profile: str,
        overrides: dict | None = None,
    ) -> MermaidTheme:
        """
        Kitap profiline uygun temayı döner.

        Args:
            profile: Kitap profili ('flutter', 'java', 'python', 'react', 'generic')
            overrides: book_manifest.yaml'dan gelen ek themeVariables

        Returns:
            Uygulanmaya hazır MermaidTheme nesnesi
        """
        theme_name = _PROFILE_MAP.get(profile.lower(), "default")
        theme = MermaidTheme.load(theme_name)

        if overrides:
            theme = theme.merge(overrides)
            logger.debug(f"Tema override'ları uygulandı: {list(overrides.keys())}")

        return theme

    @staticmethod
    def available_themes() -> list[str]:
        """Mevcut tema dosyalarının listesini döner."""
        return [p.stem for p in sorted(_THEMES_DIR.glob("*.json"))]

    @staticmethod
    def profile_to_theme(profile: str) -> str:
        """Profil adını tema adına çevirir (hata ayıklama için)."""
        return _PROFILE_MAP.get(profile.lower(), "default")
