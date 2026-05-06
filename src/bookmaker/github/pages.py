"""GitHub Pages kod sayfaları üretimi."""

from __future__ import annotations

from pathlib import Path


def generate_code_page(
    code_id: str,
    file_name: str,
    code_content: str,
    output_dir: Path,
    repo_url: str = "",
) -> Path:
    """Tek bir kod için GitHub Pages uyumlu HTML sayfası üretir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    title = f"{code_id} — {file_name}"
    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
</head>
<body>
<h1>{title}</h1>
<pre><code class="language-java">{code_content}</code></pre>
</body>
</html>"""
    out = output_dir / f"{code_id}.html"
    out.write_text(html, encoding="utf-8")
    return out


def generate_index_page(entries: list[dict], output_dir: Path, title: str = "Kod Listesi") -> Path:
    """Kod listesi için ana index sayfası üretir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "<!DOCTYPE html>",
        "<html lang='tr'>",
        "<head><meta charset='UTF-8'><title>" + title + "</title></head>",
        "<body>",
        "<h1>" + title + "</h1><ul>",
    ]
    for e in entries:
        cid = e.get("code_id", "?")
        fn = e.get("file", "?")
        url = e.get("github_url", f"{cid}.html")
        lines.append(f'<li><a href="{url}">{cid} — {fn}</a></li>')
    lines.append("</ul></body></html>")
    html = "\n".join(lines)
    out = output_dir / "index.html"
    out.write_text(html, encoding="utf-8")
    return out
