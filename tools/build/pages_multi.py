#!/usr/bin/env python3
"""Multi-page GitHub Pages build - her bolum ayri sayfa + sidebar navigasyon.

Kullanim:
    python tools/build/pages_multi.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CHAPTERS_DIR = PROJECT_ROOT / "chapters"
DOCS_DIR = PROJECT_ROOT / "docs"
CHAPTERS_OUT = DOCS_DIR / "chapters"
ASSETS_DIR = DOCS_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
BUILD_OUT = PROJECT_ROOT / "build" / "output"
PANDOC = shutil.which("pandoc") or r"C:\Program Files\Pandoc\pandoc.exe"

CHAPTER_ORDER = [
    ("bolum-01", "Java'ya Giris"),
    ("bolum-02", "Degiskenler ve Veri Tipleri"),
    ("bolum-03", "Operatorler"),
    ("bolum-04", "Kontrol Ifadeleri"),
    ("bolum-05", "Donguler"),
    ("bolum-06", "Diziler"),
    ("bolum-07", "Metotlar"),
    ("bolum-08", "Nesne Yonelimli Programlama Giris"),
    ("bolum-09", "Sinif ve Nesne Yapisi"),
    ("bolum-10", "Kalitim ve Cok Bicimlilik"),
    ("bolum-11", "Arayuzler ve Soyut Siniflar"),
    ("bolum-12", "Icerdelenmis Siniflar"),
    ("bolum-13", "Hata Yonetimi"),
    ("bolum-14", "Generics"),
    ("bolum-15", "Collections Framework"),
    ("bolum-16", "Dosya ve Akis Islems"),
    ("bolum-17", "Cok Guduklu Programlama"),
    ("bolum-18", "Lambda ifadeleri ve Stream API"),
    ("bolum-19", "Java Swing ile GUI Programlama"),
    ("bolum-20", "Ag Programlama"),
    ("bolum-21", "Veritabani Programlama"),
    ("bolum-22", "Java Modul Sistemi"),
    ("bolum-23", "Java'nin Gelecegi ve Yeni Ozellikler"),
    ("ek-a", "Java Geli tirme Ortaminin Kurulumu"),
    ("ek-b", "Temel Linux Komutlari"),
    ("ek-c", "Kod Standartlari ve Stil Kilavuzu"),
    ("ek-d", "Kaynakca ve Ileri Okumalar"),
]

SIDEBAR_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Java Programlamaya Giris</title>
<link rel="stylesheet" href="assets/style.css">
<style>
:root{--sidebar-bg:#1e293b;--sidebar-text:#e2e8f0;--sidebar-hover:#334155;--sidebar-active:#2563eb;--sidebar-width:280px}
*{margin:0;padding:0;box-sizing:border-box}
body{display:flex;min-height:100vh;font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text)}
.sidebar{position:fixed;top:0;left:0;width:var(--sidebar-width);height:100vh;background:var(--sidebar-bg);color:var(--sidebar-text);overflow-y:auto;z-index:1000;transition:transform .3s ease}
.sidebar-header{padding:1.2rem;border-bottom:1px solid rgba(255,255,255,.1)}
.sidebar-header h2{font-size:1rem;margin:0 0 .3rem;color:#fff}
.sidebar-header p{font-size:.75rem;opacity:.6;margin:0}
.sidebar-search{padding:.8rem;border-bottom:1px solid rgba(255,255,255,.08)}
.sidebar-search input{width:100%;padding:.5rem .7rem;border:1px solid rgba(255,255,255,.15);border-radius:6px;background:rgba(255,255,255,.08);color:#fff;font-size:.8rem;outline:none}
.sidebar-search input::placeholder{color:rgba(255,255,255,.35)}
.chapter-list{padding:.5rem 0}
.chapter-item{display:flex;align-items:center;padding:.55rem 1.2rem;cursor:pointer;transition:all .15s;border-left:3px solid transparent;font-size:.85rem;text-decoration:none;color:var(--sidebar-text)}
.chapter-item:hover{background:var(--sidebar-hover)}
.chapter-item.active{background:rgba(37,99,235,.15);border-left-color:var(--sidebar-active);color:#fff}
.chapter-item .num{min-width:1.8rem;font-size:.75rem;opacity:.5;margin-right:.5rem;text-align:right}
.chapter-item .title{flex:1}
.content{margin-left:var(--sidebar-width);flex:1;padding:2rem 2.5rem;min-height:100vh;max-width:900px}
#chapter-content h1{font-size:1.8rem;margin-top:0}
#chapter-content h2{font-size:1.4rem;margin-top:1.8rem}
.loading{text-align:center;padding:3rem;opacity:.5}
.error{text-align:center;padding:2rem;color:var(--accent);background:var(--code-bg);border-radius:8px}
.mobile-toggle{display:none;position:fixed;top:1rem;left:1rem;z-index:1001;background:var(--sidebar-bg);color:#fff;border:none;border-radius:8px;padding:.5rem .8rem;cursor:pointer;font-size:1.2rem}
@media(max-width:768px){.sidebar{transform:translateX(-100%)}.sidebar.open{transform:translateX(0)}.content{margin-left:0;padding:1rem}.mobile-toggle{display:block}}
@media(prefers-color-scheme:light){:root{--sidebar-bg:#1e293b;--sidebar-text:#e2e8f0}}
</style>
</head>
<body>
<button class="mobile-toggle" id="menuToggle">☰</button>
<nav class="sidebar" id="sidebar">
<div class="sidebar-header">
<h2>Java Programlamaya Giris</h2>
<p>Ismail Kirbas &copy; 2026</p>
</div>
<div class="sidebar-search">
<input type="text" id="searchInput" placeholder="Bolum ara...">
</div>
<div class="chapter-list" id="chapterList">
"""

