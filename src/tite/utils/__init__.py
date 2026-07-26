"""
Utilities module for Tite.

This module provides various utility functions and classes used
throughout the Tite application.
"""

from tite.utils.logger import setup_logger, get_logger, Logger
from tite.utils.paths import PathUtils, get_project_root, ensure_dir
from tite.utils.io import (
    read_file,
    write_file,
    read_json,
    write_json,
    read_yaml,
    write_yaml,
    read_toml,
    write_toml,
)
from tite.utils.system import SystemUtils, get_system_info
from tite.utils.archive import ArchiveUtils, extract_archive, create_archive
from tite.utils.terminal import (
    TerminalUtils,
    get_terminal_size,
    clear_screen,
    colorize,
    strip_colors,
)
from tite.utils.download import DownloadUtils, download_file, download_json
from tite.utils.platform import PlatformUtils, get_platform, is_windows, is_macos, is_linux

__all__ = [
    # Logger
    "setup_logger",
    "get_logger",
    "Logger",
    
    # Paths
    "PathUtils",
    "get_project_root",
    "ensure_dir",
    
    # IO
    "read_file",
    "write_file",
    "read_json",
    "write_json",
    "read_yaml",
    "write_yaml",
    "read_toml",
    "write_toml",
    
    # System
    "SystemUtils",
    "get_system_info",
    
    # Archive
    "ArchiveUtils",
    "extract_archive",
    "create_archive",
    
    # Terminal
    "TerminalUtils",
    "get_terminal_size",
    "clear_screen",
    "colorize",
    "strip_colors",
    
    # Download
    "DownloadUtils",
    "download_file",
    "download_json",
    
    # Platform
    "PlatformUtils",
    "get_platform",
    "is_windows",
    "is_macos",
    "is_linux",
]