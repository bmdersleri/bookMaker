"""GitHub Pages icin kitap HTML'ini olusturur."""
from pathlib import Path
import shutil, subprocess

ROOT = Path(__file__).resolve().parent.parent.parent
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
IMAGES = ASSETS / "images"
BUILD_OUT = ROOT / "build" / "output"
PANDOC = r"C:\Program Files\Pandoc\pandoc.exe"

def build():
    ASSETS.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)
    print(f"OK: dizinler olusturuldu ({DOCS})")

    # CSS
    css = '''/* bookMaker theme */
:root{--bg:#fff;--text:#1a1a2e;--accent:#2563eb;--code-bg:#f1f5f9;--border:#e2e8f0}
@media(prefers-color-scheme:dark){:root{--bg:#0f172a;--text:#e2e8f0;--accent:#60a5fa;--code-bg:#1e293b;--border:#334155}}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;line-height:1.7;color:var(--text);background:var(--bg);max-width:900px;margin:0 auto;padding:2rem 1.5rem}
h1{font-size:2rem;border-bottom:2px solid var(--accent);padding-bottom:.5rem;margin-top:2rem}
h2{font-size:1.5rem;border-bottom:1px solid var(--border);padding-bottom:.3rem;margin-top:2rem}
p{margin:1rem 0}
a{color:var(--accent);text-decoration:none}
pre{background:var(--code-bg);border:1px solid var(--border);border-radius:8px;padding:1rem;overflow-x:auto;font-size:.85rem;margin:1rem 0;font-family:'JetBrains Mono',monospace}
code{background:var(--code-bg);padding:.15rem .4rem;border-radius:4px;font-size:.85em;font-family:'JetBrains Mono',monospace}
pre code{background:none;padding:0}
blockquote{border-left:4px solid var(--accent);background:var(--code-bg);padding:.8rem 1.2rem;margin:1rem 0;border-radius:0 8px 8px 0}
table{width:100%;border-collapse:collapse;margin:1rem 0}
th,td{border:1px solid var(--border);padding:.6rem .8rem;text-align:left}
th{background:var(--accent);color:#fff}
img{max-width:100%;height:auto;border-radius:8px;margin:1.5rem 0;border:1px solid var(--border)}
nav#TOC{background:var(--code-bg);border:1px solid var(--border);border-radius:8px;padding:1.2rem 1.5rem;margin:1.5rem 0 2rem}
nav#TOC h2{margin-top:0;border:none}
footer{margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--border)}
@media(max-width:768px){body{padding:1rem;font-size:.95rem}h1{font-size:1.5rem}}
'''
    (ASSETS / "style.css").write_text(css, encoding="utf-8")
    print(f"OK: style.css ({len(css)} chars)")

    # Images
    count = 0
    for png in sorted(BUILD_OUT.glob("images/*.png")):
        shutil.copy2(png, IMAGES / png.name)
        count += 1
    print(f"OK: {count} PNG kopyalandi")

    # HTML
    src = BUILD_OUT / "java-programlamaya-giris.md"
    html_out = DOCS / "index.html"
    content = src.read_text(encoding="utf-8")
    content = content.replace("](./images/", "](./assets/images/")
    content = content.replace('src="./images/', 'src="./assets/images/')
    temp = BUILD_OUT / "_pages_temp.md"
    temp.write_text(content, encoding="utf-8")

    result = subprocess.run([
        PANDOC, str(temp),
        "--from", "markdown+yaml_metadata_block+smart+raw_html",
        "--to", "html5", "--standalone", "--toc", "--toc-depth", "3",
        "--metadata", "title=Java Programlamaya Giris",
        f"--css={ASSETS / 'style.css'}",
        "--highlight-style", "pygments", "--section-divs",
        "--wrap=preserve", "-o", str(html_out),
    ], capture_output=True, text=True, timeout=120)
    temp.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"PANDOC HATA: {result.stderr[:500]}")
        return False

    size = html_out.stat().st_size
    print(f"OK: index.html ({size/1024:.0f} KB)")

    # README
    (DOCS / "README.md").write_text(
        "# Java Programlamaya Giris\n\nIsmail Kirbas (c) 2026\n\n"
        "- [Kitabi Oku](index.html)\n"
        "- [GitHub](https://github.com/bmdersleri/bookMaker)\n",
        encoding="utf-8"
    )
    print(f"OK: README.md")

    total = sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file())
    print(f"\nToplam: {total/1024:.0f} KB")
    print(f"Site: https://bmdersleri.github.io/bookMaker/")
    return True

if __name__ == "__main__":
    import sys
    ok = build()
    sys.exit(0 if ok else 1)
