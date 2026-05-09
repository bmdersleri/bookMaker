"""Kalite degerlendirme modelleri — QualityReport, Score, vb."""
from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field
from ruamel.yaml import YAML

_yaml = YAML()
_yaml.preserve_quotes = True


class Severity(StrEnum):
    """Sorun siddet seviyesi (error, warning, info)."""

    error = "error"
    warning = "warning"
    info = "info"


class Decision(StrEnum):
    """Kalite karari (pass, pass_with_warnings, revision_required, blocked)."""

    passed = "pass"
    passed_with_warnings = "pass_with_warnings"
    revision_required = "revision_required"
    blocked = "blocked"


class IssueStatus(StrEnum):
    """Sorun durumu (open, fix_now, fix_later, accepted, resolved)."""

    open = "open"
    fix_now = "fix_now"      # 🔴 triyaj
    fix_later = "fix_later"  # 🟡 triyaj
    accepted = "accepted"    # ⚪ triyaj — override event yazar
    resolved = "resolved"


class IssueLocation(BaseModel):
    """Sorunun dosya, satir ve bolum konumu."""

    file: str = ""
    line: int | None = None
    section: str = ""


class Issue(BaseModel):
    """Bir kalite sorununu tum detaylariyla tanimlar."""

    issue_id: str
    severity: Severity
    category: str
    location: IssueLocation = Field(default_factory=IssueLocation)
    message: str
    expected: str = ""
    current: str = ""
    instruction: str = ""
    acceptance_criteria: list[str] = Field(default_factory=list)
    llm_repair_hint: str = ""
    status: IssueStatus = IssueStatus.open


class CheckResult(BaseModel):
    """Bir kontrolun sonucu (pass/fail/warning/skip)."""

    check_id: str
    status: str  # "pass" | "fail" | "warning" | "skip"
    message: str = ""


class QualityReport(BaseModel):
    """Kalite raporu — skor, karar, sorunlar ve kontroller."""

    report_id: str
    artifact_type: str
    artifact_version: str
    chapter_id: str = ""
    score: int = 0
    decision: Decision = Decision.blocked
    error_count: int = 0
    warning_count: int = 0
    issues: list[Issue] = Field(default_factory=list)
    checks: list[CheckResult] = Field(default_factory=list)

    def compute_score(self) -> int:
        """Hata ve uyarı sayısına göre skoru hesaplar."""
        errors = sum(1 for i in self.issues if i.severity == Severity.error)
        warnings = sum(1 for i in self.issues if i.severity == Severity.warning)
        score = max(0, 100 - errors * 15 - warnings * 3)
        self.score = score
        self.error_count = errors
        self.warning_count = warnings
        self.decision = self._decide(score, errors)
        return score

    @staticmethod
    def _decide(score: int, errors: int) -> Decision:
        if errors > 0 and score < 65:
            return Decision.blocked
        if errors > 0:
            return Decision.revision_required
        if score >= 90:
            return Decision.passed
        if score >= 80:
            return Decision.passed_with_warnings
        return Decision.revision_required

    def to_yaml(self, path: Path) -> None:
        """Raporu YAML dosyasina yazar."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(self.model_dump(mode="json"), f)


class GateResult(BaseModel):
    """Gecit sonucu — gecis karari ve engelleyen sorunlar."""

    gate_id: str
    passed: bool
    score: int
    decision: Decision
    blocking_issues: list[str] = Field(default_factory=list)  # issue_id listesi
    message: str = ""
