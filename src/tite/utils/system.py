"""
System utilities for Tite.

This module provides system information and utility functions.
"""
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class SystemUtils:
    """
    Utility class for system operations.
    
    This class provides static methods for getting system information,
    running commands, and managing system resources.
    """
    
    @staticmethod
    def get_os() -> str:
        """
        Get the operating system name.
        
        Returns:
            str: OS name (windows, darwin, linux, etc.)
        """
        return sys.platform
        
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
    def get_python_version() -> str:
        """
        Get Python version.
        
        Returns:
            str: Python version string
        """
        return sys.version.split()[0]
        
    @staticmethod
    def get_python_implementation() -> str:
        """
        Get Python implementation.
        
        Returns:
            str: Python implementation (CPython, PyPy, etc.)
        """
        return platform.python_implementation()
        
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """
        Get system information.
        
        Returns:
            Dict[str, str]: System information
        """
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version.split()[0],
            "python_implementation": platform.python_implementation(),
            "platform": sys.platform,
        }
        
    @staticmethod
    def run_command(
        cmd: List[str],
        cwd: Optional[Path] = None,
        capture_output: bool = True,
        check: bool = False,
    ) -> Tuple[int, str, str]:
        """
        Run a command.
        
        Args:
            cmd: Command and arguments
            cwd: Working directory
            capture_output: Whether to capture output
            check: Whether to check return code
            
        Returns:
            Tuple[int, str, str]: (return_code, stdout, stderr)
        """
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                check=check,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr
            
    @staticmethod
    def get_env_vars(prefix: Optional[str] = None) -> Dict[str, str]:
        """
        Get environment variables.
        
        Args:
            prefix: Filter by prefix
            
        Returns:
            Dict[str, str]: Environment variables
        """
        if prefix:
            return {k: v for k, v in os.environ.items() if k.startswith(prefix)}
        return dict(os.environ)
        
    @staticmethod
    def set_env_var(key: str, value: str) -> None:
        """
        Set an environment variable.
        
        Args:
            key: Variable name
            value: Variable value
        """
        os.environ[key] = value
        
    @staticmethod
    def get_cpu_count() -> int:
        """
        Get the number of CPU cores.
        
        Returns:
            int: Number of CPU cores
        """
        return os.cpu_count() or 1
        
    @staticmethod
    def get_memory_info() -> Dict[str, int]:
        """
        Get memory information.
        
        Returns:
            Dict[str, int]: Memory information
        """
        try:
            import psutil
            mem = psutil.virtual_memory()
            return {
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
                "percent": mem.percent,
            }
        except ImportError:
            return {}
            
    @staticmethod
    def get_disk_usage(path: Path) -> Dict[str, int]:
        """
        Get disk usage for a path.
        
        Args:
            path: Path to check
            
        Returns:
            Dict[str, int]: Disk usage information
        """
        try:
            import shutil
            usage = shutil.disk_usage(path)
            return {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": (usage.used / usage.total * 100),
            }
        except Exception:
            return {}
            
    @staticmethod
    def is_installed(command: str) -> bool:
        """
        Check if a command is installed.
        
        Args:
            command: Command name
            
        Returns:
            bool: True if command is installed
        """
        if SystemUtils.is_windows():
            return shutil.which(command) is not None
        else:
            result = SystemUtils.run_command(["which", command])
            return result[0] == 0


def get_system_info() -> Dict[str, str]:
    """Get system information."""
    return SystemUtils.get_system_info()