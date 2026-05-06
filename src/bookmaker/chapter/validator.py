# ruff: noqa: E501
from __future__ import annotations

import re

from bookmaker.chapter.parser import MetaBlock, ParsedChapter
from bookmaker.chapter.validation_modes import (
    CODE_KINDS,
    CODE_TEST_MODES,
    QR_POLICIES,
    VALIDATION_MODES,
)
from bookmaker.core.ids import new_issue_id
from bookmaker.models.quality import Issue, IssueLocation, Severity


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
    issues.append(
        Issue(
            issue_id=new_issue_id(),
            severity=Severity(severity),
            category=category,
            location=IssueLocation(file=file, line=line),
            message=message,
            current=context,
        )
    )


def _bool_value(value: str | None) -> bool | None:
    if value is None:
        return None
    lower = value.strip().casefold()
    if lower == "true":
        return True
    if lower == "false":
        return False
    return None


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


def _validate_frontmatter_and_headings(chapter: ParsedChapter, issues: list[Issue]) -> None:
    text = chapter.text
    file = str(chapter.path)

    if not text.strip():
        _add(issues, "error", "frontmatter.empty_file", "Dosya boş.", file, 1)
        return

    if not chapter.frontmatter:
        _add(
            issues,
            "warning",
            "frontmatter.missing",
            "YAML front matter bulunmuyor. Project-based içeriklerde zorunlu değildir; ancak export için önerilir.",
            file,
            1,
        )

    h1_matches = list(re.finditer(r"(?m)^#\s+(.+?)\s*$", text))
    if len(h1_matches) == 0:
        _add(issues, "warning", "heading.no_h1", "H1 başlığı bulunamadı.", file)
    elif len(h1_matches) > 1:
        for match in h1_matches:
            _add(
                issues,
                "error",
                "heading.multiple_h1",
                "Birden fazla H1 başlığı bulundu.",
                file,
                _line_number(text, match.start()),
                match.group(1).strip(),
            )

    previous_level = 0
    for match in re.finditer(r"(?m)^(#{1,6})\s+(.+?)\s*$", text):
        level = len(match.group(1))
        title = match.group(2).strip()
        if level >= 2 and re.match(r"^\d+(?:\.\d+)+\.?\s+", title):
            _add(
                issues,
                "error",
                "heading.manual_numbering",
                "Başlıkta manuel numaralandırma bulundu.",
                file,
                _line_number(text, match.start()),
                title,
            )
        if previous_level and level > previous_level + 1:
            _add(
                issues,
                "warning",
                "heading.level_skip",
                f"Başlık hiyerarşisi atlıyor: H{previous_level} -> H{level}.",
                file,
                _line_number(text, match.start()),
                match.group(2).strip(),
            )
        previous_level = level


def _validate_section_meta(blocks: list[MetaBlock], issues: list[Issue], file: str) -> None:
    orders: dict[str, int] = {}
    for block in [b for b in blocks if b.kind == "SECTION_META"]:
        order = block.data.get("order", "").strip()
        if not order:
            _add(
                issues,
                "error",
                "section.order_missing",
                "SECTION_META içinde order alanı eksik.",
                file,
                block.line,
            )
            continue
        if order in orders:
            _add(
                issues,
                "error",
                "section.order_duplicate",
                f"Tekrar eden SECTION_META order: {order}",
                file,
                block.line,
            )
        orders[order] = block.line


def _validate_forbidden_markers(text: str, issues: list[Issue], file: str) -> None:
    forbidden = {
        "DIAGRAM_META": "Mermaid blokları için MERMAID_META kullanın.",
        "extention": "extension yazımı kullanılmalıdır.",
        "BÖLÜM SONU": "Kaynak Markdown içinde manuel bölüm sonu işareti tutulmamalıdır.",
        "BOLUM SONU": "Kaynak Markdown içinde manuel bölüm sonu işareti tutulmamalıdır.",
    }
    for marker, message in forbidden.items():
        for match in re.finditer(re.escape(marker), text):
            _add(issues, "error", "marker.forbidden", message, file, _line_number(text, match.start()), marker)


