"""Code execution and adapter selection for bookMaker.

Provides the public API for selecting code adapters
based on profile or language.
"""

from __future__ import annotations

from bookmaker.code.runner import select_code_adapter

__all__ = ["select_code_adapter"]
