"""
Download utilities for Tite.

This module provides utilities for downloading files and data
from the internet.
"""

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse

import requests


class DownloadUtils:
    """
    Utility class for downloading files.
    
    This class provides static methods for downloading files,
    JSON data, and other content from URLs.
    """
    
    @staticmethod
    def download_file(
        url: str,
        dest_path: Union[str, Path],
        chunk_size: int = 8192,
        timeout: int = 30,
        progress_callback: Optional[callable] = None,
    ) -> Path:
        """
        Download a file from a URL.
        
        Args:
            url: URL to download from
            dest_path: Destination path
            chunk_size: Download chunk size
            timeout: Request timeout
            progress_callback: Callback for progress updates
            
        Returns:
            Path: Path to downloaded file
            
        Raises:
            requests.RequestException: If download fails
        """
        dest = Path(dest_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        # Download with progress
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total_size > 0:
                        progress_callback(downloaded, total_size)
                        
        return dest
        
    @staticmethod
    def download_json(
        url: str,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Download JSON data from a URL.
        
        Args:
            url: URL to download from
            timeout: Request timeout
            headers: Request headers
            
        Returns:
            Dict[str, Any]: Parsed JSON data
            
        Raises:
            requests.RequestException: If download fails
        """
        response = requests.get(url, timeout=timeout, headers=headers or {})
        response.raise_for_status()
        return response.json()
        
    @staticmethod
    def download_text(
        url: str,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Download text content from a URL.
        
        Args:
            url: URL to download from
            timeout: Request timeout
            headers: Request headers
            
        Returns:
            str: Text content
            
        Raises:
            requests.RequestException: If download fails
        """
        response = requests.get(url, timeout=timeout, headers=headers or {})
        response.raise_for_status()
        return response.text
        
    @staticmethod
    def download_and_extract(
        url: str,
        dest_path: Path,
        format: Optional[str] = None,
        progress_callback: Optional[callable] = None,
    ) -> Path:
        """
        Download and extract an archive.
        
        Args:
            url: URL to download from
            dest_path: Destination path for extraction
            format: Archive format (auto-detected if None)
            progress_callback: Callback for progress updates
            
        Returns:
            Path: Path to extracted directory
        """
        # Download to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
            tmp_path = Path(tmp.name)
            
        try:
            DownloadUtils.download_file(url, tmp_path, progress_callback=progress_callback)
            
            # Extract
            from tite.utils.archive import ArchiveUtils
            ArchiveUtils.extract_archive(tmp_path, dest_path)
            
            return dest_path
            
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
                
    @staticmethod
    def get_filename_from_url(url: str) -> str:
        """
        Get filename from a URL.
        
        Args:
            url: URL
            
        Returns:
            str: Filename
        """
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        if not filename:
            filename = "download"
            
        return filename
        
    @staticmethod
    def get_content_type(url: str, timeout: int = 5) -> Optional[str]:
        """
        Get content type from a URL.
        
        Args:
            url: URL
            timeout: Request timeout
            
        Returns:
            Optional[str]: Content type or None
        """
        try:
            response = requests.head(url, timeout=timeout)
            return response.headers.get('content-type')
        except Exception:
            return None
            
    @staticmethod
    def get_file_size(url: str, timeout: int = 5) -> Optional[int]:
        """
        Get file size from a URL.
        
        Args:
            url: URL
            timeout: Request timeout
            
        Returns:
            Optional[int]: File size in bytes or None
        """
        try:
            response = requests.head(url, timeout=timeout)
            content_length = response.headers.get('content-length')
            if content_length:
                return int(content_length)
        except Exception:
            pass
        return None


def download_file(url: str, dest_path: Union[str, Path]) -> Path:
    """Download a file from a URL."""
    return DownloadUtils.download_file(url, dest_path)


def download_json(url: str) -> Dict[str, Any]:
    """Download JSON data from a URL."""
    return DownloadUtils.download_json(url)