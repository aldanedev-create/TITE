"""
Virtual environment management for Tite.

This module handles virtual environment creation, detection,
activation, and management.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from loguru import logger

from tite.exceptions import EnvironmentError


class VirtualEnv:
    """
    Represents a virtual environment.
    
    Attributes:
        path: Path to the virtual environment
        name: Name of the virtual environment
        python_path: Path to Python executable
        pip_path: Path to pip executable
        activate_path: Path to activation script
    """
    
    def __init__(self, path: Path, name: Optional[str] = None):
        """
        Initialize a virtual environment.
        
        Args:
            path: Path to the virtual environment
            name: Name of the virtual environment
        """
        self.path = Path(path)
        self.name = name or self.path.name
        
        # Detect OS-specific paths
        self._detect_paths()
        
    def _detect_paths(self) -> None:
        """Detect paths for the current OS."""
        if sys.platform == "win32":
            self.bin_dir = self.path / "Scripts"
            self.python_path = self.bin_dir / "python.exe"
            self.pip_path = self.bin_dir / "pip.exe"
            self.activate_path = self.bin_dir / "activate"
        else:
            self.bin_dir = self.path / "bin"
            self.python_path = self.bin_dir / "python"
            self.pip_path = self.bin_dir / "pip"
            self.activate_path = self.bin_dir / "activate"
            
    def exists(self) -> bool:
        """Check if the virtual environment exists."""
        return self.path.exists() and self.python_path.exists()
        
    def is_active(self) -> bool:
        """Check if the virtual environment is currently active."""
        return sys.prefix == str(self.path)
        
    def get_python_version(self) -> Optional[str]:
        """
        Get the Python version in this virtual environment.
        
        Returns:
            Optional[str]: Python version string
        """
        if not self.exists():
            return None
            
        try:
            result = subprocess.run(
                [str(self.python_path), "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split()[1]
        except Exception:
            return None
            
    def get_packages(self) -> Dict[str, str]:
        """
        Get installed packages in this virtual environment.
        
        Returns:
            Dict[str, str]: Package name to version mapping
        """
        if not self.exists():
            return {}
            
        try:
            result = subprocess.run(
                [str(self.pip_path), "list", "--format=freeze"],
                capture_output=True,
                text=True,
                check=True,
            )
            
            packages = {}
            for line in result.stdout.strip().split("\n"):
                if "==" in line:
                    name, version = line.split("==", 1)
                    packages[name] = version
            return packages
        except Exception:
            return {}
            
    def install_packages(self, packages: List[str]) -> bool:
        """
        Install packages in this virtual environment.
        
        Args:
            packages: List of packages to install
            
        Returns:
            bool: True if successful
        """
        if not self.exists():
            return False
            
        try:
            subprocess.run(
                [str(self.pip_path), "install"] + packages,
                capture_output=True,
                text=True,
                check=True,
            )
            return True
        except Exception:
            return False


class VenvManager:
    """
    Manages virtual environments.
    
    This class handles creating, deleting, and managing virtual
    environments with support for different Python versions.
    
    Attributes:
        base_path: Base path for virtual environments
        default_name: Default virtual environment name
    """
    
    def __init__(self, base_path: Optional[Path] = None, default_name: str = ".venv"):
        """
        Initialize the virtual environment manager.
        
        Args:
            base_path: Base path for virtual environments
            default_name: Default virtual environment name
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.default_name = default_name
        self._venvs: Dict[str, VirtualEnv] = {}
        
    def create(
        self,
        name: Optional[str] = None,
        python_path: Optional[str] = None,
        clear: bool = False,
        system_site_packages: bool = False,
    ) -> VirtualEnv:
        """
        Create a virtual environment.
        
        Args:
            name: Name of the virtual environment
            python_path: Path to Python interpreter to use
            clear: Whether to clear existing environment
            system_site_packages: Whether to include system site packages
            
        Returns:
            VirtualEnv: Created virtual environment
            
        Raises:
            EnvironmentError: If creation fails
        """
        name = name or self.default_name
        venv_path = self.base_path / name
        
        if venv_path.exists() and clear:
            shutil.rmtree(venv_path)
            
        if venv_path.exists():
            raise EnvironmentError(f"Virtual environment already exists: {venv_path}")
            
        logger.info(f"Creating virtual environment: {venv_path}")
        
        try:
            import venv
            builder = venv.EnvBuilder(
                system_site_packages=system_site_packages,
                clear=clear,
                with_pip=True,
                upgrade=False,
            )
            
            if python_path:
                # Use specified Python
                builder.python = python_path
                
            builder.create(venv_path)
            
            venv_env = VirtualEnv(venv_path, name)
            self._venvs[name] = venv_env
            
            logger.info(f"Virtual environment created: {venv_path}")
            return venv_env
            
        except Exception as e:
            raise EnvironmentError(f"Failed to create virtual environment: {e}")
            
    def delete(self, name: Optional[str] = None) -> bool:
        """
        Delete a virtual environment.
        
        Args:
            name: Name of the virtual environment
            
        Returns:
            bool: True if deleted
        """
        name = name or self.default_name
        venv_path = self.base_path / name
        
        if not venv_path.exists():
            return False
            
        logger.info(f"Deleting virtual environment: {venv_path}")
        
        try:
            shutil.rmtree(venv_path)
            if name in self._venvs:
                del self._venvs[name]
            return True
        except Exception as e:
            logger.error(f"Failed to delete virtual environment: {e}")
            return False
            
    def get(self, name: Optional[str] = None) -> Optional[VirtualEnv]:
        """
        Get a virtual environment.
        
        Args:
            name: Name of the virtual environment
            
        Returns:
            Optional[VirtualEnv]: Virtual environment or None
        """
        name = name or self.default_name
        venv_path = self.base_path / name
        
        if not venv_path.exists():
            return None
            
        if name not in self._venvs:
            self._venvs[name] = VirtualEnv(venv_path, name)
            
        return self._venvs[name]
        
    def list_all(self) -> List[VirtualEnv]:
        """
        List all virtual environments.
        
        Returns:
            List[VirtualEnv]: List of virtual environments
        """
        venvs = []
        for path in self.base_path.iterdir():
            if path.is_dir() and self._is_venv(path):
                venv = VirtualEnv(path)
                venvs.append(venv)
                self._venvs[venv.name] = venv
        return venvs
        
    def _is_venv(self, path: Path) -> bool:
        """
        Check if a directory is a virtual environment.
        
        Args:
            path: Directory path
            
        Returns:
            bool: True if it's a virtual environment
        """
        if sys.platform == "win32":
            return (path / "Scripts" / "python.exe").exists()
        else:
            return (path / "bin" / "python").exists()
            
    def get_active(self) -> Optional[VirtualEnv]:
        """
        Get the currently active virtual environment.
        
        Returns:
            Optional[VirtualEnv]: Active virtual environment or None
        """
        if sys.prefix == sys.base_prefix:
            return None
            
        # Try to find which virtual environment is active
        for name, venv in self._venvs.items():
            if venv.is_active():
                return venv
                
        # Try to detect from sys.prefix
        venv_path = Path(sys.prefix)
        if self._is_venv(venv_path):
            return VirtualEnv(venv_path)
            
        return None
        
    def get_python_path(self, name: Optional[str] = None) -> Optional[Path]:
        """
        Get the Python path for a virtual environment.
        
        Args:
            name: Name of the virtual environment
            
        Returns:
            Optional[Path]: Path to Python or None
        """
        venv = self.get(name)
        if venv and venv.exists():
            return venv.python_path
        return None
        
    def get_pip_path(self, name: Optional[str] = None) -> Optional[Path]:
        """
        Get the pip path for a virtual environment.
        
        Args:
            name: Name of the virtual environment
            
        Returns:
            Optional[Path]: Path to pip or None
        """
        venv = self.get(name)
        if venv and venv.exists():
            return venv.pip_path
        return None