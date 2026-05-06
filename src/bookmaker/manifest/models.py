from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from ruamel.yaml import YAML

_yaml = YAML()
_yaml.default_flow_style = False


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = _yaml.load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML kökü mapping olmalıdır: {path}")
    return data


def _save_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        _yaml.dump(data, f)


class BookInfo(BaseModel):
    """Book identity section for book_manifest.yaml.

    A few legacy fields are kept optional so older manager/pipeline code can
    import and mutate BookManifest without immediately breaking.
    """

    title: str = ""
    subtitle: str | None = None
    author: str = ""
    alias: str = ""
    repo: str | None = None
    language: str = "tr"
    lang: str | None = None
    version: str = "1.0.0"
    edition: str = "1"
    year: int | str | None = None
    automation_profile: str | None = None


class ProductionConfig(BaseModel):
    producer_model: str = "deepseek-chat"
    observer_model: str = "deepseek-chat"
    producer_params: dict[str, Any] = Field(
        default_factory=lambda: {
            "temperature": 0.7,
            "max_tokens": 8000,
        }
    )
    observer_params: dict[str, Any] = Field(
        default_factory=lambda: {
            "temperature": 0.3,
            "max_tokens": 4000,
        }
    )
    generation_mode: str = "chapter_based"
    approval_required: bool = True


class StyleConfig(BaseModel):
    target_audience: str = ""
    tone: str = "akademik ama sade"
    code_language: str = ""
    framework: str | None = None
    terminology: str | None = None
    chapter_pattern: list[str] = Field(default_factory=list)


class TechnicalProfile(BaseModel):
    model_config = ConfigDict(extra="allow")


class AutomationConfig(BaseModel):
    code_meta_required: bool = True
    screenshot_required: bool = False
    minimum_screenshots_per_chapter: int = 0
    qr_policy: str = "none"
    github_code_export: bool = False
    manual_asset_override: bool = False


class BookChapterRef(BaseModel):
    """Chapter entry in book_manifest.yaml.

    New project-based manifests only need alias. Legacy code/tests may still
    refer to order, chapter_id, title, source or github_slug; they are accepted
    here to keep collection/import stable during migration.
    """

    alias: str = ""
    order: int = 0
    chapter_id: str | None = None
    title: str | None = None
    source: str | None = None
    github_slug: str | None = None

    def effective_alias(self) -> str:
        return self.alias or self.chapter_id or ""


# Backward-compatible public name expected by older tests.
ManifestChapter = BookChapterRef


class BookManifest(BaseModel):
    book: BookInfo = Field(default_factory=BookInfo)
    production: ProductionConfig = Field(default_factory=ProductionConfig)
    style: StyleConfig = Field(default_factory=StyleConfig)
    technical_profile: TechnicalProfile | None = None
    automation: AutomationConfig = Field(default_factory=AutomationConfig)
    chapters: list[BookChapterRef] = Field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> BookManifest:
        return cls.model_validate(_load_yaml(path))

    def save(self, path: Path) -> None:
        _save_yaml(path, self.model_dump(mode="json", exclude_none=True))

    def chapter_aliases(self) -> list[str]:
        return [chapter.effective_alias() for chapter in self.chapters if chapter.effective_alias()]


class ChapterReference(BaseModel):
    alias: str
    relation: str = "related"


class SectionDef(BaseModel):
    title: str
    type: str = "text"


class ScopeConfig(BaseModel):
    topics: list[str] = Field(default_factory=list)
    objectives: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)
    mini_project: str | None = None


class StructureConfig(BaseModel):
    sections: list[SectionDef] = Field(default_factory=list)
    estimated_pages: int | None = None
    code_examples_count: int | None = None
    screenshot_examples_count: int | None = None


class ChapterAutomation(BaseModel):
    code_meta_required: bool = True
    screenshot_required: bool = False
    default_code_language: str | None = None
    default_framework: str | None = None
    validation_modes: list[str] = Field(default_factory=list)
    github_export: bool = False
    qr_policy: str = "none"


class ChapterInfo(BaseModel):
    title: str
    alias: str
    order: int
    references: list[ChapterReference] = Field(default_factory=list)


class ChapterManifest(BaseModel):
    chapter: ChapterInfo
    scope: ScopeConfig = Field(default_factory=ScopeConfig)
    structure: StructureConfig = Field(default_factory=StructureConfig)
    automation: ChapterAutomation = Field(default_factory=ChapterAutomation)

    @classmethod
    def load(cls, path: Path) -> ChapterManifest:
        return cls.model_validate(_load_yaml(path))

    def save(self, path: Path) -> None:
        _save_yaml(path, self.model_dump(mode="json", exclude_none=True))


class ChapterState(BaseModel):
    """Backward-compatible chapter runtime state.

    Older authoring/pipeline code expects this object and mutates attributes
    such as current_step, score and decision. The new project-based state uses
    ChapterPipelineEntry, but keeping this lightweight model avoids import
    failures while the rest of the system is migrated.
    """

    model_config = ConfigDict(extra="allow")

    current_step: str = "planned"
    score: float | int | None = None
    decision: str | None = None
    updated_at: str | None = None


class ChapterStatus(BaseModel):
    state: str = "pending"
    draft_generated: bool = False
    review_completed: bool = False
    revision_required: bool = False
    final_approved: bool = False
    exported: bool = False
    quality_score: float | None = None
    last_review: str | None = None
    last_updated: str | None = None
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class ChapterAutomationState(BaseModel):
    code_extraction_done: bool = False
    code_tests_done: bool = False
    screenshots_done: bool = False
    qr_generation_done: bool = False
    github_links_patched: bool = False


