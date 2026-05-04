"""FastAPI tabanlı Studio GUI — dashboard, API, bölüm yönetimi."""

from __future__ import annotations

from pathlib import Path

from bookmaker.build.pipeline import build_chapter
from bookmaker.chapter.parser import parse
from bookmaker.chapter.scoring import make_report
from bookmaker.chapter.validator import validate
from bookmaker.llm.config import LLMConfig
from bookmaker.manifest.manager import ManifestManager
from bookmaker.manifest.pipeline import PipelineManager

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
except ImportError:
    FastAPI = None  # type: ignore

app: FastAPI | None = None
templates = None

if FastAPI is not None:
    app = FastAPI(title="bookMaker Studio", version="0.1.0")
    template_dir = Path(__file__).parent / "templates"
    template_dir.mkdir(parents=True, exist_ok=True)
    templates = Jinja2Templates(directory=str(template_dir))

    # --- HTML template ---
    _idx = template_dir / "index.html"
    if not _idx.exists():
        _idx.write_text(
            "<!DOCTYPE html>"
            "<html lang='tr'>"
            "<head><meta charset='UTF-8'><meta name='viewport' content='width=device-width'>"
            "<title>bookMaker Studio</title>"
            "<style>"
            "*{box-sizing:border-box;margin:0;padding:0}"
            "body{font-family:-apple-system,sans-serif;background:#f5f5f5;color:#333}"
            ".nav{background:#1a1a2e;color:#fff;padding:1em 2em}"
            ".nav h1{margin:0;font-size:1.3em}"
            ".container{max-width:1200px;margin:0 auto;padding:2em;display:grid;grid-template-columns:1fr 1fr;gap:1.5em}"
            ".card{background:#fff;border-radius:10px;padding:1.5em;box-shadow:0 2px 8px rgba(0,0,0,.08)}"
            ".card h2{font-size:1em;color:#666;margin-bottom:.5em;text-transform:uppercase;letter-spacing:.5px}"
            ".card .val{font-size:2em;font-weight:700;color:#1a1a2e}"
            ".card.full{grid-column:1/-1}"
            "table{width:100%;border-collapse:collapse;font-size:.9em;margin-top:.5em}"
            "th{text-align:left;padding:.5em;background:#f9f9f9;border-bottom:2px solid #eee;font-weight:600;color:#666}"
            "td{padding:.5em;border-bottom:1px solid #eee}"
            ".tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.8em;font-weight:600}"
            ".tag.pass{background:#d4edda;color:#155724}"
            ".tag.warn{background:#fff3cd;color:#856404}"
            ".tag.fail{background:#f8d7da;color:#721c24}"
            ".btn{display:inline-block;padding:6px 14px;border-radius:6px;text-decoration:none;font-size:.85em;margin:2px}"
            ".btn.primary{background:#1a1a2e;color:#fff}"
            ".btn.outline{border:1px solid #1a1a2e;color:#1a1a2e}"
            ".status-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1em}"
            ".status-item{text-align:center;padding:1em;background:#f9f9f9;border-radius:8px}"
            ".status-item .num{font-size:1.8em;font-weight:700;color:#1a1a2e}"
            ".status-item .lbl{font-size:.8em;color:#888;margin-top:4px}"
            "</style></head><body>"
            "<div class='nav'><h1>📚 bookMaker Studio</h1></div>"
            "<div class='container' id='app'>"
            "<div class='card full'><div class='status-grid' id='status-grid'></div></div>"
            "<div class='card full'><h2>Bolumler</h2><table id='chapters'><tr><th>ID</th><th>Baslik</th><th>Adim</th><th>Skor</th><th>Islem</th></tr></table></div>"
            "<div class='card'><h2>LLM Durum</h2><p id='llm-status'>...</p></div>"
            "<div class='card'><h2>Hizli Eylemler</h2><p><a class='btn primary' href='/'>Yenile</a></p></div>"
            "</div>"
            "<script>"
            "async function load(){let r=await fetch('/api/project');let p=await r.json();"
            "let sg=document.getElementById('status-grid');"
            "sg.innerHTML='<div class=status-item><div class=num>'+p.chapters+'</div><div class=lbl>Bolum</div></div>'"
            "+'<div class=status-item><div class=num>'+(p.title||'(bos)')+'</div><div class=lbl>Kitap</div></div>';"
            "let r2=await fetch('/api/chapters');let chs=await r2.json();"
            "let tb=document.getElementById('chapters');"
            "chs.forEach(function(ch){let row=tb.insertRow();"
            "row.insertCell().textContent=ch.chapter_id;"
            "row.insertCell().textContent=ch.title||'-';"
            "row.insertCell().textContent=ch.current_step||'planned';"
            "row.insertCell().textContent=ch.score||'-';"
            "row.insertCell().innerHTML='<a class=btn outline href=/api/check/'+ch.chapter_id+'>Check</a>';"
            "});"
            "let r3=await fetch('/api/llm-status');let llm=await r3.json();"
            "document.getElementById('llm-status').textContent=llm.status;"
            "}"
            "load();"
            "</script></body></html>",
            encoding="utf-8",
        )

    # --- Routes ---

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> str:
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/api/status")
    async def api_status() -> dict:
        return {"status": "running", "version": "0.1.0", "uptime": "active"}

    @app.get("/api/project")
    async def api_project() -> dict:
        mgr = ManifestManager(Path.cwd())
        manifest = mgr.load_or_generate()
        pipe = PipelineManager(Path.cwd())
        ps = pipe.load()
        return {
            "title": manifest.book.title or "(isimsiz)",
            "chapters": len(manifest.chapters),
            "author": manifest.book.author,
            "stage": ps.current_stage,
        }

    @app.get("/api/chapters")
    async def api_chapters() -> list[dict]:
        mgr = ManifestManager(Path.cwd())
        manifest = mgr.load_or_generate()
        pm = PipelineManager(Path.cwd())
        ps = pm.load()
        result = []
        for ch in manifest.chapters:
            cs = ps.chapters.get(ch.chapter_id)
            result.append({
                "chapter_id": ch.chapter_id,
                "title": ch.title,
                "order": ch.order,
                "status": ch.status,
                "current_step": cs.current_step if cs else "planned",
                "score": cs.score if cs else 0,
            })
        return result

    @app.get("/api/check/{chapter_id}")
    async def api_check(chapter_id: str) -> dict:
        mgr = ManifestManager(Path.cwd())
        manifest = mgr.load_or_generate()
        for ch in manifest.chapters:
            if ch.chapter_id == chapter_id:
                src = ch.source
                break
        else:
            return {"error": f"Bolum bulunamadi: {chapter_id}"}
        p = Path.cwd() / src
        if not p.exists():
            return {"error": f"Dosya bulunamadi: {p}"}
        parsed = parse(p)
        issues = validate(parsed)
        report = make_report(chapter_id, issues)
        return {
            "chapter_id": chapter_id,
            "score": report.score,
            "decision": report.decision.value,
            "errors": report.error_count,
            "warnings": report.warning_count,
        }

    @app.get("/api/build/{chapter_id}")
    async def api_build(chapter_id: str) -> dict:
        mgr = ManifestManager(Path.cwd())
        manifest = mgr.load_or_generate()
        for ch in manifest.chapters:
            if ch.chapter_id == chapter_id:
                src = ch.source
                break
        else:
            return {"error": f"Bolum bulunamadi: {chapter_id}"}
        p = Path.cwd() / src
        if not p.exists():
            return {"error": f"Dosya bulunamadi: {p}"}
        result = build_chapter(p)
        return {
            "chapter_id": chapter_id,
            "compiled": result.get("compiled", 0),
            "extracted": result.get("extracted", 0),
            "total": result.get("total_code_blocks", 0),
        }

    @app.get("/api/llm-status")
    async def api_llm_status() -> dict:
        cfg = LLMConfig(Path.cwd())
        if cfg.is_configured():
            return {"status": "Hazir", "provider": cfg.provider, "model": cfg.model}
        return {"status": "Yapilandirilmamis", "provider": "", "model": ""}


def run_studio(host: str = "127.0.0.1", port: int = 8765) -> None:
    """Studio'yu başlatır."""
    if app is None:
        raise ImportError("FastAPI veya Jinja2 kurulu degil. 'uv sync' calistirin.")
    import uvicorn
    uvicorn.run(app, host=host, port=port)
