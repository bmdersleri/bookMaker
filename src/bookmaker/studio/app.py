"""FastAPI tabanlı Studio GUI."""

from __future__ import annotations

from pathlib import Path

from bookmaker.manifest.manager import ManifestManager

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
except ImportError:
    FastAPI = None

app: FastAPI | None = None
templates = None

if FastAPI is not None:
    app = FastAPI(title="bookMaker Studio", version="0.1.0")
    template_dir = Path(__file__).parent / "templates"
    template_dir.mkdir(parents=True, exist_ok=True)
    templates = Jinja2Templates(directory=str(template_dir))

    _index_html = template_dir / "index.html"
    if not _index_html.exists():
        style = (
            "body{font-family:sans-serif;max-width:800px;"
            "margin:auto;padding:2em;}"
            "h1{color:#333;}"
            ".card{border:1px solid #ddd;padding:1em;"
            "margin:1em 0;border-radius:8px;}"
        )
        html = (
            "<!DOCTYPE html><html lang='tr'>"
            "<head><meta charset='UTF-8'><title>bookMaker Studio</title>"
            "<style>" + style + "</style></head><body>"
            "<h1>📚 bookMaker Studio</h1>"
            "<div class='card'><h2>Kitap Bilgisi</h2><p id='info'></p></div>"
            "<div class='card'><h2>Durum</h2><p id='status'>Yukleniyor...</p></div>"
            "<script>"
            "fetch('/api/status').then(r=>r.json()).then(d=>{"
            "document.getElementById('info').textContent=d.book||'Yok';"
            "document.getElementById('status').textContent=d.status||'Calisiyor';"
            "})</script></body></html>"
        )
        _index_html.write_text(html, encoding="utf-8")

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> str:
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/api/status")
    async def api_status() -> dict:
        return {"status": "running", "version": "0.1.0"}

    @app.get("/api/project")
    async def api_project() -> dict:
        mgr = ManifestManager(Path.cwd())
        manifest = mgr.load_or_generate()
        return {
            "title": manifest.book.title or "(isimsiz)",
            "chapters": len(manifest.chapters),
            "author": manifest.book.author,
        }


def run_studio(host: str = "127.0.0.1", port: int = 8765) -> None:
    """Studio'yu başlatır."""
    if app is None:
        raise ImportError("FastAPI veya Jinja2 kurulu degil.")
    import uvicorn
    uvicorn.run(app, host=host, port=port)
