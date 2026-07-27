"""
Core project manager for Tite.

Lightweight helper for looking up basic facts about a project
directory. Currently only imported by tite.modes.manager (not yet
called with specific methods elsewhere), so this intentionally stays
small; extend as new call sites need it.
"""

from pathlib import Path
from typing import Any, Dict, Union

from tite.constants import CONFIG_DIR_NAME, CONFIG_FILE_NAME


class ProjectManager:
    """
    Provides basic information and checks about a Tite project.

    Attributes:
        project_path: Path to the project directory
    """

    def __init__(self, project_path: Union[str, Path]):
        """
        Initialize the project manager.

        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)

    def exists(self) -> bool:
        """Check whether the project directory exists."""
        return self.project_path.exists()

    def is_tite_project(self) -> bool:
        """Check whether this directory has been initialized with Tite."""
        return (self.project_path / CONFIG_DIR_NAME / CONFIG_FILE_NAME).exists()

    def get_info(self) -> Dict[str, Any]:
        """Get basic information about the project."""
        return {
            "name": self.project_path.name,
            "path": str(self.project_path),
            "exists": self.exists(),
            "is_tite_project": self.is_tite_project(),
        }