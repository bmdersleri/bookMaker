"""Is servisi — arka plan is kuyrugu + pipeline worker thread."""

from __future__ import annotations

import json
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

_JOBS: dict[str, dict[str, Any]] = {}
_LOCK = threading.Lock()
_WORKER_STARTED = False

_MAX_CONCURRENT_ENRICH = 4
_MAX_LOG_ENTRIES = 50


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _rel(root: Path, path: Path) -> str:
    """Return a project-relative path with platform separators."""
    return str(path.resolve().relative_to(root.resolve()))


def _parse_iso(ts: str) -> float:
    """Parse ISO timestamp to epoch float for elapsed calculation."""
    from datetime import datetime as _dt
    try:
        return _dt.fromisoformat(ts).timestamp()
    except Exception:
        return 0.0


def _jobs_dir(root: Path) -> Path:
    return root / "logs" / "studio_jobs"


def _legacy_jobs_dir(root: Path) -> Path:
    return root / "build" / "studio_jobs"


def _generation_dir(root: Path, job_id: str) -> Path:
    return root / "logs" / "production" / job_id


def _chapter_content_dir(root: Path, chapter_id: str) -> Path:
    return root / "chapters" / chapter_id / "content"


def _draft_path(root: Path, chapter_id: str) -> Path:
    return _chapter_content_dir(root, chapter_id) / "draft.md"


def _final_path(root: Path, chapter_id: str) -> Path:
    return _chapter_content_dir(root, chapter_id) / "final.md"


def _build_source_candidates(root: Path, chapter_id: str) -> list[Path]:
    content = _chapter_content_dir(root, chapter_id)
    approved = root / "chapters" / chapter_id / "approved"
    return [
        content / "final.md",
        content / "draft.md",
        approved / f"{chapter_id}_v001.md",
        approved / f"{chapter_id}_v002.md",
        approved / "v001.md",
    ]


# ================================================================
# CRUD
# ================================================================

def create_job(step: str, chapter_id: str,
               params: dict | None = None) -> dict:
    """Yeni is olusturur."""
    job_id = uuid.uuid4().hex[:12]
    job = {
        "id": job_id, "step": step, "chapter_id": chapter_id,
        "status": "queued", "params": params or {},
        "created_at": _now(), "started_at": None,
        "finished_at": None, "elapsed_s": None,
        "progress": {"current": "", "done": 0, "total": 6, "log": []},
        "summary": {}, "error": None,
        "steps": [],
    }
    with _LOCK:
        _JOBS[job_id] = job
    return job


def get_job(job_id: str) -> dict | None:
    with _LOCK:
        job = _JOBS.get(job_id)
        return dict(job) if job else None


def list_jobs(limit: int = 20) -> list[dict]:
    with _LOCK:
        jobs = sorted(_JOBS.values(),
                      key=lambda j: j["created_at"], reverse=True)
        return [dict(j) for j in jobs[:limit]]


def update_job(job_id: str, **kwargs: Any) -> dict | None:
    with _LOCK:
        job = _JOBS.get(job_id)
        if not job:
            return None
        progress = kwargs.get("progress")
        if isinstance(progress, dict) and isinstance(job.get("progress"), dict):
            previous_log = job["progress"].get("log", [])
            merged_progress = {**job["progress"], **progress}
            if not progress.get("log") and previous_log:
                merged_progress["log"] = previous_log
            kwargs["progress"] = merged_progress
        job.update(kwargs)
        if kwargs.get("status") == "running" and not job["started_at"]:
            job["started_at"] = _now()
        if kwargs.get("status") in ("done", "error", "cancelled"):
            job["finished_at"] = _now()
            if job["started_at"]:
                s = datetime.fromisoformat(job["started_at"])
                f = datetime.fromisoformat(job["finished_at"])
                job["elapsed_s"] = round((f - s).total_seconds(), 1)
        return dict(job)


def append_log(job_id: str, msg: str) -> None:
    with _LOCK:
        job = _JOBS.get(job_id)
        if job:
            job["progress"]["log"].append(f"[{_now()}] {msg}")
            if len(job["progress"]["log"]) > _MAX_LOG_ENTRIES:
                job["progress"]["log"] = job["progress"]["log"][-_MAX_LOG_ENTRIES:]


def cancel_job(job_id: str) -> dict | None:
    return update_job(job_id, status="cancelled")


# ================================================================
# WORKER THREAD
# ================================================================

def start_worker(project_root: str | Path) -> None:
    """Arka plan is kuyrugu worker'ini baslatir (tek instance)."""
    global _WORKER_STARTED
    if _WORKER_STARTED:
        return
    _WORKER_STARTED = True
    root = Path(project_root).resolve()
    t = threading.Thread(target=_worker_loop, args=(root,), daemon=True)
    t.start()
    print("  [JOBS] Worker baslatildi")


