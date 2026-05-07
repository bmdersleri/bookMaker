"""Observer/review service for Studio.

Gözlemci LLM ile bölüm taslağını manifest ve chapter manifest'e göre
değerlendirir, sonucu logs/reviews/ altına yazar.
"""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path

from bookmaker.llm.config import LLMConfig
from bookmaker.llm.openai import OpenAICompatibleClient
from bookmaker.studio.services import prompt_service

# ── Review prompt helpers (mevcut) ──

def get_review_prompt(project_root: str | Path) -> dict:
    """Return the default observer prompt."""
    return prompt_service.get_default_prompt(project_root, "review")


def save_review_prompt(project_root: str | Path, content: str) -> dict:
    """Save the default observer prompt."""
    return prompt_service.save_default_prompt(project_root, content, "review")


# ── Chapter content helpers ──

def _chapter_alias(chapter) -> str:
    return chapter.chapter_id or chapter.alias or ""


def _chapter_matches(chapter, chapter_id: str) -> bool:
    return chapter_id in {chapter.chapter_id, chapter.alias}


def _chapter_source(chapter) -> str:
    alias = _chapter_alias(chapter)
    return chapter.source or f"chapters/{alias}/content/final.md"


def _read_chapter(root: Path, chapter_id: str) -> tuple[str | None, str | None]:
    """Read chapter content (prefer draft, fallback final). Returns (content, source_path)."""
    from bookmaker.manifest.manager import ManifestManager
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    ch = next((c for c in manifest.chapters if _chapter_matches(c, chapter_id)), None)
    if not ch:
        return None, None

    alias = _chapter_alias(ch)
    candidates = [
        root / f"chapters/{alias}/content/draft.md",
        root / f"chapters/{alias}/content/final.md",
    ]
    for p in candidates:
        if p.exists():
            return p.read_text(encoding="utf-8"), str(p.relative_to(root))
    return None, None


# ── Review storage paths ──

def _review_dir(root: Path) -> Path:
    return root / "logs" / "reviews"


def _review_paths(root: Path, chapter_id: str) -> tuple[Path, Path]:
    """Return (markdown_path, json_path) for observer review output."""
    d = _review_dir(root) / "chapters"
    d.mkdir(parents=True, exist_ok=True)
    md = d / f"{chapter_id}_observer_review.md"
    js = d / f"{chapter_id}_observer_review.json"
    return md, js


# ── Observer review generation ──

def _build_review_prompt(
    review_prompt: str,
    chapter_content: str,
    book_manifest: dict,
    chapter_manifest: dict | None,
) -> str:
    """Build the user prompt for observer LLM combining all context."""
    parts = [review_prompt, "", "---", "", "## Kitap Manifest Özeti"]
    if book_manifest:
        bm = book_manifest
        book = bm.get("book", {})
        parts.append(f"- Profil: {book.get('profile', book.get('type', 'bilinmiyor'))}")
        parts.append(f"- Dil: {book.get('language', book.get('code_language', 'bilinmiyor'))}")
        parts.append(f"- Hedef kitle: {book.get('audience', 'belirtilmemis')}")
        style = bm.get("style", {})
        if style:
            parts.append(f"- Yazım stili: {style.get('tone', 'akademik-sade')}")
            parts.append(f"- Framework: {style.get('framework', style.get('code_language', ''))}")

    if chapter_manifest:
        cm = chapter_manifest
        parts.append("")
        parts.append("## Bölüm Manifest Özeti")
        scope = cm.get("scope", {})
        if scope:
            parts.append(f"- Hedefler: {scope.get('objectives', [])}")
            parts.append(f"- Konular: {scope.get('topics', [])}")
        parts.append(f"- Zorluk: {cm.get('difficulty', 'orta')}")
        parts.append(f"- Tahmini kelime: {cm.get('estimated_words', 'belirtilmemis')}")

    parts.append("")
    parts.append("## Değerlendirilecek Bölüm İçeriği")
    parts.append("")
    parts.append(chapter_content)

    return "\n".join(parts)


