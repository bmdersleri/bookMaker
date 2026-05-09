from bookmaker.core.ids import new_event_id
from bookmaker.core.time import now_iso
from bookmaker.models.exchange import RevisionIssue, RevisionPacket
from bookmaker.models.versioning import (
    ActiveVersion,
    ChapterStep,
    EventType,
    VersionEvent,
)


def make_event(chapter_id: str = "chapter_03") -> VersionEvent:
    return VersionEvent(
        event_id=new_event_id(),
        created_at=now_iso(),
        chapter_id=chapter_id,
        event_type=EventType.draft_pasted,
        artifact_type="draft",
        artifact_version="draft_v001",
        path="chapters/chapter_03/draft_versions/draft_v001.md",
    )


def test_version_event_jsonl_roundtrip():
    ev = make_event()
    line = ev.to_jsonl_line()
    assert isinstance(line, str)
    loaded = VersionEvent.from_jsonl_line(line)
    assert loaded.event_id == ev.event_id
    assert loaded.event_type == EventType.draft_pasted


def test_version_event_fields():
    ev = make_event()
    assert ev.chapter_id == "chapter_03"
    assert ev.user_action is True
    assert ev.score is None


def test_active_version_defaults():
    av = ActiveVersion(chapter_id="chapter_03")
    assert av.current_step == ChapterStep.planned
    assert av.seed is None
    assert av.approved_chapter is None


def test_active_version_yaml_roundtrip(tmp_path):
    av = ActiveVersion(
        chapter_id="chapter_03",
        current_step=ChapterStep.outline_approved,
        seed="seed_v002",
        outline="outline_v002",
    )
    path = tmp_path / "active_version.yaml"
    av.to_yaml(path)
    loaded = ActiveVersion.from_yaml(path)
    assert loaded.chapter_id == "chapter_03"
    assert loaded.current_step == ChapterStep.outline_approved
    assert loaded.seed == "seed_v002"


def test_revision_packet_to_prompt():
    packet = RevisionPacket(
        packet_id="rev_001",
        target_artifact="normalized_v001.md",
        artifact_version="draft_v001",
        chapter_id="chapter_03",
        objective="CODE_META eksiklerini gider",
        preserve=["Tum kod bloklari", "SECTION_META bloklari"],
        issues=[
            RevisionIssue(
                issue_id="iss_001",
                severity="error",
                location="satir 142",
                current="CODE_META yok",
                expected="Kod blogundan hemen once CODE_META olmali",
                instruction="Kod blogunun hemen oncesine CODE_META ekle",
                acceptance_criteria=["Validator hata vermemeli"],
            )
        ],
    )
    prompt = packet.to_prompt()
    assert "Revizyon Gorevi" in prompt
    assert "CODE_META eksiklerini gider" in prompt
    assert "Tum kod bloklari" in prompt
    assert "iss_001" in prompt
    assert "Tam bolumu yeniden yazma" in prompt


def test_revision_packet_default_constraints():
    packet = RevisionPacket(
        packet_id="rev_002",
        target_artifact="norm_v001.md",
        artifact_version="v001",
        chapter_id="ch01",
        objective="test",
    )
    assert len(packet.constraints) == 4
    assert any("yeniden yazma" in c for c in packet.constraints)
