from pathlib import Path

from bookmaker import __version__
from bookmaker.core.encoding import read_text, write_text
from bookmaker.core.ids import new_event_id, new_issue_id, slugify
from bookmaker.core.time import now_date, now_iso


def test_version():
    assert __version__ == "0.2.0"


def test_slugify():
    assert slugify("Java Temelleri") == "java_temelleri"
    assert slugify("hello world") == "hello_world"
    assert slugify("  spaces  ") == "spaces"
    assert slugify("a--b__c") == "a_b_c"


def test_new_event_id():
    eid = new_event_id()
    assert eid.startswith("evt_")
    assert len(eid) == 16


def test_new_issue_id():
    iid = new_issue_id()
    assert iid.startswith("iss_")
    assert len(iid) == 12


def test_now_iso():
    ts = now_iso()
    assert "T" in ts
    assert "+03:00" in ts


def test_now_date():
    d = now_date()
    assert len(d) == 10
    assert d[4] == "-"


def test_read_write_text(tmp_path: Path):
    p = tmp_path / "test.md"
    write_text(p, "merhaba dünya")
    assert read_text(p) == "merhaba dünya"


def test_write_creates_parents(tmp_path: Path):
    p = tmp_path / "a" / "b" / "c.txt"
    write_text(p, "ok")
    assert p.exists()
