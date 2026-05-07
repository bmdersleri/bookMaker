"""Code adapter implementations for different programming languages.

Each adapter handles running tests on extracted code blocks
from book chapters for a specific language or platform.
"""

from __future__ import annotations

from bookmaker.code.adapters.base import CodeAdapter, ReviewOnlyAdapter
from bookmaker.code.adapters.flutter import FlutterCodeAdapter
from bookmaker.code.adapters.java import JavaCodeAdapter
from bookmaker.code.adapters.python import PythonCodeAdapter
from bookmaker.code.adapters.react import ReactCodeAdapter

__all__ = [
    "CodeAdapter",
    "FlutterCodeAdapter",
    "JavaCodeAdapter",
    "PythonCodeAdapter",
    "ReactCodeAdapter",
    "ReviewOnlyAdapter",
]
