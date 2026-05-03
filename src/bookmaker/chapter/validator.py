from __future__ import annotations

import re
from pathlib import Path

from bookmaker.chapter.parser import MetaBlock, ParsedChapter
from bookmaker.core.ids import new_issue_id
from bookmaker.models.quality import Issue, IssueLocation, Severity

_ALLOWED_VALIDATION_MODES = {"runnable", "compile_only", "review_only", "skip", "render", "capture"}
_ALLOWED_SECTION_TYPES = {"standard", "body_group", "assessment_group"}
_ALLOWED_CODE_KINDS = {"example", "application", "snippet", "broken_example", "fixed_example"}
_ALLOWED_CODE_TESTS = {
    "compile", "run", "run_assert", "compile_run", "compile_run_assert", "skip", "none",
}
_ALLOWED_QR_POLICIES = {"none", "source", "page", "dual"}

_REQUIRED_FRONTMATTER = [
    "title", "subtitle", "author", "date", "lang", "documentclass",
    "toc", "toc-depth", "numbersections", "repo", "project-alias", "chapter-alias",
]
_RECOMMENDED_FRONTMATTER = [
    "chapter_id", "chapter_type", "automation_profile", "chapter_spec",
    "processing_stage", "numbering", "github_slug", "qr_policy",
    "asset_policy", "placeholder_policy", "snippet_policy",
]
_REQUIRED_CODE_META = [
    "order", "code_id", "extension", "title", "file", "link",
    "intentional_mismatch", "validation_mode",
]
_RECOMMENDED_CODE_META = ["kind", "main_class", "extract", "test", "github", "qr_policy"]
_REQUIRED_MERMAID_META = ["order", "id", "title", "kind", "output_file", "validation_mode"]


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _add(
    issues: list[Issue],
    severity: str,
    category: str,
    message: str,
    file: str = "",
    line: int | None = None,
    context: str = "",
) -> None:
    issues.append(Issue(
        issue_id=new_issue_id(),
        severity=Severity(severity),
        category=category,
        location=IssueLocation(file=file, line=line),
        message=message,
        current=context,
    ))