CHAPTER_LINK_TPL = '<a href="#" class="chapter-item" data-slug="{slug}" data-chapter="{num}"><span class="num">{num}</span><span class="title">{title}</span></a>'

INDEX_CLOSE = """</div>
</nav>
<main class="content" id="mainContent">
<div id="welcome">
<h1>Java Programlamaya Giris</h1>
<p style="font-size:1.1rem;margin:1rem 0;opacity:.7">Ismail Kirbas &copy; 2026</p>
<hr style="margin:2rem 0;border-color:var(--border)">
<p>Kitaba baslamak icin soldaki bolumlerden birini secin.</p>
</div>
<div id="chapter-content" style="display:none"></div>
</main>
<script>
const sidebar=document.getElementById('sidebar');
document.getElementById('menuToggle').onclick=()=>sidebar.classList.toggle('open');
document.getElementById('searchInput').oninput=function(){const q=this.value.toLowerCase();document.querySelectorAll('.chapter-item').forEach(el=>{el.style.display=el.textContent.toLowerCase().includes(q)?'flex':'none'})};
document.querySelectorAll('.chapter-item').forEach(el=>{el.onclick=async function(e){e.preventDefault();document.querySelectorAll('.chapter-item').forEach(i=>i.classList.remove('active'));this.classList.add('active');const slug=this.dataset.slug;const main=document.getElementById('mainContent');document.getElementById('welcome').style.display='none';const ch=document.getElementById('chapter-content');ch.style.display='block';ch.innerHTML='<div class="loading">Yukleniyor...</div>';if(window.innerWidth<=768)sidebar.classList.remove('open');try{const res=await fetch('chapters/'+slug+'.html');if(!res.ok)throw new Error('HTTP '+res.status);let html=await res.text();ch.innerHTML=html;history.pushState({slug},'',slug);document.title=this.querySelector('.title').textContent+' - Java Programlamaya Giris'}catch(err){ch.innerHTML='<div class="error">Bolum yuklenemedi: '+err.message+'</div>'}}});
window.onpopstate=function(e){if(e.state&&e.state.slug){const el=document.querySelector('.chapter-item[data-slug="'+e.state.slug+'"]');if(el)el.click()}};
document.querySelector('.chapter-item:first-child')?.click();
</script>
</body>
</html>"""


def slug_for_file(slug: str) -> str:
    chapter_map = {s: str(i+1) for i, (s, _) in enumerate(CHAPTER_ORDER) if not s.startswith("ek-")}
    ek_map = {s: chr(65 + i) for i, (s, _) in enumerate(CHAPTER_ORDER[23:])}  # A, B, C, D
    if slug in chapter_map:
        return chapter_map[slug]
    if slug in ek_map:
        return ek_map[slug]
    return slug


def ensure_dirs():
    CHAPTERS_OUT.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def copy_assets():
    css_src = ASSETS_DIR / "style.css"
    if css_src.exists():
        print(f"  CSS: {css_src} ({css_src.stat().st_size} bytes)")


