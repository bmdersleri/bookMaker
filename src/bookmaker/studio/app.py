"""FastAPI uygulaması — route'lar + aktif kitap sistemi."""

from __future__ import annotations

import time
from pathlib import Path

try:
    from fastapi import FastAPI, WebSocket
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, FileResponse
    from fastapi.staticfiles import StaticFiles
except ImportError:
    FastAPI = None  # type: ignore

from bookmaker.studio.jobs import create_job, list_jobs
from bookmaker.studio.services import (assemble_service, build_service,
                                       export_service, llm_service,
                                       manifest_service, pipeline_service,
                                       quality_service, wizard_service)

app: FastAPI | None = None

# ================================================================
# AKTIF KITAP SISTEMI
# ================================================================
_active_book: str | None = None
_CONFIG_FILE = "build/studio_config.json"


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
        """Build çıktı dosyalarını sunar (PNG, DOCX, PDF vb)."""
        full = get_active_book() / "build" / file_path
        if not full.resolve().is_relative_to(get_active_book().resolve()):
            from fastapi.responses import PlainTextResponse
            return PlainTextResponse("Forbidden", status_code=403)
        if not full.exists():
            from fastapi.responses import PlainTextResponse
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
        candidates = [
            root / "book_projects",
            root.parent if root.parent.name == "book_projects" else None,
            Path.cwd() / "book_projects",
        ]
        bp = None
        for c in candidates:
            if c and c.exists():
                bp = c
                break
        if not bp or not bp.exists():
            return []
        import yaml as _yaml

        def _normalize_title(val):
            if isinstance(val, dict):
                return val.get("tr") or val.get("en") or str(val)
            return str(val) if val else ""

        projects = []
        for d in sorted(bp.iterdir()):
            if d.is_dir():
                profile = d / "book_profile.yaml"
                title = d.name
                if profile.exists():
                    try:
                        data = _yaml.safe_load(
                            profile.read_text(encoding="utf-8"))
                        if data and "book" in data:
                            title = _normalize_title(
                                data["book"].get("title", d.name))
                    except Exception:
                        pass
                projects.append(
                    {"name": d.name, "path": str(d), "title": title})
        return projects

    @app.get("/api/active-book")
    async def api_active_book_get() -> dict:
        root = get_active_book()
        name = root.name
        profile = root / "book_profile.yaml"
        title = name
        if profile.exists():
            import yaml as _yaml
            try:
                data = _yaml.safe_load(
                    profile.read_text(encoding="utf-8"))
                if data and "book" in data:
                    raw = data["book"].get("title", name)
                    if isinstance(raw, dict):
                        title = raw.get("tr") or raw.get("en") or str(raw)
                    else:
                        title = str(raw) if raw else name
            except Exception:
                pass
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
        return manifest_service.get_project_info(get_active_book())

    @app.get("/api/pipeline-state")
    async def api_pipeline_state() -> dict:
        return manifest_service.get_pipeline_state(get_active_book())

    # ================================================================
    # Chapters
    # ================================================================
    @app.get("/api/chapters")
    async def api_chapters() -> list[dict]:
        return manifest_service.get_chapter_list(get_active_book())

    @app.post("/api/chapters")
    async def api_chapter_create(data: dict) -> dict:
        return manifest_service.add_chapter(
            get_active_book(), data.get("chapter_id", ""),
            data.get("title", ""), data.get("order"))

    @app.put("/api/chapters/{chapter_id}")
    async def api_chapter_update(chapter_id: str, data: dict) -> dict:
        return manifest_service.update_chapter(
            get_active_book(), chapter_id, data)

    @app.delete("/api/chapters/{chapter_id}")
    async def api_chapter_delete(chapter_id: str) -> dict:
        return manifest_service.remove_chapter(
            get_active_book(), chapter_id)

    @app.put("/api/chapters/reorder")
    async def api_chapter_reorder(data: dict) -> dict:
        return manifest_service.reorder_chapters(
            get_active_book(), data.get("chapter_ids", []))

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
    # Build & Export
    # ================================================================
    @app.post("/api/extract/code")
    async def api_extract_code(data: dict | None = None) -> dict:
        cid = data.get("chapter_id") if data else None
        return export_service.extract_code(get_active_book(), cid)

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
        gen = pipeline_service.get_generator(get_active_book())
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
    # Pipeline (REST)
    # ================================================================
    @app.post("/api/generate/{chapter_id}")
    async def api_generate(chapter_id: str,
                           data: dict | None = None) -> dict:
        cfg = llm_service.get_status(get_active_book())
        if not cfg.get("configured"):
            return {"error": "LLM yapılandırılmamış"}
        d = data or {}
        title = d.get("title") or chapter_id
        ch_info = pipeline_service.get_chapter_info(
            get_active_book(), chapter_id)
        return pipeline_service.run_generation(
            get_active_book(), chapter_id, title,
            d.get("concepts"), d.get("enrich_types"),
            ch_info.get("order") if ch_info else None)

    # ================================================================
    # Jobs
    # ================================================================
    @app.get("/api/jobs")
    async def api_jobs() -> list[dict]:
        return list_jobs()

    @app.post("/api/jobs")
    async def api_job_create(data: dict) -> dict:
        return create_job(
            data.get("step", "generate"),
            data.get("chapter_id", ""), data.get("params"))

    # ================================================================
    # WebSocket: Pipeline + Prompt/Response canlı takip
    # ================================================================
    @app.websocket("/ws/api/generate/{chapter_id}")
    async def ws_generate(websocket: WebSocket, chapter_id: str) -> None:
        import asyncio
        import concurrent.futures
        import json as _json

        root = get_active_book()
        await websocket.accept()

        config_data = {}
        try:
            raw = await asyncio.wait_for(
                websocket.receive_text(), timeout=10)
            config_data = _json.loads(raw)
        except (asyncio.TimeoutError, Exception):
            pass

        cfg = llm_service.get_status(root)
        if not cfg.get("configured"):
            await websocket.send_text(_json.dumps(
                {"type": "error",
                 "message": "LLM yapılandırılmamış"},
                ensure_ascii=False))
            await websocket.close()
            return

        gen = pipeline_service.get_generator(root)
        if not gen:
            await websocket.send_text(_json.dumps(
                {"type": "error",
                 "message": "LLM istemcisi başlatılamadı"},
                ensure_ascii=False))
            await websocket.close()
            return

        ch_info = pipeline_service.get_chapter_info(root, chapter_id)
        title = (config_data.get("title")
                 or (ch_info.get("title") if ch_info else chapter_id))
        concepts = config_data.get("concepts") or []
        enrich_types = config_data.get("enrich_types") or [
            "ozet", "sozluk", "soru", "alistirma", "hata", "kopru"]
        GEN_DIR = root / "build" / "generation"
        GEN_DIR.mkdir(parents=True, exist_ok=True)

        loop = asyncio.get_event_loop()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        t_all = time.time()

        async def send(msg: dict) -> None:
            try:
                await websocket.send_text(
                    _json.dumps(msg, ensure_ascii=False))
            except Exception:
                pass

        async def run_step(name: str, label: str, prompt_text: str,
                           fn, *args) -> str:
            await send({"type": "prompt", "step": name,
                        "label": label, "prompt": prompt_text[:2000]})
            await send({"type": "step", "step": name,
                        "status": "running", "label": label})
            t0 = time.time()
            try:
                result = await loop.run_in_executor(pool, fn, *args)
                el = time.time() - t0
                wc = len(result.split()) if isinstance(result, str) else 0
                await send({"type": "response", "step": name,
                            "label": label, "response": result[:2000],
                            "words": wc})
                await send({"type": "step", "step": name,
                            "status": "done", "label": label,
                            "words": wc, "elapsed_s": round(el, 1)})
                return result
            except Exception as e:
                el = time.time() - t0
                await send({"type": "step", "step": name,
                            "status": "error", "label": label,
                            "error": str(e)[:200],
                            "elapsed_s": round(el, 1)})
                raise

        try:
            from bookmaker.generation.spec import (
                generate_spec, build_seed_from_spec_prompt,
                build_spec_prompt, validate_spec,
                build_spec_validation_prompt)
            from bookmaker.generation.postprocess import (
                normalize, extract_sections)
            from bookmaker.generation.prompts import (
                SYSTEM_AUTHOR,
                build_enrich_summary_prompt,
                build_enrich_glossary_prompt,
                build_enrich_questions_prompt,
                build_enrich_exercises_prompt,
                build_enrich_errors_prompt,
                build_enrich_bridge_prompt)

            # SPEC
            sp = build_spec_prompt(
                title, concepts or [f"{title} ana kavramları"],
                f"Hedef: {cfg.get('model', 'deepseek-chat')}",
                ch_info.get("order") if ch_info else None)
            spec = await run_step(
                "spec", "Spesifikasyon", sp,
                generate_spec, gen.client, title,
                concepts or [f"{title} ana kavramları"],
                f"Hedef: {cfg.get('model', 'deepseek-chat')}",
                ch_info.get("order") if ch_info else None)

            # VALIDATE
            vp = build_spec_validation_prompt(spec, title)
            validation = await run_step(
                "validate", "Doğrulama", vp,
                validate_spec, gen.client, spec, title)

            # SEED
            sd = build_seed_from_spec_prompt(spec, title)
            seed_raw = await run_step(
                "seed", "Seed Üretimi", sd,
                lambda: gen.client.generate_text(SYSTEM_AUTHOR, sd))

            # NORMALIZE
            normalized = await run_step(
                "normalize", "Normalizasyon", "",
                lambda: normalize(seed_raw, chapter_id, title, gen.config))

            # ENRICH
            sections = extract_sections(normalized)
            headings = [s["heading"] for s in sections
                        if s["heading"] != "__title__"]
            ctx_lines = [l for l in normalized.splitlines()
                         if not l.startswith("---")]
            context = "\n".join(ctx_lines[:20])
            enrich_parts = {}
            builders = {
                "ozet": ("Bölüm Özeti",
                         build_enrich_summary_prompt, 3),
                "sozluk": ("Terim Sözlüğü",
                           build_enrich_glossary_prompt, 3),
                "soru": ("Kendini Değerlendirme",
                         build_enrich_questions_prompt, 3),
                "alistirma": ("Programlama Alıştırmaları",
                              build_enrich_exercises_prompt, 3),
                "hata": ("Sık Yapılan Hatalar",
                         build_enrich_errors_prompt, 3),
                "kopru": ("Sonraki Bölüme Köprü",
                          build_enrich_bridge_prompt, 4),
            }
            for etype in enrich_types:
                if etype not in builders:
                    continue
                stitle, builder, nargs = builders[etype]
                up = (builder(chapter_title=title, next_chapter=None,
                              headings=headings, context=context)
                      if nargs == 4
                      else builder(chapter_title=title,
                                   headings=headings,
                                   context=context))
                r = await run_step(
                    f"enrich_{etype}", stitle, up,
                    lambda p=up: gen.client.generate_text(
                        SYSTEM_AUTHOR, p))
                enrich_parts[etype] = r

            # ASSEMBLE
            def _assemble():
                from bookmaker.generation.postprocess import (
                    insert_section)
                text = normalized
                for key, stitle in reversed([
                    ("alistirma", "Programlama alistirmalari"),
                    ("soru", "Kendini degerlendirme sorulari"),
                    ("sozluk", "Terim sozlugu"),
                    ("ozet", "Bolum ozeti"),
                    ("hata",
                     "Sik yapilan hatalar ve yanlis sezgiler"),
                ]):
                    if key in enrich_parts and enrich_parts[key]:
                        text = insert_section(text, stitle,
                                               enrich_parts[key])
                if "kopru" in enrich_parts and enrich_parts["kopru"]:
                    text = insert_section(
                        text, "Bir sonraki bolume kopru",
                        enrich_parts["kopru"])
                return text

            await run_step("assemble", "Birleştirme", "", _assemble)

            final = _assemble()
            (GEN_DIR / "step4_final.md").write_text(
                final, encoding="utf-8")
            (GEN_DIR / "step0_spec.md").write_text(
                spec, encoding="utf-8")
            (GEN_DIR / "step1_seed.md").write_text(
                seed_raw, encoding="utf-8")
            (GEN_DIR / "step2_normalized.md").write_text(
                normalized, encoding="utf-8")
            fmap = {"ozet": "summary", "sozluk": "glossary",
                    "soru": "questions", "alistirma": "exercises",
                    "hata": "errors", "kopru": "bridge"}
            for k, v in enrich_parts.items():
                if k in fmap:
                    (GEN_DIR /
                     f"step3_enrich_{fmap[k]}.md").write_text(
                        v, encoding="utf-8")

            total_elapsed = time.time() - t_all
            try:
                from bookmaker.authoring.pipeline import (
                    AuthoringPipeline)
                AuthoringPipeline(root).paste_draft(
                    chapter_id, final)
                AuthoringPipeline(root).advance(
                    chapter_id, "full_text_pasted")
            except Exception:
                pass

            await send(
                {"type": "complete",
                 "elapsed_s": round(total_elapsed, 1),
                 "final_words": len(final.split()),
                 "path": "build/generation/step4_final.md",
                 "enriched_count": len(enrich_parts)})
        except Exception as e:
            await send({"type": "error", "message": str(e)[:300]})
        finally:
            pool.shutdown(wait=False)
            try:
                await websocket.close()
            except Exception:
                pass


def run_studio(host: str = "127.0.0.1", port: int = 8765) -> None:
    if app is None:
        raise ImportError("FastAPI kurulu değil")
    import uvicorn
    uvicorn.run(app, host=host, port=port, ws_ping_interval=300, ws_ping_timeout=600)
