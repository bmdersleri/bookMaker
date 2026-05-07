"""bookmaker.production.screenshot_strategies"""

from bookmaker.production.screenshot_strategies.base import (
    ScreenshotConfig,
    ScreenshotResult,
    ScreenshotStrategy,
)
from bookmaker.production.screenshot_strategies.python_console import PythonConsoleStrategy
from bookmaker.production.screenshot_strategies.python_plot import PythonPlotStrategy
from bookmaker.production.screenshot_strategies.react_component import ReactComponentStrategy

__all__ = [
    "ScreenshotConfig",
    "ScreenshotResult",
    "ScreenshotStrategy",
    "PythonPlotStrategy",
    "PythonConsoleStrategy",
    "ReactComponentStrategy",
]
