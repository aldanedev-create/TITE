"""
Archive utilities for Tite.

This module provides utilities for creating and extracting archives
in various formats.
"""

import shutil
import tarfile
import zipfile
from pathlib import Path
from typing import List, Optional, Union


class ArchiveUtils:
    """
    Utility class for archive operations.
    
    This class provides static methods for creating and extracting
    archives in zip, tar, and other formats.
    """
    
    @staticmethod
    def extract_archive(
        archive_path: Path,
        extract_path: Path,
        format: Optional[str] = None,
    ) -> None:
        """
        Extract an archive.
        
        Args:
            archive_path: Path to archive
            extract_path: Path to extract to
            format: Archive format (auto-detected if None)
            
        Raises:
            ValueError: If format is not supported
        """
        extract_path.mkdir(parents=True, exist_ok=True)
        
        # Auto-detect format
        if format is None:
            suffix = archive_path.suffix.lower()
            if suffix == ".zip":
                format = "zip"
            elif suffix in (".tar", ".gz", ".tgz", ".bz2", ".xz"):
                format = "tar"
            else:
                raise ValueError(f"Unknown archive format: {suffix}")
                
        if format == "zip":
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
        elif format == "tar":
            with tarfile.open(archive_path, "r") as tar_ref:
                tar_ref.extractall(extract_path)
        else:
            raise ValueError(f"Unsupported archive format: {format}")
            
    @staticmethod
    def create_archive(
        source_path: Path,
        archive_path: Path,
        format: str = "zip",
        compression: Optional[str] = None,
    ) -> None:
        """
        Create an archive.
        
        Args:
            source_path: Path to archive
            archive_path: Output archive path
            format: Archive format (zip, tar)
            compression: Compression type (gz, bz2, xz)
            
        Raises:
            ValueError: If format is not supported
        """
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "zip":
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zip_ref:
                if source_path.is_file():
                    zip_ref.write(source_path, source_path.name)
                else:
                    for file_path in source_path.rglob("*"):
                        if file_path.is_file():
                            arcname = file_path.relative_to(source_path.parent)
                            zip_ref.write(file_path, str(arcname))
        elif format == "tar":
            mode = "w"
            if compression == "gz":
                mode = "w:gz"
            elif compression == "bz2":
                mode = "w:bz2"
            elif compression == "xz":
                mode = "w:xz"
            elif compression:
                raise ValueError(f"Unsupported compression: {compression}")
                
            with tarfile.open(archive_path, mode) as tar_ref:
                tar_ref.add(source_path, arcname=source_path.name)
        else:
            raise ValueError(f"Unsupported archive format: {format}")
            
    @staticmethod
    def list_archive(archive_path: Path) -> List[str]:
        """
        List contents of an archive.
        
        Args:
            archive_path: Path to archive
            
        Returns:
            List[str]: List of files in the archive
            
        Raises:
            ValueError: If format is not supported
        """
        suffix = archive_path.suffix.lower()
        
        if suffix == ".zip":
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                return [f.filename for f in zip_ref.filelist]
        elif suffix in (".tar", ".gz", ".tgz", ".bz2", ".xz"):
            with tarfile.open(archive_path, "r") as tar_ref:
                return [m.name for m in tar_ref.getmembers()]
        else:
            raise ValueError(f"Unknown archive format: {suffix}")
            
    @staticmethod
    def get_archive_info(archive_path: Path) -> dict:
        """
        Get information about an archive.
        
        Args:
            archive_path: Path to archive
            
        Returns:
            dict: Archive information
        """
        info = {
            "path": str(archive_path),
            "size": archive_path.stat().st_size,
            "format": archive_path.suffix.lower(),
            "file_count": 0,
        }
        
        try:
            files = ArchiveUtils.list_archive(archive_path)
            info["file_count"] = len(files)
        except Exception:
            pass
            
        return info


def extract_archive(archive_path: Path, extract_path: Path) -> None:
    """Extract an archive."""
    ArchiveUtils.extract_archive(archive_path, extract_path)


def create_archive(source_path: Path, archive_path: Path, format: str = "zip") -> None:
    """Create an archive."""
    ArchiveUtils.create_archive(source_path, archive_path, format)