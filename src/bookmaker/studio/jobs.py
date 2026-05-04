"""İş servisi — arka plan iş kuyruğu."""

from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

_JOBS: dict[str, dict[str, Any]] = {}
_LOCK = threading.Lock()


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def create_job(step: str, chapter_id: str,
               params: dict | None = None) -> dict:
    """Yeni iş oluşturur."""
    job_id = uuid.uuid4().hex[:12]
    job = {
        "id": job_id, "step": step, "chapter_id": chapter_id,
        "status": "queued", "params": params or {},
        "created_at": _now(), "started_at": None,
        "finished_at": None, "elapsed_s": None,
        "summary": {}, "error": None,
    }
    with _LOCK:
        _JOBS[job_id] = job
    return job


def get_job(job_id: str) -> dict | None:
    """İş durumunu döndürür."""
    with _LOCK:
        job = _JOBS.get(job_id)
        if job:
            return dict(job)
    return None


def list_jobs(limit: int = 20) -> list[dict]:
    """Tüm işleri listeler (en yeniden en eskiye)."""
    with _LOCK:
        jobs = sorted(_JOBS.values(),
                      key=lambda j: j["created_at"], reverse=True)
        return [dict(j) for j in jobs[:limit]]


def update_job(job_id: str, **kwargs) -> dict | None:
    """İş durumunu günceller."""
    with _LOCK:
        job = _JOBS.get(job_id)
        if job:
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
    return None


def cancel_job(job_id: str) -> dict | None:
    """İşi iptal eder."""
    return update_job(job_id, status="cancelled")


def save_jobs(project_root: str | Path) -> None:
    """İşleri dosyaya kaydeder."""
    path = Path(project_root).resolve() / "build" / "studio_jobs"
    path.mkdir(parents=True, exist_ok=True)
    with _LOCK:
        for jid, job in _JOBS.items():
            (path / f"{jid}.json").write_text(
                json.dumps(job, ensure_ascii=False, indent=2),
                encoding="utf-8")


def load_jobs(project_root: str | Path) -> None:
    """İşleri dosyadan yükler."""
    path = Path(project_root).resolve() / "build" / "studio_jobs"
    if not path.exists():
        return
    with _LOCK:
        for f in sorted(path.glob("*.json")):
            try:
                job = json.loads(f.read_text(encoding="utf-8"))
                _JOBS[job["id"]] = job
            except (json.JSONDecodeError, KeyError):
                pass