def _validate_placeholders(text: str, issues: list[Issue], file: str, final_mode: bool) -> None:
    pattern = re.compile(r"(?:\bTODO\b|\bFIXME\b|\[\.{3}\]|\(\.{3}\))", re.IGNORECASE)
    for match in pattern.finditer(text):
        _add(
            issues,
            "error" if final_mode else "warning",
            "placeholder.found",
            f"Placeholder bulundu: {match.group(0)}",
            file,
            _line_number(text, match.start()),
            match.group(0),
        )

    if final_mode:
        for match in re.finditer(r"\{[A-Za-z0-9_-]+\}", text):
            _add(
                issues,
                "error",
                "final.placeholder_unresolved",
                "Final modda çözümsüz placeholder kaldı.",
                file,
                _line_number(text, match.start()),
                match.group(0),
            )


def _validate_code_meta(text: str, blocks: list[MetaBlock], issues: list[Issue], file: str) -> None:
    code_ids: dict[str, int] = {}

    for block in [b for b in blocks if b.kind == "CODE_META"]:
        data = block.data

        for required in ["code_id", "file", "validation_mode"]:
            if required not in data:
                _add(
                    issues,
                    "error",
                    "code.required_missing",
                    f"CODE_META alanı eksik: {required}",
                    file,
                    block.line,
                )

        language = data.get("language") or data.get("extension")
        if not language:
            _add(
                issues,
                "warning",
                "code.language_missing",
                "CODE_META içinde language veya extension önerilir.",
                file,
                block.line,
            )

        mode = data.get("validation_mode", "")
        if mode and mode not in VALIDATION_MODES:
            _add(
                issues,
                "error",
                "code.validation_mode_unknown",
                f"Bilinmeyen validation_mode: {mode}",
                file,
                block.line,
            )

        test = data.get("test", "")
        if test and test not in CODE_TEST_MODES:
            _add(issues, "error", "code.test_unknown", f"Bilinmeyen test modu: {test}", file, block.line)

        kind = data.get("kind", "")
        if kind and kind not in CODE_KINDS:
            _add(issues, "warning", "code.kind_unknown", f"Bilinmeyen code kind: {kind}", file, block.line)

        qr_policy = data.get("qr_policy", "")
        if qr_policy and qr_policy not in QR_POLICIES:
            _add(
                issues,
                "error",
                "code.qr_policy_unknown",
                f"Bilinmeyen qr_policy: {qr_policy}",
                file,
                block.line,
            )

        for bool_field in ["extract", "github", "screenshot_required", "intentional_mismatch"]:
            if bool_field in data and _bool_value(data.get(bool_field)) is None:
                _add(
                    issues,
                    "error",
                    f"code.{bool_field}_invalid",
                    f"{bool_field} true veya false olmalıdır.",
                    file,
                    block.line,
                )

        code_id = data.get("code_id", "")
        if code_id:
            if code_id in code_ids:
                _add(issues, "error", "code.id_duplicate", f"Tekrar eden code_id: {code_id}", file, block.line)
            code_ids[code_id] = block.line

        fence = _find_next_code_fence(text, block.end)
        if not fence:
            _add(issues, "error", "code.fence_missing", "CODE_META sonrasında kod bloğu bulunamadı.", file, block.line)
            continue

        lang, _, fence_start, _ = fence
        between = text[block.end:fence_start]
        if re.search(r"(?m)^#{1,6}\s+", between):
            _add(
                issues,
                "error",
                "code.heading_before_fence",
                "CODE_META ile kod bloğu arasına başlık girmiş.",
                file,
                block.line,
            )

        if language and lang and language.casefold() != lang.casefold():
            _add(
                issues,
                "warning",
                "code.lang_mismatch",
                "Kod bloğu dili CODE_META language/extension alanıyla uyuşmuyor.",
                file,
                _line_number(text, fence_start),
                f"{lang} != {language}",
            )

        if (language or "").casefold() == "java":
            intentional_mismatch = _bool_value(data.get("intentional_mismatch")) is True
            declared_file = data.get("file", "").strip().strip("\"'")
            class_match = re.search(r"\bpublic\s+class\s+([A-Za-z_][A-Za-z0-9_]*)", fence[1])
            if declared_file and class_match and not intentional_mismatch:
                expected_class = declared_file.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
                if expected_class.endswith(".java"):
                    expected_class = expected_class[:-5]
                actual_class = class_match.group(1)
                if expected_class and actual_class != expected_class:
                    _add(
                        issues,
                        "error",
                        "java.file_class_mismatch",
                        "Java dosya adı ile public class adı uyuşmuyor.",
                        file,
                        _line_number(text, fence_start),
                        f"{declared_file} != {actual_class}",
                    )


