"""Toolchain readiness check tests — monkeypatched, no real tool deps."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import MagicMock

from bookmaker.core.toolchain import _check_tool, check_toolchain

# ---------------------------------------------------------------------------
# _check_tool unit tests
# ---------------------------------------------------------------------------


def test_check_tool_found_with_version(monkeypatch) -> None:
    monkeypatch.setattr(
        "bookmaker.core.toolchain.shutil.which",
        lambda name: f"/usr/bin/{name}",
    )
    monkeypatch.setattr(
        "bookmaker.core.toolchain.subprocess.run",
        lambda cmd, **kwargs: MagicMock(
            returncode=0, stdout="Python 3.12.0", stderr="",
        ),
    )
    result = _check_tool("python", ["--version"])
    assert result.available is True
    assert result.version == "Python 3.12.0"
    assert result.path == "/usr/bin/python"


def test_check_tool_not_found(monkeypatch) -> None:
    monkeypatch.setattr(
        "bookmaker.core.toolchain.shutil.which",
        lambda name: None,
    )
    result = _check_tool("nonexistent")
    assert result.available is False
    assert result.version is None
    assert result.path is None


def test_check_tool_found_no_version_args(monkeypatch) -> None:
    monkeypatch.setattr(
        "bookmaker.core.toolchain.shutil.which",
        lambda name: f"/usr/bin/{name}",
    )
    result = _check_tool("some-tool")
    assert result.available is True
    assert result.version is None
    assert result.path == "/usr/bin/some-tool"


def test_check_tool_version_timeout(monkeypatch) -> None:
    monkeypatch.setattr(
        "bookmaker.core.toolchain.shutil.which",
        lambda name: f"/usr/bin/{name}",
    )
    monkeypatch.setattr(
        "bookmaker.core.toolchain.subprocess.run",
        lambda cmd, **kwargs: (_ for _ in ()).throw(
            subprocess.TimeoutExpired(cmd, 10)),
    )
    result = _check_tool("slow-tool", ["--version"])
    assert result.available is True
    assert result.version is None


def test_check_tool_version_error(monkeypatch) -> None:
    monkeypatch.setattr(
        "bookmaker.core.toolchain.shutil.which",
        lambda name: f"/usr/bin/{name}",
    )
    monkeypatch.setattr(
        "bookmaker.core.toolchain.subprocess.run",
        lambda cmd, **kwargs: (_ for _ in ()).throw(
            OSError("broken binary")),
    )
    result = _check_tool("broken-tool", ["--version"])
    assert result.available is True
    assert result.version is None


# ---------------------------------------------------------------------------
# check_toolchain integration tests
# ---------------------------------------------------------------------------


def test_check_toolchain_all_available(monkeypatch) -> None:
    def fake_which(name):
        return f"/usr/bin/{name}"

    def fake_run(cmd, **kwargs):
        return MagicMock(
            returncode=0, stdout=f"{cmd[0].split('/')[-1]} x.y.z", stderr="",
        )

    monkeypatch.setattr("bookmaker.core.toolchain.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.core.toolchain.subprocess.run", fake_run)

    result = check_toolchain()
    assert result["status"] == "ok"
    assert result["errors"] == []
    assert result["warnings"] == []
    for key in ("python", "uv", "pandoc", "node"):
        assert result["tools"][key]["available"] is True
        assert result["tools"][key]["version"] is not None


def test_check_toolchain_optional_missing_warns(monkeypatch) -> None:
    def fake_which(name):
        if name in ("python", "uv"):
            return f"/usr/bin/{name}"
        return None

    def fake_run(cmd, **kwargs):
        return MagicMock(
            returncode=0, stdout=f"{cmd[0].split('/')[-1]} x.y.z", stderr="",
        )

    monkeypatch.setattr("bookmaker.core.toolchain.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.core.toolchain.subprocess.run", fake_run)

    result = check_toolchain()
    assert result["status"] == "warning"
    assert result["errors"] == []
    assert len(result["warnings"]) > 0
    assert result["tools"]["python"]["available"] is True
    assert result["tools"]["dart"]["available"] is False


def test_check_toolchain_critical_missing_errors(monkeypatch) -> None:
    def fake_which(name):
        if name == "python":
            return None  # critical
        if name == "uv":
            return None  # critical
        return f"/usr/bin/{name}"

    def fake_run(cmd, **kwargs):
        return MagicMock(
            returncode=0, stdout=f"{cmd[0].split('/')[-1]} x.y.z", stderr="",
        )

    monkeypatch.setattr("bookmaker.core.toolchain.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.core.toolchain.subprocess.run", fake_run)

    result = check_toolchain()
    assert result["status"] == "error"
    assert len(result["errors"]) >= 2
    assert result["tools"]["python"]["available"] is False
    assert result["tools"]["uv"]["available"] is False


def test_check_toolchain_json_serializable(monkeypatch) -> None:
    def fake_which(name):
        return f"/usr/bin/{name}"

    def fake_run(cmd, **kwargs):
        return MagicMock(
            returncode=0, stdout=f"{cmd[0].split('/')[-1]} 1.0", stderr="",
        )

    monkeypatch.setattr("bookmaker.core.toolchain.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.core.toolchain.subprocess.run", fake_run)

    result = check_toolchain()
    serialized = json.dumps(result, ensure_ascii=False)
    assert isinstance(serialized, str)
    roundtrip = json.loads(serialized)
    assert roundtrip["status"] == "ok"


def test_check_toolchain_fields(monkeypatch) -> None:
    def fake_which(name):
        return f"/usr/bin/{name}"

    def fake_run(cmd, **kwargs):
        return MagicMock(
            returncode=0, stdout=f"{cmd[0].split('/')[-1]} 1.0", stderr="",
        )

    monkeypatch.setattr("bookmaker.core.toolchain.shutil.which", fake_which)
    monkeypatch.setattr("bookmaker.core.toolchain.subprocess.run", fake_run)

    result = check_toolchain()
    for field in ("status", "errors", "warnings", "tools"):
        assert field in result
    assert isinstance(result["errors"], list)
    assert isinstance(result["warnings"], list)
    assert isinstance(result["tools"], dict)
    for info in result["tools"].values():
        assert "available" in info
        assert "version" in info
