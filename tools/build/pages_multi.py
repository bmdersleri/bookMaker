#!/usr/bin/env python3
"""Multi-page build - her bolum ayri HTML, mermaid bloklari global sayaçla resme cevrilir."""
from __future__ import annotations

import re, shutil, subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CHAPTERS_SRC = PROJECT_ROOT / "chapters"
DOCS_DIR = PROJECT_ROOT / "docs"
CHAPTERS_OUT = DOCS_DIR / "chapters"
ASSETS_DIR = DOCS_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
BUILD_OUT = PROJECT_ROOT / "build" / "output"
PANDOC = shutil.which("pandoc") or r"C:\Program Files\Pandoc\pandoc.exe"

CHAPTER_ORDER = [
    ("bolum-01", "1. Java'ya Giris"),
    ("bolum-02", "2. Degiskenler ve Veri Tipleri"),
    ("bolum-03", "3. Operatorler"),
    ("bolum-04", "4. Kontrol Ifadeleri"),
    ("bolum-05", "5. Donguler"),
    ("bolum-06", "6. Diziler"),
    ("bolum-07", "7. Metotlar"),
    ("bolum-08", "8. Nesne Yonelimli Programlama Giris"),
    ("bolum-09", "9. Sinif ve Nesne Yapisi"),
    ("bolum-10", "10. Kalitim ve Cok Bicimlilik"),
    ("bolum-11", "11. Arayuzler ve Soyut Siniflar"),
    ("bolum-12", "12. Icerdelenmis Siniflar"),
    ("bolum-13", "13. Hata Yonetimi"),
    ("bolum-14", "14. Generics"),
    ("bolum-15", "15. Collections Framework"),
    ("bolum-16", "16. Dosya ve Akis Islems"),
    ("bolum-17", "17. Cok Guduklu Programlama"),
    ("bolum-18", "18. Lambda Ifadeleri ve Stream API"),
    ("bolum-19", "19. Java Swing ile GUI Programlama"),
    ("bolum-20", "20. Ag Programlama"),
    ("bolum-21", "21. Veritabani Programlama"),
    ("bolum-22", "22. Java Modul Sistemi"),
    ("bolum-23", "23. Java'nin Gelecegi ve Yeni Ozellikler"),
    ("ek-a", "Ek A: Java Gelistirme Ortaminin Kurulumu"),
    ("ek-b", "Ek B: Temel Linux Komutlari"),
    ("ek-c", "Ek C: Kod Standartlari ve Stil Kilavuzu"),
    ("ek-d", "Ek D: Kaynakca ve Ileri Okumalar"),
]

SIDEBAR_HTML = """<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Java Programlamaya Giris</title><link rel="stylesheet" href="assets/style.css"><style>
:root{--sb:#1e293b;--st:#e2e8f0;--sh:#334155;--sa:#2563eb;--sw:280px}
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;min-height:100vh;font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text)}
.sidebar{position:fixed;top:0;left:0;width:var(--sw);height:100vh;background:var(--sb);color:var(--st);overflow-y:auto;z-index:1000;transition:transform .3s}
.sidebar-header{padding:1.2rem;border-bottom:1px solid rgba(255,255,255,.1)}
.sidebar-header h2{font-size:1rem;margin:0 0 .3rem;color:#fff}
.sidebar-header p{font-size:.75rem;opacity:.6;margin:0}
.sidebar-search{padding:.8rem;border-bottom:1px solid rgba(255,255,255,.08)}
.sidebar-search input{width:100%;padding:.5rem .7rem;border:1px solid rgba(255,255,255,.15);border-radius:6px;background:rgba(255,255,255,.08);color:#fff;font-size:.8rem;outline:none}
.sidebar-search input::placeholder{color:rgba(255,255,255,.35)}
.chapter-list{padding:.5rem 0}
.chapter-item{display:flex;align-items:center;padding:.55rem 1.2rem;cursor:pointer;transition:all .15s;border-left:3px solid transparent;font-size:.85rem;text-decoration:none;color:var(--st)}
.chapter-item:hover{background:var(--sh)}
.chapter-item.active{background:rgba(37,99,235,.15);border-left-color:var(--sa);color:#fff}
.chapter-item .num{min-width:1.8rem;font-size:.75rem;opacity:.5;margin-right:.5rem;text-align:right}
.chapter-item .title{flex:1}
.content{margin-left:var(--sw);flex:1;padding:2rem 2.5rem;min-height:100vh;max-width:900px}
.mobile-toggle{display:none;position:fixed;top:1rem;left:1rem;z-index:1001;background:var(--sb);color:#fff;border:none;border-radius:8px;padding:.5rem .8rem;cursor:pointer;font-size:1.2rem}
@media(max-width:768px){.sidebar{transform:translateX(-100%)}.sidebar.open{transform:translateX(0)}.content{margin-left:0;padding:1rem}.mobile-toggle{display:block}}
</style></head><body>
<button class="mobile-toggle" id="menuToggle">☰</button>
<nav class="sidebar" id="sidebar">
<div class="sidebar-header"><h2>Java Programlamaya Giris</h2><p>Ismail Kirbas</p></div>
<div class="sidebar-search"><input type="text" id="searchInput" placeholder="Bolum ara..."></div>
<div class="chapter-list" id="chapterList">"""