def _validate_mermaid(text: str, blocks: list[MetaBlock], issues: list[Issue], file: str) -> None:
    mermaid_fences = list(re.finditer(r"```mermaid\b", text))
    mermaid_blocks = [b for b in blocks if b.kind == "MERMAID_META"]

    if len(mermaid_fences) != len(mermaid_blocks):
        _add(
            issues,
            "warning",
            "mermaid.meta_count",
            f"Mermaid fence sayısı ile MERMAID_META sayısı farklı: {len(mermaid_fences)} != {len(mermaid_blocks)}",
            file,
        )

    seen_ids: set[str] = set()
    for block in mermaid_blocks:
        mid = block.data.get("id", "")
        if not mid:
            _add(issues, "warning", "mermaid.id_missing", "MERMAID_META id alanı eksik.", file, block.line)
        elif mid in seen_ids:
            _add(issues, "error", "mermaid.duplicate_id", f"Tekrar eden Mermaid id: {mid}", file, block.line)
        seen_ids.add(mid)

        fence = _find_next_code_fence(text, block.end)
        if not fence or fence[0] != "mermaid":
            _add(
                issues,
                "error",
                "mermaid.fence_missing",
                "MERMAID_META sonrasında mermaid kod bloğu bulunamadı.",
                file,
                block.line,
            )


def _validate_screenshots(text: str, blocks: list[MetaBlock], issues: list[Issue], file: str) -> None:
    screenshot_markers = set(re.findall(r"\[SCREENSHOT:([A-Za-z0-9_-]+)\]", text))
    screenshot_meta_ids = {
        block.data.get("id", "")
        for block in blocks
        if block.kind == "SCREENSHOT_META" and block.data.get("id")
    }

    for marker in screenshot_markers:
        if marker not in screenshot_meta_ids:
            _add(
                issues,
                "warning",
                "screenshot.meta_missing",
                f"[SCREENSHOT:{marker}] için SCREENSHOT_META bulunamadı.",
                file,
            )

    for meta_id in screenshot_meta_ids:
        if meta_id not in screenshot_markers:
            _add(
                issues,
                "warning",
                "screenshot.marker_missing",
                f"SCREENSHOT_META id={meta_id} için Markdown marker bulunamadı.",
                file,
            )


def validate(chapter: ParsedChapter, final_mode: bool = False) -> list[Issue]:
    """Bölümü doğrular ve Issue listesi döndürür."""
    issues: list[Issue] = []
    text = chapter.text
    blocks = chapter.meta_blocks
    file_str = str(chapter.path)

    _validate_frontmatter_and_headings(chapter, issues)
    _validate_forbidden_markers(text, issues, file_str)
    _validate_placeholders(text, issues, file_str, final_mode)
    _validate_section_meta(blocks, issues, file_str)
    _validate_code_meta(text, blocks, issues, file_str)
    _validate_mermaid(text, blocks, issues, file_str)
    _validate_screenshots(text, blocks, issues, file_str)

    return issues
