"""Kitap projesi exchange/transfer modelleri."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RevisionIssue(BaseModel):
    """Revizyon gerektiren bir sorunu tanimlar."""

    issue_id: str
    severity: str
    location: str = ""
    expected: str = ""
    current: str = ""
    instruction: str = ""
    acceptance_criteria: list[str] = Field(default_factory=list)


class RevisionPacket(BaseModel):
    """Bir revizyon gorevi icin sorun ve kisitlama paketi."""

    packet_id: str
    target_artifact: str
    artifact_version: str
    chapter_id: str
    objective: str
    preserve: list[str] = Field(default_factory=list)
    issues: list[RevisionIssue] = Field(default_factory=list)
    constraints: list[str] = Field(
        default_factory=lambda: [
            "Tam bolumu yeniden yazma.",
            "preserve listesindeki hicbir blogu degistirme.",
            "CHAPTER_SPEC kurallarini koru.",
            "Kapsam disi konulari ekleme.",
        ]
    )

    def to_prompt(self) -> str:
        """LLM'e kopyalanabilir revizyon promptu üretir."""
        lines = [
            f"# Revizyon Gorevi: {self.objective}",
            "",
            "## Degistirilmemesi Gerekenler",
        ]
        for p in self.preserve:
            lines.append(f"- {p}")
        lines += ["", "## Duzeltilmesi Gereken Sorunlar"]
        for i, issue in enumerate(self.issues, 1):
            lines.append(f"\n### Sorun {i}: {issue.issue_id}")
            if issue.location:
                lines.append(f"- Konum: {issue.location}")
            if issue.current:
                lines.append(f"- Mevcut: {issue.current}")
            if issue.expected:
                lines.append(f"- Beklenen: {issue.expected}")
            lines.append(f"- Talimat: {issue.instruction}")
        lines += ["", "## Kisitlamalar"]
        for c in self.constraints:
            lines.append(f"- {c}")
        return "\n".join(lines)
