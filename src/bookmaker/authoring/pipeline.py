"""Authoring pipeline — seed → outline → draft → approve."""

from __future__ import annotations

from pathlib import Path

from bookmaker.chapter.parser import parse
from bookmaker.chapter.scoring import make_report
from bookmaker.chapter.validator import validate
from bookmaker.manifest.manager import ManifestManager
from bookmaker.manifest.models import ChapterState
from bookmaker.manifest.pipeline import PipelineManager
from bookmaker.models.book import ChapterSeed
from bookmaker.storage.files import (
    approved_path,
    chapter_workspace,
    draft_path,
    outline_path,
    seed_path,
)


def _ensure_workspace(project_root: Path, chapter_id: str) -> None:
    ws = chapter_workspace(project_root, chapter_id)
    for sub in ["seed", "outline_versions", "draft_versions", "approved"]:
        (ws / sub).mkdir(parents=True, exist_ok=True)


class AuthoringPipeline:
    """Bolum yazim pipeline'i — durum makinesi."""

    VALID_STEPS = {
        "planned", "seeded", "outline_prompt_ready", "outline_pasted",
        "outline_reviewed", "outline_revision_required", "outline_approved",
        "full_text_prompt_ready", "full_text_pasted", "normalized",
        "full_text_reviewed", "full_text_revision_required", "full_text_approved",
        "technical_check_running", "technical_check_failed", "technical_check_passed",
        "approved", "ready_for_export",
    }

    def __init__(self, project_root: Path) -> None:
        self.root = project_root.resolve()
        self.manifest_mgr = ManifestManager(self.root)
        self.pipeline_mgr = PipelineManager(self.root)

    def get_state(self, chapter_id: str) -> ChapterState:
        state = self.pipeline_mgr.load()
        return state.chapters.get(chapter_id, ChapterState())

    def set_state(self, chapter_id: str, **kwargs) -> ChapterState:
        return self.pipeline_mgr.update_chapter(chapter_id, **kwargs)

    def advance(self, chapter_id: str, target_step: str) -> ChapterState:
        assert target_step in self.VALID_STEPS, f"Invalid step: {target_step}"
        return self.set_state(chapter_id, current_step=target_step)

    def seed(self, chapter_id: str, **fields) -> ChapterSeed:
        _ensure_workspace(self.root, chapter_id)
        seed = ChapterSeed(chapter_id=chapter_id, **fields)
        seed.to_yaml(seed_path(self.root, chapter_id))
        self.advance(chapter_id, "seeded")
        return seed

    def load_seed(self, chapter_id: str) -> ChapterSeed | None:
        sp = seed_path(self.root, chapter_id)
        if not sp.exists():
            return None
        return ChapterSeed.from_yaml(sp)

    def make_outline_prompt(self, chapter_id: str) -> str:
        seed = self.load_seed(chapter_id)
        if not seed:
            return ""
        manifest = self.manifest_mgr.load_or_generate()
        book_title = manifest.book.title or "Kitap"
        lines = [
            f"# Outline Prompt — {chapter_id}",
            f"**Kitap:** {book_title}",
            f"**Bolum:** {chapter_id}",
            "",
            "## Bolum Amaci",
            seed.purpose or "(belirtilmemis)",
            "",
            "## Ogrenme Ciktilari",
        ]
        for o in seed.learning_outcomes:
            lines.append(f"- {o}")
        lines += ["", "## Zorunlu Kavramlar"]
        for c in seed.mandatory_concepts:
            lines.append(f"- {c}")
        lines += ["", "## Kapsam Disi"]
        for o in seed.out_of_scope:
            lines.append(f"- {o}")
        lines += [
            "",
            "Yukaridaki girdiye gore ayrintili bir outline hazirla.",
        ]
        self.advance(chapter_id, "outline_prompt_ready")
        return "\n".join(lines)

    def paste_outline(self, chapter_id: str, outline_text: str, version: str = "v001") -> Path:
        p = outline_path(self.root, chapter_id, version)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(outline_text, encoding="utf-8")
        self.advance(chapter_id, "outline_pasted")
        return p

    def review_outline(self, chapter_id: str, outline_version: str = "v001") -> dict:
        seed = self.load_seed(chapter_id)
        outline_p = outline_path(self.root, chapter_id, outline_version)
        if not outline_p.exists() or not seed:
            return {"decision": "blocked", "message": "Seed veya outline bulunamadi."}
        text = outline_p.read_text(encoding="utf-8")
        import re
        lines = text.splitlines()
        headings = []
        for i, line in enumerate(lines, 1):
            m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
            if m:
                from bookmaker.chapter.parser import Heading
                headings.append(Heading(
                    level=len(m.group(1)), title=m.group(2).strip(), line=i,
                ))
        issues = []
        h1 = [h for h in headings if h.level == 1]
        if len(h1) != 1:
            issues.append("Outline tek H1 baslik icermeli.")
        h2 = [h for h in headings if h.level == 2]
        if len(h2) < 3:
            issues.append("Outline en az 3 H2 alt baslik icermeli.")
        for concept in seed.mandatory_concepts:
            if concept.lower() not in text.lower():
                issues.append(f"Zorunlu kavram outline'da bulunamadi: {concept}")
        decision = "pass" if len(issues) == 0 else "revision_required"
        if decision == "pass":
            self.advance(chapter_id, "outline_reviewed")
        else:
            self.advance(chapter_id, "outline_revision_required")
        return {
            "decision": decision,
            "issues": issues,
            "heading_count_h1": len(h1),
            "heading_count_h2": len(h2),
        }

    def make_draft_prompt(self, chapter_id: str, outline_version: str = "v001") -> str:
        seed = self.load_seed(chapter_id)
        outline_p = outline_path(self.root, chapter_id, outline_version)
        if not seed or not outline_p.exists():
            return ""
        outline = outline_p.read_text(encoding="utf-8")
        manifest = self.manifest_mgr.load_or_generate()
        book_title = manifest.book.title or "Kitap"
        lines = [
            f"# Tam Metin Promptu — {chapter_id}",
            f"**Kitap:** {book_title}",
            "",
            "## Seed",
            seed.purpose or "",
            "",
            "## Outline",
            outline,
            "",
            "Yukaridaki seed ve outline'a gore CHAPTER_SPEC.md uyumlu",
            "tam bolum Markdown metnini CODE_META bloklariyla birlikte uret.",
        ]
        self.advance(chapter_id, "full_text_prompt_ready")
        return "\n".join(lines)

    def paste_draft(self, chapter_id: str, draft_text: str, version: str = "v001") -> Path:
        p = draft_path(self.root, chapter_id, version)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(draft_text, encoding="utf-8")
        self.advance(chapter_id, "full_text_pasted")
        return p

    def review_draft(self, chapter_id: str, draft_version: str = "v001") -> dict:
        dp = draft_path(self.root, chapter_id, draft_version)
        if not dp.exists():
            return {"decision": "blocked", "message": "Draft bulunamadi."}
        parsed = parse(dp)
        issues = validate(parsed)
        report = make_report(chapter_id, issues)
        self.set_state(chapter_id, score=report.score, decision=report.decision.value)
        if report.decision.value == "blocked":
            self.advance(chapter_id, "full_text_revision_required")
        elif report.decision.value in ("pass", "pass_with_warnings"):
            self.advance(chapter_id, "full_text_reviewed")
        else:
            self.advance(chapter_id, "full_text_revision_required")
        return {
            "decision": report.decision.value,
            "score": report.score,
            "error_count": report.error_count,
            "warning_count": report.warning_count,
        }

    def approve(self, chapter_id: str, draft_version: str = "v001") -> Path:
        dp = draft_path(self.root, chapter_id, draft_version)
        if not dp.exists():
            raise FileNotFoundError(f"Draft bulunamadi: {dp}")
        ap = approved_path(self.root, chapter_id)
        ap.write_text(dp.read_text(encoding="utf-8"), encoding="utf-8")
        self.advance(chapter_id, "approved")
        return ap
