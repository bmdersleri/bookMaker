from pathlib import Path


def find_project_root(start: Path | None = None) -> Path | None:
    """book_profile.yaml dosyasını yukarı doğru arayarak proje kökünü bulur."""
    current = (start or Path.cwd()).resolve()
    for parent in [current, *current.parents]:
        if (parent / "book_profile.yaml").exists():
            return parent
    return None


def chapter_dir(project_root: Path, chapter_id: str) -> Path:
    return project_root / "chapters" / chapter_id


def approved_path(project_root: Path, chapter_id: str) -> Path:
    return chapter_dir(project_root, chapter_id) / "approved" / f"{chapter_id}.md"


def version_log_path(project_root: Path, chapter_id: str) -> Path:
    return chapter_dir(project_root, chapter_id) / "version_log.jsonl"


def active_version_path(project_root: Path, chapter_id: str) -> Path:
    return chapter_dir(project_root, chapter_id) / "active_version.yaml"
