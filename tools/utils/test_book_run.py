"""Quick book validation test."""
from pathlib import Path
from bookmaker.chapter.book_validator import validate_book

chapters_dir = Path("chapters")
images_dir = Path("build/output/images")

if not images_dir.exists():
    images_dir = None

result = validate_book(chapters_dir, images_dir)
report = result.report

print(f"Score: {report.score}")
print(f"Decision: {report.decision.value}")
print(f"Errors: {report.error_count}")
print(f"Warnings: {report.warning_count}")
print(f"Total chapters: {len(result.chapter_sizes)}")

if report.issues:
    print(f"\nIssues ({len(report.issues)}):")
    for iss in report.issues[:10]:
        print(f"  [{iss.severity.value}] {iss.category}: {iss.message}")
    if len(report.issues) > 10:
        print(f"  ... and {len(report.issues) - 10} more")

if result.chapter_reports:
    passed = sum(1 for r in result.chapter_reports.values() if r.decision.value in ("pass", "pass_with_warnings"))
    failed = sum(1 for r in result.chapter_reports.values() if r.decision.value not in ("pass", "pass_with_warnings"))
    print(f"\nChapter-level: {passed} passed, {failed} needs revision")
