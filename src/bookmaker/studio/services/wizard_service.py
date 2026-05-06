"""Kitap oluşturma sihirbazı servisi."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from bookmaker.generation.prompts import SYSTEM_AUTHOR

_DEFAULT_CHAPTERS = [
    "bolum-01", "bolum-02", "bolum-03", "bolum-04", "bolum-05",
    "bolum-06", "bolum-07", "bolum-08", "bolum-09", "bolum-10",
    "bolum-11", "bolum-12", "bolum-13", "bolum-14", "bolum-15",
    "bolum-16", "bolum-17", "bolum-18", "bolum-19", "bolum-20",
    "bolum-21", "bolum-22", "bolum-23",
    "ek-a", "ek-b", "ek-c", "ek-d",
]

# ================================================================
# CREATE BOOK
# ================================================================

def create_book(project_root: str | Path, data: dict) -> dict:
    """Yeni kitap projesi oluşturur.

    data = {
        "project_name": "java-temelleri",
        "title": "Java'nın Temelleri",
        "title_en": "Java Fundamentals",
        "author": "İsmail Kırbaş",
        "language": "tr",
        "chapter_count": 23,
        "appendix_count": 4,
        "chapters": ["bolum-01", ...],       # opsiyonel: manuel plan
        "book_type": "ders_kitabi",          # ders_kitabi | referans | el_kitabi
    }
    """
    try:
        root = Path(project_root).resolve()
        project_name = data.get("project_name", "").strip()
        if not project_name or not project_name.replace("-", "").replace("_", "").isalnum():
            return {"error": "Geçersiz proje adı. Sadece a-z, 0-9, -, _ kullanın."}

        book_dir = root / "book_projects" / project_name
        if book_dir.exists():
            return {"error": f"Proje zaten var: {project_name}"}

        # Dizin yapısını oluştur
        _create_directory_structure(book_dir, data)

        # Dosyaları oluştur
        chapter_count = data.get("chapter_count", 23)
        appendix_count = data.get("appendix_count", 4)
        chapters = data.get("chapters") or _DEFAULT_CHAPTERS[:chapter_count + appendix_count]

        _create_book_profile(book_dir, data)
        _create_book_manifest(book_dir, data, chapters)
        _create_book_architecture(book_dir, data)
        _create_pipeline_state(book_dir, chapters)
        _create_llm_config(book_dir, data)
        _create_chapter_dirs(book_dir, chapters)

        return {"project_name": project_name,
                "path": str(book_dir.relative_to(root)),
                "chapters": len(chapters),
                "title": data.get("title", "")}

    except Exception as e:
        return {"error": f"Kitap oluşturulamadı: {str(e)[:300]}"}


def _create_directory_structure(book_dir: Path, data: dict) -> None:
    """Proje dizin yapısını oluşturur."""
    dirs = [
        book_dir,
        book_dir / "chapters",
        book_dir / "build",
        book_dir / "build" / "exports",
        book_dir / "build" / "code",
        book_dir / "build" / "mermaid_images",
        book_dir / "build" / "generation",
        book_dir / "kodlar",
        book_dir / "assets" / "auto",
        book_dir / "assets" / "manual",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def _create_book_profile(book_dir: Path, data: dict) -> None:
    """book_profile.yaml oluşturur."""
    import yaml as _yaml
    profile = {
        "book": {
            "title": data.get("title", ""),
            "author": data.get("author", ""),
            "language": data.get("language", "tr"),
            "lang": data.get("language", "tr-TR"),
            "target_audience": data.get("audience", "universite_1"),
        },
        "pandoc": {
            "from_format": "markdown+tex_math_single_backslash",
            "reference_doc": "build/referenceV17_java_temelleri.docx",
            "toc": True,
            "toc_depth": 2,
        },
        "outputs": {"docx": True, "pdf": False, "epub": False, "html_site": False},
        "ci": {"enabled": True, "fail_on_code_error": True},
    }
    (book_dir / "book_profile.yaml").write_text(
        _yaml.dump(profile, allow_unicode=True, default_flow_style=False),
        encoding="utf-8")


def _create_book_manifest(book_dir: Path, data: dict, chapters: list[str]) -> None:
    """book_manifest.yaml oluşturur."""
    import yaml as _yaml
    manifest = {
        "book": {
            "title": data.get("title", ""),
            "author": data.get("author", ""),
            "lang": data.get("language", "tr-TR"),
        },
        "paths": {"chapters_dir": "chapters", "build_dir": "build"},
        "chapters": [
            {
                "order": i + 1,
                "chapter_id": cid,
                "title": "",
                "status": "planned",
                "source": f"chapters/{cid}/approved/{cid}_v001.md",
            }
            for i, cid in enumerate(chapters)
        ],
    }
    (book_dir / "book_manifest.yaml").write_text(
        _yaml.dump(manifest, allow_unicode=True, default_flow_style=False),
        encoding="utf-8")


def _create_book_architecture(book_dir: Path, data: dict) -> None:
    """book_architecture.yaml oluşturur."""
    import yaml as _yaml
    arch = {
        "book_id": data.get("project_name", ""),
        "title": data.get("title", ""),
        "type": data.get("book_type", "ders_kitabi"),
        "version": "0.1.0",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    (book_dir / "book_architecture.yaml").write_text(
        _yaml.dump(arch, allow_unicode=True, default_flow_style=False),
        encoding="utf-8")


def _create_pipeline_state(book_dir: Path, chapters: list[str]) -> None:
    """pipeline_state.yaml oluşturur."""
    import yaml as _yaml
    state = {
        "book_id": book_dir.name,
        "pipeline_id": f"pl_{book_dir.name}_{datetime.now().strftime('%Y%m%d')}_001",
        "current_stage": "authoring",
        "chapters": {
            cid: {"current_step": "planned", "score": 0,
                  "decision": "revision_required", "error_count": 0,
                  "warning_count": 0}
            for cid in chapters
        },
    }
    (book_dir / "pipeline_state.yaml").write_text(
        _yaml.dump(state, allow_unicode=True, default_flow_style=False),
        encoding="utf-8")


def _create_llm_config(book_dir: Path, data: dict) -> None:
    """llm_config.json oluşturur."""
    cfg = [{
        "provider": data.get("provider", "deepseek"),
        "api_key": data.get("api_key", ""),
        "model": data.get("model", "deepseek-chat"),
    }]
    (book_dir / "llm_config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def _create_chapter_dirs(book_dir: Path, chapters: list[str]) -> None:
    """Bölüm dizinlerini oluşturur."""
    for cid in chapters:
        cdir = book_dir / "chapters" / cid
        for sub in ["approved", "draft_versions", "seed", "outline_versions"]:
            (cdir / sub).mkdir(parents=True, exist_ok=True)


# ================================================================
# LLM PLAN
# ================================================================

def generate_llm_plan(project_root: str | Path, client: Any,
                      topic: str, chapter_count: int = 23,
                      appendix_count: int = 4,
                      language: str = "tr") -> list[dict]:
    """LLM ile bölüm planı oluşturur.

    Returns:
        [{"chapter_id": "bolum-01", "title": "Java'ya Giriş", "type": "core"}, ...]
    """
    prompt = f"""## Görev: Kitap Bölüm Planı Oluştur

