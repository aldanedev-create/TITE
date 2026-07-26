"""
Automation mode for Tite.

This module provides the Automation mode configuration for Tite,
including task scheduling, scripting, and automation workflows.
"""

from tite.modes.automation.mode import AutomationMode
from tite.modes.automation.structure import AutomationStructure
from tite.modes.automation.config import AutomationConfig
from tite.modes.automation.packages import AUTOMATION_PACKAGES

__all__ = [
    "AutomationMode",
    "AutomationStructure",
    "AutomationConfig",
    "AUTOMATION_PACKAGES",
]