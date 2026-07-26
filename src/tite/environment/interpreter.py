"""
Interpreter management for Tite.

This module handles Python interpreter selection, validation,
and management for Tite projects.
"""

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger

from tite.environment.python import PythonManager, PythonVersion
from tite.exceptions import EnvironmentError


@dataclass
class InterpreterInfo:
    """
    Information about a Python interpreter.
    
    Attributes:
        path: Path to the interpreter
        version: Python version
        executable: Executable name
        is_venv: Whether it's a virtual environment
        is_active: Whether it's currently active
        location: Installation location
    """
    path: Path
    version: PythonVersion
    executable: str = ""
    is_venv: bool = False
    is_active: bool = False
    location: str = ""
    packages: Dict[str, str] = field(default_factory=dict)
    
    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.path} ({self.version})"
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "path": str(self.path),
            "version": str(self.version),
            "executable": self.executable,
            "is_venv": self.is_venv,
            "is_active": self.is_active,
            "location": self.location,
            "packages": self.packages,
        }


class InterpreterManager:
    """
    Manages Python interpreters.
    
    This class handles discovering, selecting, and validating
    Python interpreters for Tite projects.
    
    Attributes:
        python_manager: Python version manager
        interpreters: Available interpreters
        selected: Selected interpreter
    """
    
    def __init__(self):
        """Initialize the interpreter manager."""
        self.python_manager = PythonManager()
        self.interpreters: List[InterpreterInfo] = []
        self.selected: Optional[InterpreterInfo] = None
        self._scan_interpreters()
        
    def _scan_interpreters(self) -> None:
        """Scan for available interpreters."""
        self.interpreters = []
        
        # Add current interpreter
        current = InterpreterInfo(
            path=Path(sys.executable),
            version=self.python_manager.current_version,
            executable=sys.executable,
            is_venv=sys.prefix != sys.base_prefix,
            is_active=True,
            location=sys.prefix,
        )
        self.interpreters.append(current)
        
        # Scan for other interpreters
        for version_str, path in self.python_manager.interpreters.items():
            if path != Path(sys.executable):
                version = self.python_manager._parse_version(version_str)
                interpreter = InterpreterInfo(
                    path=path,
                    version=version,
                    executable=path.name,
                    is_venv=False,
                    is_active=False,
                    location=str(path.parent),
                )
                self.interpreters.append(interpreter)
                
    def get_interpreters(self) -> List[InterpreterInfo]:
        """
        Get all available interpreters.
        
        Returns:
            List[InterpreterInfo]: Available interpreters
        """
        return self.interpreters
        
    def get_interpreter(self, version: Optional[str] = None) -> Optional[InterpreterInfo]:
        """
        Get an interpreter by version.
        
        Args:
            version: Python version string
            
        Returns:
            Optional[InterpreterInfo]: Interpreter or None
        """
        if version is None:
            return self._get_current_interpreter()
            
        for interpreter in self.interpreters:
            if str(interpreter.version) == version:
                return interpreter
            if str(interpreter.version).startswith(version):
                return interpreter
        return None
        
    def _get_current_interpreter(self) -> InterpreterInfo:
        """
        Get the current interpreter.
        
        Returns:
            InterpreterInfo: Current interpreter
        """
        for interpreter in self.interpreters:
            if interpreter.is_active:
                return interpreter
                
        # Fallback to creating from current
        return InterpreterInfo(
            path=Path(sys.executable),
            version=self.python_manager.current_version,
            executable=sys.executable,
            is_venv=sys.prefix != sys.base_prefix,
            is_active=True,
            location=sys.prefix,
        )
        
    def select_interpreter(self, version: str) -> Optional[InterpreterInfo]:
        """
        Select an interpreter by version.
        
        Args:
            version: Python version string
            
        Returns:
            Optional[InterpreterInfo]: Selected interpreter or None
        """
        interpreter = self.get_interpreter(version)
        if interpreter:
            self.selected = interpreter
            return interpreter
        return None
        
    def validate_interpreter(self, required_version: str) -> bool:
        """
        Validate interpreter version compatibility.
        
        Args:
            required_version: Required version string
            
        Returns:
            bool: True if compatible
            
        Raises:
            EnvironmentError: If incompatible
        """
        return self.python_manager.validate_version(required_version)
        
    def get_interpreter_info(self, path: Optional[Path] = None) -> InterpreterInfo:
        """
        Get information about an interpreter.
        
        Args:
            path: Path to interpreter (uses current if None)
            
        Returns:
            InterpreterInfo: Interpreter information
        """
        if path is None:
            return self._get_current_interpreter()
            
        try:
            result = subprocess.run(
                [str(path), "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            version_str = result.stdout.strip().split()[1]
            
            # Parse version
            parts = version_str.split(".")
            major = int(parts[0]) if len(parts) > 0 else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            micro = int(parts[2]) if len(parts) > 2 else 0
            
            version = PythonVersion(major=major, minor=minor, micro=micro)
            
            # Check if it's a virtual environment
            is_venv = False
            location = str(path.parent)
            
            # Try to get prefix
            try:
                result = subprocess.run(
                    [str(path), "-c", "import sys; print(sys.prefix)"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                prefix = result.stdout.strip()
                
                # Check if it's a virtual environment
                if prefix != sys.base_prefix:
                    is_venv = True
                    location = prefix
            except Exception:
                pass
                
            return InterpreterInfo(
                path=path,
                version=version,
                executable=path.name,
                is_venv=is_venv,
                is_active=path == Path(sys.executable),
                location=location,
            )
        except Exception as e:
            raise EnvironmentError(f"Failed to get interpreter info: {e}")
            
    def get_packages(self, interpreter: Optional[InterpreterInfo] = None) -> Dict[str, str]:
        """
        Get installed packages for an interpreter.
        
        Args:
            interpreter: Interpreter (uses selected if None)
            
        Returns:
            Dict[str, str]: Package name to version mapping
        """
        if interpreter is None:
            interpreter = self.selected or self._get_current_interpreter()
            
        try:
            result = subprocess.run(
                [str(interpreter.path), "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
                check=True,
            )
            
            data = json.loads(result.stdout)
            packages = {}
            for item in data:
                name = item.get("name", "")
                version = item.get("version", "")
                if name and version:
                    packages[name] = version
            return packages
        except Exception:
            return {}
            
    def get_available_versions(self) -> List[str]:
        """
        Get available Python versions.
        
        Returns:
            List[str]: Available version strings
        """
        versions = set()
        for interpreter in self.interpreters:
            versions.add(str(interpreter.version))
        return sorted(versions)
        
    def get_environment_info(self) -> Dict[str, Any]:
        """
        Get environment information.
        
        Returns:
            Dict[str, Any]: Environment information
        """
        current = self._get_current_interpreter()
        
        return {
            "interpreter": str(current.path),
            "version": str(current.version),
            "is_venv": current.is_venv,
            "location": current.location,
            "packages": current.packages,
            "available_versions": self.get_available_versions(),
            "platform": sys.platform,
            "python_path": sys.path,
        }