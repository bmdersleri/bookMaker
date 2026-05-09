from bookmaker.core.ids import new_issue_id
from bookmaker.models.quality import (
    Decision,
    GateResult,
    Issue,
    IssueLocation,
    IssueStatus,
    QualityReport,
    Severity,
)


def make_issue(severity: Severity, category: str = "test") -> Issue:
    return Issue(
        issue_id=new_issue_id(),
        severity=severity,
        category=category,
        message="test issue",
    )


def test_score_no_issues():
    report = QualityReport(
        report_id="r001",
        artifact_type="draft",
        artifact_version="v001",
        issues=[],
    )
    score = report.compute_score()
    assert score == 100
    assert report.decision == Decision.passed


def test_score_one_error():
    report = QualityReport(
        report_id="r002",
        artifact_type="draft",
        artifact_version="v001",
        issues=[make_issue(Severity.error)],
    )
    score = report.compute_score()
    assert score == 85
    assert report.decision == Decision.revision_required
    assert report.error_count == 1


def test_score_many_errors_blocked():
    issues = [make_issue(Severity.error) for _ in range(5)]
    report = QualityReport(
        report_id="r003",
        artifact_type="draft",
        artifact_version="v001",
        issues=issues,
    )
    score = report.compute_score()
    assert score == 25
    assert report.decision == Decision.blocked


def test_score_only_warnings():
    issues = [make_issue(Severity.warning) for _ in range(3)]
    report = QualityReport(
        report_id="r004",
        artifact_type="draft",
        artifact_version="v001",
        issues=issues,
    )
    score = report.compute_score()
    assert score == 91
    assert report.decision == Decision.passed


def test_score_minimum_zero():
    issues = [make_issue(Severity.error) for _ in range(10)]
    report = QualityReport(
        report_id="r005",
        artifact_type="draft",
        artifact_version="v001",
        issues=issues,
    )
    score = report.compute_score()
    assert score == 0


def test_issue_triage_statuses():
    issue = make_issue(Severity.warning)
    assert issue.status == IssueStatus.open
    issue.status = IssueStatus.accepted
    assert issue.status == IssueStatus.accepted


def test_gate_result():
    gate = GateResult(
        gate_id="outline_quality",
        passed=False,
        score=72,
        decision=Decision.revision_required,
        blocking_issues=["iss_abc123"],
        message="Zorunlu kavramlar eksik",
    )
    assert not gate.passed
    assert gate.score == 72


def test_issue_location():
    issue = Issue(
        issue_id="iss_001",
        severity=Severity.error,
        category="code_meta",
        location=IssueLocation(file="chapter_03/draft_v001.md", line=142),
        message="CODE_META eksik",
    )
    assert issue.location.line == 142
