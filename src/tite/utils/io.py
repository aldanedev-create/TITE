"""
IO utilities for Tite.

This module provides input/output utilities for reading and writing
files in various formats.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml


def read_file(path: Path, encoding: str = "utf-8") -> str:
    """
    Read a text file.
    
    Args:
        path: File path
        encoding: File encoding
        
    Returns:
        str: File content
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding=encoding)


def write_file(path: Path, content: str, encoding: str = "utf-8") -> None:
    """
    Write a text file.
    
    Args:
        path: File path
        content: Content to write
        encoding: File encoding
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)


def read_bytes(path: Path) -> bytes:
    """
    Read a binary file.
    
    Args:
        path: File path
        
    Returns:
        bytes: File content
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_bytes()


def write_bytes(path: Path, content: bytes) -> None:
    """
    Write a binary file.
    
    Args:
        path: File path
        content: Content to write
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def read_json(path: Path) -> Any:
    """
    Read a JSON file.
    
    Args:
        path: File path
        
    Returns:
        Any: Parsed JSON data
    """
    content = read_file(path)
    return json.loads(content)


def write_json(path: Path, data: Any, indent: int = 2) -> None:
    """
    Write a JSON file.
    
    Args:
        path: File path
        data: Data to write
        indent: JSON indentation
    """
    content = json.dumps(data, indent=indent, ensure_ascii=False)
    write_file(path, content)


def read_yaml(path: Path) -> Any:
    """
    Read a YAML file.
    
    Args:
        path: File path
        
    Returns:
        Any: Parsed YAML data
    """
    content = read_file(path)
    return yaml.safe_load(content)


def write_yaml(path: Path, data: Any) -> None:
    """
    Write a YAML file.
    
    Args:
        path: File path
        data: Data to write
    """
    content = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    write_file(path, content)


def read_toml(path: Path) -> Dict[str, Any]:
    """
    Read a TOML file.
    
    Args:
        path: File path
        
    Returns:
        Dict[str, Any]: Parsed TOML data
    """
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib
        
    content = read_bytes(path)
    return tomllib.loads(content.decode("utf-8"))


def write_toml(path: Path, data: Dict[str, Any]) -> None:
    """
    Write a TOML file.
    
    Args:
        path: File path
        data: Data to write
    """
    try:
        import tomli_w
    except ImportError:
        raise ImportError("tomli_w is required for writing TOML files")
        
    content = tomli_w.dumps(data)
    write_file(path, content)


def read_env(path: Path) -> Dict[str, str]:
    """
    Read a .env file.
    
    Args:
        path: File path
        
    Returns:
        Dict[str, str]: Environment variables
    """
    env_vars = {}
    
    if not path.exists():
        return env_vars
        
    for line in read_file(path).split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        if "=" in line:
            key, value = line.split("=", 1)
            env_vars[key.strip()] = value.strip().strip('"').strip("'")
            
    return env_vars


def write_env(path: Path, data: Dict[str, str]) -> None:
    """
    Write a .env file.
    
    Args:
        path: File path
        data: Environment variables
    """
    lines = []
    for key, value in data.items():
        lines.append(f"{key}={value}")
    write_file(path, "\n".join(lines))