"""FastAPI uygulaması — route'lar + aktif kitap sistemi."""

from __future__ import annotations

from pathlib import Path

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, HTMLResponse
    from fastapi.staticfiles import StaticFiles
except ImportError:
    FastAPI = None  # type: ignore

from bookmaker.studio.services import (
    assemble_service,
    book_service,
    build_service,
    chapter_service,
    export_service,
    generation_service,
    llm_service,
    observer_service,
    pipeline_service,
    prompt_service,
    quality_service,
    wizard_service,
)

app: FastAPI | None = None

# ================================================================
# AKTIF KITAP SISTEMI
# ================================================================
_active_book: str | None = None
_CONFIG_FILE = "build/studio_config.json"


def _manifest_book_info(project_root: Path) -> dict[str, str]:
    manifest_path = project_root / "book_manifest.yaml"
    if not manifest_path.exists():
        return {}
    try:
        from bookmaker.manifest.models import BookManifest

        manifest = BookManifest.load(manifest_path)
    except Exception:
        return {}
    return {
        "name": manifest.book.alias or project_root.name,
        "title": manifest.book.title or project_root.name,
        "author": manifest.book.author or "",
    }


def _project_search_roots(root: Path) -> list[Path]:
    candidates = [
        root / "book_projects",
        root.parent if root.parent.name == "book_projects" else None,
        Path.cwd() / "book_projects",
    ]
    result: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate is None:
            continue
        resolved = candidate.resolve()
        if resolved not in seen:
            result.append(resolved)
            seen.add(resolved)
    return result


def get_active_book() -> Path:
    """Aktif kitap dizinini döndürür, yoksa CWD kullanır."""
    global _active_book
    if _active_book is not None:
        return Path(_active_book).resolve()
    cfg = Path.cwd() / _CONFIG_FILE
    if cfg.exists():
        import json as _json
        try:
            d = _json.loads(cfg.read_text(encoding="utf-8"))
            p = d.get("active_book", "")
            if p and Path(p).exists():
                _active_book = p
                return Path(p).resolve()
        except Exception:
            pass
    return Path.cwd()


def save_active_book(path_str: str) -> None:
    """Aktif kitap yolunu kaydeder."""
    global _active_book
    cfg = Path.cwd() / _CONFIG_FILE
    cfg.parent.mkdir(parents=True, exist_ok=True)
    import json as _json
    cfg.write_text(
        _json.dumps({"active_book": str(path_str)},
                     ensure_ascii=False, indent=2),
        encoding="utf-8")
    _active_book = path_str