def generate_observer_review(
    project_root: str | Path,
    chapter_id: str,
    *,
    save_report: bool = True,
) -> dict:
    """Observer LLM ile bölüm taslağını değerlendir.

    Args:
        project_root: Kitap proje kök dizini
        chapter_id: Bölüm alias/id
        save_report: Sonucu logs/reviews/ altına yaz

    Returns:
        {
            "chapter_id": str,
            "review": str (markdown),
            "path": str (relative),
            "elapsed_s": float,
            "error": str (varsa)
        }
    """
    root = Path(project_root).resolve()

    # LLM yapılandırması
    cfg = LLMConfig(root)
    if not cfg.is_configured():
        return {"chapter_id": chapter_id, "error": "LLM yapilandirilmamis"}

    # Bölüm içeriği
    content, src_path = _read_chapter(root, chapter_id)
    if not content:
        return {"chapter_id": chapter_id,
                "error": f"Bölüm içeriği bulunamadi: {chapter_id}"}

    # Review prompt
    prompt_result = get_review_prompt(root)
    review_prompt = prompt_result.get("content", "")
    if not review_prompt.strip():
        return {"chapter_id": chapter_id,
                "error": "Review promptu bos veya bulunamadi"}

    # Manifest bilgileri
    from bookmaker.manifest.manager import ManifestManager
    mgr = ManifestManager(root)
    try:
        book_manifest = mgr.load_or_generate().model_dump() if hasattr(
            mgr.load_or_generate(), "model_dump") else {}
    except Exception:
        book_manifest = {}

    chapter_manifest = None
    chapter_manifest_path = root / "chapters" / chapter_id / "chapter_manifest.yaml"
    if chapter_manifest_path.exists():
        try:
            import yaml
            chapter_manifest = yaml.safe_load(chapter_manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Observer LLM çağrısı
    user_prompt = _build_review_prompt(review_prompt, content, book_manifest, chapter_manifest)
    client = OpenAICompatibleClient(
        api_key=cfg.api_key,
        model=cfg.model,
        base_url=cfg.base_url,
        timeout=300,
        max_retries=2,
        api_log_dir=str(root / "logs"),
    )

    started = time.time()
    try:
        review_text = client.generate_text(
            review_prompt, user_prompt, max_tokens=4096, temperature=0.3
        )
    except RuntimeError as exc:
        return {"chapter_id": chapter_id,
                "error": f"Observer LLM hatasi: {str(exc)[:300]}"}

    elapsed = round(time.time() - started, 1)
    result: dict = {
        "chapter_id": chapter_id,
        "review": review_text,
        "elapsed_s": elapsed,
        "source": src_path,
    }

    # Kaydet
    if save_report and review_text:
        md_path, json_path = _review_paths(root, chapter_id)
        timestamp = datetime.now(UTC).isoformat()

        md_content = (
            f"# Observer Review — {chapter_id}\n\n"
            f"- **Tarih**: {timestamp}\n"
            f"- **Kaynak**: {src_path}\n"
            f"- **Model**: {cfg.model}\n"
            f"- **Süre**: {elapsed}s\n\n"
            f"---\n\n"
            f"{review_text}\n"
        )
        md_path.write_text(md_content, encoding="utf-8")

        json_data = {
            "chapter_id": chapter_id,
            "timestamp": timestamp,
            "source": src_path,
            "model": cfg.model,
            "elapsed_s": elapsed,
            "review": review_text,
        }
        json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False),
                           encoding="utf-8")

        result["path"] = str(md_path.relative_to(root))
        result["json_path"] = str(json_path.relative_to(root))

    return result


# ── Review listing ──

def list_observer_reviews(
    project_root: str | Path,
    chapter_id: str | None = None,
) -> list[dict]:
    """Observer review kayıtlarını listele.

    Args:
        project_root: Kitap proje kök dizini
        chapter_id: Verilirse sadece o bölümün review'leri

    Returns:
        [{chapter_id, timestamp, path, json_path, exists}, ...]
    """
    root = Path(project_root).resolve()
    review_chapters_dir = _review_dir(root) / "chapters"

    if chapter_id:
        patterns = [f"{chapter_id}_observer_review.json"]
    else:
        patterns = None  # tümünü tara

    results = []
    if not review_chapters_dir.exists():
        return results

    for json_file in sorted(review_chapters_dir.glob("*_observer_review.json"),
                            reverse=True):
        if patterns and json_file.name not in patterns:
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            cid = data.get("chapter_id", json_file.stem.replace("_observer_review", ""))
            md_file = review_chapters_dir / f"{cid}_observer_review.md"
            results.append({
                "chapter_id": cid,
                "timestamp": data.get("timestamp", ""),
                "source": data.get("source", ""),
                "model": data.get("model", ""),
                "elapsed_s": data.get("elapsed_s", 0),
                "path": str(md_file.relative_to(root)) if md_file.exists() else None,
                "json_path": str(json_file.relative_to(root)),
                "exists": True,
                "review_preview": data.get("review", "")[:300],
            })
        except (json.JSONDecodeError, OSError):
            results.append({
                "chapter_id": json_file.stem.replace("_observer_review", ""),
                "error": "JSON okunamadi",
                "path": str(json_file.relative_to(root)),
            })
    return results


def get_observer_review(project_root: str | Path, chapter_id: str) -> dict:
    """En son observer review'i tam metin olarak döndür."""
    root = Path(project_root).resolve()
    _, json_path = _review_paths(root, chapter_id)
    if not json_path.exists():
        return {"chapter_id": chapter_id, "error": "Observer review bulunamadi"}

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        return {
            "chapter_id": chapter_id,
            "timestamp": data.get("timestamp", ""),
            "source": data.get("source", ""),
            "model": data.get("model", ""),
            "elapsed_s": data.get("elapsed_s", 0),
            "review": data.get("review", ""),
            "path": str(json_path.relative_to(root)),
        }
    except (json.JSONDecodeError, OSError) as exc:
        return {"chapter_id": chapter_id,
                "error": f"Review okunamadi: {str(exc)[:200]}"}


def compare_observer_vs_validator(project_root: str | Path,
                                  chapter_id: str) -> dict:
    """Observer review ile validator sonuçlarını karşılaştır.

    Validator yapısal/hızlı kontrol yapar, observer LLM ise derin içerik
    değerlendirmesi. Bu fonksiyon iki perspektifi birleştirir.
    """
    from bookmaker.studio.services import quality_service

    root = Path(project_root).resolve()

    # Validator sonucu
    val_result = quality_service.validate_chapter(root, chapter_id)

    # Observer sonucu
    obs_result = get_observer_review(root, chapter_id)

    return {
        "chapter_id": chapter_id,
        "validator": {
            "score": val_result.get("score", 0),
            "decision": val_result.get("decision", ""),
            "errors": val_result.get("errors", 0),
            "warnings": val_result.get("warnings", 0),
            "issues": val_result.get("issues", []),
        },
        "observer": {
            "available": "review" in obs_result,
            "timestamp": obs_result.get("timestamp", ""),
            "model": obs_result.get("model", ""),
            "elapsed_s": obs_result.get("elapsed_s", 0),
            "preview": obs_result.get("review", "")[:500] if "review" in obs_result else "",
        },
    }
