"""Manifest okuma/yazma/doğrulama yöneticisi."""

from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML

from bookmaker.manifest.models import BookManifest

_yaml = YAML()


class ManifestManager:
    def __init__(self, project_root: Path) -> None:
        self.root = project_root.resolve()

    def manifest_path(self) -> Path:
        return self.root / "book_manifest.yaml"

    def exists(self) -> bool:
        return self.manifest_path().exists()

    def load(self) -> BookManifest:
        if not self.exists():
            return BookManifest()
        return BookManifest.load(self.manifest_path())

    def save(self, manifest: BookManifest) -> Path:
        p = self.manifest_path()
        manifest.save(p)
        return p

    def load_or_generate(self) -> BookManifest:
        """Manifest varsa yukle, yoksa bos BookManifest doner."""
        if self.exists():
            return self.load()
        return BookManifest()

    def validate(self) -> list[str]:
        """Manifest doğrulama — sorun listesi döndürür."""
        issues: list[str] = []
        if not self.exists():
            issues.append("book_manifest.yaml bulunamadi.")
            return issues

        manifest = self.load()
        if not manifest.book.title:
            issues.append("book.title bos.")
        if not manifest.chapters:
            issues.append("Hic bolum tanimli degil.")
        else:
            seen = set()
            orders = []
            for ch in manifest.chapters:
                if ch.chapter_id in seen:
                    issues.append(f"Yinelenen chapter_id: {ch.chapter_id}")
                seen.add(ch.chapter_id)
                if ch.order in orders:
                    issues.append(f"Yinelenen order: {ch.order}")
                orders.append(ch.order)
        return issues