def _normalize_title(value: str) -> str:
    value = value.strip().strip('"').strip("'")
    value = re.sub(r"[`*_]+", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.casefold()


def _bool_value(value: str | None) -> bool | None:
    if value is None:
        return None
    lower = value.strip().casefold()
    if lower == "true":
        return True
    if lower == "false":
        return False
    return None


def _resolve_template(
    value: str,
    frontmatter: dict[str, str],
    local: dict[str, str] | None = None,
) -> str:
    local = local or {}
    replacements = {
        "repo": frontmatter.get("repo", ""),
        "project-alias": frontmatter.get("project-alias", ""),
        "chapter-alias": frontmatter.get("chapter-alias", frontmatter.get("chapter_id", "")),
        "chapter_id": frontmatter.get("chapter_id", frontmatter.get("chapter-alias", "")),
    }
    replacements.update(local)
    for key, val in replacements.items():
        value = value.replace("{" + key + "}", val)
    return value


def _find_next_heading(text: str, offset: int) -> tuple[int, str, int] | None:
    match = re.search(r"(?m)^(#{1,6})\s+(.+?)\s*$", text[offset:])
    if not match:
        return None
    line = _line_number(text, offset + match.start())
    return len(match.group(1)), match.group(2).strip(), line


def _find_next_code_fence(text: str, offset: int) -> tuple[str, str, int, int] | None:
    match = re.search(
        r"```(?P<lang>[A-Za-z0-9_+\-.]*)\s*\n(?P<code>.*?)(?:\n```)",
        text[offset:],
        re.DOTALL,
    )
    if not match:
        return None
    lang = match.group("lang").strip()
    code = match.group("code")
    start = offset + match.start()
    end = offset + match.end()
    return lang, code, start, end


def _validate_frontmatter(
    text: str,
    frontmatter: dict[str, str],
    issues: list[Issue],
    file: str,
) -> None:
    if not frontmatter:
        _add(issues, "error", "frontmatter.missing", "YAML front matter is missing.", file, 1)
        return
    for field in _REQUIRED_FRONTMATTER:
        if field not in frontmatter:
            _add(issues, "error", "frontmatter.required_missing",
                 f"Required front matter field missing: {field}", file, 1)
    for field in _RECOMMENDED_FRONTMATTER:
        if field not in frontmatter:
            _add(issues, "warning", "frontmatter.recommended_missing",
                 f"Recommended front matter field missing: {field}", file, 1)

    h1_matches = list(re.finditer(r"(?m)^#\s+(.+?)\s*$", text))
    if len(h1_matches) != 1:
        _add(issues, "error", "heading.h1_count",
             f"Expected exactly one H1 heading, found {len(h1_matches)}.", file)

    for heading in re.finditer(r"(?m)^(#{1,6})\s+(.+?)\s*$", text):
        title = heading.group(2).strip()
        if (
            re.match(r"^(Bolum|Bölüm)\s+\d+[:.\s]", title, re.IGNORECASE)
            or re.match(r"^\d+(?:\.\d+)+\s+", title)
        ):
            _add(issues, "error", "heading.manual_numbering",
                 "Manual chapter/section numbering is not allowed in headings.",
                 file, _line_number(text, heading.start()), title)


def _validate_forbidden_markers(text: str, issues: list[Issue], file: str) -> None:
    forbidden = {
        "DIAGRAM_META": "Use MERMAID_META for Mermaid blocks.",
        "extention": "Use extension instead of extention.",
        "BÖLÜM SONU": "Do not keep a manual chapter-end marker in source Markdown.",
        "BOLUM SONU": "Do not keep a manual chapter-end marker in source Markdown.",
    }
    for marker, message in forbidden.items():
        for match in re.finditer(re.escape(marker), text):
            _add(issues, "error", "marker.forbidden", message,
                 file, _line_number(text, match.start()), marker)


def _validate_sections(
    text: str,
    blocks: list[MetaBlock],
    issues: list[Issue],
    file: str,
) -> None:
    section_blocks = [b for b in blocks if b.kind == "SECTION_META"]
    seen_orders: dict[str, int] = {}
    numeric_orders: list[int] = []

    for block in section_blocks:
        data = block.data
        order = data.get("order")
        title = data.get("title")
        section_type = data.get("section_type", "standard")

        if not order:
            _add(issues, "error", "section.order_missing",
                 "SECTION_META order is missing.", file, block.line)
        else:
            numeric_orders.append(int(order) if order.isdigit() else -1)
            if order in seen_orders:
                _add(issues, "error", "section.order_duplicate",
                     f"Duplicate SECTION_META order: {order}", file, block.line)
            seen_orders[order] = block.line

        if not title:
            _add(issues, "error", "section.title_missing",
                 "SECTION_META title is missing.", file, block.line)

        if section_type not in _ALLOWED_SECTION_TYPES:
            _add(issues, "warning", "section.type_unknown",
                 f"Unknown section_type: {section_type}", file, block.line)

        heading = _find_next_heading(text, block.end)
        if not heading:
            _add(issues, "error", "section.heading_missing",
                 "SECTION_META is not followed by a heading.", file, block.line)
            continue
        level, heading_title, heading_line = heading

        if section_type == "standard" and level != 2:
            _add(issues, "warning", "section.heading_level",
                 "Standard SECTION_META should be followed by an H2 heading.",
                 file, heading_line, heading_title)

        if (
            section_type == "standard"
            and title
            and _normalize_title(title) != _normalize_title(heading_title)
        ):
            _add(issues, "error", "section.title_heading_mismatch",
                 "SECTION_META title does not match the following heading.",
                 file, block.line, f"{title} != {heading_title}")

    if numeric_orders and numeric_orders != sorted(numeric_orders):
        _add(issues, "error", "section.order_not_increasing",
             "SECTION_META orders are not increasing.", file)


def _effective_code_id(meta: dict[str, str], frontmatter: dict[str, str]) -> str:
    order = meta.get("order", "")
    return _resolve_template(meta.get("code_id", ""), frontmatter, {"order": order})


def _validate_java_code(
    text: str,
    block: MetaBlock,
    code: str,
    issues: list[Issue],
    file: str,
) -> None:
    file_name = block.data.get("file", "")
    if not file_name:
        return
    expected_class = Path(file_name).stem
    class_match = re.search(r"\bpublic\s+class\s+([A-Za-z_][A-Za-z0-9_]*)", code)
    if not class_match:
        _add(issues, "error", "java.public_class_missing",
             "Runnable/compile_only Java code must declare a public class.",
             file, block.line, file_name)
        return
    actual_class = class_match.group(1)
    declared_main = block.data.get("main_class")
    if declared_main and declared_main != actual_class:
        _add(issues, "error", "java.main_class_mismatch",
             "CODE_META main_class does not match the declared public class.",
             file, block.line, f"{declared_main} != {actual_class}")
    if expected_class != actual_class:
        _add(issues, "error", "java.file_class_mismatch",
             "Java file name and public class name do not match.",
             file, block.line, f"{file_name} -> {actual_class}")
    dosya_match = re.search(r"(?m)^\s*//\s*Dosya:\s*(\S+)\s*$", code)
    if dosya_match and dosya_match.group(1) != file_name:
        _add(issues, "warning", "java.file_comment_mismatch",
             "Java file comment does not match CODE_META file.",
             file, block.line, f"{file_name} != {dosya_match.group(1)}")


def _validate_code_meta(
    text: str,
    blocks: list[MetaBlock],
    frontmatter: dict[str, str],
    issues: list[Issue],
    file: str,
) -> None:
    code_blocks = [b for b in blocks if b.kind == "CODE_META"]
    code_ids: dict[str, MetaBlock] = {}
    paired_refs: list[tuple[MetaBlock, str]] = []

    for block in code_blocks:
        data = block.data
        for f in _REQUIRED_CODE_META:
            if f not in data:
                _add(issues, "error", "code.required_missing",
                     f"CODE_META field missing: {f}", file, block.line)
        for f in _RECOMMENDED_CODE_META:
            if f not in data:
                _add(issues, "warning", "code.recommended_missing",
                     f"CODE_META recommended field missing: {f}", file, block.line)

        mode = data.get("validation_mode", "")
        if mode and mode not in _ALLOWED_VALIDATION_MODES:
            _add(issues, "error", "code.validation_mode_unknown",
                 f"Unknown validation_mode: {mode}", file, block.line)

        kind = data.get("kind", "")
        if kind and kind not in _ALLOWED_CODE_KINDS:
            _add(issues, "error", "code.kind_unknown",
                 f"Unknown code kind: {kind}", file, block.line)

        test = data.get("test", "")
        if test and test not in _ALLOWED_CODE_TESTS:
            _add(issues, "error", "code.test_unknown",
                 f"Unknown test mode: {test}", file, block.line)

        qr_policy = data.get("qr_policy", "")
        if qr_policy and qr_policy not in _ALLOWED_QR_POLICIES:
            _add(issues, "error", "code.qr_policy_unknown",
                 f"Unknown qr_policy: {qr_policy}", file, block.line)

        extract = _bool_value(data.get("extract"))
        github = _bool_value(data.get("github"))
        if data.get("extract") is not None and extract is None:
            _add(issues, "error", "code.extract_invalid",
                 "extract must be true or false.", file, block.line)
        if data.get("github") is not None and github is None:
            _add(issues, "error", "code.github_invalid",
                 "github must be true or false.", file, block.line)

        if test == "compile_run_assert" and "expected_stdout_contains" not in data:
            _add(issues, "error", "code.expected_stdout_missing",
                 "compile_run_assert requires expected_stdout_contains.", file, block.line)

        if kind == "broken_example" and test != "skip":
            _add(issues, "error", "code.broken_test_mode",
                 "broken_example should use test: skip.", file, block.line)
        if kind == "fixed_example" and _bool_value(data.get("intentional_mismatch")):
            _add(issues, "error", "code.fixed_marked_mismatch",
                 "fixed_example cannot be an intentional mismatch.", file, block.line)

        if data.get("code_id") and re.search(r"\{[^}]+\}", data["code_id"]):
            _add(issues, "warning", "code.id_template",
                 "Concrete code_id is preferred in canonical chapter examples.", file, block.line)

        mismatch = _bool_value(data.get("intentional_mismatch"))
        if mismatch is None:
            _add(issues, "error", "code.intentional_mismatch_invalid",
                 "intentional_mismatch must be true or false.", file, block.line)
        elif mismatch:
            for f in ["mismatch_kind", "mismatch_summary", "expected_outcome"]:
                if f not in data:
                    _add(issues, "error", "code.mismatch_field_missing",
                         f"{f} is required for intentional mismatch.", file, block.line)
            if mode != "review_only":
                _add(issues, "error", "code.mismatch_mode",
                     "intentional_mismatch: true should use validation_mode: review_only.",
                     file, block.line)
        elif mode == "review_only":
            _add(issues, "warning", "code.review_without_mismatch",
                 "review_only code is not marked as intentional_mismatch.", file, block.line)

        code_id = _effective_code_id(data, frontmatter)
        if code_id:
            if code_id in code_ids:
                _add(issues, "error", "code.id_duplicate",
                     f"Duplicate code_id: {code_id}", file, block.line)
            code_ids[code_id] = block

        if "paired_with" in data:
            paired = _resolve_template(
                data["paired_with"], frontmatter, {"order": data.get("order", "")}
            )
            paired_refs.append((block, paired))

        fence = _find_next_code_fence(text, block.end)
        if not fence:
            _add(issues, "error", "code.fence_missing",
                 "CODE_META is not followed by a fenced code block.", file, block.line)
            continue
        lang, code, fence_start, _ = fence
        between = text[block.end:fence_start]
        if re.search(r"(?m)^#{1,6}\s+", between):
            _add(issues, "error", "code.heading_before_fence",
                 "A heading appears between CODE_META and its code fence.", file, block.line)

        extension = data.get("extension", "")
        if extension and lang and extension.casefold() != lang.casefold():
            _add(issues, "warning", "code.lang_extension_mismatch",
                 "Code fence language does not match CODE_META extension.",
                 file, _line_number(text, fence_start), f"{lang} != {extension}")

        if extension.casefold() == "java" and (
            mode in {"runnable", "compile_only"} or data.get("main_class")
        ):
            _validate_java_code(text, block, code, issues, file)

    for block, paired in paired_refs:
        if paired not in code_ids:
            _add(issues, "error", "code.paired_missing",
                 f"paired_with target not found: {paired}", file, block.line)


def _validate_mermaid(
    text: str,
    blocks: list[MetaBlock],
    issues: list[Issue],
    file: str,
) -> None:
    mermaid_fences = list(re.finditer(r"```mermaid\b", text))
    mermaid_blocks = [b for b in blocks if b.kind == "MERMAID_META"]

    if len(mermaid_fences) != len(mermaid_blocks):
        _add(
            issues, "error", "mermaid.meta_count",
            f"Mermaid fence count and MERMAID_META count differ: "
            f"{len(mermaid_fences)} != {len(mermaid_blocks)}",
            file,
        )

    for block in mermaid_blocks:
        for f in _REQUIRED_MERMAID_META:
            if f not in block.data:
                _add(issues, "error", "mermaid.required_missing",
                     f"MERMAID_META field missing: {f}", file, block.line)
        mode = block.data.get("validation_mode", "")
        if mode and mode not in _ALLOWED_VALIDATION_MODES:
            _add(issues, "error", "mermaid.validation_mode_unknown",
                 f"Unknown validation_mode: {mode}", file, block.line)
        fence = _find_next_code_fence(text, block.end)
        if not fence or fence[0] != "mermaid":
            _add(issues, "error", "mermaid.fence_missing",
                 "MERMAID_META is not followed by a mermaid code fence.", file, block.line)


def _validate_final_placeholders(text: str, issues: list[Issue], file: str) -> None:
    for match in re.finditer(r"\{[A-Za-z0-9_-]+\}", text):
        _add(issues, "error", "final.placeholder_unresolved",
             "Unresolved placeholder remains in final mode.",
             file, _line_number(text, match.start()), match.group(0))


def validate(chapter: ParsedChapter, final_mode: bool = False) -> list[Issue]:
    """Bölümü doğrular ve Issue listesi döndürür."""
    issues: list[Issue] = []
    text = chapter.text
    frontmatter = chapter.frontmatter
    blocks = chapter.meta_blocks
    file_str = str(chapter.path)

    _validate_frontmatter(text, frontmatter, issues, file_str)
    _validate_forbidden_markers(text, issues, file_str)
    _validate_sections(text, blocks, issues, file_str)
    _validate_code_meta(text, blocks, frontmatter, issues, file_str)
    _validate_mermaid(text, blocks, issues, file_str)
    if final_mode:
        _validate_final_placeholders(text, issues, file_str)

    return issues
