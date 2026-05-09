"""Authoring pipeline testleri."""

from pathlib import Path

from bookmaker.authoring.pipeline import AuthoringPipeline


def _ensure_workspace(root: Path, chapter_id: str) -> None:
    for sub in ["seed", "outline_versions", "draft_versions", "approved"]:
        (root / "chapters" / chapter_id / sub).mkdir(parents=True, exist_ok=True)


def test_seed_creates_yaml(tmp_path: Path) -> None:
    pipe = AuthoringPipeline(tmp_path)
    seed = pipe.seed("bolum-1", purpose="Test")
    assert seed.chapter_id == "bolum-1"
    state = pipe.get_state("bolum-1")
    assert state.current_step == "seeded"


def test_outline_prompt_generated(tmp_path: Path) -> None:
    pipe = AuthoringPipeline(tmp_path)
    pipe.seed("bolum-1", purpose="Test", learning_outcomes=["O1"],
              mandatory_concepts=["K1"], out_of_scope=["D1"])
    prompt = pipe.make_outline_prompt("bolum-1")
    assert "bolum-1" in prompt
    assert "O1" in prompt
    state = pipe.get_state("bolum-1")
    assert state.current_step == "outline_prompt_ready"


def test_outline_paste_and_review(tmp_path: Path) -> None:
    pipe = AuthoringPipeline(tmp_path)
    pipe.seed("bolum-1", purpose="T", mandatory_concepts=["Kavram1"])

    p = pipe.paste_outline("bolum-1", "# Outline\n## G\n## G2\n## G3\n")
    assert p.exists()
    assert pipe.get_state("bolum-1").current_step == "outline_pasted"

    result = pipe.review_outline("bolum-1")
    assert "decision" in result


def test_draft_flow(tmp_path: Path) -> None:
    pipe = AuthoringPipeline(tmp_path)
    pipe.seed("bolum-1", purpose="Draft test", mandatory_concepts=["K1"])
    pipe.paste_outline("bolum-1", "# Outline\n## G\n## G2\n## G3\n")

    prompt = pipe.make_draft_prompt("bolum-1")
    assert prompt and "bolum-1" in prompt
    assert pipe.get_state("bolum-1").current_step == "full_text_prompt_ready"

    draft = (
        "---\ntitle: T\nsubtitle: K\nauthor: T\ndate: '2026'\n"
        "lang: tr-TR\ndocumentclass: report\ntoc: true\ntoc-depth: 3\n"
        "numbersections: true\nrepo: t\nproject-alias: t\n"
        "chapter-alias: bolum-1\nchapter_id: bolum-1\n---\n"
        "# Test\n## Giris\n\nIcerik.\n"
    )
    p = pipe.paste_draft("bolum-1", draft)
    assert p.exists()
    assert pipe.get_state("bolum-1").current_step == "full_text_pasted"

    result = pipe.review_draft("bolum-1")
    assert "score" in result
    assert "decision" in result


def test_approve_flow(tmp_path: Path) -> None:
    pipe = AuthoringPipeline(tmp_path)
    pipe.seed("bolum-1")
    pipe.paste_draft("bolum-1", "# Approved\nOK.\n")
    ap = pipe.approve("bolum-1")
    assert ap.exists()
    assert pipe.get_state("bolum-1").current_step == "approved"


def test_no_seed_returns_none(tmp_path: Path) -> None:
    pipe = AuthoringPipeline(tmp_path)
    assert pipe.load_seed("yok") is None
