"""Surum yonetimi modelleri — Version, VersionHistory."""
from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel
from ruamel.yaml import YAML

_yaml = YAML()
_yaml.preserve_quotes = True


class EventType(StrEnum):
    """Surum olay tipleri (seed_created, outline_pasted, vb.)."""

    seed_created = "seed_created"
    seed_updated = "seed_updated"
    seed_approved = "seed_approved"
    outline_prompt_created = "outline_prompt_created"
    outline_pasted = "outline_pasted"
    outline_evaluated = "outline_evaluated"
    outline_revision_packet_created = "outline_revision_packet_created"
    outline_approved = "outline_approved"
    draft_prompt_created = "draft_prompt_created"
    draft_pasted = "draft_pasted"
    draft_normalized = "draft_normalized"
    draft_evaluated = "draft_evaluated"
    draft_revision_packet_created = "draft_revision_packet_created"
    draft_approved = "draft_approved"
    technical_check_started = "technical_check_started"
    technical_check_passed = "technical_check_passed"
    technical_check_failed = "technical_check_failed"
    chapter_approved = "chapter_approved"
    version_restored = "version_restored"
    override_accepted = "override_accepted"


class ChapterStep(StrEnum):
    """Bolum adim durumlari (planned, seeded, ..., ready_for_export)."""

    planned = "planned"
    seeded = "seeded"
    outline_prompt_ready = "outline_prompt_ready"
    outline_pasted = "outline_pasted"
    outline_reviewed = "outline_reviewed"
    outline_revision_required = "outline_revision_required"
    outline_approved = "outline_approved"
    full_text_prompt_ready = "full_text_prompt_ready"
    full_text_pasted = "full_text_pasted"
    normalized = "normalized"
    full_text_reviewed = "full_text_reviewed"
    full_text_revision_required = "full_text_revision_required"
    full_text_approved = "full_text_approved"
    technical_check_running = "technical_check_running"
    technical_check_failed = "technical_check_failed"
    technical_check_passed = "technical_check_passed"
    approved = "approved"
    ready_for_export = "ready_for_export"


class VersionEvent(BaseModel):
    """Bir surum olayini kaydeder — zaman, tur, versiyon, skor."""

    event_id: str
    created_at: str
    chapter_id: str
    event_type: EventType
    artifact_type: str = ""
    artifact_version: str = ""
    path: str = ""
    score: int | None = None
    parent_version: str | None = None
    user_action: bool = True
    notes: str = ""

    def to_jsonl_line(self) -> str:
        """Olayi JSONL satirina donusturur."""
        import json
        return json.dumps(self.model_dump(mode="json"), ensure_ascii=False)

    @classmethod
    def from_jsonl_line(cls, line: str) -> VersionEvent:
        """JSONL satirindan olay yukler."""
        import json
        return cls.model_validate(json.loads(line))


class ActiveVersion(BaseModel):
    """Bir bolumun aktif versiyon ve adim bilgisi."""

    chapter_id: str
    current_step: ChapterStep = ChapterStep.planned
    seed: str | None = None
    outline: str | None = None
    full_text: str | None = None
    approved_chapter: str | None = None

    def to_yaml(self, path: Path) -> None:
        """Aktif versiyonu YAML dosyasina yazar."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(self.model_dump(mode="json"), f)

    @classmethod
    def from_yaml(cls, path: Path) -> ActiveVersion:
        """YAML dosyasindan aktif versiyon yukler."""
        with open(path, encoding="utf-8") as f:
            data = _yaml.load(f)
        return cls.model_validate(data)