def _worker_loop(root: Path) -> None:
    """Surekli kuyrugu kontrol eder, siradaki isi isler."""
    while True:
        job = _dequeue()
        if job:
            _execute_job(root, job)
        time.sleep(1)


def _dequeue() -> dict | None:
    with _LOCK:
        for job in _JOBS.values():
            if job["status"] == "queued":
                job["status"] = "running"
                job["started_at"] = _now()
                return dict(job)
    return None


def _execute_job(root: Path, job: dict) -> None:
    """Pipeline isini calistirir — ChapterGenerator uzerinden."""
    job_id = job["id"]
    chapter_id = job["chapter_id"]
    step = job["step"]
    params = job["params"]

    try:
        if step == "generate":
            _run_pipeline(root, job_id, chapter_id, params)
        elif step == "build":
            _run_build(root, job_id, chapter_id, params)
        else:
            update_job(job_id, status="done",
                       summary={"message": f"Bilinmeyen adim: {step}"})
    except Exception as e:
        update_job(job_id, status="error", error=str(e)[:500])
        append_log(job_id, f"HATA: {e}")


def _run_pipeline(root: Path, job_id: str, chapter_id: str, params: dict) -> None:
    """ChapterGenerator pipeline'ini adim adim calistirir, progress gunceller."""
    import concurrent.futures

    from bookmaker.generation.pipeline import ChapterGenerator
    from bookmaker.generation.postprocess import (
        extract_sections,
        insert_section,
        normalize,
    )
    from bookmaker.generation.prompts import (
        SYSTEM_AUTHOR,
        build_enrich_bridge_prompt,
        build_enrich_errors_prompt,
        build_enrich_exercises_prompt,
        build_enrich_glossary_prompt,
        build_enrich_questions_prompt,
        build_enrich_summary_prompt,
        build_system_author,
    )
    from bookmaker.generation.spec import (
        build_seed_from_spec_prompt,
        build_spec_prompt,
        generate_spec,
        validate_spec,
    )

    gen = ChapterGenerator(root)
    if not gen.is_ready():
        update_job(job_id, status="error", error="LLM yapilandirilmamis")
        return

    title = params.get("title") or chapter_id
    concepts = params.get("concepts") or [f"{title} ana kavramlari"]
    enrich_types = params.get("enrich_types") or [
        "ozet", "sozluk", "soru", "alistirma", "hata", "kopru"]

    GEN_DIR = _generation_dir(root, job_id)
    GEN_DIR.mkdir(parents=True, exist_ok=True)
    t_all = time.time()
    model = gen.llm_config.model
    code_lang = gen.config.primary_code_language if gen.config else "java"

    def progress(step_name: str, status: str, detail: str = "",
                 prompt_file: str = "", output_file: str = "") -> None:
        step_order = {
            "spec": 1, "validate": 2, "seed": 3,
            "normalize": 4, "enrich": 5, "assemble": 6,
        }
        order = step_order.get(step_name, 0)
        update_job(job_id, progress={
            "current": step_name, "done": order - 1, "total": 6,
            "log": [],  # preserved by update_job merge behavior
        })
        append_log(job_id, f"[{status}] {step_name}: {detail}".rstrip(": "))

        # Steps tracking for UI detail panel
        job = get_job(job_id)
        if job and status == "running":
            job["steps"].append({
                "name": step_name, "status": "running",
                "started_at": _now(), "elapsed_s": None,
                "prompt_file": "", "output_file": "",
            })
        elif job and status == "done" and job["steps"]:
            for s in reversed(job["steps"]):
                if s["name"] == step_name and s["status"] == "running":
                    s["status"] = "done"
                    started = s.get("started_at")
                    s["elapsed_s"] = (
                        round(time.time() - _parse_iso(started), 1)
                        if started else None
                    )
                    if prompt_file:
                        s["prompt_file"] = prompt_file
                    if output_file:
                        s["output_file"] = output_file
                    break

    # STEP 1: SPEC
    progress("spec", "running")
    t0 = time.time()
    spec = generate_spec(gen.client, title, concepts,
                          f"Hedef: {model}", params.get("chapter_no"),
                          code_language=code_lang)
    (GEN_DIR / "step0_spec.md").write_text(spec, encoding="utf-8")
    (GEN_DIR / "prompt0_spec.txt").write_text(
        build_spec_prompt(title, concepts, f"Hedef: {model}",
                          params.get("chapter_no"), code_language=code_lang),
        encoding="utf-8")
    progress("spec", "done", f"{len(spec.split())} kel, {time.time()-t0:.1f}s",
             prompt_file=_rel(root, GEN_DIR / "prompt0_spec.txt"),
             output_file=_rel(root, GEN_DIR / "step0_spec.md"))

    # STEP 2: VALIDATE
    progress("validate", "running")
    t0 = time.time()
    try:
        validation = validate_spec(gen.client, spec, title,
                                   code_language=code_lang)
        vnotes = validation.get("notes", "") if isinstance(validation, dict) else str(validation)
        validate_status = validation.get("status", "?") if isinstance(validation, dict) else "OK"
        (GEN_DIR / "step0_validation.md").write_text(str(vnotes), encoding="utf-8")
        progress("validate", "done", f"{validate_status}, {time.time() - t0:.1f}s",
                 output_file=_rel(root, GEN_DIR / "step0_validation.md"))
    except Exception as e:
        progress("validate", "done", f"atlandi: {e}")
        vnotes = str(e)

    # STEP 3: SEED
    progress("seed", "running")
    t0 = time.time()
    sd = build_seed_from_spec_prompt(spec, title, code_language=code_lang)
    (GEN_DIR / "prompt1_seed.txt").write_text(sd, encoding="utf-8")
    system_prompt = build_system_author(code_lang) if code_lang != "java" else SYSTEM_AUTHOR
    seed_raw = gen.client.generate_text_with_resume(system_prompt, sd)
    (GEN_DIR / "step1_seed.md").write_text(seed_raw, encoding="utf-8")
    progress("seed", "done", f"{len(seed_raw.split())} kel, {time.time()-t0:.1f}s",
             prompt_file=_rel(root, GEN_DIR / "prompt1_seed.txt"),
             output_file=_rel(root, GEN_DIR / "step1_seed.md"))

    # STEP 4: NORMALIZE
    progress("normalize", "running")
    t0 = time.time()
    normalized = normalize(seed_raw, chapter_id, title, gen.config)
    (GEN_DIR / "step2_normalized.md").write_text(normalized, encoding="utf-8")
    progress("normalize", "done", f"{len(normalized.split())} kel, {time.time()-t0:.1f}s",
             output_file=_rel(root, GEN_DIR / "step2_normalized.md"))

    # STEP 5: ENRICH (parallel)
    progress("enrich", "running")
    t0 = time.time()
    sections = extract_sections(normalized)
    headings = [s["heading"] for s in sections if s["heading"] != "__title__"]
    ctx_lines = [line for line in normalized.splitlines() if not line.startswith("---")]
    context = "\n".join(ctx_lines[:20])

    builders: dict = {
        "ozet": ("Bolum Ozeti", build_enrich_summary_prompt, 3),
        "sozluk": ("Terim Sozlugu", build_enrich_glossary_prompt, 3),
        "soru": ("Kendini Degerlendirme", build_enrich_questions_prompt, 3),
        "alistirma": ("Programlama Alistirmalari", build_enrich_exercises_prompt, 3),
        "hata": ("Sik Yapilan Hatalar", build_enrich_errors_prompt, 3),
        "kopru": ("Sonraki Bolume Kopru", build_enrich_bridge_prompt, 4),
    }
    enrich_parts: dict[str, str] = {}
    pending_types = [e for e in enrich_types if e in builders]

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=min(len(pending_types), _MAX_CONCURRENT_ENRICH)
    ) as pool:
        fmap = {}
        for etype in pending_types:
            stitle, builder, nargs = builders[etype]
            up = (builder(chapter_title=title, next_chapter=None,
                          headings=headings, context=context)
                  if nargs == 4
                  else builder(chapter_title=title, headings=headings,
                               context=context))
            fmap[pool.submit(gen.client.generate_text, system_prompt, up)] = etype

        for fut in concurrent.futures.as_completed(fmap):
            etype = fmap[fut]
            try:
                result_text = fut.result()
                enrich_parts[etype] = result_text
                fkey = {"ozet": "summary", "sozluk": "glossary",
                        "soru": "questions", "alistirma": "exercises",
                        "hata": "errors", "kopru": "bridge"}.get(etype, etype)
                (GEN_DIR / f"step3_enrich_{fkey}.md").write_text(
                    result_text, encoding="utf-8")
                append_log(job_id, f"  enrich/{etype}: {len(result_text.split())} kel")
            except Exception as e:
                append_log(job_id, f"  enrich/{etype}: HATA - {e}")

    enrich_files = []
    for etype in enrich_parts:
        fkey = {"ozet": "summary", "sozluk": "glossary",
                "soru": "questions", "alistirma": "exercises",
                "hata": "errors", "kopru": "bridge"}.get(etype, etype)
        enrich_files.append(_rel(root, GEN_DIR / f"step3_enrich_{fkey}.md"))
    enrich_status = f"{len(enrich_parts)}/{len(pending_types)} tamam, {time.time() - t0:.1f}s"
    progress("enrich", "done", enrich_status,
             output_file=", ".join(e for e in enrich_files))

    # STEP 6: ASSEMBLE
    progress("assemble", "running")
    t0 = time.time()
    text = normalized
    end_order = [
        ("alistirma", "Programlama alistirmalari",
         ["alıştırma", "alistirma"]),
        ("soru", "Kendini degerlendirme sorulari",
         ["soru", "değerlendirme", "degerlendirme"]),
        ("sozluk", "Terim sozlugu", ["sözlük", "sozluk"]),
        ("ozet", "Bolum ozeti", ["özet", "ozet"]),
        ("hata", "Sik yapilan hatalar ve yanlis sezgiler",
         ["hata", "yanlış", "yanlis", "yanilgi"]),
    ]
    for key, stitle, terms in reversed(end_order):
        if key in enrich_parts and enrich_parts[key]:
            text = insert_section(text, stitle, enrich_parts[key],
                                 turkish_terms=terms)
    if "kopru" in enrich_parts and enrich_parts["kopru"]:
        text = insert_section(text, "Bir sonraki bolume kopru",
                              enrich_parts["kopru"],
                              turkish_terms=["köprü", "kopru"])

    final = normalize(text, chapter_id, title, gen.config)
    (GEN_DIR / "step4_final.md").write_text(final, encoding="utf-8")
    draft_path = _draft_path(root, chapter_id)
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text(final, encoding="utf-8")
    progress("assemble", "done", f"{len(final.split())} kel, {time.time()-t0:.1f}s",
             output_file=_rel(root, GEN_DIR / "step4_final.md"))
    total_elapsed = round(time.time() - t_all, 1)
    (GEN_DIR / "metrics.json").write_text(
        json.dumps({"chapter": chapter_id, "words": len(final.split()),
                     "time": total_elapsed, "model": model},
                   ensure_ascii=False), encoding="utf-8")

    try:
        from bookmaker.manifest.pipeline import PipelineManager

        PipelineManager(root).update_chapter(chapter_id, current_step="full_text_pasted")
    except Exception as exc:
        append_log(job_id, f"Pipeline state guncellenemedi: {exc}")

    update_job(job_id, status="done", summary={
        "chapter_id": chapter_id, "title": title,
        "words": len(final.split()),
        "elapsed_s": total_elapsed,
        "enriched_count": len(enrich_parts),
        "path": _rel(root, draft_path),
        "draft_path": _rel(root, draft_path),
        "log_path": _rel(root, GEN_DIR),
    })
    append_log(job_id, f"DONE: {len(final.split())} kel, {total_elapsed}s")


