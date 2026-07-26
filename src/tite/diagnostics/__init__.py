"""
Diagnostics module for Tite.

This module provides health checking, diagnostics, and reporting
functionality for Tite projects.
"""

from tite.diagnostics.doctor import Doctor
from tite.diagnostics.health import HealthChecker, HealthStatus
from tite.diagnostics.checks import (
    Check,
    CheckResult,
    CheckStatus,
    PythonCheck,
    VenvCheck,
    GitCheck,
    ProjectFilesCheck,
    DependenciesCheck,
    ConfigCheck,
)
from tite.diagnostics.report import ReportGenerator, ReportFormat

__all__ = [
    "Doctor",
    "HealthChecker",
    "HealthStatus",
    "Check",
    "CheckResult",
    "CheckStatus",
    "PythonCheck",
    "VenvCheck",
    "GitCheck",
    "ProjectFilesCheck",
    "DependenciesCheck",
    "ConfigCheck",
    "ReportGenerator",
    "ReportFormat",
]