if FastAPI is not None:
    app = FastAPI(title="bookMaker Studio", version="0.2.0")
    _root = Path(__file__).parent.resolve()
    _static = _root / "static"
    _templates = _root / "templates"

    app.add_middleware(CORSMiddleware, allow_origins=["*"],
                       allow_methods=["*"], allow_headers=["*"])
    _static.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(_static)), name="static")

    @app.get("/output/{file_path:path}")
    async def serve_output(file_path: str):
        """Project output dosyalarını güvenli şekilde sunar."""
        from fastapi.responses import PlainTextResponse

        root = get_active_book().resolve()
        rel = Path(file_path)
        if rel.is_absolute() or any(part == ".." for part in rel.parts):
            return PlainTextResponse("Forbidden", status_code=403)
        if not rel.parts or rel.parts[0] not in {"exports", "logs", "build"}:
            return PlainTextResponse("Forbidden", status_code=403)
        full = (root / rel).resolve()
        if not full.is_relative_to(root):
            return PlainTextResponse("Forbidden", status_code=403)
        if not full.exists():
            return PlainTextResponse("Not found", status_code=404)
        return FileResponse(str(full))

    # ================================================================
    # HTML Dashboard
    # ================================================================
    def _read_index() -> str:
        idx = _templates / "index.html"
        if idx.exists():
            return idx.read_text(encoding="utf-8")
        return "<html><body><h1>Template not found</h1></body></html>"

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return _read_index()

    # ================================================================
    # Active Book & Projects
    # ================================================================
    @app.get("/api/projects")
    async def api_projects() -> list[dict]:
        root = get_active_book()
        bp = None
        for candidate in _project_search_roots(root):
            if candidate.exists():
                bp = candidate
                break
        if not bp or not bp.exists():
            return []

        projects = []
        for d in sorted(bp.iterdir()):
            if not d.is_dir():
                continue
            info = _manifest_book_info(d)
            if not info:
                continue
            projects.append({"name": info["name"], "path": str(d), "title": info["title"]})
        return projects

    @app.get("/api/active-book")
    async def api_active_book_get() -> dict:
        root = get_active_book()
        info = _manifest_book_info(root)
        name = info.get("name") or root.name
        title = info.get("title") or name
        return {"path": str(root), "name": name, "title": title}

    @app.post("/api/active-book")
    async def api_active_book_set(data: dict) -> dict:
        book_path = data.get("path", "")
        if not book_path or not Path(book_path).exists():
            return {"error": "Geçersiz kitap yolu"}
        save_active_book(book_path)
        name = Path(book_path).name
        return {"path": book_path, "name": name, "status": "ok"}

    # ================================================================
    # Status
    # ================================================================
    @app.get("/api/status")
    async def api_status() -> dict:
        return {"status": "running", "version": "0.2.0"}

    @app.get("/api/project")
    async def api_project() -> dict:
        return book_service.get_project_info(get_active_book())

    @app.get("/api/pipeline-state")
    async def api_pipeline_state() -> dict:
        return pipeline_service.get_pipeline_state(get_active_book())

    # ================================================================
    # Chapters
    # ================================================================
    @app.get("/api/chapters")
    async def api_chapters() -> list[dict]:
        return chapter_service.get_chapter_list(get_active_book())

    @app.post("/api/chapters")
    async def api_chapter_create(data: dict) -> dict:
        return chapter_service.add_chapter(
            get_active_book(), data.get("chapter_id", ""),
            data.get("title", ""), data.get("order"))

    @app.put("/api/chapters/reorder")
    async def api_chapter_reorder(data: dict) -> dict:
        return chapter_service.reorder_chapters(
            get_active_book(), data.get("chapter_ids", []))

    @app.put("/api/chapters/{chapter_id}")
    async def api_chapter_update(chapter_id: str, data: dict) -> dict:
        return chapter_service.update_chapter(
            get_active_book(), chapter_id, data)

    @app.delete("/api/chapters/{chapter_id}")
    async def api_chapter_delete(chapter_id: str) -> dict:
        return chapter_service.remove_chapter(
            get_active_book(), chapter_id)

    # ================================================================
    # Prompts
    # ================================================================
    @app.get("/api/prompts/default/{prompt_type}")
    async def api_default_prompt_get(prompt_type: str) -> dict:
        return prompt_service.get_default_prompt(get_active_book(), prompt_type)

    @app.put("/api/prompts/default/{prompt_type}")
    async def api_default_prompt_save(prompt_type: str, data: dict) -> dict:
        return prompt_service.save_default_prompt(
            get_active_book(), data.get("content", ""), prompt_type)

    @app.get("/api/prompts/chapter/{chapter_id}")
    async def api_chapter_prompt_get(chapter_id: str) -> dict:
        return prompt_service.get_chapter_prompt(get_active_book(), chapter_id)

    @app.put("/api/prompts/chapter/{chapter_id}")
    async def api_chapter_prompt_save(chapter_id: str, data: dict) -> dict:
        return prompt_service.save_chapter_prompt(
            get_active_book(), chapter_id, data.get("content", ""))

    # ================================================================
    # Content & Quality
    # ================================================================
    @app.get("/api/view/{chapter_id}")
    async def api_view(chapter_id: str) -> dict:
        return quality_service.get_chapter_content(
            get_active_book(), chapter_id)

    @app.get("/api/check/{chapter_id}")
    async def api_check(chapter_id: str) -> dict:
        return quality_service.validate_chapter(
            get_active_book(), chapter_id)

    # ================================================================
    # Build
    # ================================================================
    @app.get("/api/build/{chapter_id}")
    async def api_build(chapter_id: str) -> dict:
        return build_service.build_docx(get_active_book(), chapter_id)

    # ================================================================
    # LLM
    # ================================================================
    @app.get("/api/llm-status")
    async def api_llm_status() -> dict:
        return llm_service.get_status(get_active_book())

    @app.post("/api/llm-configure")
    async def api_llm_configure(data: dict) -> dict:
        api_key = data.get("api_key", "")
        if not api_key:
            return {"error": "API anahtari gerekli"}
        return llm_service.configure(
            get_active_book(), data.get("provider", "deepseek"),
            api_key, data.get("model", "deepseek-chat"))

    @app.post("/api/llm-test")
    async def api_llm_test() -> dict:
        return llm_service.test_connection(get_active_book())

    # ================================================================
    # Quality, Stats, Search, Code
    # ================================================================
    @app.get("/api/quality/report")
    async def api_quality_report() -> list[dict]:
        return quality_service.get_quality_report(get_active_book())

    @app.get("/api/quality/book")
    async def api_quality_book() -> dict:
        return quality_service.get_book_quality_report(get_active_book())

    @app.get("/api/quality/report/{chapter_id}")
    async def api_quality_report_one(chapter_id: str) -> dict:
        result = quality_service.get_quality_report(
            get_active_book(), chapter_id)
        return result if isinstance(result, dict) \
            else {"error": "Bulunamadi"}

    @app.get("/api/stats")
    async def api_stats() -> dict:
        return quality_service.get_book_stats(get_active_book())

    @app.get("/api/search")
    async def api_search(q: str = "", chapter: str | None = None,
                         regex: bool = False) -> list[dict]:
        return quality_service.search_content(
            get_active_book(), q, chapter, regex)

    @app.post("/api/code/validate")
    async def api_code_validate(data: dict) -> dict:
        return quality_service.compile_code(
            get_active_book(), data.get("chapter_id", ""))

    # ================================================================
    # Observer Reviews
    # ================================================================
    @app.get("/api/observer/reviews")
    async def api_observer_reviews(chapter: str | None = None) -> list[dict]:
        return observer_service.list_observer_reviews(
            get_active_book(), chapter)

    @app.get("/api/observer/review/{chapter_id}")
    async def api_observer_review_get(chapter_id: str) -> dict:
        return observer_service.get_observer_review(
            get_active_book(), chapter_id)

    @app.post("/api/observer/review/{chapter_id}")
    async def api_observer_review_generate(chapter_id: str) -> dict:
        return observer_service.generate_observer_review(
            get_active_book(), chapter_id, save_report=True)

    @app.get("/api/observer/compare/{chapter_id}")
    async def api_observer_compare(chapter_id: str) -> dict:
        return observer_service.compare_observer_vs_validator(
            get_active_book(), chapter_id)

    # ================================================================
    # Build & Export
    # ================================================================
    @app.post("/api/extract/code")
    async def api_extract_code(data: dict | None = None) -> dict:
        cid = data.get("chapter_id") if data else None
        return export_service.extract_code(get_active_book(), cid)

    @app.get("/api/export/targets")
    async def api_export_targets() -> dict:
        return export_service.get_export_targets(get_active_book())

    @app.post("/api/extract/{chapter_id}")
    async def api_extract(chapter_id: str,
                          data: dict | None = None) -> dict:
        lang = (data.get("language") if data else None) or "java"
        return quality_service.extract_code_blocks(
            get_active_book(), chapter_id, lang)

    @app.post("/api/assemble")
    async def api_assemble(data: dict | None = None) -> dict:
        chs = (data.get("chapter_ids") if data else None) or None
        return export_service.assemble_book(get_active_book(), chs)

    @app.post("/api/export/{fmt}")
    async def api_export(fmt: str, data: dict | None = None) -> dict:
        chs = (data.get("chapter_ids") if data else None) or None
        return export_service.export_to_format(get_active_book(), fmt, chs)

    @app.post("/api/render/mermaid")
    async def api_render_mermaid(data: dict | None = None) -> dict:
        cid = data.get("chapter_id") if data else None
        return export_service.render_mermaid(get_active_book(), cid)

    @app.post("/api/backup")
    async def api_backup() -> dict:
        return export_service.create_backup(get_active_book())

    @app.post("/api/restore")
    async def api_restore(data: dict) -> dict:
        return export_service.restore_backup(
            get_active_book(), data.get("path", ""))

    @app.post("/api/index")
    async def api_index() -> dict:
        return assemble_service.generate_index(get_active_book())

    @app.post("/api/glossary")
    async def api_glossary() -> dict:
        return assemble_service.generate_glossary(get_active_book())

    # ================================================================
    # Wizard
    # ================================================================
    @app.post("/api/book/create")
    async def api_book_create(data: dict) -> dict:
        return wizard_service.create_book(get_active_book(), data)

    @app.post("/api/wizard/plan")
    async def api_wizard_plan(data: dict) -> dict:
        cfg = llm_service.get_status(get_active_book())
        if not cfg.get("configured"):
            return {"error": "LLM yapılandırılmamış"}
        gen = generation_service.get_generator(get_active_book())
        if not gen:
            return {"error": "LLM istemcisi başlatılamadı"}
        plan = wizard_service.generate_llm_plan(
            get_active_book(), gen.client,
            data.get("topic", ""),
            data.get("chapter_count", 23),
            data.get("appendix_count", 4),
            data.get("language", "tr"))
        return {"chapters": plan, "count": len(plan)}

    # ================================================================
    # Pipeline — Job Queue tabanli (async, polling)
    # ================================================================
    @app.post("/api/generate/{chapter_id}")
    async def api_generate(chapter_id: str,
                           data: dict | None = None) -> dict:
        """Pipeline isini kuyruga ekler, hemen job_id doner."""
        from bookmaker.studio.jobs import create_job, load_jobs, save_jobs

        cfg = llm_service.get_status(get_active_book())
        if not cfg.get("configured"):
            return {"error": "LLM yapılandırılmamış"}
        d = data or {}
        title = d.get("title") or chapter_id
        ch_info = chapter_service.get_chapter_info(
            get_active_book(), chapter_id)
        params = {
            "title": title,
            "concepts": d.get("concepts"),
            "enrich_types": d.get("enrich_types"),
            "chapter_no": ch_info.get("order") if ch_info else None,
        }
        root = get_active_book()
        load_jobs(root)
        job = create_job("generate", chapter_id, params)
        save_jobs(root)
        return {"job_id": job["id"], "chapter_id": chapter_id,
                "status": "queued", "message": "Is kuyruga eklendi. "
                "GET /api/jobs/{job_id} ile durumu sorgulayin."}

    # ================================================================
    # Jobs
    # ================================================================
    @app.get("/api/jobs")
    async def api_jobs() -> list[dict]:
        from bookmaker.studio.jobs import list_jobs, load_jobs
        load_jobs(get_active_book())
        return list_jobs()

    @app.get("/api/jobs/{job_id}")
    async def api_job_get(job_id: str) -> dict:
        from bookmaker.studio.jobs import get_job
        job = get_job(job_id)
        if not job:
            return {"error": "Is bulunamadi"}
        return job

    @app.post("/api/jobs")
    async def api_job_create(data: dict) -> dict:
        from bookmaker.studio.jobs import create_job, load_jobs, save_jobs

        root = get_active_book()
        load_jobs(root)
        job = create_job(
            data.get("step", "generate"),
            data.get("chapter_id", ""), data.get("params"))
        save_jobs(root)
        return job

    @app.post("/api/jobs/{job_id}/cancel")
    async def api_job_cancel(job_id: str) -> dict:
        from bookmaker.studio.jobs import cancel_job, save_jobs
        job = cancel_job(job_id)
        if not job:
            return {"error": "Is bulunamadi"}
        save_jobs(get_active_book())
        return {"job_id": job_id, "status": "cancelled"}

def run_studio(host: str = "127.0.0.1", port: int = 8765) -> None:
    if app is None:
        raise ImportError("FastAPI kurulu değil")
    from bookmaker.studio.jobs import load_jobs, start_worker

    load_jobs(get_active_book())
    start_worker(get_active_book())
    import uvicorn

    uvicorn.run(app, host=host, port=port)
