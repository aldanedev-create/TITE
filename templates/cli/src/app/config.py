"""
Configuration management for the CLI application.

This module handles loading and managing configuration from
files and environment variables.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv


class Config:
    """
    Application configuration.
    
    Attributes:
        data: Configuration data dictionary
        config_path: Path to the configuration file
    """
    
    def __init__(self, data: Optional[Dict[str, Any]] = None, config_path: Optional[Path] = None):
        """
        Initialize the configuration.
        
        Args:
            data: Configuration data
            config_path: Path to configuration file
        """
        self.data = data or {}
        self.config_path = config_path
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.data[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict[str, Any]: Configuration data
        """
        return self.data
    
    def save(self) -> None:
        """Save configuration to file."""
        if self.config_path:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)


def load_config(
    config_path: Optional[str] = None,
    env_prefix: str = "APP_",
) -> Config:
    """
    Load configuration from various sources.
    
    Args:
        config_path: Path to configuration file
        env_prefix: Prefix for environment variables
        
    Returns:
        Config: Loaded configuration
    """
    data = {}
    
    # Load from environment variables
    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            config_key = key[len(env_prefix):].lower()
            data[config_key] = _parse_env_value(value)
    
    # Load from config file
    if config_path:
        path = Path(config_path)
        if path.exists():
            file_data = _load_file_config(path)
            data.update(file_data)
    
    # Load default config
    default_data = _get_default_config()
    data = {**default_data, **data}
    
    return Config(data, Path(config_path) if config_path else None)


def _load_file_config(path: Path) -> Dict[str, Any]:
    """
    Load configuration from a file.
    
    Args:
        path: Path to configuration file
        
    Returns:
        Dict[str, Any]: Loaded configuration
    """
    suffix = path.suffix.lower()
    
    if suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    elif suffix in (".yaml", ".yml"):
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    elif suffix == ".toml":
        import tomllib
        with open(path, "rb") as f:
            return tomllib.load(f)
    else:
        # Try to parse as JSON
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}


def _parse_env_value(value: str) -> Any:
    """
    Parse environment variable value.
    
    Args:
        value: String value
        
    Returns:
        Any: Parsed value
    """
    # Boolean
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    
    # Integer
    try:
        if value.isdigit():
            return int(value)
    except ValueError:
        pass
    
    # Float
    try:
        if "." in value:
            return float(value)
    except ValueError:
        pass
    
    # List (comma-separated)
    if "," in value and not value.startswith("'"):
        return [item.strip() for item in value.split(",")]
    
    return value


def _get_default_config() -> Dict[str, Any]:
    """
    Get default configuration.
    
    Returns:
        Dict[str, Any]: Default configuration
    """
    return {
        "name": "{{ project_name }}",
        "version": "0.1.0",
        "debug": False,
        "log_level": "INFO",
        "greeting": "Welcome to {{ project_name }}!",
    }


def get_config_path() -> Path:
    """
    Get the default configuration path.
    
    Returns:
        Path: Default configuration path
    """
    # Check current directory
    current = Path.cwd()
    for path in [
        current / "config.json",
        current / "config.yaml",
        current / "config.yml",
        current / "config.toml",
        current / ".config.json",
    ]:
        if path.exists():
            return path
    
    # Check home directory
    home = Path.home()
    config_dir = home / ".config" / "{{ project_name }}"
    if config_dir.exists():
        for path in [
            config_dir / "config.json",
            config_dir / "config.yaml",
        ]:
            if path.exists():
                return path
    
    # Default path
    return Path.cwd() / ".config" / "{{ project_name }}" / "config.json"