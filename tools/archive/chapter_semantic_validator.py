from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ALLOWED_VALIDATION_MODES = {"runnable", "compile_only", "review_only", "skip", "render", "capture"}
ALLOWED_SECTION_TYPES = {"standard", "body_group", "assessment_group"}
ALLOWED_CODE_KINDS = {"example", "application", "snippet", "broken_example", "fixed_example"}
ALLOWED_CODE_TESTS = {"compile", "run", "run_assert", "compile_run", "compile_run_assert", "skip", "none"}
ALLOWED_QR_POLICIES = {"none", "source", "page", "dual"}

REQUIRED_FRONTMATTER_FIELDS = [
    "title",
    "subtitle",
    "author",
    "date",
    "lang",
    "documentclass",
    "toc",
    "toc-depth",
    "numbersections",
    "repo",
    "project-alias",
    "chapter-alias",
]

RECOMMENDED_FRONTMATTER_FIELDS = [
    "chapter_id",
    "chapter_type",
    "automation_profile",
    "chapter_spec",
    "processing_stage",
    "numbering",
    "github_slug",
    "qr_policy",
    "asset_policy",
    "placeholder_policy",
    "snippet_policy",
]

REQUIRED_CODE_META_FIELDS = [
    "order",
    "code_id",
    "extension",
    "title",
    "file",
    "link",
    "intentional_mismatch",
    "validation_mode",
]

RECOMMENDED_CODE_META_FIELDS = [
    "kind",
    "main_class",
    "extract",
    "test",
    "github",
    "qr_policy",
]

REQUIRED_MERMAID_META_FIELDS = [
    "order",
    "id",
    "title",
    "kind",
    "output_file",
    "validation_mode",
]


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    line: int | None = None
    context: str | None = None


@dataclass
class MetaBlock:
    kind: str
    body: str
    data: dict[str, str]
    start: int
    end: int
    line: int


