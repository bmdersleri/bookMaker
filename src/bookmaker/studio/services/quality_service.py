"""Kalite servisi — validasyon, raporlama, istatistik, arama, kod derleme."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from bookmaker.chapter.parser import parse
from bookmaker.chapter.scoring import make_report
from bookmaker.chapter.validator import validate


def _chapter_alias(chapter) -> str:
    return chapter.chapter_id or chapter.alias or ""


def _chapter_matches(chapter, chapter_id: str) -> bool:
    return chapter_id in {chapter.chapter_id, chapter.alias}


def _chapter_source(chapter) -> str:
    alias = _chapter_alias(chapter)
    return chapter.source or f"chapters/{alias}/content/final.md"


def validate_chapter(project_root: str | Path, chapter_id: str) -> dict:
    """Bölümü valide eder."""
    root = Path(project_root).resolve()
    from bookmaker.manifest.manager import ManifestManager
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    src = next((_chapter_source(ch) for ch in manifest.chapters
                if _chapter_matches(ch, chapter_id)), None)
    if not src:
        return {"error": f"Bölüm bulunamadi: {chapter_id}"}
    p = root / src
    if not p.exists():
        return {"error": f"Dosya bulunamadi: {p}"}
    try:
        parsed = parse(p)
        issues = validate(parsed)
        report = make_report(chapter_id, issues)
        return {"chapter_id": chapter_id, "score": report.score,
                "decision": report.decision.value,
                "errors": report.error_count,
                "warnings": report.warning_count,
                "info_count": report.info_count,
                "total_issues": report.error_count + report.warning_count}
    except Exception as e:
        return {"error": f"Validasyon hatasi: {str(e)[:200]}"}


def get_chapter_content(project_root: str | Path, chapter_id: str) -> dict:
    """Bölüm içeriğini döndürür."""
    root = Path(project_root).resolve()
    from bookmaker.manifest.manager import ManifestManager
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    src = next((_chapter_source(ch) for ch in manifest.chapters
                if _chapter_matches(ch, chapter_id)), None)
    if not src:
        return {"error": f"Bölüm bulunamadi: {chapter_id}"}
    base = root / "chapters" / chapter_id / "approved"
    candidates = [root / src, base / f"{chapter_id}_v001.md",
                  base / f"{chapter_id}_v002.md", base / "v001.md"]
    for p in candidates:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            return {"chapter_id": chapter_id,
                    "path": str(p.relative_to(root)),
                    "words": len(text.split()),
                    "chars": len(text),
                    "preview": text[:500], "full": text}
    return {"error": f"İçerik bulunamadi: {chapter_id}"}


def get_quality_report(project_root: str | Path,
                       chapter_id: str | None = None) -> list[dict] | dict:
    """Tüm bölümlerin veya tek bölümün kalite raporunu döndürür."""
    from bookmaker.manifest.manager import ManifestManager
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    chapters_to_check = []
    if chapter_id:
        chapters_to_check = [chapter_id]
    else:
        chapters_to_check = [_chapter_alias(ch) for ch in manifest.chapters]

    results = []
    for cid in chapters_to_check:
        src = next((_chapter_source(ch) for ch in manifest.chapters
                    if _chapter_matches(ch, cid)), None)
        if not src:
            results.append({chapter_id: cid, "error": "Bulunamadi"})
            continue
        p = root / src
        if not p.exists():
            results.append({"chapter_id": cid, "error": "Dosya yok",
                            "score": 0, "errors": 0, "warnings": 0})
            continue
        try:
            parsed = parse(p)
            issues = validate(parsed)
            report = make_report(cid, issues)
            results.append({"chapter_id": cid, "score": report.score,
                            "decision": report.decision.value,
                            "errors": report.error_count,
                            "warnings": report.warning_count,
                            "info_count": report.info_count,
                            "total_issues": report.error_count + report.warning_count})
        except Exception as e:
            results.append({"chapter_id": cid, "error": str(e)[:100],
                            "score": 0})
    if chapter_id and results:
        return results[0]
    return results


def get_book_stats(project_root: str | Path) -> dict:
    """Kitap geneli istatistikleri döndürür."""
    from bookmaker.manifest.manager import ManifestManager
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    total_words = 0
    total_chars = 0
    total_code = 0
    total_mermaid = 0
    total_tables = 0
    word_counts = []

    for ch in manifest.chapters:
        src = _chapter_source(ch)
        p = root / src if src else None
        if p and p.exists():
            text = p.read_text(encoding="utf-8")
            wc = len(text.split())
            total_words += wc
            total_chars += len(text)
            total_code += len(re.findall(r'```', text)) // 2
            total_mermaid += len(re.findall(r'```mermaid', text))
            total_tables += len(re.findall(r'^\|.*\|$', text, re.MULTILINE))
            alias = _chapter_alias(ch)
            word_counts.append({"chapter_id": alias,
                                "words": wc, "title": ch.title or alias})
        else:
            alias = _chapter_alias(ch)
            word_counts.append({"chapter_id": alias,
                                "words": 0, "title": ch.title or alias})

    reading_minutes = round(total_words / 200)
    chapter_count = len(manifest.chapters)

    # En uzun/kısa bölüm
    if word_counts:
        longest = max(word_counts, key=lambda x: x["words"])
        shortest = min(word_counts, key=lambda x: x["words"])
    else:
        longest = {"chapter_id": "-", "words": 0}
        shortest = {"chapter_id": "-", "words": 0}

    return {"total_words": total_words, "total_chars": total_chars,
            "total_code_blocks": total_code, "total_mermaid": total_mermaid,
            "total_tables": total_tables,
            "reading_minutes": reading_minutes,
            "estimated_hours": round(reading_minutes / 60, 1),
            "chapter_count": chapter_count,
            "average_words": round(total_words / chapter_count) if chapter_count else 0,
            "longest_chapter": longest,
            "shortest_chapter": shortest,
            "word_distribution": word_counts}


def search_content(project_root: str | Path, query: str,
                   chapter_id: str | None = None,
                   use_regex: bool = False) -> list[dict]:
    """Tam metin arama — tüm bölümlerde veya tek bölümde."""
    from bookmaker.manifest.manager import ManifestManager
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    results = []
    for ch in manifest.chapters:
        if chapter_id and not _chapter_matches(ch, chapter_id):
            continue
        src = _chapter_source(ch)
        p = root / src if src else None
        if not p or not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        for i, line in enumerate(lines):
            try:
                if use_regex:
                    match = re.search(query, line)
                else:
                    match = query.lower() in line.lower()
            except re.error:
                continue
            if match:
                # Bağlam (context): eşleşen satır + 1 önce + 1 sonra
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                context = "\n".join(lines[start:end])
                results.append({
                    "chapter_id": _chapter_alias(ch),
                    "line": i + 1,
                    "context": context[:500],
                    "text": line[:200],
                })
    return results


def compile_code(project_root: str | Path, chapter_id: str) -> dict:
    """Kod bloklarını javac ile derler."""
    from bookmaker.manifest.manager import ManifestManager
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    src = next((_chapter_source(ch) for ch in manifest.chapters
                if _chapter_matches(ch, chapter_id)), None)
    if not src:
        return {"error": f"Bölüm bulunamadi: {chapter_id}"}
    p = root / src
    if not p.exists():
        return {"error": f"Dosya bulunamadi: {p}"}

    text = p.read_text(encoding="utf-8")
    java_blocks = re.findall(r'```java\n(.*?)```', text, re.DOTALL)
    if not java_blocks:
        return {"chapter_id": chapter_id, "blocks": 0,
                "compiled": 0, "errors": []}

    # Geçici dizine yaz
    tmp_dir = root / "build" / "code_check" / chapter_id
    tmp_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, block in enumerate(java_blocks):
        # Sınıf adını bul
        class_match = re.search(r'public\s+class\s+(\w+)', block)
        if not class_match:
            results.append({"block": i + 1, "status": "skipped",
                            "reason": "Sınıf adı bulunamadi",
                            "class_name": "unknown"})
            continue
        class_name = class_match.group(1)
        fname = f"{class_name}.java"
        fpath = tmp_dir / fname
        fpath.write_text(block, encoding="utf-8")

        # Javac ile derle
        try:
            proc = subprocess.run(
                ["javac", str(fpath)],
                capture_output=True, text=True,
                timeout=30, cwd=str(tmp_dir))
            if proc.returncode == 0:
                results.append({"block": i + 1, "status": "ok",
                                "class_name": class_name})
            else:
                # Hata satırlarını parse et
                error_lines = [
                    line.strip() for line in proc.stderr.splitlines() if line.strip()
                ][:5]
                results.append({"block": i + 1, "status": "error",
                                "class_name": class_name,
                                "errors": error_lines})
        except FileNotFoundError:
            results.append({"block": i + 1, "status": "skipped",
                            "reason": "javac bulunamadi",
                            "class_name": class_name})
        except subprocess.TimeoutExpired:
            results.append({"block": i + 1, "status": "error",
                            "class_name": class_name,
                            "errors": ["Derleme zamani asimi (30s)"]})

    compiled = sum(1 for r in results if r["status"] == "ok")
    errors = [r for r in results if r["status"] == "error"]

    return {"chapter_id": chapter_id, "blocks": len(java_blocks),
            "compiled": compiled, "failed": len(errors),
            "results": results}


def extract_code_blocks(project_root: str | Path, chapter_id: str,
                        language: str = "java") -> dict:
    """Kod bloklarını ayıklayıp build/code/ altına .java dosyası olarak kaydeder."""
    root = Path(project_root).resolve()
    text_data = get_chapter_content(root, chapter_id)
    if "error" in text_data:
        return text_data

    text = text_data.get("full", "")
    blocks = re.findall(rf'```{language}\n(.*?)```', text, re.DOTALL)

    lang_ext = {"java": ".java", "python": ".py", "javascript": ".js",
                "html": ".html", "css": ".css", "xml": ".xml"}
    ext = lang_ext.get(language, ".txt")

    out_dir = root / "build" / "code" / chapter_id
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = 0
    files = []
    for i, block in enumerate(blocks):
        # İlk satırdan sınıf adını bul, yoksa generik
        first_line = block.strip().splitlines()[0] if block.strip() else ""
        class_match = re.search(r'(?:public\s+)?(?:class|func|def|function)\s+(\w+)',
                                first_line)
        base_name = class_match.group(1) if class_match else f"block_{i+1:03d}"
        fname = f"{base_name}{ext}"

        # Aynı dosya varsa index ekle
        idx = 1
        while (out_dir / fname).exists():
            fname = f"{base_name}_{idx:03d}{ext}"
            idx += 1

        (out_dir / fname).write_text(block, encoding="utf-8")
        saved += 1
        files.append(fname)

    return {"chapter_id": chapter_id, "language": language,
            "extracted": saved, "output_dir": str(out_dir.relative_to(root)),
            "files": files}