def _run_build(root: Path, job_id: str, chapter_id: str, params: dict) -> None:
    """DOCX build isini calistirir."""
    from bookmaker.build.pipeline import build_chapter

    append_log(job_id, "Build basliyor...")
    t0 = time.time()

    source_path = params.get("source_path")
    if source_path:
        p = root / source_path
    else:
        p = next((c for c in _build_source_candidates(root, chapter_id) if c.exists()), None)

    if not p or not p.exists():
        update_job(job_id, status="error", error=f"Kaynak bulunamadi: {chapter_id}")
        return

    result = build_chapter(p)
    elapsed = round(time.time() - t0, 1)
    update_job(job_id, status="done", summary={
        "chapter_id": chapter_id,
        "compiled": result.get("compiled", 0),
        "extracted": result.get("extracted", 0),
        "total": result.get("total_code_blocks", 0),
        "elapsed_s": elapsed,
    })
    append_log(job_id, f"Build done: {elapsed}s")


def save_jobs(project_root: str | Path) -> None:
    path = _jobs_dir(Path(project_root).resolve())
    path.mkdir(parents=True, exist_ok=True)
    with _LOCK:
        for jid, job in _JOBS.items():
            (path / f"{jid}.json").write_text(
                json.dumps(job, ensure_ascii=False, indent=2),
                encoding="utf-8")


def load_jobs(project_root: str | Path) -> None:
    root = Path(project_root).resolve()
    paths = [_jobs_dir(root), _legacy_jobs_dir(root)]
    with _LOCK:
        for path in paths:
            if not path.exists():
                continue
            for f in sorted(path.glob("*.json")):
                try:
                    job = json.loads(f.read_text(encoding="utf-8"))
                    _JOBS[job["id"]] = job
                except (json.JSONDecodeError, KeyError):
                    pass