@dataclass
class ValidationResult:
    path: str
    score: int
    decision: str
    summary: dict[str, int]
    issues: list[Issue]


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def normalize_title(value: str) -> str:
    value = value.strip().strip('"').strip("'")
    value = re.sub(r"[`*_]+", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.casefold()


def parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_key_values(body: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*?)\s*$", line)
        if match:
            result[match.group(1)] = parse_scalar(match.group(2))
    return result


def parse_frontmatter(text: str) -> tuple[dict[str, str], int | None]:
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.startswith("---"):
        return {}, None
    match = re.match(r"(?s)^---\s*\n(.*?)\n---\s*(?:\n|$)", text)
    if not match:
        return {}, 1
    return parse_key_values(match.group(1)), 1


def parse_meta_blocks(text: str) -> list[MetaBlock]:
    blocks: list[MetaBlock] = []
    pattern = re.compile(r"<!--\s*(?P<kind>[A-Z_]+)\s*(?P<body>.*?)-->", re.DOTALL)
    for match in pattern.finditer(text):
        body = match.group("body")
        blocks.append(
            MetaBlock(
                kind=match.group("kind"),
                body=body,
                data=parse_key_values(body),
                start=match.start(),
                end=match.end(),
                line=line_number(text, match.start()),
            )
        )
    return blocks


def find_next_heading(text: str, offset: int) -> tuple[int, str, int] | None:
    match = re.search(r"(?m)^(#{1,6})\s+(.+?)\s*$", text[offset:])
    if not match:
        return None
    line = line_number(text, offset + match.start())
    level = len(match.group(1))
    title = match.group(2).strip()
    return level, title, line


def find_next_code_fence(text: str, offset: int) -> tuple[str, str, int, int] | None:
    match = re.search(r"```(?P<lang>[A-Za-z0-9_+\-.]*)\s*\n(?P<code>.*?)(?:\n```)", text[offset:], re.DOTALL)
    if not match:
        return None
    lang = match.group("lang").strip()
    code = match.group("code")
    start = offset + match.start()
    end = offset + match.end()
    return lang, code, start, end


def resolve_template(value: str, frontmatter: dict[str, str], local: dict[str, str] | None = None) -> str:
    local = local or {}
    replacements = {
        "repo": frontmatter.get("repo", ""),
        "project-alias": frontmatter.get("project-alias", ""),
        "chapter-alias": frontmatter.get("chapter-alias", frontmatter.get("chapter_id", "")),
        "chapter_id": frontmatter.get("chapter_id", frontmatter.get("chapter-alias", "")),
    }
    replacements.update(local)
    for key, replacement in replacements.items():
        value = value.replace("{" + key + "}", replacement)
    return value


def bool_value(value: str | None) -> bool | None:
    if value is None:
        return None
    lowered = value.strip().casefold()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return None


def add_issue(
    issues: list[Issue],
    severity: str,
    code: str,
    message: str,
    line: int | None = None,
    context: str | None = None,
) -> None:
    issues.append(Issue(severity=severity, code=code, message=message, line=line, context=context))


def validate_frontmatter(text: str, frontmatter: dict[str, str], issues: list[Issue]) -> None:
    if not frontmatter:
        add_issue(issues, "error", "frontmatter.missing", "YAML front matter is missing.", 1)
        return
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in frontmatter:
            add_issue(issues, "error", "frontmatter.required_missing", f"Required front matter field missing: {field}", 1)
    for field in RECOMMENDED_FRONTMATTER_FIELDS:
        if field not in frontmatter:
            add_issue(
                issues,
                "warning",
                "frontmatter.recommended_missing",
                f"Recommended front matter field missing: {field}",
                1,
            )

    h1_matches = list(re.finditer(r"(?m)^#\s+(.+?)\s*$", text))
    if len(h1_matches) != 1:
        add_issue(issues, "error", "heading.h1_count", f"Expected exactly one H1 heading, found {len(h1_matches)}.")
    for heading in re.finditer(r"(?m)^(#{1,6})\s+(.+?)\s*$", text):
        title = heading.group(2).strip()
        if re.match(r"^(Bolum|Bölüm)\s+\d+[:.\s]", title, re.IGNORECASE) or re.match(r"^\d+(?:\.\d+)+\s+", title):
            add_issue(
                issues,
                "error",
                "heading.manual_numbering",
                "Manual chapter/section numbering is not allowed in headings.",
                line_number(text, heading.start()),
                title,
            )


def validate_forbidden_markers(text: str, issues: list[Issue]) -> None:
    forbidden = {
        "DIAGRAM_META": "Use MERMAID_META for Mermaid blocks.",
        "extention": "Use extension instead of extention.",
        "BÖLÜM SONU": "Do not keep a manual chapter-end marker in source Markdown.",
        "BOLUM SONU": "Do not keep a manual chapter-end marker in source Markdown.",
    }
    for marker, message in forbidden.items():
        for match in re.finditer(re.escape(marker), text):
            add_issue(issues, "error", "marker.forbidden", message, line_number(text, match.start()), marker)


def validate_sections(text: str, blocks: Iterable[MetaBlock], issues: list[Issue]) -> None:
    section_blocks = [block for block in blocks if block.kind == "SECTION_META"]
    seen_orders: dict[str, int] = {}
    numeric_orders: list[int] = []
    for block in section_blocks:
        data = block.data
        order = data.get("order")
        title = data.get("title")
        section_type = data.get("section_type", "standard")
        if not order:
            add_issue(issues, "error", "section.order_missing", "SECTION_META order is missing.", block.line)
        else:
            numeric_orders.append(int(order) if order.isdigit() else -1)
            if order in seen_orders:
                add_issue(
                    issues,
                    "error",
                    "section.order_duplicate",
                    f"Duplicate SECTION_META order: {order}",
                    block.line,
                )
            seen_orders[order] = block.line
        if not title:
            add_issue(issues, "error", "section.title_missing", "SECTION_META title is missing.", block.line)
        if section_type not in ALLOWED_SECTION_TYPES:
            add_issue(
                issues,
                "warning",
                "section.type_unknown",
                f"Unknown section_type: {section_type}",
                block.line,
            )

        heading = find_next_heading(text, block.end)
        if not heading:
            add_issue(issues, "error", "section.heading_missing", "SECTION_META is not followed by a heading.", block.line)
            continue
        level, heading_title, heading_line = heading
        if section_type == "standard" and level != 2:
            add_issue(
                issues,
                "warning",
                "section.heading_level",
                "Standard SECTION_META should be followed by an H2 heading.",
                heading_line,
                heading_title,
            )
        if section_type == "standard" and title and normalize_title(title) != normalize_title(heading_title):
            add_issue(
                issues,
                "error",
                "section.title_heading_mismatch",
                "SECTION_META title does not match the following heading.",
                block.line,
                f"{title} != {heading_title}",
            )

    if numeric_orders and numeric_orders != sorted(numeric_orders):
        add_issue(issues, "error", "section.order_not_increasing", "SECTION_META orders are not increasing.")


def effective_code_id(meta: dict[str, str], frontmatter: dict[str, str]) -> str:
    order = meta.get("order", "")
    return resolve_template(meta.get("code_id", ""), frontmatter, {"order": order})


def validate_code_meta(text: str, blocks: Iterable[MetaBlock], frontmatter: dict[str, str], issues: list[Issue]) -> None:
    code_blocks = [block for block in blocks if block.kind == "CODE_META"]
    code_ids: dict[str, MetaBlock] = {}
    paired_refs: list[tuple[MetaBlock, str]] = []

    for block in code_blocks:
        data = block.data
        for field in REQUIRED_CODE_META_FIELDS:
            if field not in data:
                add_issue(issues, "error", "code.required_missing", f"CODE_META field missing: {field}", block.line)
        for field in RECOMMENDED_CODE_META_FIELDS:
            if field not in data:
                add_issue(issues, "warning", "code.recommended_missing", f"CODE_META recommended field missing: {field}", block.line)

        mode = data.get("validation_mode", "")
        if mode and mode not in ALLOWED_VALIDATION_MODES:
            add_issue(issues, "error", "code.validation_mode_unknown", f"Unknown validation_mode: {mode}", block.line)
        kind = data.get("kind", "")
        if kind and kind not in ALLOWED_CODE_KINDS:
            add_issue(issues, "error", "code.kind_unknown", f"Unknown code kind: {kind}", block.line)
        test = data.get("test", "")
        if test and test not in ALLOWED_CODE_TESTS:
            add_issue(issues, "error", "code.test_unknown", f"Unknown test mode: {test}", block.line)
        qr_policy = data.get("qr_policy", "")
        if qr_policy and qr_policy not in ALLOWED_QR_POLICIES:
            add_issue(issues, "error", "code.qr_policy_unknown", f"Unknown qr_policy: {qr_policy}", block.line)
        extract = bool_value(data.get("extract"))
        github = bool_value(data.get("github"))
        if data.get("extract") is not None and extract is None:
            add_issue(issues, "error", "code.extract_invalid", "extract must be true or false.", block.line)
        if data.get("github") is not None and github is None:
            add_issue(issues, "error", "code.github_invalid", "github must be true or false.", block.line)
        if test == "compile_run_assert" and "expected_stdout_contains" not in data:
            add_issue(
                issues,
                "error",
                "code.expected_stdout_missing",
                "compile_run_assert requires expected_stdout_contains.",
                block.line,
            )
        if kind == "broken_example" and test != "skip":
            add_issue(issues, "error", "code.broken_test_mode", "broken_example should use test: skip.", block.line)
        if kind == "fixed_example" and bool_value(data.get("intentional_mismatch")):
            add_issue(issues, "error", "code.fixed_marked_mismatch", "fixed_example cannot be an intentional mismatch.", block.line)
        if data.get("code_id") and re.search(r"\{[^}]+\}", data["code_id"]):
            add_issue(issues, "warning", "code.id_template", "Concrete code_id is preferred in canonical chapter examples.", block.line)

        mismatch = bool_value(data.get("intentional_mismatch"))
        if mismatch is None:
            add_issue(
                issues,
                "error",
                "code.intentional_mismatch_invalid",
                "intentional_mismatch must be true or false.",
                block.line,
            )
        elif mismatch:
            for field in ["mismatch_kind", "mismatch_summary", "expected_outcome"]:
                if field not in data:
                    add_issue(issues, "error", "code.mismatch_field_missing", f"{field} is required for intentional mismatch.", block.line)
            if mode != "review_only":
                add_issue(
                    issues,
                    "error",
                    "code.mismatch_mode",
                    "intentional_mismatch: true should use validation_mode: review_only.",
                    block.line,
                )
        elif mode == "review_only":
            add_issue(
                issues,
                "warning",
                "code.review_without_mismatch",
                "review_only code is not marked as intentional_mismatch.",
                block.line,
            )

        code_id = effective_code_id(data, frontmatter)
        if code_id:
            if code_id in code_ids:
                add_issue(issues, "error", "code.id_duplicate", f"Duplicate code_id: {code_id}", block.line)
            code_ids[code_id] = block

        if "paired_with" in data:
            paired = resolve_template(data["paired_with"], frontmatter, {"order": data.get("order", "")})
            paired_refs.append((block, paired))

        fence = find_next_code_fence(text, block.end)
        if not fence:
            add_issue(issues, "error", "code.fence_missing", "CODE_META is not followed by a fenced code block.", block.line)
            continue
        lang, code, fence_start, _ = fence
        between = text[block.end:fence_start]
        if re.search(r"(?m)^#{1,6}\s+", between):
            add_issue(issues, "error", "code.heading_before_fence", "A heading appears between CODE_META and its code fence.", block.line)

        extension = data.get("extension", "")
        if extension and lang and extension.casefold() != lang.casefold():
            add_issue(
                issues,
                "warning",
                "code.lang_extension_mismatch",
                "Code fence language does not match CODE_META extension.",
                line_number(text, fence_start),
                f"{lang} != {extension}",
            )

        if extension.casefold() == "java" and (mode in {"runnable", "compile_only"} or data.get("main_class")):
            validate_java_code(text, block, code, issues)

        if data.get("qrfile") and "qrfile" not in text[block.end : fence_start + 1_000]:
            add_issue(
                issues,
                "warning",
                "code.qrfile_not_referenced",
                "qrfile is set but a nearby QR image reference was not found.",
                block.line,
            )

    for block, paired in paired_refs:
        if paired not in code_ids:
            add_issue(issues, "error", "code.paired_missing", f"paired_with target not found: {paired}", block.line)


def validate_java_code(text: str, block: MetaBlock, code: str, issues: list[Issue]) -> None:
    file_name = block.data.get("file", "")
    if not file_name:
        return
    expected_class = Path(file_name).stem
    class_match = re.search(r"\bpublic\s+class\s+([A-Za-z_][A-Za-z0-9_]*)", code)
    if not class_match:
        add_issue(
            issues,
            "error",
            "java.public_class_missing",
            "Runnable/compile_only Java code must declare a public class.",
            block.line,
            file_name,
        )
        return
    actual_class = class_match.group(1)
    declared_main_class = block.data.get("main_class")
    if declared_main_class and declared_main_class != actual_class:
        add_issue(
            issues,
            "error",
            "java.main_class_mismatch",
            "CODE_META main_class does not match the declared public class.",
            block.line,
            f"{declared_main_class} != {actual_class}",
        )
    if expected_class != actual_class:
        add_issue(
            issues,
            "error",
            "java.file_class_mismatch",
            "Java file name and public class name do not match.",
            block.line,
            f"{file_name} -> {actual_class}",
        )

    dosya_match = re.search(r"(?m)^\s*//\s*Dosya:\s*(\S+)\s*$", code)
    if dosya_match and dosya_match.group(1) != file_name:
        add_issue(
            issues,
            "warning",
            "java.file_comment_mismatch",
            "Java file comment does not match CODE_META file.",
            block.line,
            f"{file_name} != {dosya_match.group(1)}",
        )


def validate_mermaid(text: str, blocks: Iterable[MetaBlock], issues: list[Issue]) -> None:
    mermaid_fences = list(re.finditer(r"```mermaid\b", text))
    mermaid_blocks = [block for block in blocks if block.kind == "MERMAID_META"]
    if len(mermaid_fences) != len(mermaid_blocks):
        add_issue(
            issues,
            "error",
            "mermaid.meta_count",
            f"Mermaid fence count and MERMAID_META count differ: {len(mermaid_fences)} != {len(mermaid_blocks)}",
        )
    for block in mermaid_blocks:
        for field in REQUIRED_MERMAID_META_FIELDS:
            if field not in block.data:
                add_issue(issues, "error", "mermaid.required_missing", f"MERMAID_META field missing: {field}", block.line)
        mode = block.data.get("validation_mode", "")
        if mode and mode not in ALLOWED_VALIDATION_MODES:
            add_issue(issues, "error", "mermaid.validation_mode_unknown", f"Unknown validation_mode: {mode}", block.line)
        fence = find_next_code_fence(text, block.end)
        if not fence or fence[0] != "mermaid":
            add_issue(issues, "error", "mermaid.fence_missing", "MERMAID_META is not followed by a mermaid code fence.", block.line)


def validate_final_placeholders(text: str, issues: list[Issue]) -> None:
    for match in re.finditer(r"\{[A-Za-z0-9_-]+\}", text):
        add_issue(
            issues,
            "error",
            "final.placeholder_unresolved",
            "Unresolved placeholder remains in final mode.",
            line_number(text, match.start()),
            match.group(0),
        )


def compute_result(path: Path, issues: list[Issue]) -> ValidationResult:
    summary = {
        "errors": sum(1 for issue in issues if issue.severity == "error"),
        "warnings": sum(1 for issue in issues if issue.severity == "warning"),
        "info": sum(1 for issue in issues if issue.severity == "info"),
    }
    score = max(0, 100 - summary["errors"] * 15 - summary["warnings"] * 3)
    if summary["errors"]:
        decision = "BLOCKED"
    elif score >= 90:
        decision = "PASS"
    elif score >= 80:
        decision = "PASS_WITH_WARNINGS"
    elif score >= 65:
        decision = "REVISION_REQUIRED"
    else:
        decision = "BLOCKED"
    return ValidationResult(path=str(path), score=score, decision=decision, summary=summary, issues=issues)


def validate(path: Path, final_mode: bool = False) -> ValidationResult:
    text = path.read_text(encoding="utf-8")
    issues: list[Issue] = []
    frontmatter, _ = parse_frontmatter(text)
    blocks = parse_meta_blocks(text)

    validate_frontmatter(text, frontmatter, issues)
    validate_forbidden_markers(text, issues)
    validate_sections(text, blocks, issues)
    validate_code_meta(text, blocks, frontmatter, issues)
    validate_mermaid(text, blocks, issues)
    if final_mode:
        validate_final_placeholders(text, issues)

    return compute_result(path, issues)


def result_to_markdown(result: ValidationResult) -> str:
    lines = [
        "# Chapter Semantic Validation Report",
        "",
        f"- File: `{result.path}`",
        f"- Decision: `{result.decision}`",
        f"- Score: `{result.score}`",
        f"- Errors: `{result.summary['errors']}`",
        f"- Warnings: `{result.summary['warnings']}`",
        "",
        "| Severity | Code | Line | Message | Context |",
        "|---|---|---:|---|---|",
    ]
    if not result.issues:
        lines.append("| info | clean |  | No issues found. |  |")
    for issue in result.issues:
        line = "" if issue.line is None else str(issue.line)
        context = "" if issue.context is None else issue.context.replace("|", "\\|")
        message = issue.message.replace("|", "\\|")
        lines.append(f"| {issue.severity} | `{issue.code}` | {line} | {message} | `{context}` |")
    lines.append("")
    return "\n".join(lines)


def write_reports(result: ValidationResult, json_path: Path | None, markdown_path: Path | None) -> None:
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps(
                {
                    **asdict(result),
                    "issues": [asdict(issue) for issue in result.issues],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    if markdown_path:
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(result_to_markdown(result), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a bookMaker chapter Markdown file.")
    parser.add_argument("path", type=Path, help="Chapter Markdown file to validate.")
    parser.add_argument("--final", action="store_true", help="Treat unresolved placeholders as errors.")
    parser.add_argument("--json", type=Path, default=Path("build/reports/chapter_semantic_report.json"))
    parser.add_argument("--markdown", type=Path, default=Path("build/reports/chapter_semantic_report.md"))
    parser.add_argument("--no-write", action="store_true", help="Do not write report files.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = validate(args.path, final_mode=args.final)
    if not args.no_write:
        write_reports(result, args.json, args.markdown)
    print(f"{result.decision} score={result.score} errors={result.summary['errors']} warnings={result.summary['warnings']}")
    return 1 if result.summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
