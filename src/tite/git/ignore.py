"""
Git ignore management for Tite.

This module handles .gitignore file management with support for
common Python patterns and custom rules.
"""

import fnmatch
from pathlib import Path
from typing import List, Optional, Set, Union

from loguru import logger

from tite.exceptions import FileOperationError


class GitIgnore:
    """
    Manages .gitignore files.
    
    This class provides functionality for creating, reading,
    updating, and validating .gitignore files.
    
    Attributes:
        path: Path to .gitignore file
        patterns: Set of ignore patterns
    """
    
    # Default Python patterns
    DEFAULT_PATTERNS = [
        "# Byte-compiled / optimized / DLL files",
        "__pycache__/",
        "*.py[cod]",
        "*$py.class",
        "*.so",
        "*.pyd",
        "*.pyo",
        "",
        "# Virtual environments",
        ".venv/",
        "venv/",
        "ENV/",
        "env/",
        "env.bak/",
        "",
        "# Distribution / packaging",
        "build/",
        "dist/",
        "*.egg-info/",
        "*.egg",
        "*.egg-info/",
        "MANIFEST",
        ".eggs/",
        "",
        "# Unit test / coverage reports",
        "htmlcov/",
        ".tox/",
        ".nox/",
        ".coverage",
        ".coverage.*",
        ".cache",
        "nosetests.xml",
        "coverage.xml",
        "*.cover",
        ".pytest_cache/",
        ".mypy_cache/",
        ".ruff_cache/",
        ".hypothesis/",
        "",
        "# Environment variables",
        ".env",
        ".env.local",
        ".env.*.local",
        ".envrc",
        ".direnv/",
        "",
        "# IDE / Editor",
        ".idea/",
        ".vscode/",
        "*.iml",
        "*.swp",
        "*.swo",
        "*~",
        ".DS_Store",
        "Thumbs.db",
        "",
        "# Tite specific",
        ".tite/",
        "*.tite.lock",
        "",
        "# Logs",
        "logs/",
        "*.log",
        "*.pid",
        "*.pid.lock",
        "",
        "# Databases",
        "*.db",
        "*.sqlite",
        "*.sqlite3",
        "",
        "# Secrets",
        "*.key",
        "*.pem",
        "*.crt",
        "*.csr",
        "*.p12",
        "*.pfx",
        "*.p8",
        "*.p7b",
        "*.cer",
        "*.der",
        "*.gpg",
        "*.asc",
        "",
        "# Data files",
        "*.csv",
        "*.tsv",
        "*.parquet",
        "*.pickle",
        "*.pkl",
        "*.joblib",
        "*.dill",
        "*.npy",
        "*.npz",
        "*.mat",
        "*.h5",
        "*.hdf5",
        "*.nc",
        "*.netcdf",
        "*.feather",
        "*.arrow",
        "*.jsonl",
        "*.ndjson",
        "",
        "# Model files",
        "*.model",
        "*.models",
        "*.weights",
        "*.weight",
        "*.ckpt",
        "*.pt",
        "*.pth",
        "*.pb",
        "*.onnx",
        "*.tflite",
        "",
        "# Jupyter Notebooks",
        ".ipynb_checkpoints/",
        "*.ipynb_checkpoints/",
        "",
        "# Temporary files",
        "*.tmp",
        "*.temp",
        "*.bak",
        "*.backup",
        "*.swp",
        "*.swo",
    ]
    
    def __init__(self, path: Union[str, Path]):
        """
        Initialize .gitignore manager.
        
        Args:
            path: Path to .gitignore file
        """
        self.path = Path(path)
        self.patterns: Set[str] = set()
        self._load()
        
    def _load(self) -> None:
        """Load patterns from .gitignore file."""
        if self.path.exists():
            try:
                content = self.path.read_text(encoding="utf-8")
                self.patterns = set(self._parse_content(content))
            except Exception:
                self.patterns = set()
        else:
            self.patterns = set()
            
    def _parse_content(self, content: str) -> List[str]:
        """
        Parse .gitignore content.
        
        Args:
            content: .gitignore content
            
        Returns:
            List[str]: List of patterns
        """
        patterns = []
        for line in content.split("\n"):
            line = line.rstrip("\n\r")
            if line and not line.startswith("#"):
                patterns.append(line)
        return patterns
        
    def add(self, pattern: str) -> None:
        """
        Add a pattern to .gitignore.
        
        Args:
            pattern: Pattern to add
        """
        self.patterns.add(pattern)
        self._save()
        
    def remove(self, pattern: str) -> bool:
        """
        Remove a pattern from .gitignore.
        
        Args:
            pattern: Pattern to remove
            
        Returns:
            bool: True if pattern was removed
        """
        if pattern in self.patterns:
            self.patterns.remove(pattern)
            self._save()
            return True
        return False
        
    def _save(self) -> None:
        """Save patterns to .gitignore file."""
        try:
            content = self._format_content()
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(content, encoding="utf-8")
        except Exception as e:
            raise FileOperationError(str(self.path), "write", str(e))
            
    def _format_content(self) -> str:
        """
        Format patterns for .gitignore file.
        
        Returns:
            str: Formatted content
        """
        lines = []
        patterns = sorted(self.patterns)
        
        # Add default header
        lines.append("# Auto-generated by Tite")
        lines.append("")
        lines.append("# Python")
        lines.append("__pycache__/")
        lines.append("*.py[cod]")
        lines.append("*.so")
        lines.append("*.pyd")
        lines.append("*.pyo")
        lines.append("")
        
        # Add custom patterns
        for pattern in patterns:
            if pattern not in self.DEFAULT_PATTERNS:
                lines.append(pattern)
                
        return "\n".join(lines)
        
    def matches(self, path: Path) -> bool:
        """
        Check if a path matches any pattern.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path is ignored
        """
        path_str = str(path)
        for pattern in self.patterns:
            if fnmatch.fnmatch(path_str, pattern):
                return True
            if pattern in path_str:
                return True
        return False
        
    def add_default_patterns(self) -> None:
        """Add default Python patterns."""
        for pattern in self.DEFAULT_PATTERNS:
            if pattern and not pattern.startswith("#"):
                self.patterns.add(pattern)
        self._save()
        
    def get_patterns(self) -> List[str]:
        """
        Get all patterns.
        
        Returns:
            List[str]: List of patterns
        """
        return sorted(self.patterns)


