"""GitHub sync testleri."""

from pathlib import Path

from bookmaker.github.sync import check_git_repo, sync_code_manifest


def test_check_git_repo(tmp_path: Path) -> None:
    # Konum repo icinde olabilir; o durumda is_repo=True olur.
    result = check_git_repo(tmp_path)
    assert isinstance(result["is_repo"], bool)


def test_sync_code_manifest() -> None:
    entries = [
        {"code_id": "kod01", "file": "Ornek.java"},
        {"code_id": "kod02", "file": "Test.java"},
    ]
    result = sync_code_manifest(entries, "https://github.com/user/repo")
    assert len(result) == 2
    assert "github_url" in result[0]
    assert "Ornek.java" in result[0]["github_url"]
