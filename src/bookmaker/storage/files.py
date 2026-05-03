from __future__ import annotations

from pathlib import Path

from bookmaker.models.versioning import VersionEvent


def append_event(log_path: Path, event: VersionEvent) -> None:
    """version_log.jsonl dosyasına event ekler."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(event.to_jsonl_line() + "\n")


def read_events(log_path: Path) -> list[VersionEvent]:
    """version_log.jsonl dosyasındaki tüm eventleri okur."""
    if not log_path.exists():
        return []
    events = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(VersionEvent.from_jsonl_line(line))
    return events


def chapter_workspace(project_root: Path, chapter_id: str) -> Path:
    return project_root / "chapters" / chapter_id


def seed_path(project_root: Path, chapter_id: str, version: str = "seed_v001") -> Path:
    return chapter_workspace(project_root, chapter_id) / "seed" / f"{version}.yaml"


def outline_path(project_root: Path, chapter_id: str, version: str) -> Path:
    return chapter_workspace(project_root, chapter_id) / "outline_versions" / f"{version}.md"


def draft_path(project_root: Path, chapter_id: str, version: str) -> Path:
    return chapter_workspace(project_root, chapter_id) / "draft_versions" / f"{version}.md"


def approved_path(project_root: Path, chapter_id: str, version: str = "v001") -> Path:
    return chapter_workspace(project_root, chapter_id) / "approved" / f"{chapter_id}_{version}.md"


def version_log_path(project_root: Path, chapter_id: str) -> Path:
    return chapter_workspace(project_root, chapter_id) / "version_log.jsonl"


def active_version_path(project_root: Path, chapter_id: str) -> Path:
    return chapter_workspace(project_root, chapter_id) / "active_version.yaml"
