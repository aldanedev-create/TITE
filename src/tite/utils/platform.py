"""
Platform utilities for Tite.

This module provides platform detection and OS-specific utility
functions.
"""
import tempfile
import os
import platform
import sys
from pathlib import Path
from typing import Dict, Optional


class PlatformUtils:
    """
    Utility class for platform detection.
    
    This class provides methods for detecting the current platform
    and getting platform-specific information.
    """
    
    @staticmethod
    def get_platform() -> str:
        """
        Get the current platform.
        
        Returns:
            str: Platform name (windows, macos, linux, etc.)
        """
        system = platform.system().lower()
        if system == "darwin":
            return "macos"
        elif system == "windows":
            return "windows"
        elif system == "linux":
            return "linux"
        else:
            return system
            
    @staticmethod
    def is_windows() -> bool:
        """Check if running on Windows."""
        return sys.platform == "win32"
        
    @staticmethod
    def is_macos() -> bool:
        """Check if running on macOS."""
        return sys.platform == "darwin"
        
    @staticmethod
    def is_linux() -> bool:
        """Check if running on Linux."""
        return sys.platform.startswith("linux")
        
    @staticmethod
    def is_cygwin() -> bool:
        """Check if running on Cygwin."""
        return sys.platform.startswith("cygwin")
        
    @staticmethod
    def is_msys() -> bool:
        """Check if running on MSYS."""
        return sys.platform.startswith("msys")
        
    @staticmethod
    def is_termux() -> bool:
        """Check if running on Termux."""
        return os.environ.get("TERMUX_VERSION") is not None
        
    @staticmethod
    def get_os_name() -> str:
        """
        Get the OS name.
        
        Returns:
            str: OS name
        """
        return platform.system()
        
    @staticmethod
    def get_os_version() -> str:
        """
        Get the OS version.
        
        Returns:
            str: OS version
        """
        return platform.version()
        
    @staticmethod
    def get_os_release() -> str:
        """
        Get the OS release.
        
        Returns:
            str: OS release
        """
        return platform.release()
        
    @staticmethod
    def get_machine() -> str:
        """
        Get the machine architecture.
        
        Returns:
            str: Machine architecture
        """
        return platform.machine()
        
    @staticmethod
    def get_processor() -> str:
        """
        Get the processor type.
        
        Returns:
            str: Processor type
        """
        return platform.processor()
        
    @staticmethod
    def get_architecture() -> str:
        """
        Get the system architecture.
        
        Returns:
            str: Architecture (32bit, 64bit)
        """
        return platform.architecture()[0]
        
    @staticmethod
    def get_platform_info() -> Dict[str, str]:
        """
        Get platform information.
        
        Returns:
            Dict[str, str]: Platform information
        """
        return {
            "platform": PlatformUtils.get_platform(),
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "architecture": PlatformUtils.get_architecture(),
            "python_version": sys.version.split()[0],
            "python_implementation": platform.python_implementation(),
        }
        
    @staticmethod
    def get_system_path_separator() -> str:
        """
        Get the system path separator.
        
        Returns:
            str: Path separator
        """
        return os.path.sep
        
    @staticmethod
    def get_system_pathsep() -> str:
        """
        Get the system pathsep.
        
        Returns:
            str: Pathsep
        """
        return os.pathsep
        
    @staticmethod
    def get_system_encoding() -> str:
        """
        Get the system encoding.
        
        Returns:
            str: System encoding
        """
        return sys.getdefaultencoding()
        
    @staticmethod
    def get_temp_dir() -> Path:
        """
        Get the system temp directory.
        
        Returns:
            Path: Temp directory path
        """
        return Path(tempfile.gettempdir())
        
    @staticmethod
    def get_user_home() -> Path:
        """
        Get the user home directory.
        
        Returns:
            Path: User home directory
        """
        return Path.home()
        
    @staticmethod
    def get_current_user() -> str:
        """
        Get the current user name.
        
        Returns:
            str: User name
        """
        return os.environ.get("USER", os.environ.get("USERNAME", "unknown"))


def get_platform() -> str:
    """Get the current platform."""
    return PlatformUtils.get_platform()


def is_windows() -> bool:
    """Check if running on Windows."""
    return PlatformUtils.is_windows()


def is_macos() -> bool:
    """Check if running on macOS."""
    return PlatformUtils.is_macos()


def is_linux() -> bool:
    """Check if running on Linux."""
    return PlatformUtils.is_linux()