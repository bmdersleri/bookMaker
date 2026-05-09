-- bookmaker SQLite şeması v1

CREATE TABLE IF NOT EXISTS projects (
    id          TEXT PRIMARY KEY,
    root_path   TEXT NOT NULL,
    title       TEXT NOT NULL,
    book_id     TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chapters (
    id              TEXT PRIMARY KEY,
    project_id      TEXT NOT NULL REFERENCES projects(id),
    chapter_id      TEXT NOT NULL,
    title           TEXT NOT NULL,
    chapter_order   INTEGER NOT NULL,
    status          TEXT NOT NULL DEFAULT 'planned',
    current_step    TEXT NOT NULL DEFAULT 'planned',
    active_version  TEXT,
    last_score      INTEGER,
    updated_at      TEXT NOT NULL,
    UNIQUE (project_id, chapter_id)
);

CREATE TABLE IF NOT EXISTS artifacts (
    id               TEXT PRIMARY KEY,
    project_id       TEXT NOT NULL REFERENCES projects(id),
    chapter_id       TEXT,
    artifact_type    TEXT NOT NULL,
    artifact_version TEXT NOT NULL,
    path             TEXT NOT NULL,
    checksum         TEXT,
    created_at       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS version_events (
    id               TEXT PRIMARY KEY,
    project_id       TEXT NOT NULL REFERENCES projects(id),
    chapter_id       TEXT,
    event_type       TEXT NOT NULL,
    artifact_type    TEXT,
    artifact_version TEXT,
    path             TEXT,
    score            INTEGER,
    payload_json     TEXT,
    user_action      INTEGER NOT NULL DEFAULT 1,
    created_at       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_reports (
    id               TEXT PRIMARY KEY,
    project_id       TEXT NOT NULL REFERENCES projects(id),
    chapter_id       TEXT,
    artifact_type    TEXT NOT NULL,
    artifact_version TEXT NOT NULL,
    score            INTEGER NOT NULL,
    decision         TEXT NOT NULL,
    error_count      INTEGER NOT NULL DEFAULT 0,
    warning_count    INTEGER NOT NULL DEFAULT 0,
    report_path      TEXT NOT NULL,
    created_at       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS issues (
    id               TEXT PRIMARY KEY,
    report_id        TEXT NOT NULL REFERENCES quality_reports(id),
    severity         TEXT NOT NULL,
    category         TEXT NOT NULL,
    file_path        TEXT,
    line             INTEGER,
    message          TEXT NOT NULL,
    expected         TEXT,
    current_value    TEXT,
    instruction      TEXT,
    status           TEXT NOT NULL DEFAULT 'open'
);