class IgnoreManager:
    """
    Manages ignore patterns across multiple files.
    
    This class provides functionality for managing .gitignore,
    .dockerignore, and other ignore files.
    
    Attributes:
        gitignore: .gitignore manager
    """
    
    def __init__(self, project_path: Path):
        """
        Initialize the ignore manager.
        
        Args:
            project_path: Project path
        """
        self.project_path = Path(project_path)
        self.gitignore = GitIgnore(self.project_path / ".gitignore")
        self.dockerignore = GitIgnore(self.project_path / ".dockerignore")
        
    def add_gitignore(self, pattern: str) -> None:
        """Add a pattern to .gitignore."""
        self.gitignore.add(pattern)
        
    def add_dockerignore(self, pattern: str) -> None:
        """Add a pattern to .dockerignore."""
        self.dockerignore.add(pattern)
        
    def add_common_python_ignores(self) -> None:
        """Add common Python ignore patterns."""
        patterns = [
            "__pycache__/",
            "*.py[cod]",
            "*.so",
            "*.pyd",
            "*.pyo",
            ".venv/",
            "venv/",
            "env/",
            "build/",
            "dist/",
            "*.egg-info/",
            ".pytest_cache/",
            ".mypy_cache/",
            ".ruff_cache/",
            ".coverage",
            "coverage.xml",
            "htmlcov/",
            ".env",
            ".idea/",
            ".vscode/",
            "*.iml",
            ".DS_Store",
            "Thumbs.db",
            "logs/",
            "*.log",
            "*.db",
            "*.sqlite",
            "*.key",
            "*.pem",
            "*.crt",
            ".tite/",
        ]
        
        for pattern in patterns:
            self.gitignore.add(pattern)
            
    def get_ignored_files(self) -> List[Path]:
        """
        Get all ignored files.
        
        Returns:
            List[Path]: List of ignored file paths
        """
        ignored = []
        for path in self.project_path.rglob("*"):
            if self.gitignore.matches(path):
                ignored.append(path)
        return ignored
        
    def is_ignored(self, path: Path) -> bool:
        """
        Check if a path is ignored.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if ignored
        """
        return self.gitignore.matches(path)