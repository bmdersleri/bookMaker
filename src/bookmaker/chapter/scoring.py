from __future__ import annotations

from bookmaker.core.ids import new_issue_id
from bookmaker.models.quality import Issue, QualityReport


def make_report(
    chapter_id: str,
    issues: list[Issue],
    report_id: str | None = None,
    artifact_version: str = "draft",
) -> QualityReport:
    """Issue listesinden skorlanmış bir QualityReport üretir."""
    report = QualityReport(
        report_id=report_id or new_issue_id(),
        artifact_type="chapter",
        artifact_version=artifact_version,
        chapter_id=chapter_id,
        issues=issues,
    )
    report.compute_score()
    return report
