"""
Python management for Tite.

This module handles Python version detection, validation,
and management for Tite projects.
"""

import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from loguru import logger

from tite.exceptions import EnvironmentError


@dataclass
class PythonVersion:
    """
    Python version information.
    
    Attributes:
        major: Major version number
        minor: Minor version number
        micro: Micro version number
        release_level: Release level (final, alpha, beta, etc.)
        serial: Release serial number
    """
    major: int
    minor: int
    micro: int
    release_level: str = "final"
    serial: int = 0
    
    def __str__(self) -> str:
        """Return version string."""
        if self.release_level == "final":
            return f"{self.major}.{self.minor}.{self.micro}"
        return f"{self.major}.{self.minor}.{self.micro}{self.release_level[0]}{self.serial}"
        
    def __eq__(self, other) -> bool:
        """Check equality with another version."""
        if isinstance(other, PythonVersion):
            return (self.major, self.minor, self.micro) == (other.major, other.minor, other.micro)
        return str(self) == str(other)
        
    def __lt__(self, other) -> bool:
        """Check if this version is less than another."""
        if isinstance(other, PythonVersion):
            return (self.major, self.minor, self.micro) < (other.major, other.minor, other.micro)
        return str(self) < str(other)
        
    def __le__(self, other) -> bool:
        """Check if this version is less than or equal to another."""
        if isinstance(other, PythonVersion):
            return (self.major, self.minor, self.micro) <= (other.major, other.minor, other.micro)
        return str(self) <= str(other)
        
    def __gt__(self, other) -> bool:
        """Check if this version is greater than another."""
        if isinstance(other, PythonVersion):
            return (self.major, self.minor, self.micro) > (other.major, other.minor, other.micro)
        return str(self) > str(other)
        
    def __ge__(self, other) -> bool:
        """Check if this version is greater than or equal to another."""
        if isinstance(other, PythonVersion):
            return (self.major, self.minor, self.micro) >= (other.major, other.minor, other.micro)
        return str(self) >= str(other)
        
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to tuple."""
        return (self.major, self.minor, self.micro)
        
    def to_string(self, include_serial: bool = False) -> str:
        """Convert to string."""
        if include_serial:
            return str(self)
        return f"{self.major}.{self.minor}.{self.micro}"


class PythonManager:
    """
    Manages Python versions and interpreters.
    
    This class handles detecting Python versions, finding
    Python interpreters, and validating version compatibility.
    
    Attributes:
        current_version: Current Python version
        interpreters: Available Python interpreters
    """
    
    def __init__(self):
        """Initialize the Python manager."""
        self.current_version = self._get_current_version()
        self.interpreters: Dict[str, Path] = {}
        self._scan_interpreters()
        
    def _get_current_version(self) -> PythonVersion:
        """
        Get the current Python version.
        
        Returns:
            PythonVersion: Current Python version
        """
        version = sys.version_info
        return PythonVersion(
            major=version.major,
            minor=version.minor,
            micro=version.micro,
            release_level=version.releaselevel,
            serial=version.serial,
        )
        
    def _scan_interpreters(self) -> None:
        """Scan for available Python interpreters."""
        self.interpreters = {}
        
        # Add current interpreter
        self.interpreters[str(self.current_version)] = Path(sys.executable)
        
        # Scan common locations
        common_paths = self._get_common_paths()
        
        for path in common_paths:
            if path.exists():
                for python_path in self._find_python_in_path(path):
                    version = self._get_version_from_interpreter(python_path)
                    if version and str(version) not in self.interpreters:
                        self.interpreters[str(version)] = python_path
                        
    def _get_common_paths(self) -> List[Path]:
        """
        Get common paths for Python interpreters.
        
        Returns:
            List[Path]: Common paths
        """
        if sys.platform == "win32":
            return [
                Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Python",
                Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Python",
                Path(os.environ.get("APPDATA", "")) / "Python",
                Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Python",
            ]
        else:
            return [
                Path("/usr/bin"),
                Path("/usr/local/bin"),
                Path("/opt"),
                Path("/opt/homebrew/bin"),
            ]
            
    def _find_python_in_path(self, path: Path) -> List[Path]:
        """
        Find Python interpreters in a path.
        
        Args:
            path: Directory path
            
        Returns:
            List[Path]: Python interpreter paths
        """
        pythons = []
        for file in path.glob("python*"):
            if file.is_file() and self._is_python_executable(file):
                pythons.append(file)
        return pythons
        
    def _is_python_executable(self, path: Path) -> bool:
        """
        Check if a file is a Python executable.
        
        Args:
            path: File path
            
        Returns:
            bool: True if it's a Python executable
        """
        try:
            result = subprocess.run(
                [str(path), "--version"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            return result.returncode == 0 and "Python" in result.stdout
        except Exception:
            return False
            
    def _get_version_from_interpreter(self, path: Path) -> Optional[PythonVersion]:
        """
        Get version from a Python interpreter.
        
        Args:
            path: Path to Python interpreter
            
        Returns:
            Optional[PythonVersion]: Python version or None
        """
        try:
            result = subprocess.run(
                [str(path), "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            version_str = result.stdout.strip().split()[1]
            
            # Parse version string
            parts = version_str.split(".")
            if len(parts) >= 2:
                major = int(parts[0])
                minor = int(parts[1])
                micro = int(parts[2]) if len(parts) > 2 else 0
                return PythonVersion(major=major, minor=minor, micro=micro)
        except Exception:
            pass
        return None
        
    def get_version(self) -> PythonVersion:
        """
        Get the current Python version.
        
        Returns:
            PythonVersion: Current Python version
        """
        return self.current_version
        
    def get_interpreter(self, version: Optional[str] = None) -> Optional[Path]:
        """
        Get path to a Python interpreter.
        
        Args:
            version: Python version string (e.g., "3.12")
            
        Returns:
            Optional[Path]: Path to interpreter or None
        """
        if version is None:
            return Path(sys.executable)
            
        # Try exact match
        if version in self.interpreters:
            return self.interpreters[version]
            
        # Try partial match
        for v, path in self.interpreters.items():
            if v.startswith(version):
                return path
                
        return None
        
    def get_available_versions(self) -> List[str]:
        """
        Get available Python versions.
        
        Returns:
            List[str]: Available version strings
        """
        return sorted(self.interpreters.keys())
        
    def validate_version(self, required_version: str) -> bool:
        """
        Validate Python version compatibility.
        
        Args:
            required_version: Required version string (e.g., ">=3.9")
            
        Returns:
            bool: True if compatible
            
        Raises:
            EnvironmentError: If version is incompatible
        """
        current = self.current_version
        current_str = str(current)
        
        # Simple version check
        if required_version.startswith(">="):
            min_version_str = required_version[2:].strip()
            min_version = self._parse_version(min_version_str)
            if current < min_version:
                raise EnvironmentError(
                    f"Python {required_version} is required, current version is {current_str}"
                )
            return True
        elif required_version.startswith("<="):
            max_version_str = required_version[2:].strip()
            max_version = self._parse_version(max_version_str)
            if current > max_version:
                raise EnvironmentError(
                    f"Python {required_version} is required, current version is {current_str}"
                )
            return True
        else:
            # Exact version
            required = self._parse_version(required_version)
            if current != required:
                raise EnvironmentError(
                    f"Python {required_version} is required, current version is {current_str}"
                )
            return True
            
    def _parse_version(self, version_str: str) -> PythonVersion:
        """
        Parse a version string.
        
        Args:
            version_str: Version string
            
        Returns:
            PythonVersion: Parsed version
        """
        parts = version_str.split(".")
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        micro = int(parts[2]) if len(parts) > 2 else 0
        return PythonVersion(major=major, minor=minor, micro=micro)
        
    def get_system_info(self) -> Dict[str, str]:
        """
        Get system information.
        
        Returns:
            Dict[str, str]: System information
        """
        return {
            "python_version": str(self.current_version),
            "python_executable": sys.executable,
            "python_prefix": sys.prefix,
            "platform": platform.system(),
            "platform_release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }