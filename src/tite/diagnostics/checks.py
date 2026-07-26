"""
Health checks for Tite.

This module provides individual health checks for various aspects
of a Tite project.
"""

import importlib
import os
import subprocess
import sys
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from tite.core.config import ConfigManager
from tite.core.environment import EnvironmentManager
from tite.core.git import GitManager


class CheckStatus(Enum):
    """Status of a check."""
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"
    SKIPPED = "skipped"


class CheckResult:
    """
    Result of a health check.
    
    Attributes:
        check_name: Name of the check
        status: Check status
        message: Status message
        details: Additional details
        recommendations: List of recommendations
    """
    
    def __init__(
        self,
        check_name: str,
        status: CheckStatus,
        message: str = "",
        details: Optional[Dict[str, Any]] = None,
        recommendations: Optional[List[str]] = None,
    ):
        """
        Initialize a check result.
        
        Args:
            check_name: Name of the check
            status: Check status
            message: Status message
            details: Additional details
            recommendations: List of recommendations
        """
        self.check_name = check_name
        self.status = status
        self.message = message
        self.details = details or {}
        self.recommendations = recommendations or []
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "check": self.check_name,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
            "recommendations": self.recommendations,
        }


class Check(ABC):
    """
    Abstract base class for health checks.
    
    Attributes:
        name: Name of the check
        project_path: Path to the project
    """
    
    def __init__(self, project_path: Path, name: str):
        """
        Initialize a check.
        
        Args:
            project_path: Path to the project
            name: Name of the check
        """
        self.project_path = Path(project_path)
        self.name = name
        
    @abstractmethod
    def run(self) -> CheckResult:
        """
        Run the check.
        
        Returns:
            CheckResult: Result of the check
        """
        pass


class PythonCheck(Check):
    """
    Checks Python installation and version.
    """
    
    def __init__(self, project_path: Path):
        super().__init__(project_path, "Python Version")
        
    def run(self) -> CheckResult:
        """Check Python version."""
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        # Check if version meets minimum requirements
        if version.major >= 3 and version.minor >= 9:
            return CheckResult(
                self.name,
                CheckStatus.PASSED,
                f"Python {version_str} detected",
                {"version": version_str, "path": sys.executable},
            )
        else:
            return CheckResult(
                self.name,
                CheckStatus.FAILED,
                f"Python {version_str} is not supported (Python 3.9+ required)",
                {"version": version_str, "path": sys.executable},
                ["Install Python 3.9 or higher"],
            )


class VenvCheck(Check):
    """
    Checks virtual environment.
    """
    
    def __init__(self, project_path: Path):
        super().__init__(project_path, "Virtual Environment")
        
    def run(self) -> CheckResult:
        """Check virtual environment."""
        env_manager = EnvironmentManager(self.project_path)
        
        if env_manager.venv_exists():
            venv_path = env_manager.venv_path
            python_path = env_manager.get_python_path()
            
            if env_manager.is_venv_active():
                return CheckResult(
                    self.name,
                    CheckStatus.PASSED,
                    f"Virtual environment active at {venv_path}",
                    {"path": str(venv_path), "python": str(python_path), "active": True},
                )
            else:
                return CheckResult(
                    self.name,
                    CheckStatus.WARNING,
                    f"Virtual environment exists but is not active",
                    {"path": str(venv_path), "python": str(python_path), "active": False},
                    ["Activate the virtual environment: source .venv/bin/activate"],
                )
        else:
            return CheckResult(
                self.name,
                CheckStatus.FAILED,
                "Virtual environment not found",
                {"path": str(self.project_path / ".venv")},
                ["Create a virtual environment: python -m venv .venv"],
            )


class GitCheck(Check):
    """
    Checks Git repository.
    """
    
    def __init__(self, project_path: Path):
        super().__init__(project_path, "Git Repository")
        
    def run(self) -> CheckResult:
        """Check Git repository."""
        git_manager = GitManager(self.project_path)
        
        if git_manager.is_initialized():
            branch = git_manager.get_current_branch()
            status = git_manager.get_status()
            
            if status and status.get("changes"):
                return CheckResult(
                    self.name,
                    CheckStatus.WARNING,
                    f"Git repository initialized on branch {branch} with uncommitted changes",
                    {"branch": branch, "changes": len(status.get("changes", [])), 
                     "untracked": len(status.get("untracked", []))},
                    ["Commit changes: git add . && git commit -m 'message'"],
                )
            else:
                return CheckResult(
                    self.name,
                    CheckStatus.PASSED,
                    f"Git repository initialized on branch {branch}",
                    {"branch": branch, "clean": True},
                )
        else:
            return CheckResult(
                self.name,
                CheckStatus.FAILED,
                "Git repository not initialized",
                {},
                ["Initialize Git: git init"],
            )


