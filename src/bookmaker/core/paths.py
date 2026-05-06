from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ChapterPaths:
    """Convention-based paths for one chapter."""

    root: Path

    @property
    def alias(self) -> str:
        return self.root.name

    @property
    def manifest(self) -> Path:
        return self.root / "chapter_manifest.yaml"

    @property
    def prompt(self) -> Path:
        return self.root / "prompt.md"

    @property
    def content_dir(self) -> Path:
        return self.root / "content"

    @property
    def draft(self) -> Path:
        return self.content_dir / "draft.md"

    @property
    def final(self) -> Path:
        return self.content_dir / "final.md"

    @property
    def revisions_dir(self) -> Path:
        return self.content_dir / "revisions"


@dataclass(frozen=True)
class BookPaths:
    """Convention-based paths for a book project."""

    root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "root", self.root.resolve())

    @property
    def book_manifest(self) -> Path:
        return self.root / "book_manifest.yaml"

    @property
    def pipeline_state(self) -> Path:
        return self.root / "pipeline_state.yaml"

    @property
    def prompts_dir(self) -> Path:
        return self.root / "prompts"

    @property
    def default_chapter_prompt(self) -> Path:
        return self.prompts_dir / "default_chapter.md"

    @property
    def default_review_prompt(self) -> Path:
        return self.prompts_dir / "default_review.md"

    @property
    def chapters_dir(self) -> Path:
        return self.root / "chapters"

    @property
    def exports_dir(self) -> Path:
        return self.root / "exports"

    @property
    def exports_docx_dir(self) -> Path:
        return self.exports_dir / "docx"

    @property
    def exports_pdf_dir(self) -> Path:
        return self.exports_dir / "pdf"

    @property
    def exports_md_dir(self) -> Path:
        return self.exports_dir / "md"

    @property
    def logs_dir(self) -> Path:
        return self.root / "logs"

    @property
    def logs_production_dir(self) -> Path:
        return self.logs_dir / "production"

    @property
    def logs_errors_dir(self) -> Path:
        return self.logs_dir / "errors"

    @property
    def logs_reviews_dir(self) -> Path:
        return self.logs_dir / "reviews"

    def chapter(self, alias: str) -> ChapterPaths:
        return ChapterPaths(self.chapters_dir / alias)

    def ensure_base_dirs(self) -> None:
        for path in [
            self.prompts_dir,
            self.chapters_dir,
            self.exports_docx_dir,
            self.exports_pdf_dir,
            self.exports_md_dir,
            self.logs_production_dir,
            self.logs_errors_dir,
            self.logs_reviews_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def discover(cls, start: Path | None = None) -> BookPaths:
        """Find the nearest parent containing book_manifest.yaml."""
        current = (start or Path.cwd()).resolve()
        if current.is_file():
            current = current.parent
        for candidate in [current, *current.parents]:
            if (candidate / "book_manifest.yaml").exists():
                return cls(candidate)
        raise FileNotFoundError(
            f"book_manifest.yaml bulunamadı. Başlangıç noktası: {current}"
        )
