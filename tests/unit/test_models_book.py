import pytest
from pydantic import ValidationError

from bookmaker.models.book import (
    BookArchitecture,
    BookProfile,
    ChapterArchEntry,
    ChapterSeed,
    ChapterStatus,
    ChapterType,
    ExportTarget,
)

# ── BookProfile ──────────────────────────────────────────────────────────────

def test_book_profile_defaults():
    p = BookProfile(book_id="java_temelleri", title="Java Temelleri")
    assert p.language == "tr-TR"
    assert p.export_targets == [ExportTarget.docx]
    assert p.level == "beginner"


def test_book_profile_invalid_id():
    with pytest.raises(ValidationError):
        BookProfile(book_id="Java Temelleri!", title="Test")


def test_book_profile_yaml_roundtrip(tmp_path):
    p = BookProfile(
        book_id="java_temelleri",
        title="Java Temelleri",
        author="Test Yazar",
        export_targets=[ExportTarget.docx, ExportTarget.mkdocs],
    )
    path = tmp_path / "book_profile.yaml"
    p.to_yaml(path)
    loaded = BookProfile.from_yaml(path)
    assert loaded.book_id == p.book_id
    assert loaded.title == p.title
    assert loaded.export_targets == p.export_targets


# ── BookArchitecture ─────────────────────────────────────────────────────────

def test_book_architecture_sorted_by_order():
    arch = BookArchitecture(
        book_id="java_temelleri",
        chapters=[
            ChapterArchEntry(chapter_id="ch03", order=3, title="Bölüm 3"),
            ChapterArchEntry(chapter_id="ch01", order=1, title="Bölüm 1"),
            ChapterArchEntry(chapter_id="ch02", order=2, title="Bölüm 2"),
        ],
    )
    assert [c.order for c in arch.chapters] == [1, 2, 3]


def test_book_architecture_duplicate_order_raises():
    with pytest.raises(ValidationError):
        BookArchitecture(
            book_id="test",
            chapters=[
                ChapterArchEntry(chapter_id="ch01", order=1, title="A"),
                ChapterArchEntry(chapter_id="ch02", order=1, title="B"),
            ],
        )


def test_book_architecture_duplicate_id_raises():
    with pytest.raises(ValidationError):
        BookArchitecture(
            book_id="test",
            chapters=[
                ChapterArchEntry(chapter_id="ch01", order=1, title="A"),
                ChapterArchEntry(chapter_id="ch01", order=2, title="B"),
            ],
        )


def test_book_architecture_yaml_roundtrip(tmp_path):
    arch = BookArchitecture(
        book_id="java_temelleri",
        chapters=[
            ChapterArchEntry(
                chapter_id="chapter_01",
                order=1,
                title="Java'ya Giris",
                chapter_type=ChapterType.core,
                status=ChapterStatus.planned,
            )
        ],
    )
    path = tmp_path / "book_architecture.yaml"
    arch.to_yaml(path)
    loaded = BookArchitecture.from_yaml(path)
    assert len(loaded.chapters) == 1
    assert loaded.chapters[0].chapter_id == "chapter_01"


# ── ChapterSeed ───────────────────────────────────────────────────────────────

def test_chapter_seed_not_ready_when_empty():
    seed = ChapterSeed(chapter_id="chapter_01")
    assert not seed.is_ready()


def test_chapter_seed_ready():
    seed = ChapterSeed(
        chapter_id="chapter_01",
        purpose="Java temellerini ogret",
        learning_outcomes=["degiskenleri tanimlamak"],
        mandatory_concepts=["int", "String"],
        out_of_scope=["OOP"],
    )
    assert seed.is_ready()


def test_chapter_seed_yaml_roundtrip(tmp_path):
    seed = ChapterSeed(
        chapter_id="chapter_03",
        purpose="Dosya islemlerini ogret",
        learning_outcomes=["dosya okuma", "dosya yazma"],
        mandatory_concepts=["FileWriter", "BufferedReader"],
        out_of_scope=["NIO2"],
    )
    path = tmp_path / "seed.yaml"
    seed.to_yaml(path)
    loaded = ChapterSeed.from_yaml(path)
    assert loaded.chapter_id == "chapter_03"
    assert loaded.mandatory_concepts == ["FileWriter", "BufferedReader"]
    assert loaded.is_ready()
