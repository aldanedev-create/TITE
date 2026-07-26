"""
Package management for Tite.

This module handles package installation, management, and
dependency resolution for Python projects.
"""

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger

from tite.exceptions import EnvironmentError


@dataclass
class PackageInfo:
    """
    Information about a package.
    
    Attributes:
        name: Package name
        version: Package version
        description: Package description
        author: Package author
        license: Package license
        homepage: Package homepage
        dependencies: Package dependencies
    """
    name: str
    version: str
    description: str = ""
    author: str = ""
    license: str = ""
    homepage: str = ""
    dependencies: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.name}=={self.version}"
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "license": self.license,
            "homepage": self.homepage,
            "dependencies": self.dependencies,
        }


class PackageManager:
    """
    Manages Python packages.
    
    This class handles package installation, listing, and
    management with support for pip and other package managers.
    
    Attributes:
        python_path: Path to Python interpreter
        pip_path: Path to pip executable
        packages: Installed packages
    """
    
    def __init__(self, python_path: Optional[Path] = None):
        """
        Initialize the package manager.
        
        Args:
            python_path: Path to Python interpreter
        """
        self.python_path = Path(python_path) if python_path else Path(sys.executable)
        self.pip_path = self._find_pip()
        self.packages: Dict[str, PackageInfo] = {}
        self._load_packages()
        
    def _find_pip(self) -> Optional[Path]:
        """
        Find pip executable.
        
        Returns:
            Optional[Path]: Path to pip or None
        """
        # Try python -m pip
        try:
            subprocess.run(
                [str(self.python_path), "-m", "pip", "--version"],
                capture_output=True,
                check=True,
            )
            # pip is available as a module
            return None
        except Exception:
            pass
            
        # Try pip in PATH
        pip_names = ["pip", "pip3"]
        for name in pip_names:
            try:
                result = subprocess.run(
                    ["which", name],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                if result.stdout.strip():
                    return Path(result.stdout.strip())
            except Exception:
                pass
                
        return None
        
    def _load_packages(self) -> None:
        """Load installed packages."""
        self.packages = self.get_installed_packages()
        
    def get_installed_packages(self) -> Dict[str, PackageInfo]:
        """
        Get installed packages.
        
        Returns:
            Dict[str, PackageInfo]: Package name to info mapping
        """
        packages = {}
        
        try:
            # Get package list
            result = subprocess.run(
                [str(self.python_path), "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
                check=True,
            )
            
            data = json.loads(result.stdout)
            
            for item in data:
                name = item.get("name", "")
                version = item.get("version", "")
                if name and version:
                    packages[name] = PackageInfo(
                        name=name,
                        version=version,
                    )
                    
            # Get detailed info for each package
            for name in list(packages.keys()):
                try:
                    info = self._get_package_info(name)
                    if info:
                        packages[name] = info
                except Exception:
                    pass
                    
        except Exception as e:
            logger.warning(f"Failed to load packages: {e}")
            
        return packages
        
    def _get_package_info(self, name: str) -> Optional[PackageInfo]:
        """
        Get detailed information about a package.
        
        Args:
            name: Package name
            
        Returns:
            Optional[PackageInfo]: Package information or None
        """
        try:
            result = subprocess.run(
                [str(self.python_path), "-m", "pip", "show", name],
                capture_output=True,
                text=True,
                check=True,
            )
            
            info = {}
            for line in result.stdout.strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    info[key.strip().lower()] = value.strip()
                    
            return PackageInfo(
                name=name,
                version=info.get("version", ""),
                description=info.get("summary", ""),
                author=info.get("author", ""),
                license=info.get("license", ""),
                homepage=info.get("home-page", ""),
                dependencies=info.get("requires", "").split(", ") if info.get("requires") else [],
            )
        except Exception:
            return None
            
    def install(
        self,
        packages: List[str],
        upgrade: bool = False,
        no_deps: bool = False,
    ) -> bool:
        """
        Install packages.
        
        Args:
            packages: List of packages to install
            upgrade: Whether to upgrade existing packages
            no_deps: Whether to skip dependency installation
            
        Returns:
            bool: True if successful
        """
        if not packages:
            return True
            
        cmd = [str(self.python_path), "-m", "pip", "install"]
        
        if upgrade:
            cmd.append("--upgrade")
        if no_deps:
            cmd.append("--no-deps")
            
        cmd.extend(packages)
        
        try:
            logger.info(f"Installing packages: {', '.join(packages)}")
            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            # Reload packages
            self._load_packages()
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install packages: {e.stderr}")
            return False
            
    def uninstall(self, packages: List[str]) -> bool:
        """
        Uninstall packages.
        
        Args:
            packages: List of packages to uninstall
            
        Returns:
            bool: True if successful
        """
        if not packages:
            return True
            
        try:
            logger.info(f"Uninstalling packages: {', '.join(packages)}")
            subprocess.run(
                [str(self.python_path), "-m", "pip", "uninstall", "-y"] + packages,
                capture_output=True,
                text=True,
                check=True,
            )
            # Reload packages
            self._load_packages()
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to uninstall packages: {e.stderr}")
            return False
            
    def update(self, packages: List[str]) -> bool:
        """
        Update packages.
        
        Args:
            packages: List of packages to update
            
        Returns:
            bool: True if successful
        """
        return self.install(packages, upgrade=True)
        
    def install_requirements(self, requirements_file: Path) -> bool:
        """
        Install packages from a requirements file.
        
        Args:
            requirements_file: Path to requirements file
            
        Returns:
            bool: True if successful
        """
        if not requirements_file.exists():
            logger.warning(f"Requirements file not found: {requirements_file}")
            return False
            
        try:
            logger.info(f"Installing from: {requirements_file}")
            subprocess.run(
                [str(self.python_path), "-m", "pip", "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True,
                check=True,
            )
            # Reload packages
            self._load_packages()
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install requirements: {e.stderr}")
            return False
            
    def freeze(self, output_file: Optional[Path] = None) -> str:
        """
        Freeze installed packages to requirements format.
        
        Args:
            output_file: Optional file to write to
            
        Returns:
            str: Requirements string
        """
        try:
            result = subprocess.run(
                [str(self.python_path), "-m", "pip", "freeze"],
                capture_output=True,
                text=True,
                check=True,
            )
            
            content = result.stdout.strip()
            
            if output_file:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(content)
                logger.info(f"Requirements saved to: {output_file}")
                
            return content
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to freeze packages: {e.stderr}")
            return ""
            
    def check_outdated(self) -> List[Tuple[str, str, str]]:
        """
        Check for outdated packages.
        
        Returns:
            List[Tuple[str, str, str]]: (package, current_version, latest_version)
        """
        outdated = []
        
        try:
            result = subprocess.run(
                [str(self.python_path), "-m", "pip", "list", "--outdated", "--format=json"],
                capture_output=True,
                text=True,
                check=True,
            )
            
            data = json.loads(result.stdout)
            
            for item in data:
                name = item.get("name", "")
                current = item.get("version", "")
                latest = item.get("latest_version", "")
                if name and current and latest:
                    outdated.append((name, current, latest))
                    
        except Exception as e:
            logger.warning(f"Failed to check outdated packages: {e}")
            
        return outdated
        
    def get_dependencies(self, package: str) -> List[str]:
        """
        Get dependencies of a package.
        
        Args:
            package: Package name
            
        Returns:
            List[str]: List of dependencies
        """
        info = self._get_package_info(package)
        return info.dependencies if info else []