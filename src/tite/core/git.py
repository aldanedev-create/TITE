"""
Core Git manager for Tite.

Wraps tite.git.repository.GitRepository and tite.git.init.GitInitializer
to provide the interface used by the CLI commands and diagnostics.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union

from tite.git.repository import GitRepository
from tite.git.init import GitInitializer


class GitManager:
    """
    Manages the Git repository for a single project.

    Attributes:
        project_path: Path to the project directory
    """

    def __init__(self, project_path: Union[str, Path]):
        """
        Initialize the Git manager.

        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)
        self._repo = GitRepository(self.project_path)

    def init(self) -> bool:
        """Initialize a Git repository with standard configuration."""
        initializer = GitInitializer(self.project_path)
        return initializer.init_standard()

    def is_initialized(self) -> bool:
        """Check whether a Git repository has been initialized."""
        return self._repo.is_initialized()

    def get_current_branch(self) -> Optional[str]:
        """Get the current branch name."""
        return self._repo.get_branch()

    def get_remote_url(self, name: str = "origin") -> Optional[str]:
        """Get the URL of a remote (defaults to origin)."""
        return self._repo.get_remote(name)

    def get_status(self) -> Dict[str, Any]:
        """Get the repository status (branch, changes, untracked files, etc.)."""
        return self._repo.get_status()