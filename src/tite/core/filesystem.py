"""
Core filesystem manager for Tite.

Wraps tite.utils.paths and tite.utils.io to provide the project-scoped
file/directory operations used by the bootstrap engine and blueprint
builder.
"""

from pathlib import Path
from typing import Union

from tite.exceptions import FileOperationError
from tite.utils.io import write_file as _write_file
from tite.utils.io import read_file as _read_file
from tite.utils.paths import PathUtils


class FileSystemManager:
    """
    Manages file and directory creation for a single project.

    Attributes:
        project_path: Path to the project directory
    """

    def __init__(self, project_path: Union[str, Path]):
        """
        Initialize the filesystem manager.

        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)

    def create_directory(self, path: Union[str, Path], exist_ok: bool = True) -> Path:
        """
        Create a directory (and any missing parents).

        Args:
            path: Directory path (absolute, or relative to project_path)
            exist_ok: Whether it's fine for the directory to already exist

        Returns:
            Path: The created directory path
        """
        target = self._resolve(path)
        try:
            if target.exists() and not exist_ok:
                raise FileOperationError(str(target), "create directory", "Directory already exists")
            return PathUtils.ensure_dir(target)
        except FileOperationError:
            raise
        except Exception as e:
            raise FileOperationError(str(target), "create directory", str(e))

    def write_file(self, path: Union[str, Path], content: str, encoding: str = "utf-8") -> Path:
        """
        Write text content to a file, creating parent directories as needed.

        Args:
            path: File path (absolute, or relative to project_path)
            content: Content to write
            encoding: File encoding

        Returns:
            Path: The written file path
        """
        target = self._resolve(path)
        try:
            _write_file(target, content, encoding=encoding)
            return target
        except Exception as e:
            raise FileOperationError(str(target), "write file", str(e))

    def read_file(self, path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Read text content from a file.

        Args:
            path: File path (absolute, or relative to project_path)
            encoding: File encoding

        Returns:
            str: File content
        """
        target = self._resolve(path)
        try:
            return _read_file(target, encoding=encoding)
        except Exception as e:
            raise FileOperationError(str(target), "read file", str(e))

    def exists(self, path: Union[str, Path]) -> bool:
        """Check whether a file or directory exists."""
        return self._resolve(path).exists()

    def _resolve(self, path: Union[str, Path]) -> Path:
        """Resolve a path relative to the project directory if not absolute."""
        path = Path(path)
        if path.is_absolute():
            return path
        return self.project_path / path