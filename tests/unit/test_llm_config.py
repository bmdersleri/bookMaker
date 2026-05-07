from __future__ import annotations

from pathlib import Path


def test_ambos_configured_is_backward_compatible(tmp_path: Path) -> None:
    from bookmaker.llm.config import LLMConfig

    cfg = LLMConfig(tmp_path)

    assert isinstance(cfg.ambos_configured, bool)
    assert cfg.ambos_configured is False