**Konu:** {topic}
**Bölüm Sayısı:** {chapter_count} ana bölüm + {appendix_count} ek
**Dil:** {language}

Her bölüm için:
- chapter_id: "bolum-XX" formatında (XX = 01'den başlayarak)
- title: Bölüm başlığı (20-80 karakter)
- type: "core" veya "appendix"

Ekler (appendix) için chapter_id: "ek-X" formatında (X = a, b, c, d)

Sadece aşağıdaki JSON formatında yanıt ver, başka metin ekleme:
```json
[
  {{"chapter_id": "bolum-01", "title": "...", "type": "core"}},
  ...
]
```"""

    try:
        result = client.generate_text(SYSTEM_AUTHOR, prompt, temperature=0.7, max_tokens=4096)
        # JSON çıkar
        import re as _re
        json_match = _re.search(r'\[.*\]', result, _re.DOTALL)
        if json_match:
            import json as _json
            chapters = _json.loads(json_match.group())
            if isinstance(chapters, list):
                return chapters
        return _generate_default_plan(chapter_count, appendix_count)
    except Exception:
        return _generate_default_plan(chapter_count, appendix_count)


def _generate_default_plan(chapter_count: int = 23,
                           appendix_count: int = 4) -> list[dict]:
    """LLM hatası durumunda varsayılan plan."""
    chapters = []
    for i in range(1, chapter_count + 1):
        chapters.append({
            "chapter_id": f"bolum-{i:02d}",
            "title": f"Bölüm {i}",
            "type": "core",
        })
    for i, letter in enumerate("abcd"):
        if i < appendix_count:
            chapters.append({
                "chapter_id": f"ek-{letter}",
                "title": f"Ek {letter.upper()}",
                "type": "appendix",
            })
    return chapters
