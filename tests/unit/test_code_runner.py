from __future__ import annotations


def test_unknown_code_profile_uses_review_only_adapter() -> None:
    from bookmaker.code.adapters.base import ReviewOnlyAdapter
    from bookmaker.code.runner import select_code_adapter

    adapter = select_code_adapter(None, None)

    assert isinstance(adapter, ReviewOnlyAdapter)

