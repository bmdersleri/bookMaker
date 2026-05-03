"""Production mermaid testleri."""

from pathlib import Path

from bookmaker.production.mermaid import extract_mermaid_blocks


def test_extract_no_mermaid(tmp_path: Path) -> None:
    text = "# Baslik\nNormal icerik.\n"
    blocks = extract_mermaid_blocks(text)
    assert blocks == []


def test_extract_single_mermaid(tmp_path: Path) -> None:
    text = "```mermaid\nflowchart TD\nA-->B\n```\n"
    blocks = extract_mermaid_blocks(text)
    assert len(blocks) == 1
    assert "flowchart" in blocks[0]["code"]


def test_extract_multiple_mermaid(tmp_path: Path) -> None:
    text = (
        "1:\n```mermaid\ngraph LR\nA-->B\n```\n"
        "2:\n```mermaid\ngraph RL\nB-->A\n```\n"
    )
    blocks = extract_mermaid_blocks(text)
    assert len(blocks) == 2


def test_render_mermaid_timeout_returns_error(tmp_path: Path) -> None:
    from bookmaker.production.mermaid import render_mermaid

    # mmdc yoksa error döner
    result = render_mermaid("flowchart TD\nA", tmp_path / "none" / "test.png")
    assert result["status"] in ("error", "timeout", "failed")
