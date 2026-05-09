"""Scoring birim testleri."""

from bookmaker.chapter.scoring import make_report
from bookmaker.models.quality import Decision, Issue, IssueLocation, Severity


def _make_issue(severity: Severity, category: str, message: str = "Test issue") -> Issue:
    return Issue(
        issue_id=f"test_{category}_{severity.value}",
        severity=severity,
        category=category,
        location=IssueLocation(),
        message=message,
    )


class TestMakeReport:
    def test_empty_issues_gives_full_score(self) -> None:
        report = make_report("test-chapter", [])
        assert report.score == 100
        assert report.decision == Decision.passed
        assert report.error_count == 0
        assert report.warning_count == 0
        assert report.chapter_id == "test-chapter"

    def test_one_error_reduces_score(self) -> None:
        issues = [_make_issue(Severity.error, "test")]
        report = make_report("test", issues)
        assert report.score == 85  # 100 - 1*15
        assert report.error_count == 1
        assert report.decision == Decision.revision_required

    def test_many_errors_can_block(self) -> None:
        issues = [_make_issue(Severity.error, "test") for _ in range(4)]
        report = make_report("test", issues)
        assert report.score <= 40  # 100 - 4*15 = 40
        assert report.decision in (Decision.revision_required, Decision.blocked)

    def test_warnings_affect_score_lightly(self) -> None:
        issues = [_make_issue(Severity.warning, "test") for _ in range(3)]
        report = make_report("test", issues)
        assert report.score == 91  # 100 - 3*3
        # 0 errors, score=91 >=90 -> passed
        assert report.decision == Decision.passed

    def test_error_and_warning_combined(self) -> None:
        issues = [
            _make_issue(Severity.error, "err"),
            _make_issue(Severity.warning, "warn"),
        ]
        report = make_report("test", issues)
        assert report.score == 82  # 100 - 1*15 - 1*3
        assert report.error_count == 1
        assert report.warning_count == 1
        assert report.decision == Decision.revision_required

    def test_multiple_severities(self) -> None:
        issues = [
            _make_issue(Severity.error, "err1"),
            _make_issue(Severity.error, "err2"),
            _make_issue(Severity.warning, "warn1"),
            _make_issue(Severity.warning, "warn2"),
            _make_issue(Severity.info, "info1"),
        ]
        report = make_report("test", issues)
        assert report.error_count == 2
        assert report.warning_count == 2
        assert report.issues == issues  # info da listede

    def test_custom_report_id(self) -> None:
        report = make_report("test", [], report_id="custom-001")
        assert report.report_id == "custom-001"

    def test_custom_artifact_version(self) -> None:
        report = make_report("test", [], artifact_version="approved")
        assert report.artifact_version == "approved"

    def test_negative_score_clamped_to_zero(self) -> None:
        issues = [_make_issue(Severity.error, "test") for _ in range(10)]
        report = make_report("test", issues)
        assert report.score >= 0


class TestDecisionThresholds:
    def test_score_90_plus_is_passed(self) -> None:
        issues = [_make_issue(Severity.warning, "w1")]
        report = make_report("test", issues)
        assert report.score >= 90
        # 0 errors, score >=90 -> passed
        assert report.decision == Decision.passed

    def test_score_80_89_is_passed_with_warnings(self) -> None:
        issues = [_make_issue(Severity.warning, "w") for _ in range(6)]
        report = make_report("test", issues)
        # 100 - 6*3 = 82
        assert report.score == 82
        # 0 errors, score 80-89 -> passed_with_warnings
        assert report.decision == Decision.passed_with_warnings
