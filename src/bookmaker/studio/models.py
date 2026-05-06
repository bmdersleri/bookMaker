"""Pydantic request/response modelleri — bookMaker Studio API'si."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

# ================================================================
# CHAPTER
# ================================================================

class ChapterOut(BaseModel):
    """Bölüm bilgisi (response)."""
    chapter_id: str
    title: str
    order: int
    status: str = "planned"
    current_step: str = "planned"
    score: int = 0
    decision: str = "unknown"
    errors: int = 0


class ChapterCreate(BaseModel):
    """Yeni bölüm (request)."""
    chapter_id: str = Field(..., pattern=r"^[a-z0-9_-]+$")
    title: str = Field(..., min_length=1, max_length=200)
    order: int | None = None


class ChapterUpdate(BaseModel):
    """Bölüm güncelleme (request)."""
    title: str | None = None
    order: int | None = None
    status: str | None = None


class ChapterReorder(BaseModel):
    """Bölüm sırası güncelleme (request)."""
    chapter_ids: list[str] = Field(..., min_length=1)


# ================================================================
# GENERATE / PIPELINE
# ================================================================

class GenerateRequest(BaseModel):
    """Pipeline başlatma parametreleri."""
    title: str | None = None
    concepts: list[str] = Field(default_factory=list)
    enrich_types: list[str] = Field(
        default_factory=lambda: ["ozet", "sozluk", "soru", "alistirma", "hata", "kopru"]
    )
    temperature: float = Field(default=0.7, ge=0.0, le=1.5)


class GenerateResponse(BaseModel):
    """Pipeline sonuç (REST)."""
    chapter_id: str
    title: str
    elapsed_s: float = 0
    spec_words: int = 0
    seed_words: int = 0
    final_words: int = 0
    enriched_count: int = 0
    path: str | None = None
    error: str | None = None


# ================================================================
# JOB
# ================================================================

class JobOut(BaseModel):
    """İş durumu."""
    id: str
    step: str  # generate, build, extract, render
    chapter_id: str
    status: str  # queued, running, done, error, cancelled
    created_at: str
    started_at: str | None = None
    finished_at: str | None = None
    elapsed_s: float | None = None
    summary: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class JobCreate(BaseModel):
    """Yeni iş oluşturma."""
    step: str = "generate"
    chapter_id: str
    params: dict[str, Any] = Field(default_factory=dict)


# ================================================================
# LLM
# ================================================================

class LlmConfigRequest(BaseModel):
    """LLM yapılandırma."""
    provider: str = "deepseek"
    api_key: str = Field(..., min_length=1)
    model: str = "deepseek-chat"


class LlmStatusOut(BaseModel):
    """LLM durumu."""
    status: str
    provider: str = ""
    model: str = ""
    configured: bool = False


# ================================================================
# PROJECT
# ================================================================

class ProjectOut(BaseModel):
    """Proje bilgisi."""
    title: str = "(isimsiz)"
    chapters: int = 0
    author: str = "—"
    stage: str = "authoring"
    stage_counts: dict[str, int] = Field(default_factory=dict)


class PipelineStateOut(BaseModel):
    """Pipeline durumu."""
    pipeline_id: str = ""
    current_stage: str = ""
    chapters: dict[str, Any] = Field(default_factory=dict)


# ================================================================
# WIZARD
# ================================================================

class BookCreateRequest(BaseModel):
    """Yeni kitap oluşturma."""
    project_name: str = Field(..., pattern=r"^[a-z0-9_-]+$")
    title: str = Field(..., min_length=1, max_length=100)
    title_en: str | None = None
    author: str = Field(..., min_length=1)
    language: str = "tr"
    chapter_count: int = Field(default=23, ge=1, le=50)


class WizardPlanRequest(BaseModel):
    """LLM bölüm planı oluşturma."""
    topic: str = Field(..., min_length=3)
    chapter_count: int = 23
    appendix_count: int = 4
    language: str = "tr"


# ================================================================
# BUILD
# ================================================================

class BuildResult(BaseModel):
    """Build sonucu."""
    chapter_id: str
    compiled: int = 0
    extracted: int = 0
    total: int = 0
    error: str | None = None


class ExportRequest(BaseModel):
    """Export isteği."""
    format: str = Field(..., pattern=r"^(docx|pdf|epub|html)$")
    chapter_ids: list[str] | None = None  # None = tüm kitap
    reference_docx: str | None = None


# ================================================================
# HEALTH / STATUS
# ================================================================

class StatusOut(BaseModel):
    """Sunucu durumu."""
    status: str = "running"
    version: str = "0.1.0"
    uptime: str = "active"
