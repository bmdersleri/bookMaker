"""GitHub kod senkronizasyonu."""

from __future__ import annotations

import subprocess
from pathlib import Path


def check_git_repo(project_root: Path) -> dict:
    """Git repo durumunu kontrol eder."""
    result: dict = {"is_repo": False, "branch": "", "remote": "", "has_changes": False}
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, timeout=5, cwd=str(project_root),
        )
        if proc.returncode != 0 or proc.stdout.strip() != "true":
            return result
        result["is_repo"] = True
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5, cwd=str(project_root),
        )
        result["branch"] = branch.stdout.strip()
        remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5, cwd=str(project_root),
        )
        result["remote"] = remote.stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=5, cwd=str(project_root),
        )
        result["has_changes"] = bool(status.stdout.strip())
    except Exception as e:
        result["error"] = str(e)
    return result


def push_code_files(code_dir: Path, repo_root: Path, commit_msg: str = "auto: code sync") -> dict:
    """Kod dosyalarını repo'ya ekler ve push eder."""
    result: dict = {"files_added": 0, "committed": False, "pushed": False}
    try:
        subprocess.run(
            ["git", "add", "-A", str(code_dir)],
            capture_output=True, text=True, timeout=15, cwd=str(repo_root),
        )
        changed = subprocess.run(
            ["git", "status", "--porcelain", str(code_dir)],
            capture_output=True, text=True, timeout=5, cwd=str(repo_root),
        )
        st = changed.stdout.strip()
        result["files_added"] = len(st.splitlines()) if st else 0
        if result["files_added"] == 0:
            return result

        commit = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True, text=True, timeout=15, cwd=str(repo_root),
        )
        result["committed"] = commit.returncode == 0
        result["commit_output"] = commit.stdout

        push = subprocess.run(
            ["git", "push"],
            capture_output=True, text=True, timeout=30, cwd=str(repo_root),
        )
        result["pushed"] = push.returncode == 0
        result["push_output"] = push.stdout
        if push.stderr:
            result["push_error"] = push.stderr
    except subprocess.TimeoutExpired:
        result["error"] = "Operation timed out"
    except FileNotFoundError:
        result["error"] = "git not found in PATH"
    except Exception as e:
        result["error"] = str(e)
    return result


def sync_code_manifest(
    code_entries: list[dict],
    repo_url: str,
    branch: str = "main",
    code_root: str = "build/code",
) -> list[dict]:
    """Kod manifestine GitHub URL'leri ekler."""
    for entry in code_entries:
        code_id = entry.get("code_id", "")
        file_name = entry.get("file", "")
        if code_id and file_name:
            entry["github_url"] = (
                f"{repo_url}/blob/{branch}/{code_root}/{code_id}/{file_name}"
            )
    return code_entries