def copy_images():
    src_dir = BUILD_OUT / "images"
    if not src_dir.exists():
        print("  [WARN] Kaynak goruntu dizini yok")
        return
    count = 0
    for png in sorted(src_dir.glob("*.png")):
        shutil.copy2(png, IMAGES_DIR / png.name)
        count += 1
    print(f"  Gorseller: {count} PNG")


def build_chapter_html(slug: str, title: str) -> bool:
    src_md = CHAPTERS_DIR / slug / "draft_versions" / "v001.md"
    dst_html = CHAPTERS_OUT / f"{slug}.html"
    
    if not src_md.exists():
        print(f"  [WARN] {slug}: kaynak MD bulunamadi")
        return False
    
    content = src_md.read_text(encoding="utf-8")
    
    # Gorsel yollari
    content = content.replace("./images/", "../assets/images/")
    content = content.replace('src="./images/', 'src="../assets/images/')
    
    # Mermaid kod bloklarini sil
    content = re.sub(r"```mermaid\s*.*?```\s*", "", content, flags=re.DOTALL)
    
    # Frontmatter ekle
    fm = f"""---
title: "{title}"
subtitle: "Java Programlamaya Giris"
author: "Ismail Kirbas"
lang: tr
---
"""
    content = fm + "\n" + content.lstrip()
    # Ilk H1'i kitap adindan bolum adina cevir
    content = re.sub(r"^# .+", f"# {title}", content, count=1)
    
    temp_md = BUILD_OUT / f"_multi_{slug}.md"
    temp_md.write_text(content, encoding="utf-8")
    
    css_path = "../assets/style.css"
    
    cmd = [
        PANDOC,
        str(temp_md),
        "--from", "markdown+yaml_metadata_block+smart+raw_html",
        "--to", "html5",
        "--standalone",
        "--toc", "--toc-depth", "2",
        "--metadata", f"title={title}",
        f"--css={css_path}",
        "--highlight-style", "pygments",
        "--section-divs",
        "--wrap=preserve",
        "-o", str(dst_html),
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    temp_md.unlink(missing_ok=True)
    
    if result.returncode != 0:
        print(f"  [ERROR] {slug}: pandoc basarisiz ({result.returncode})")
        return False
    
    size = dst_html.stat().st_size
    print(f"  {slug}.html: {size//1024} KB")
    return True


def build_index():
    idx_path = DOCS_DIR / "index.html"
    
    # Sidebar items
    items = []
    for i, (slug, title) in enumerate(CHAPTER_ORDER, 1):
        num = str(i)
        items.append(f'<a href="#" class="chapter-item" data-slug="{slug}" data-chapter="{num}"><span class="num">{num}</span><span class="title">{title}</span></a>')
    
    # Ayrac
    sidebar_items = "\n".join(items[:23])
    sidebar_items += '\n<div style="border-top:1px solid rgba(255,255,255,.1);margin:.5rem 1rem;padding-top:.5rem;font-size:.7rem;opacity:.4;text-transform:uppercase;letter-spacing:1px">Ekler</div>\n'
    sidebar_items += "\n".join(items[23:])
    
    html = SIDEBAR_HTML + sidebar_items + INDEX_CLOSE
    idx_path.write_text(html, encoding="utf-8")
    print(f"\n  index.html: {idx_path.stat().st_size//1024} KB")
    return True


def build():
    print("=" * 50)
    print("  bookMaker — Multi-Page Build")
    print("=" * 50)
    
    ensure_dirs()
    copy_assets()
    copy_images()
    
    print(f"\n  {len(CHAPTER_ORDER)} bolum HTML'i olusturuluyor...")
    ok = 0
    for slug, title in CHAPTER_ORDER:
        if build_chapter_html(slug, title):
            ok += 1
    
    print(f"\n  Basarili: {ok}/{len(CHAPTER_ORDER)} bolum")
    
    build_index()
    
    total = sum(f.stat().st_size for f in DOCS_DIR.rglob("*") if f.is_file())
    print(f"\n  Toplam: {total:,} bytes ({total/1024:.0f} KB)")
    print(f"  Dizin: {DOCS_DIR}")
    print("=" * 50)
    return True


if __name__ == "__main__":
    import sys
    success = build()
    sys.exit(0 if success else 1)
