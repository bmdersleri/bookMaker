"""bookmaker.production.screenshot_strategies"""

from bookmaker.production.screenshot_strategies.base import (
    ScreenshotConfig,
    ScreenshotResult,
    ScreenshotStrategy,
)
from bookmaker.production.screenshot_strategies.flutter_golden import FlutterGoldenStrategy
from bookmaker.production.screenshot_strategies.flutter_web import FlutterWebStrategy
from bookmaker.production.screenshot_strategies.python_console import PythonConsoleStrategy
from bookmaker.production.screenshot_strategies.python_plot import PythonPlotStrategy
from bookmaker.production.screenshot_strategies.react_component import ReactComponentStrategy

__all__ = [
    "FlutterGoldenStrategy",
    "FlutterWebStrategy",
    "PythonConsoleStrategy",
    "PythonPlotStrategy",
    "ReactComponentStrategy",
    "ScreenshotConfig",
    "ScreenshotResult",
    "ScreenshotStrategy",
]
