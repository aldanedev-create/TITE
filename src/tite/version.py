"""
Version management for Tite.

This module provides version information and utilities for the Tite package.
"""

import importlib.metadata
import sys
from typing import Optional, Tuple

# Version string
__version__ = "0.1.0"


def get_version() -> str:
    """
    Get the current version of Tite.
    
    Returns:
        str: Version string
        
    Examples:
        >>> get_version()
        '0.1.0'
    """
    return __version__


def get_python_version() -> Tuple[int, int, int]:
    """
    Get the current Python version.
    
    Returns:
        Tuple[int, int, int]: (major, minor, micro) version
        
    Examples:
        >>> get_python_version()
        (3, 12, 0)
    """
    return sys.version_info[:3]


def get_python_version_string() -> str:
    """
    Get the current Python version as a string.
    
    Returns:
        str: Python version string
        
    Examples:
        >>> get_python_version_string()
        '3.12.0'
    """
    major, minor, micro = get_python_version()
    return f"{major}.{minor}.{micro}"


def get_system_info() -> dict:
    """
    Get system information.
    
    Returns:
        dict: System information including Python version, platform, etc.
        
    Examples:
        >>> get_system_info()
        {
            'python_version': '3.12.0',
            'platform': 'linux',
            'architecture': '64bit',
            'implementation': 'CPython',
        }
    """
    import platform
    
    return {
        "python_version": get_python_version_string(),
        "platform": platform.system().lower(),
        "platform_release": platform.release(),
        "architecture": platform.machine(),
        "implementation": platform.python_implementation(),
    }


def get_package_version(package_name: str) -> Optional[str]:
    """
    Get the version of an installed package.
    
    Args:
        package_name: Name of the package
        
    Returns:
        Optional[str]: Version string or None if not found
        
    Examples:
        >>> get_package_version("click")
        '8.1.7'
    """
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return None


def check_version_compatibility(
    min_version: str = "3.9.0",
    max_version: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    Check if the current Python version is compatible.
    
    Args:
        min_version: Minimum required version
        max_version: Maximum allowed version (optional)
        
    Returns:
        Tuple[bool, str]: (is_compatible, message)
        
    Examples:
        >>> check_version_compatibility("3.9.0")
        (True, "Python version 3.12.0 is compatible")
    """
    from packaging import version
    
    current = get_python_version_string()
    current_parsed = version.parse(current)
    
    min_parsed = version.parse(min_version)
    if current_parsed < min_parsed:
        return False, f"Python {min_version}+ is required (current: {current})"
    
    if max_version:
        max_parsed = version.parse(max_version)
        if current_parsed > max_parsed:
            return False, f"Python {max_version} or lower is required (current: {current})"
    
    return True, f"Python version {current} is compatible"


def format_version_info() -> str:
    """
    Format version information for display.
    
    Returns:
        str: Formatted version info string
        
    Examples:
        >>> print(format_version_info())
        Tite: 0.1.0
        Python: 3.12.0
        Platform: linux
        Implementation: CPython
        Architecture: x86_64
    """
    info = get_system_info()
    
    lines = [
        f"Tite: {get_version()}",
        f"Python: {info['python_version']}",
        f"Platform: {info['platform']}",
        f"Implementation: {info['implementation']}",
        f"Architecture: {info['architecture']}",
    ]
    
    return "\n".join(lines)