INDEX_CLOSE = """</div></nav>
<main class="content" id="mainContent">
<div id="welcome"><h1>Java Programlamaya Giris</h1><p style="margin:1rem 0;opacity:.7">Ismail Kirbas</p><p>Kitaba baslamak icin soldaki bolumlerden birini secin.</p></div>
<div id="chapter-content" style="display:none"></div></main>
<script>
const s=document.getElementById('sidebar');
document.getElementById('menuToggle').onclick=()=>s.classList.toggle('open');
document.getElementById('searchInput').oninput=function(){const q=this.value.toLowerCase();document.querySelectorAll('.chapter-item').forEach(e=>{e.style.display=e.textContent.toLowerCase().includes(q)?'flex':'none'})};
document.querySelectorAll('.chapter-item').forEach(e=>{e.onclick=async function(ev){ev.preventDefault();document.querySelectorAll('.chapter-item').forEach(i=>i.classList.remove('active'));this.classList.add('active');const slug=this.dataset.slug;document.getElementById('welcome').style.display='none';const c=document.getElementById('chapter-content');c.style.display='block';c.innerHTML='<div class="loading" style="text-align:center;padding:2rem;opacity:.5">Yukleniyor...</div>';if(window.innerWidth<=768)s.classList.remove('open');try{const r=await fetch('chapters/'+slug+'.html');if(!r.ok)throw new Error('HTTP '+r.status);c.innerHTML=await r.text();history.pushState({slug},'',slug);document.title=this.querySelector('.title').textContent+' - Java Programlamaya Giris'}catch(err){c.innerHTML='<div class="error" style="padding:2rem;text-align:center;color:red">Hata: '+err.message+'</div>'}}});
window.onpopstate=function(e){if(e.state&&e.state.slug)document.querySelector('.chapter-item[data-slug="'+e.state.slug+'"]')?.click()};
</script></body></html>"""

mermaid_counter = [0]  # global counter (list for mutability in nested function)

def _replace_mermaid(match):
    """Replace ```mermaid block with image reference."""
    mermaid_counter[0] += 1
    idx = mermaid_counter[0]
    # eger build/output/images/mermaid-{idx:03d}.png varsa...
    img_path = BUILD_OUT / "images" / f"mermaid-{idx:03d}.png"
    if img_path.exists() or (BUILD_OUT / "images" / f"mermaid-{idx:03d}.mmd").exists():
        return f"\n![Mermaid Diyagram {idx}](assets/images/mermaid-{idx:03d}.png)\n"
    return ""

def ensure_dirs():
    CHAPTERS_OUT.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def copy_images():
    src = BUILD_OUT / "images"
    if not src.exists():
        print("  [WARN] Kaynak goruntu dizini yok")
        return
    count = 0
    for png in sorted(src.glob("*.png")):
        shutil.copy2(png, IMAGES_DIR / png.name)
        count += 1
    print(f"  Gorseller: {count} PNG -> {IMAGES_DIR}")

def build_chapter(slug, title):
    src = CHAPTERS_SRC / slug / "draft_versions" / "v001.md"
    dst = CHAPTERS_OUT / f"{slug}.html"
    if not src.exists():
        print(f"  [WARN] {slug}: kaynak yok")
        return False
    content = src.read_text(encoding="utf-8")
    # Mermaid bloklarini resim referanslarina cevir
    content = re.sub(r"```mermaid\s*.*?```\s*", _replace_mermaid, content, flags=re.DOTALL)
    # Gorsel yollari (varsa)
    content = content.replace("./images/", "../assets/images/")
    content = content.replace('src="./images/', 'src="../assets/images/')
    # Frontmatter + H1
    fm = f"---\ntitle: \"{title}\"\nauthor: \"Ismail Kirbas\"\nlang: tr\n---\n"
    content = fm + "# " + title + "\n\n" + content
    temp_md = BUILD_OUT / f"_m_{slug}.md"
    temp_md.write_text(content, encoding="utf-8")
    r = subprocess.run([PANDOC, str(temp_md),
        "--from", "markdown+yaml_metadata_block+smart+raw_html",
        "--to", "html5", "--standalone", "--toc", "--toc-depth", "2",
        "--metadata", f"title={title}", "--css=../assets/style.css",
        "--highlight-style", "pygments", "--section-divs",
        "--wrap=preserve", "-o", str(dst)],
        capture_output=True, text=True, timeout=120)
    temp_md.unlink(missing_ok=True)
    if r.returncode != 0:
        print(f"  [ERROR] {slug}: pandoc basarisiz")
        if r.stderr: print(f"    {r.stderr[:200]}")
        return False
    print(f"  {slug}.html: {dst.stat().st_size//1024} KB")
    return True

def build_index():
    items = []
    for slug, t in CHAPTER_ORDER:
        items.append(f'<a href="#" class="chapter-item" data-slug="{slug}"><span class="title">{t}</span></a>')
    sidebar = "\n".join(items[:23])
    sidebar += '\n<div style="border-top:1px solid rgba(255,255,255,.1);margin:.5rem 1rem;padding-top:.5rem;font-size:.7rem;opacity:.4;text-transform:uppercase;letter-spacing:1px">EKLER</div>\n'
    sidebar += "\n".join(items[23:])
    idx = DOCS_DIR / "index.html"
    idx.write_text(SIDEBAR_HTML + sidebar + INDEX_CLOSE, encoding="utf-8")
    print(f"  index.html: {idx.stat().st_size//1024} KB")

def build():
    print("="*50)
    print("  bookMaker — Multi-Page Build")
    print("="*50)
    ensure_dirs()
    copy_images()
    ok = 0
    for slug, t in CHAPTER_ORDER:
        if build_chapter(slug, t): ok += 1
    print(f"\n  Basarili: {ok}/{len(CHAPTER_ORDER)} bolum (mermaid: {mermaid_counter[0]} adet)")
    build_index()
    total = sum(f.stat().st_size for f in DOCS_DIR.rglob("*") if f.is_file())
    print(f"  Toplam: {total//1024} KB")
    return True

if __name__ == "__main__":
    import sys
    sys.exit(0 if build() else 1)
