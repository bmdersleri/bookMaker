"""FastAPI uygulaması — sadece route'lar, logic servislerde."""

from __future__ import annotations

import time
from pathlib import Path

try:
    from fastapi import FastAPI, WebSocket
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse
    from fastapi.staticfiles import StaticFiles
except ImportError:
    FastAPI = None  # type: ignore

from bookmaker.studio.jobs import create_job, list_jobs
from bookmaker.studio.services import (build_service, export_service,
                                       llm_service, manifest_service,
                                       pipeline_service, quality_service,
                                       wizard_service)

app: FastAPI | None = None

if FastAPI is not None:
    app = FastAPI(title="bookMaker Studio", version="0.2.0")
    _root = Path(__file__).parent.resolve()
    _static = _root / "static"
    _templates = _root / "templates"

    app.add_middleware(CORSMiddleware, allow_origins=["*"],
                       allow_methods=["*"], allow_headers=["*"])
    _static.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(_static)), name="static")

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
    # Status
    # ================================================================
    @app.get("/api/status")
    async def api_status() -> dict:
        return {"status": "running", "version": "0.2.0"}

    @app.get("/api/project")
    async def api_project() -> dict:
        return manifest_service.get_project_info(Path.cwd())

    @app.get("/api/pipeline-state")
    async def api_pipeline_state() -> dict:
        return manifest_service.get_pipeline_state(Path.cwd())

    # ================================================================
    # Chapters
    # ================================================================
    @app.get("/api/chapters")
    async def api_chapters() -> list[dict]:
        return manifest_service.get_chapter_list(Path.cwd())

    @app.post("/api/chapters")
    async def api_chapter_create(data: dict) -> dict:
        return manifest_service.add_chapter(
            Path.cwd(), data.get("chapter_id", ""),
            data.get("title", ""), data.get("order"))

    @app.put("/api/chapters/{chapter_id}")
    async def api_chapter_update(chapter_id: str, data: dict) -> dict:
        return manifest_service.update_chapter(Path.cwd(), chapter_id, data)

    @app.delete("/api/chapters/{chapter_id}")
    async def api_chapter_delete(chapter_id: str) -> dict:
        return manifest_service.remove_chapter(Path.cwd(), chapter_id)

    @app.put("/api/chapters/reorder")
    async def api_chapter_reorder(data: dict) -> dict:
        return manifest_service.reorder_chapters(
            Path.cwd(), data.get("chapter_ids", []))

    # ================================================================
    # Content & Quality
    # ================================================================
    @app.get("/api/view/{chapter_id}")
    async def api_view(chapter_id: str) -> dict:
        return quality_service.get_chapter_content(Path.cwd(), chapter_id)

    @app.get("/api/check/{chapter_id}")
    async def api_check(chapter_id: str) -> dict:
        return quality_service.validate_chapter(Path.cwd(), chapter_id)

    # ================================================================
    # Build
    # ================================================================
    @app.get("/api/build/{chapter_id}")
    async def api_build(chapter_id: str) -> dict:
        return build_service.build_docx(Path.cwd(), chapter_id)

    # ================================================================
    # LLM
    # ================================================================
    @app.get("/api/llm-status")
    async def api_llm_status() -> dict:
        return llm_service.get_status(Path.cwd())

    @app.post("/api/llm-configure")
    async def api_llm_configure(data: dict) -> dict:
        api_key = data.get("api_key", "")
        if not api_key:
            return {"error": "API anahtari gerekli"}
        return llm_service.configure(
            Path.cwd(), data.get("provider", "deepseek"),
            api_key, data.get("model", "deepseek-chat"))

    @app.post("/api/llm-test")
    async def api_llm_test() -> dict:
        return llm_service.test_connection(Path.cwd())

    # ================================================================
    # Quality, Stats, Search, Code
    # ================================================================

    @app.get("/api/quality/report")
    async def api_quality_report() -> list[dict]:
        return quality_service.get_quality_report(Path.cwd())

    @app.get("/api/quality/report/{chapter_id}")
    async def api_quality_report_one(chapter_id: str) -> dict:
        result = quality_service.get_quality_report(Path.cwd(), chapter_id)
        if isinstance(result, dict):
            return result
        return {"error": "Bulunamadi"} if not result else result

    @app.get("/api/stats")
    async def api_stats() -> dict:
        return quality_service.get_book_stats(Path.cwd())

    @app.get("/api/search")
    async def api_search(q: str = "", chapter: str | None = None,
                         regex: bool = False) -> list[dict]:
        return quality_service.search_content(Path.cwd(), q, chapter, regex)

    @app.post("/api/code/validate")
    async def api_code_validate(data: dict) -> dict:
        return quality_service.compile_code(
            Path.cwd(), data.get("chapter_id", ""))

    @app.post("/api/extract/{chapter_id}")
    async def api_extract(chapter_id: str,
                          data: dict | None = None) -> dict:
        lang = (data.get("language") if data else None) or "java"
        return quality_service.extract_code_blocks(Path.cwd(), chapter_id, lang)

    # ================================================================
    # Build & Export
    # ================================================================

    @app.post("/api/assemble")
    async def api_assemble(data: dict | None = None) -> dict:
        chs = (data.get("chapter_ids") if data else None) or None
        return export_service.assemble_book(Path.cwd(), chs)

    @app.post("/api/export/{fmt}")
    async def api_export(fmt: str, data: dict | None = None) -> dict:
        chs = (data.get("chapter_ids") if data else None) or None
        return export_service.export_to_format(Path.cwd(), fmt, chs)

    @app.post("/api/render/mermaid")
    async def api_render_mermaid(data: dict | None = None) -> dict:
        cid = data.get("chapter_id") if data else None
        return export_service.render_mermaid(Path.cwd(), cid)

    @app.post("/api/extract/code")
    async def api_extract_code(data: dict | None = None) -> dict:
        cid = data.get("chapter_id") if data else None
        return export_service.extract_code(Path.cwd(), cid)

    @app.post("/api/backup")
    async def api_backup() -> dict:
        return export_service.create_backup(Path.cwd())

    @app.post("/api/restore")
    async def api_restore(data: dict) -> dict:
        return export_service.restore_backup(
            Path.cwd(), data.get("path", ""))

    # ================================================================
    # Wizard
    # ================================================================

    @app.post("/api/book/create")
    async def api_book_create(data: dict) -> dict:
        return wizard_service.create_book(Path.cwd(), data)

    @app.post("/api/wizard/plan")
    async def api_wizard_plan(data: dict) -> dict:
        cfg = llm_service.get_status(Path.cwd())
        if not cfg.get("configured"):
            return {"error": "LLM yapılandırılmamış"}
        gen = pipeline_service.get_generator(Path.cwd())
        if not gen:
            return {"error": "LLM istemcisi başlatılamadı"}
        plan = wizard_service.generate_llm_plan(
            Path.cwd(), gen.client,
            data.get("topic", ""),
            data.get("chapter_count", 23),
            data.get("appendix_count", 4),
            data.get("language", "tr"))
        return {"chapters": plan, "count": len(plan)}

    # ================================================================
    # Pipeline (REST)
    # ================================================================
    @app.post("/api/generate/{chapter_id}")
    async def api_generate(chapter_id: str, data: dict | None = None) -> dict:
        cfg = llm_service.get_status(Path.cwd())
        if not cfg.get("configured"):
            return {"error": "LLM yapılandırılmamış"}
        d = data or {}
        title = d.get("title") or chapter_id
        return pipeline_service.run_generation(
            Path.cwd(), chapter_id, title,
            d.get("concepts"), d.get("enrich_types"),
            pipeline_service.get_chapter_info(Path.cwd(), chapter_id).get("order")
            if pipeline_service.get_chapter_info(Path.cwd(), chapter_id) else None)

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

        root = Path.cwd().resolve()
        await websocket.accept()

        # Config al
        config_data = {}
        try:
            raw = await asyncio.wait_for(websocket.receive_text(), timeout=10)
            config_data = _json.loads(raw)
        except (asyncio.TimeoutError, Exception):
            pass

        cfg = llm_service.get_status(root)
        if not cfg.get("configured"):
            await websocket.send_text(_json.dumps(
                {"type": "error", "message": "LLM yapılandırılmamış"}, ensure_ascii=False))
            await websocket.close()
            return

        gen = pipeline_service.get_generator(root)
        if not gen:
            await websocket.send_text(_json.dumps(
                {"type": "error", "message": "LLM istemcisi başlatılamadı"}, ensure_ascii=False))
            await websocket.close()
            return

        ch_info = pipeline_service.get_chapter_info(root, chapter_id)
        title = config_data.get("title") or (ch_info.get("title") if ch_info else chapter_id)
        concepts = config_data.get("concepts") or []
        enrich_types = config_data.get("enrich_types") or [
            "ozet", "sozluk", "soru", "alistirma", "hata", "kopru"]
        GEN_DIR = root / "build" / "generation"
        GEN_DIR.mkdir(parents=True, exist_ok=True)

        loop = asyncio.get_event_loop()
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        t_all = time.time()
        cancelled = False

        async def send(msg: dict) -> None:
            try:
                await websocket.send_text(_json.dumps(msg, ensure_ascii=False))
            except Exception:
                pass

        async def run_step(name: str, step_label: str, prompt_text: str, fn, *args) -> str:
            nonlocal cancelled
            # Önce prompt'u gönder
            await send({"type": "prompt", "step": name, "label": step_label,
                        "prompt": prompt_text[:2000]})
            await send({"type": "step", "step": name, "status": "running", "label": step_label})
            t0 = time.time()
            try:
                result = await loop.run_in_executor(pool, fn, *args)
                el = time.time() - t0
                wc = len(result.split()) if isinstance(result, str) else 0
                await send({"type": "response", "step": name, "label": step_label,
                            "response": result[:2000], "words": wc})
                await send({"type": "step", "step": name, "status": "done",
                            "label": step_label, "words": wc, "elapsed_s": round(el, 1)})
                return result
            except Exception as e:
                el = time.time() - t0
                await send({"type": "step", "step": name, "status": "error",
                            "label": step_label, "error": str(e)[:200],
                            "elapsed_s": round(el, 1)})
                raise

        try:
            from bookmaker.generation.spec import (generate_spec,
                build_seed_from_spec_prompt, build_spec_prompt,
                validate_spec, build_spec_validation_prompt)
            from bookmaker.generation.postprocess import normalize, extract_sections
            from bookmaker.generation.prompts import (
                SYSTEM_AUTHOR, build_enrich_summary_prompt,
                build_enrich_glossary_prompt, build_enrich_questions_prompt,
                build_enrich_exercises_prompt, build_enrich_errors_prompt,
                build_enrich_bridge_prompt)

            # SPEC
            spec_prompt_text = build_spec_prompt(
                title, concepts or [f"{title} ana kavramları"],
                f"Hedef: {cfg.get('model', 'deepseek-chat')}",
                ch_info.get("order") if ch_info else None)
            spec = await run_step("spec", "Spesifikasyon", spec_prompt_text,
                                  generate_spec, gen.client, title,
                                  concepts or [f"{title} ana kavramları"],
                                  f"Hedef: {cfg.get('model', 'deepseek-chat')}",
                                  ch_info.get("order") if ch_info else None)

            # VALIDATE
            val_prompt = build_spec_validation_prompt(spec, title)
            validation = await run_step("validate", "Doğrulama", val_prompt,
                                        validate_spec, gen.client, spec, title)

            # SEED
            seed_prompt = build_seed_from_spec_prompt(spec, title)
            seed_raw = await run_step("seed", "Seed Üretimi", seed_prompt,
                                      lambda: gen.client.generate_text(SYSTEM_AUTHOR, seed_prompt))

            # NORMALIZE
            normalized = await run_step("normalize", "Normalizasyon", "",
                                        lambda: normalize(seed_raw, chapter_id, title, gen.config))

            # ENRICH
            sections = extract_sections(normalized)
            headings = [s["heading"] for s in sections if s["heading"] != "__title__"]
            ctx_lines = [l for l in normalized.splitlines() if not l.startswith("---")]
            context = "\n".join(ctx_lines[:20])
            enrich_parts = {}
            builders = {
                "ozet": ("Bölüm Özeti", build_enrich_summary_prompt, 3),
                "sozluk": ("Terim Sözlüğü", build_enrich_glossary_prompt, 3),
                "soru": ("Kendini Değerlendirme", build_enrich_questions_prompt, 3),
                "alistirma": ("Programlama Alıştırmaları", build_enrich_exercises_prompt, 3),
                "hata": ("Sık Yapılan Hatalar", build_enrich_errors_prompt, 3),
                "kopru": ("Sonraki Bölüme Köprü", build_enrich_bridge_prompt, 4),
            }
            for etype in enrich_types:
                if etype not in builders:
                    continue
                stitle, builder, nargs = builders[etype]
                up = (builder(chapter_title=title, next_chapter=None,
                              headings=headings, context=context)
                      if nargs == 4
                      else builder(chapter_title=title, headings=headings, context=context))
                r = await run_step(f"enrich_{etype}", stitle, up,
                                   lambda p=up: gen.client.generate_text(SYSTEM_AUTHOR, p))
                enrich_parts[etype] = r

            # ASSEMBLE
            def _assemble():
                from bookmaker.generation.postprocess import insert_section
                text = normalized
                for key, stitle in reversed([
                    ("alistirma", "Programlama alistirmalari"),
                    ("soru", "Kendini degerlendirme sorulari"),
                    ("sozluk", "Terim sozlugu"),
                    ("ozet", "Bolum ozeti"),
                    ("hata", "Sik yapilan hatalar ve yanlis sezgiler"),
                ]):
                    if key in enrich_parts and enrich_parts[key]:
                        text = insert_section(text, stitle, enrich_parts[key])
                if "kopru" in enrich_parts and enrich_parts["kopru"]:
                    text = insert_section(text, "Bir sonraki bolume kopru",
                                          enrich_parts["kopru"])
                return text
            await run_step("assemble", "Birleştirme", "", _assemble)

            # KAYDET
            (GEN_DIR / "step4_final.md").write_text(final := _assemble(), encoding="utf-8")
            (GEN_DIR / "step0_spec.md").write_text(spec, encoding="utf-8")
            (GEN_DIR / "step1_seed.md").write_text(seed_raw, encoding="utf-8")
            (GEN_DIR / "step2_normalized.md").write_text(normalized, encoding="utf-8")
            fmap = {"ozet": "summary", "sozluk": "glossary", "soru": "questions",
                    "alistirma": "exercises", "hata": "errors", "kopru": "bridge"}
            for k, v in enrich_parts.items():
                if k in fmap:
                    (GEN_DIR / f"step3_enrich_{fmap[k]}.md").write_text(v, encoding="utf-8")

            total_elapsed = time.time() - t_all
            try:
                from bookmaker.authoring.pipeline import AuthoringPipeline
                AuthoringPipeline(root).paste_draft(chapter_id, final)
                AuthoringPipeline(root).advance(chapter_id, "full_text_pasted")
            except Exception:
                pass

            await send({"type": "complete", "elapsed_s": round(total_elapsed, 1),
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
    uvicorn.run(app, host=host, port=port)
