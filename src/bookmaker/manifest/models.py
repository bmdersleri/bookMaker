"""Manifest modelleri — book_manifest.yaml ve pipeline_state.yaml."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field
from ruamel.yaml import YAML

_yaml = YAML()
_yaml.preserve_quotes = True


class ManifestChapter(BaseModel):
    order: int = 0
    chapter_id: str = ""
    source: str = ""
    title: str = ""
    github_slug: str = ""
    status: str = "planned"


class BookInfo(BaseModel):
    title: str = ""
    subtitle: str = ""
    author: str = ""
    lang: str = "tr-TR"
    numbering_policy: str = "build_time"
    automation_profile: str = "academic_technical_book_v1"


class ManifestPaths(BaseModel):
    chapters_dir: str = "chapters"
    assets_auto: str = "assets/auto"
    assets_manual: str = "assets/manual"
    assets_locked: str = "assets/locked"
    assets_final: str = "assets/final"
    build_dir: str = "build"
    dist_dir: str = "dist"


class PandocConfig(BaseModel):
    reference_doc: str = ""
    lua_filter: str = ""
    input_format: str = "markdown+tex_math_single_backslash"


class RepositoryInfo(BaseModel):
    owner: str = ""
    repo: str = ""
    branch: str = "main"
    code_root: str = "kodlar"
    pages_root: str = ""
    raw_root: str = ""


class BookManifest(BaseModel):
    book: BookInfo = Field(default_factory=BookInfo)
    paths: ManifestPaths = Field(default_factory=ManifestPaths)
    pandoc: PandocConfig = Field(default_factory=PandocConfig)
    repository: RepositoryInfo = Field(default_factory=RepositoryInfo)
    chapters: list[ManifestChapter] = Field(default_factory=list)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(self.model_dump(mode="json"), f)

    @classmethod
    def load(cls, path: Path) -> BookManifest:
        with open(path, encoding="utf-8") as f:
            data = _yaml.load(f)
        return cls.model_validate(data)


class ChapterState(BaseModel):
    current_step: str = "planned"
    score: int = 0
    decision: str = "blocked"


class PipelineState(BaseModel):
    book_id: str = ""
    pipeline_id: str = ""
    current_stage: str = "authoring"
    chapters: dict[str, ChapterState] = Field(default_factory=dict)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            _yaml.dump(self.model_dump(mode="json"), f)

    @classmethod
    def load(cls, path: Path) -> PipelineState:
        with open(path, encoding="utf-8") as f:
            data = _yaml.load(f)
        return cls.model_validate(data)
