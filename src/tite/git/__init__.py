"""
Git module for Tite.

This module provides Git integration for Tite projects including
repository initialization, .gitignore management, hooks, and
repository operations.
"""

from tite.git.init import GitInit, GitInitializer
from tite.git.ignore import GitIgnore, IgnoreManager
from tite.git.hooks import GitHooks, HookManager
from tite.git.repository import GitRepository, RepositoryManager

__all__ = [
    "GitInit",
    "GitInitializer",
    "GitIgnore",
    "IgnoreManager",
    "GitHooks",
    "HookManager",
    "GitRepository",
    "RepositoryManager",
]