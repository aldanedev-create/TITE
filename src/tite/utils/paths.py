"""
Path utilities for Tite.

This module provides path manipulation and resolution utilities.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Union


class PathUtils:
    """
    Utility class for path operations.
    
    This class provides static methods for path manipulation,
    resolution, and validation.
    """
    
    @staticmethod
    def resolve(path: Union[str, Path]) -> Path:
        """
        Resolve a path to an absolute path.
        
        Args:
            path: Path to resolve
            
        Returns:
            Path: Resolved absolute path
        """
        return Path(path).resolve()
        
    @staticmethod
    def is_relative_to(path: Path, parent: Path) -> bool:
        """
        Check if a path is relative to a parent path.
        
        Args:
            path: Path to check
            parent: Parent path
            
        Returns:
            bool: True if path is relative to parent
        """
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False
            
    @staticmethod
    def get_relative_path(path: Path, base: Path) -> Path:
        """
        Get the relative path from base to path.
        
        Args:
            path: Target path
            base: Base path
            
        Returns:
            Path: Relative path
        """
        try:
            return path.relative_to(base)
        except ValueError:
            return path
            
    @staticmethod
    def ensure_dir(path: Path) -> Path:
        """
        Ensure a directory exists.
        
        Args:
            path: Directory path
            
        Returns:
            Path: The directory path
        """
        path.mkdir(parents=True, exist_ok=True)
        return path
        
    @staticmethod
    def ensure_file(path: Path) -> Path:
        """
        Ensure the parent directory of a file exists.
        
        Args:
            path: File path
            
        Returns:
            Path: The file path
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
        
    @staticmethod
    def find_files(
        root: Path,
        pattern: str = "*",
        recursive: bool = True,
        exclude: Optional[List[str]] = None,
    ) -> List[Path]:
        """
        Find files matching a pattern.
        
        Args:
            root: Root directory
            pattern: Glob pattern
            recursive: Whether to search recursively
            exclude: List of patterns to exclude
            
        Returns:
            List[Path]: List of matching file paths
        """
        exclude = exclude or []
        
        if recursive:
            iterator = root.rglob(pattern)
        else:
            iterator = root.glob(pattern)
            
        files = []
        for path in iterator:
            if path.is_file():
                should_exclude = False
                for ex in exclude:
                    if ex in str(path) or path.match(ex):
                        should_exclude = True
                        break
                if not should_exclude:
                    files.append(path)
                    
        return files
        
    @staticmethod
    def get_file_size(path: Path) -> int:
        """
        Get file size in bytes.
        
        Args:
            path: File path
            
        Returns:
            int: File size in bytes
        """
        if path.exists():
            return path.stat().st_size
        return 0
        
    @staticmethod
    def get_file_extension(path: Path) -> str:
        """
        Get file extension.
        
        Args:
            path: File path
            
        Returns:
            str: File extension (including dot)
        """
        return path.suffix.lower()
        
    @staticmethod
    def get_file_name_without_extension(path: Path) -> str:
        """
        Get file name without extension.
        
        Args:
            path: File path
            
        Returns:
            str: File name without extension
        """
        return path.stem
        
    @staticmethod
    def get_parent_path(path: Path, levels: int = 1) -> Path:
        """
        Get parent path at a certain level.
        
        Args:
            path: Path
            levels: Number of levels to go up
            
        Returns:
            Path: Parent path
        """
        result = path
        for _ in range(levels):
            result = result.parent
        return result
        
    @staticmethod
    def is_subpath(path: Path, parent: Path) -> bool:
        """
        Check if a path is a subpath of another.
        
        Args:
            path: Path to check
            parent: Parent path
            
        Returns:
            bool: True if path is a subpath
        """
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False
            
    @staticmethod
    def get_common_parent(paths: List[Path]) -> Optional[Path]:
        """
        Get the common parent directory of multiple paths.
        
        Args:
            paths: List of paths
            
        Returns:
            Optional[Path]: Common parent path or None
        """
        if not paths:
            return None
            
        common = paths[0].parent
        for path in paths[1:]:
            while not PathUtils.is_relative_to(path, common) and common != common.parent:
                common = common.parent
                
        if PathUtils.is_relative_to(paths[0], common):
            return common
        return None
        
    @staticmethod
    def get_project_root() -> Path:
        """
        Get the project root directory.
        
        Returns:
            Path: Project root path
        """
        # Try to find using pyproject.toml
        current = Path.cwd()
        while current != current.parent:
            if (current / "pyproject.toml").exists():
                return current
            current = current.parent
            
        # Try to find using .git
        current = Path.cwd()
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent
            
        return Path.cwd()


def get_project_root() -> Path:
    """Get the project root directory."""
    return PathUtils.get_project_root()


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists."""
    return PathUtils.ensure_dir(path)