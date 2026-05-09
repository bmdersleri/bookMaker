"""Assemble servisi — kitap birleştirme, indeks, glossary."""

from __future__ import annotations

import re
from pathlib import Path

from bookmaker.manifest.manager import ManifestManager


def assemble_book(project_root: str | Path,
                  chapter_ids: list[str] | None = None) -> dict:
    """Tüm bölüm markdown'larını birleştirip kitap.md olarak kaydeder."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    targets = []
    for ch in manifest.chapters:
        if chapter_ids and ch.chapter_id not in chapter_ids:
            continue
        src = ch.source
        p = root / src if src else None
        if p and p.exists():
            targets.append((ch.order, ch.chapter_id, ch.title or ch.chapter_id, p))

    targets.sort(key=lambda x: x[0])

    out_dir = root / "build"
    out_dir.mkdir(parents=True, exist_ok=True)

    toc_lines = ["# İçindekiler\n"]
    body_parts = []
    heading_map: dict[str, list[str]] = {}  # chapter_id -> headings

    for order, cid, title, path in targets:
        text = path.read_text(encoding="utf-8")
        toc_lines.append(f"{order}. [{title}](#{cid})")
        body_parts.append(f"\n\n---\n\n{text}")
        # Topla başlıkları indeks için
        headings = re.findall(r'^#{2,4}\s+(.+)$', text, re.MULTILINE)
        heading_map[cid] = [h.strip() for h in headings]

    full_text = "\n".join(toc_lines) + "\n\n---\n\n" + "\n".join(body_parts).lstrip("\n")
    out_path = out_dir / "kitap_birlestirilmis.md"
    out_path.write_text(full_text, encoding="utf-8")

    return {
        "path": str(out_path.relative_to(root)),
        "words": len(full_text.split()),
        "chars": len(full_text),
        "chapters": len(targets),
        "output": full_text[:500],
    }


def generate_index(project_root: str | Path) -> dict:
    """Tüm bölüm başlıklarından detaylı indeks oluşturur."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    index_entries: list[dict] = []

    for ch in manifest.chapters:
        src = ch.source
        p = root / src if src else None
        if not p or not p.exists():
            continue

        text = p.read_text(encoding="utf-8")
        headings = re.findall(r'^(#{2,4})\s+(.+)$', text, re.MULTILINE)

        for level_marker, heading in headings:
            level = len(level_marker)  # 2, 3, 4
            index_entries.append({
                "chapter_id": ch.chapter_id,
                "chapter_title": ch.title or ch.chapter_id,
                "level": level,
                "heading": heading.strip(),
                "order": ch.order,
            })

    out_dir = root / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "indeks.md"

    lines = ["# İndeks\n"]
    for entry in index_entries:
        indent = "  " * (entry["level"] - 2)
        lines.append(f"{indent}- **{entry['heading']}** → {entry['chapter_id']}")

    out_path.write_text("\n".join(lines), encoding="utf-8")

    return {
        "path": str(out_path.relative_to(root)),
        "entries": len(index_entries),
        "chapters_indexed": len({e["chapter_id"] for e in index_entries}),
    }


def generate_glossary(project_root: str | Path) -> dict:
    """Koddaki sınıf/metot isimlerinden glossary oluşturur."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    terms: dict[str, set[str]] = {}  # term -> set of chapter_ids

    for ch in manifest.chapters:
        src = ch.source
        p = root / src if src else None
        if not p or not p.exists():
            continue

        text = p.read_text(encoding="utf-8")

        # Java sınıf isimleri
        for m in re.finditer(r'```java\n(.*?)```', text, re.DOTALL):
            block = m.group(1)
            classes = re.findall(r'(?:public\s+)?class\s+(\w+)', block)
            for cls in classes:
                terms.setdefault(cls, set()).add(ch.chapter_id)
            methods = re.findall(r'(?:public|private|protected)\s+\w+\s+(\w+)\s*\(', block)
            for method in methods:
                terms.setdefault(method, set()).add(ch.chapter_id)

        # Markdown içindeki **vurgulu** terimler
        for m in re.finditer(r'\*\*(.+?)\*\*', text):
            term = m.group(1).strip()
            if len(term) > 2 and len(term) < 50 and not term.startswith("http"):
                terms.setdefault(term, set()).add(ch.chapter_id)

    out_dir = root / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "glossary.md"

    lines = ["# Glossary / Terimler Sözlüğü\n"]
    for term in sorted(terms.keys(), key=str.lower):
        chapters_str = ", ".join(sorted(terms[term]))
        lines.append(f"- **{term}**: {chapters_str}")

    out_path.write_text("\n".join(lines), encoding="utf-8")

    return {
        "path": str(out_path.relative_to(root)),
        "terms": len(terms),
    }
