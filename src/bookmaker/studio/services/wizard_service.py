"""Kitap oluşturma sihirbazı servisi."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from bookmaker.core.time import now_iso
from bookmaker.generation.prompts import SYSTEM_AUTHOR
from bookmaker.manifest.models import BookManifest, PipelineState

_yaml = YAML()
_yaml.default_flow_style = False

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

        workspace = _book_projects_workspace(root)
        book_dir = workspace / project_name
        if book_dir.exists():
            return {"error": f"Proje zaten var: {project_name}"}

        _create_directory_structure(book_dir, data)

        chapter_count = data.get("chapter_count", 23)
        appendix_count = data.get("appendix_count", 4)
        chapters = _normalize_chapters(
            data.get("chapters"),
            chapter_count,
            appendix_count,
        )

        _create_book_profile(book_dir, data, chapters)
        _create_book_manifest(book_dir, data, chapters)

        chapter_aliases = [chapter["alias"] for chapter in chapters]
        _create_pipeline_state(book_dir, chapter_aliases)
        _create_llm_config(book_dir, data)
        _create_chapter_workspaces(book_dir, chapters)

        return {"project_name": project_name,
                "path": str(book_dir.relative_to(workspace.parent)),
                "chapters": len(chapters),
                "title": data.get("title", "")}

    except Exception as e:
        return {"error": f"Kitap oluşturulamadı: {str(e)[:300]}"}


def _book_projects_workspace(root: Path) -> Path:
    """Yeni kitap projelerinin yazılacağı book_projects dizinini bulur."""
    if root.name == "book_projects":
        return root
    if (root / "book_projects").exists():
        return root / "book_projects"
    if (root / "book_manifest.yaml").exists() and root.parent.name == "book_projects":
        return root.parent
    return root / "book_projects"


def _create_directory_structure(book_dir: Path, data: dict) -> None:
    """Proje dizin yapısını oluşturur."""
    dirs = [
        book_dir,
        book_dir / "prompts",
        book_dir / "chapters",
        book_dir / "exports" / "docx",
        book_dir / "exports" / "pdf",
        book_dir / "exports" / "md",
        book_dir / "logs" / "production",
        book_dir / "logs" / "errors",
        book_dir / "logs" / "reviews",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def _create_book_profile(book_dir: Path, data: dict, chapters: list[dict[str, str]]) -> None:
    """book_profile.yaml oluşturur — ChapterGenerator ve legacy araçlar için gerekli.

    ChapterGenerator is_ready() kontrolünde book_profile.yaml arar.
    Wizard kitaplarında bu dosya yoksa pipeline işleri başarısız olur.
    """
    from datetime import datetime

    project_name = book_dir.name
    audience_map = {
        "universite_1": "Universite 1. sinif ogrencileri",
        "universite_2": "Universite 2. sinif ogrencileri",
        "lise": "Lise ogrencileri",
        "yeni_baslayan": "Programlamaya yeni baslayanlar",
        "profesyonel": "Profesyonel yazilimcilar",
    }
    audience_key = data.get("audience", "universite_1")
    audience_tr = audience_map.get(audience_key, audience_key)

    code_lang = data.get("code_language", "") or ""
    if not code_lang:
        name_lower = project_name.casefold()
        if "java" in name_lower:
            code_lang = "java"
        elif "flutter" in name_lower or "dart" in name_lower:
            code_lang = "dart"
        elif "python" in name_lower:
            code_lang = "python"
        else:
            code_lang = "java"

    profile: dict = {
        "book": {
            "book_id": project_name,
            "title": {"tr": data.get("title", project_name)},
            "author": data.get("author", ""),
            "primary_code_language": code_lang,
            "level": "beginner",
            "domain": "programming",
            "audience": {"tr": audience_tr},
            "edition": "1",
            "year": datetime.now().year,
        },
        "language": {
            "primary_language": data.get("language", "tr"),
        },
        "chapters": [
            {
                "chapter_id": ch["alias"],
                "title": ch["title"],
                "status": "planned",
                "order": i + 1,
            }
            for i, ch in enumerate(chapters)
        ],
    }

    profile_path = book_dir / "book_profile.yaml"
    with profile_path.open("w", encoding="utf-8") as handle:
        _yaml.dump(profile, handle)
    print(f"  [WIZARD] book_profile.yaml olusturuldu: {profile_path}")


def _normalize_chapters(
    chapters: Any,
    chapter_count: int,
    appendix_count: int,
) -> list[dict[str, str]]:
    """Normalize string/dict chapter plans to alias/title mappings."""
    chapter_count = int(chapter_count or 23)
    appendix_count = int(appendix_count or 0)
    raw_chapters = chapters or _DEFAULT_CHAPTERS[:chapter_count + appendix_count]
    normalized = []
    for item in raw_chapters:
        if isinstance(item, dict):
            alias = str(item.get("alias") or item.get("chapter_id") or "").strip()
            title = str(item.get("title") or alias).strip()
        else:
            alias = str(item).strip()
            title = alias
        if alias:
            normalized.append({"alias": alias, "title": title or alias})
    return normalized


def _create_book_manifest(book_dir: Path, data: dict, chapters: list[dict[str, str]]) -> None:
    """book_manifest.yaml oluşturur."""
    book_type = data.get("book_type", "ders_kitabi")
    manifest = {
        "book": {
            "title": data.get("title", ""),
            "subtitle": data.get("title_en", ""),
            "author": data.get("author", ""),
            "alias": book_dir.name,
            "language": data.get("language", "tr"),
            "version": "0.1.0",
            "edition": "1",
            "year": datetime.now().year,
            "type": book_type,
        },
        "production": {
            "producer_model": data.get("model", "deepseek-chat"),
            "observer_model": data.get("observer_model", data.get("model", "deepseek-chat")),
            "generation_mode": "chapter_based",
            "approval_required": True,
        },
        "style": {
            "target_audience": data.get("audience", "universite_1"),
            "tone": "akademik ama sade",
            "code_language": "java" if "java" in book_dir.name.casefold() else "",
            "framework": "flutter" if "flutter" in book_dir.name.casefold() else None,
        },
        "automation": {
            "code_meta_required": True,
            "screenshot_required": "flutter" in book_dir.name.casefold(),
            "minimum_screenshots_per_chapter": 1 if "flutter" in book_dir.name.casefold() else 0,
            "qr_policy": "dual",
            "github_code_export": True,
        },
        "chapters": [
            {
                "alias": chapter["alias"],
                "order": i + 1,
                "title": chapter["title"],
                "status": "planned",
            }
            for i, chapter in enumerate(chapters)
        ],
    }
    with (book_dir / "book_manifest.yaml").open("w", encoding="utf-8") as handle:
        _yaml.dump(manifest, handle)


def _create_pipeline_state(book_dir: Path, chapters: list[str]) -> None:
    """pipeline_state.yaml oluşturur."""
    from bookmaker.chapter.validation_modes import resolve_validation_profile_from_manifest

    manifest = BookManifest.load(book_dir / "book_manifest.yaml")
    state = PipelineState.init_from_book_manifest(manifest, created_at=now_iso())
    state.current_stage = "authoring"
    state.pipeline.global_state = "authoring"
    state.production_context.profile = resolve_validation_profile_from_manifest(manifest)
    state.save(book_dir / "pipeline_state.yaml")


def _create_llm_config(book_dir: Path, data: dict) -> None:
    """llm_config.json oluşturur."""
    cfg = [{
        "provider": data.get("provider", "deepseek"),
        "api_key": data.get("api_key", ""),
        "model": data.get("model", "deepseek-chat"),
    }]
    (book_dir / "llm_config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def _create_chapter_workspaces(book_dir: Path, chapters: list[dict[str, str]]) -> None:
    """Project-based bölüm workspace'lerini oluşturur."""
    _write_text(book_dir / "prompts" / "default_chapter.md", "# Varsayılan Bölüm Promptu\n\n")
    _write_text(book_dir / "prompts" / "default_review.md", "# Varsayılan Review Promptu\n\n")
    for order, chapter in enumerate(chapters, start=1):
        cid = chapter["alias"]
        title = chapter["title"]
        chapter_root = book_dir / "chapters" / cid
        content_dir = chapter_root / "content"
        (content_dir / "revisions").mkdir(parents=True, exist_ok=True)
        _write_text(chapter_root / "prompt.md", f"# {title}\n\n")
        _write_text(content_dir / "draft.md", f"# {title}\n\n> Taslak henüz üretilmedi.\n")
        _write_text(content_dir / "final.md", f"# {title}\n\n> Final henüz onaylanmadı.\n")
        chapter_manifest = {
            "chapter": {
                "title": title,
                "alias": cid,
                "order": order,
                "references": [],
            },
            "scope": {"topics": [cid], "objectives": [], "exclusions": []},
            "structure": {"sections": []},
            "automation": {"validation_modes": ["review_only"]},
        }
        with (chapter_root / "chapter_manifest.yaml").open("w", encoding="utf-8") as handle:
            _yaml.dump(chapter_manifest, handle)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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
