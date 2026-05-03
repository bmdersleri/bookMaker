
from bookmaker.core.ids import new_event_id
from bookmaker.core.time import now_iso
from bookmaker.models.versioning import EventType, VersionEvent
from bookmaker.storage.files import append_event, chapter_workspace, read_events
from bookmaker.storage.sqlite import ensure_schema, table_names

EXPECTED_TABLES = {
    "artifacts",
    "chapters",
    "issues",
    "projects",
    "quality_reports",
    "version_events",
}


def test_ensure_schema_creates_tables(tmp_path):
    db_path = tmp_path / "bookmaker.sqlite"
    ensure_schema(db_path)
    assert db_path.exists()
    tables = set(table_names(db_path))
    assert EXPECTED_TABLES == tables


def test_ensure_schema_idempotent(tmp_path):
    db_path = tmp_path / "bookmaker.sqlite"
    ensure_schema(db_path)
    ensure_schema(db_path)  # ikinci çalışma hata vermemeli
    assert set(table_names(db_path)) == EXPECTED_TABLES


def test_append_and_read_events(tmp_path):
    log = tmp_path / "version_log.jsonl"
    ev1 = VersionEvent(
        event_id=new_event_id(),
        created_at=now_iso(),
        chapter_id="chapter_03",
        event_type=EventType.draft_pasted,
        artifact_version="draft_v001",
    )
    ev2 = VersionEvent(
        event_id=new_event_id(),
        created_at=now_iso(),
        chapter_id="chapter_03",
        event_type=EventType.draft_evaluated,
        artifact_version="draft_v001",
        score=87,
    )
    append_event(log, ev1)
    append_event(log, ev2)

    events = read_events(log)
    assert len(events) == 2
    assert events[0].event_type == EventType.draft_pasted
    assert events[1].score == 87


def test_read_events_missing_file(tmp_path):
    log = tmp_path / "nonexistent.jsonl"
    assert read_events(log) == []


def test_chapter_workspace_path(tmp_path):
    ws = chapter_workspace(tmp_path, "chapter_03")
    assert ws == tmp_path / "chapters" / "chapter_03"
