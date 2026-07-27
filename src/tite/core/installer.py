"""
Core package installer for Tite.

Installs Python packages into a project's virtual environment,
falling back to the current interpreter's pip if no venv exists yet.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Union

from tite.core.environment import EnvironmentManager


class PackageInstaller:
    """
    Installs packages for a project.

    Attributes:
        project_path: Path to the project directory
    """

    def __init__(self, project_path: Union[str, Path]):
        """
        Initialize the package installer.

        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)
        self._env_manager = EnvironmentManager(self.project_path)

    def install_packages(self, packages: List[str]) -> bool:
        """
        Install a list of packages.

        Uses the project's virtual environment if one exists; otherwise
        falls back to the current Python interpreter's pip.

        Args:
            packages: List of package specifiers (e.g. "requests>=2.31.0")

        Returns:
            bool: True if installation succeeded
        """
        if not packages:
            return True

        if self._env_manager.venv_exists():
            return self._env_manager.install_packages(packages)

        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install"] + list(packages),
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except Exception:
            return False