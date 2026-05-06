from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator
from ruamel.yaml import YAML

_yaml = YAML()
_yaml.preserve_quotes = True


class ExportTarget(StrEnum):
    docx = "docx"
    pdf = "pdf"
    epub = "epub"
    mkdocs = "mkdocs"
    html = "html"


class ChapterType(StrEnum):
    core = "core"
    appendix = "appendix"
    intro = "intro"
    lab = "lab"


class ChapterStatus(StrEnum):
    planned = "planned"
    seeded = "seeded"
    outline_approved = "outline_approved"
    full_text_approved = "full_text_approved"
    approved = "approved"
    ready_for_export = "ready_for_export"


class BookProfile(BaseModel):
    book_id: str
    title: str
    subtitle: str = ""
    author: str = ""
    language: str = "tr-TR"
    audience: str = ""
    level: str = "beginner"
    domain: str = "programming"
    primary_code_language: str = "java"
    export_targets: list[ExportTarget] = Field(default_factory=lambda: [ExportTarget.docx])
    quality_profile: str = "academic_technical_book_v1"

    @field_validator("book_id")
    @classmethod
    def book_id_is_slug(cls, v: str) -> str:
        import re
        if not re.match(r"^[a-z0-9_-]+$", v):
            raise ValueError("book_id sadece küçük harf, rakam, _ ve - içerebilir")
        return v

    def to_yaml(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(self.model_dump(mode="json"), f)

    @classmethod
    def from_yaml(cls, path: Path) -> BookProfile:
        with open(path, encoding="utf-8") as f:
            data = _yaml.load(f)
        return cls.model_validate(data)


class ChapterArchEntry(BaseModel):
    chapter_id: str
    order: int
    title: str
    chapter_type: ChapterType = ChapterType.core
    status: ChapterStatus = ChapterStatus.planned
    purpose: str = ""
    expected_learning_outcomes: list[str] = Field(default_factory=list)
    mandatory_concepts: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)


class BookArchitecture(BaseModel):
    book_id: str
    chapters: list[ChapterArchEntry] = Field(default_factory=list)

    @field_validator("chapters")
    @classmethod
    def orders_unique(cls, v: list[ChapterArchEntry]) -> list[ChapterArchEntry]:
        orders = [c.order for c in v]
        if len(orders) != len(set(orders)):
            raise ValueError("chapter order değerleri benzersiz olmalı")
        ids = [c.chapter_id for c in v]
        if len(ids) != len(set(ids)):
            raise ValueError("chapter_id değerleri benzersiz olmalı")
        return sorted(v, key=lambda c: c.order)

    def to_yaml(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(self.model_dump(mode="json"), f)

    @classmethod
    def from_yaml(cls, path: Path) -> BookArchitecture:
        with open(path, encoding="utf-8") as f:
            data = _yaml.load(f)
        return cls.model_validate(data)


class ChapterSeed(BaseModel):
    chapter_id: str
    purpose: str = ""
    target_reader_state: str = ""
    learning_outcomes: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    mandatory_concepts: list[str] = Field(default_factory=list)
    required_examples: list[str] = Field(default_factory=list)
    required_code_items: list[str] = Field(default_factory=list)
    intentional_mismatch_examples: list[str] = Field(default_factory=list)
    required_diagrams: list[str] = Field(default_factory=list)
    required_assets: list[str] = Field(default_factory=list)
    mini_application: str = ""
    common_mistakes: list[str] = Field(default_factory=list)
    exercises: list[str] = Field(default_factory=list)
    lab_task: str = ""
    out_of_scope: list[str] = Field(default_factory=list)
    author_notes: str = ""

    def is_ready(self) -> bool:
        """Seed onaylanabilir mi? Zorunlu alanlar dolu mu?"""
        return bool(
            self.purpose
            and self.learning_outcomes
            and self.mandatory_concepts
            and self.out_of_scope
        )

    def to_yaml(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(self.model_dump(mode="json"), f)

    @classmethod
    def from_yaml(cls, path: Path) -> ChapterSeed:
        with open(path, encoding="utf-8") as f:
            data = _yaml.load(f)
        return cls.model_validate(data)
