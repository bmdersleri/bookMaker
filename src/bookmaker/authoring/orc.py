"""Outline Review Command (ORC) — outline kalite kontrolü."""

from __future__ import annotations

from pathlib import Path

from bookmaker.authoring.pipeline import AuthoringPipeline


class ORC:
    """Outline Review Command — outline kalite kontrolü ve raporlama."""

    def __init__(self, project_root: Path) -> None:
        self.pipe = AuthoringPipeline(project_root)

    def check(self, chapter_id: str, outline_version: str = "v001") -> dict:
        """Outline kontrolü yap ve rapor döndür."""
        return self.pipe.review_outline(chapter_id, outline_version)

    def format_report(self, result: dict) -> str:
        """ORC sonucunu okunabilir metne çevir."""
        lines = ["ORC Raporu", f"Karar: {result.get('decision', '?')}", ""]
        issues = result.get("issues", [])
        if issues:
            lines.append(f"Sorunlar ({len(issues)}):")
            for i, iss in enumerate(issues, 1):
                lines.append(f"  {i}. {iss}")
        else:
            lines.append("Sorun yok.")
        return "\n".join(lines)