class ProjectFilesCheck(Check):
    """
    Checks project files and structure.
    """
    
    def __init__(self, project_path: Path):
        super().__init__(project_path, "Project Files")
        
    def run(self) -> CheckResult:
        """Check project files."""
        required_files = [
            "README.md",
            "pyproject.toml",
            ".gitignore",
        ]
        
        required_dirs = [
            "src",
            "tests",
        ]
        
        missing_files = []
        missing_dirs = []
        
        for file_name in required_files:
            if not (self.project_path / file_name).exists():
                missing_files.append(file_name)
                
        for dir_name in required_dirs:
            if not (self.project_path / dir_name).exists():
                missing_dirs.append(dir_name)
                
        if missing_files or missing_dirs:
            details = {}
            if missing_files:
                details["missing_files"] = missing_files
            if missing_dirs:
                details["missing_dirs"] = missing_dirs
                
            return CheckResult(
                self.name,
                CheckStatus.FAILED,
                "Required project files or directories are missing",
                details,
                ["Create missing files and directories"],
            )
        else:
            return CheckResult(
                self.name,
                CheckStatus.PASSED,
                "All required project files are present",
                {"files": required_files, "directories": required_dirs},
            )


class DependenciesCheck(Check):
    """
    Checks project dependencies.
    """
    
    def __init__(self, project_path: Path):
        super().__init__(project_path, "Dependencies")
        
    def run(self) -> CheckResult:
        """Check dependencies."""
        config_manager = ConfigManager(self.project_path)
        env_manager = EnvironmentManager(self.project_path)
        
        try:
            config = config_manager.load_config()
            dependencies = config.get("project", {}).get("dependencies", {})
        except Exception:
            dependencies = {}
            
        if not dependencies:
            return CheckResult(
                self.name,
                CheckStatus.WARNING,
                "No dependencies defined in pyproject.toml",
                {"dependencies": []},
                ["Add dependencies to pyproject.toml"],
            )
            
        # Check if dependencies are installed
        installed_packages = {}
        if env_manager.venv_exists():
            installed_packages = env_manager.get_installed_packages()
            
        missing_packages = []
        for dep in dependencies:
            if dep not in installed_packages:
                missing_packages.append(dep)
                
        if missing_packages:
            return CheckResult(
                self.name,
                CheckStatus.FAILED,
                f"Missing {len(missing_packages)} dependencies",
                {"missing": missing_packages, "installed": len(installed_packages)},
                [f"Install missing dependencies: pip install {' '.join(missing_packages)}"],
            )
        else:
            return CheckResult(
                self.name,
                CheckStatus.PASSED,
                f"All {len(dependencies)} dependencies are installed",
                {"installed": list(dependencies.keys())},
            )


class ConfigCheck(Check):
    """
    Checks project configuration.
    """
    
    def __init__(self, project_path: Path):
        super().__init__(project_path, "Configuration")
        
    def run(self) -> CheckResult:
        """Check configuration."""
        config_manager = ConfigManager(self.project_path)
        
        try:
            config = config_manager.load_config()
            
            # Check required config fields
            required_fields = ["project.name"]
            missing_fields = []
            
            for field in required_fields:
                if not config_manager.get(field):
                    missing_fields.append(field)
                    
            if missing_fields:
                return CheckResult(
                    self.name,
                    CheckStatus.FAILED,
                    "Missing required configuration fields",
                    {"missing": missing_fields},
                    ["Update configuration with required fields"],
                )
            else:
                return CheckResult(
                    self.name,
                    CheckStatus.PASSED,
                    "Configuration is valid",
                    {"project": config.get("project", {})},
                )
        except Exception as e:
            return CheckResult(
                self.name,
                CheckStatus.FAILED,
                f"Failed to load configuration: {str(e)}",
                {},
                ["Check configuration syntax and format"],
            )