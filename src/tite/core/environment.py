"""
Core environment manager for Tite.

Wraps tite.environment.venv.VenvManager/VirtualEnv to provide the
project-scoped interface used by the CLI commands and diagnostics.
"""

import sys
from pathlib import Path
from typing import Dict, Optional, Union

from tite.environment.venv import VenvManager, VirtualEnv


class EnvironmentManager:
    """
    Manages the Python virtual environment for a single project.

    Attributes:
        project_path: Path to the project directory
        venv_path: Path to the project's virtual environment (.venv)
    """

    def __init__(self, project_path: Union[str, Path], venv_name: str = ".venv"):
        """
        Initialize the environment manager.

        Args:
            project_path: Path to the project directory
            venv_name: Name of the virtual environment directory
        """
        self.project_path = Path(project_path)
        self.venv_name = venv_name
        self.venv_path = self.project_path / venv_name
        self._venv_manager = VenvManager(self.project_path, default_name=venv_name)

    def _get_venv(self) -> Optional[VirtualEnv]:
        return self._venv_manager.get(self.venv_name)

    def venv_exists(self) -> bool:
        """Check whether the project's virtual environment exists."""
        venv = self._get_venv()
        return venv is not None and venv.exists()

    def is_venv_active(self) -> bool:
        """Check whether the project's virtual environment is currently active."""
        return sys.prefix == str(self.venv_path)

    def get_python_path(self) -> Path:
        """Get the path to the venv's Python executable."""
        venv = self._get_venv()
        if venv:
            return venv.python_path
        return VirtualEnv(self.venv_path, self.venv_name).python_path

    def get_pip_path(self) -> Path:
        """Get the path to the venv's pip executable."""
        venv = self._get_venv()
        if venv:
            return venv.pip_path
        return VirtualEnv(self.venv_path, self.venv_name).pip_path

    def get_python_version(self) -> Optional[str]:
        """Get the Python version installed in the venv."""
        venv = self._get_venv()
        if venv:
            return venv.get_python_version()
        return None

    def get_installed_packages(self) -> Dict[str, str]:
        """Get installed packages (name -> version) in the venv."""
        venv = self._get_venv()
        if venv:
            return venv.get_packages()
        return {}

    def create_venv(self, clear: bool = False, system_site_packages: bool = False) -> VirtualEnv:
        """Create the project's virtual environment."""
        if self.venv_exists() and not clear:
            return self._get_venv()
        return self._venv_manager.create(
            name=self.venv_name,
            clear=clear,
            system_site_packages=system_site_packages,
        )

    def install_packages(self, packages) -> bool:
        """Install a list of packages into the project's virtual environment."""
        venv = self._get_venv()
        if not venv:
            return False
        return venv.install_packages(packages)