class ChapterPipelineEntry(BaseModel):
    alias: str
    order: int
    status: ChapterStatus = Field(default_factory=ChapterStatus)
    automation: ChapterAutomationState = Field(default_factory=ChapterAutomationState)


class InputPolicy(BaseModel):
    use_book_manifest: bool = True
    use_chapter_manifest: bool = True
    use_chapter_prompt_if_exists: bool = True
    fallback_to_default_chapter_prompt: bool = True


class ReviewPolicy(BaseModel):
    observer_review_required: bool = True
    fallback_to_default_review_prompt: bool = True
    minimum_quality_score_for_approval: int = 85


class ProductionContext(BaseModel):
    producer_model: str = "deepseek-chat"
    observer_model: str = "deepseek-chat"
    generation_mode: str = "chapter_based"
    approval_required: bool = True
    default_input_policy: InputPolicy = Field(default_factory=InputPolicy)
    review_policy: ReviewPolicy = Field(default_factory=ReviewPolicy)


class QualityGatesPerChapter(BaseModel):
    manifest_exists: bool = True
    draft_required: bool = True
    review_required_before_final: bool = True
    final_required_for_export: bool = True
    unresolved_placeholders_allowed: bool = False
    code_meta_required_for_extractable_code: bool = True
    screenshot_marker_required: bool = True


class QualityGatesBookLevel(BaseModel):
    chapter_order_from_book_manifest: bool = True
    chapter_alias_references_only: bool = True
    no_framework_files_inside_project: bool = True
    exports_stay_inside_project: bool = True


class QualityGates(BaseModel):
    per_chapter: QualityGatesPerChapter = Field(default_factory=QualityGatesPerChapter)
    book_level: QualityGatesBookLevel = Field(default_factory=QualityGatesBookLevel)


class ExportState(BaseModel):
    merged_markdown_generated: bool = False
    docx_generated: bool = False
    pdf_generated: bool = False
    last_export_version: str | None = None
    last_exported_at: str | None = None
    included_chapters: list[str] = Field(default_factory=list)


class PipelineInfo(BaseModel):
    schema_version: str = "1.0"
    book_alias: str = ""
    current_version: str = "v001"
    global_state: str = "initialized"
    created_at: str = ""
    updated_at: str = ""
    active_chapter: str | None = None
    last_completed_chapter: str | None = None
    next_action: str | None = None


class HistoryEntry(BaseModel):
    at: str
    event: str
    note: str = ""


class PipelineState(BaseModel):
    pipeline: PipelineInfo = Field(default_factory=PipelineInfo)
    production_context: ProductionContext = Field(default_factory=ProductionContext)
    quality_gates: QualityGates = Field(default_factory=QualityGates)

    # New manifests use a list[ChapterPipelineEntry]. Legacy pipeline manager
    # uses dict[str, ChapterState]. Accept both during migration.
    chapters: list[ChapterPipelineEntry] | dict[str, ChapterState] = Field(default_factory=list)

    export_state: ExportState = Field(default_factory=ExportState)
    history: list[HistoryEntry] = Field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> PipelineState:
        return cls.model_validate(_load_yaml(path))

    def save(self, path: Path) -> None:
        _save_yaml(path, self.model_dump(mode="json", exclude_none=True))

    @classmethod
    def init_from_book_manifest(
        cls,
        manifest: BookManifest,
        created_at: str,
        current_version: str = "v001",
        active_chapter: str | None = None,
    ) -> PipelineState:
        aliases = manifest.chapter_aliases()
        active = active_chapter or (aliases[0] if aliases else None)
        return cls(
            pipeline=PipelineInfo(
                book_alias=manifest.book.alias,
                current_version=current_version,
                created_at=created_at,
                updated_at=created_at,
                active_chapter=active,
                next_action=(
                    f"İlk taslak için chapters/{active}/prompt.md kullanılacak."
                    if active else "Kitap bölüm listesi boş."
                ),
            ),
            production_context=ProductionContext(
                producer_model=manifest.production.producer_model,
                observer_model=manifest.production.observer_model,
                generation_mode=manifest.production.generation_mode,
                approval_required=manifest.production.approval_required,
            ),
            chapters=[
                ChapterPipelineEntry(alias=alias, order=index + 1)
                for index, alias in enumerate(aliases)
            ],
            history=[
                HistoryEntry(
                    at=created_at,
                    event="pipeline_initialized",
                    note="pipeline_state.yaml book_manifest.yaml üzerinden oluşturuldu.",
                )
            ],
        )

    def sync_chapters(self, manifest: BookManifest) -> None:
        if isinstance(self.chapters, dict):
            existing: dict[str, ChapterState | ChapterPipelineEntry] = self.chapters
        else:
            existing = {entry.alias: entry for entry in self.chapters}

        synced: list[ChapterPipelineEntry] = []
        for index, alias in enumerate(manifest.chapter_aliases(), start=1):
            entry = existing.get(alias)
            if isinstance(entry, ChapterPipelineEntry):
                entry.order = index
                synced.append(entry)
            else:
                synced.append(ChapterPipelineEntry(alias=alias, order=index))

        self.chapters = synced
        self.pipeline.book_alias = manifest.book.alias

    def get_chapter(self, alias: str) -> ChapterPipelineEntry | ChapterState | None:
        if isinstance(self.chapters, dict):
            return self.chapters.get(alias)
        for entry in self.chapters:
            if entry.alias == alias:
                return entry
        return None
