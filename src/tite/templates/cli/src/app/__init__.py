"""
CLI application package for {{ project_name }}.

This package provides the command-line interface for the application.
"""

from app.main import main
from app.commands import register_commands
from app.config import load_config

__all__ = [
    "main",
    "register_commands",
    "load_config",
]