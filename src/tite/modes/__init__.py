"""
Modes module for Tite.

This module provides domain-specific project modes for common Python development
workflows including Data Science, AI/ML, and Automation.
"""

from tite.modes.manager import ModeManager
from tite.modes.registry import ModeRegistry
from tite.modes.loader import ModeLoader
from tite.modes.validator import ModeValidator

# Mode submodules
from tite.modes.data import DataMode
from tite.modes.ai import AIMode
from tite.modes.automation import AutomationMode

__all__ = [
    # Core
    "ModeManager",
    "ModeRegistry",
    "ModeLoader",
    "ModeValidator",
    
    # Mode implementations
    "DataMode",
    "AIMode",
    "AutomationMode",
]