"""
Configuration loader for Tite.

This module handles loading configuration from various sources
including files, environment variables, and default values.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml

from tite.config.defaults import DefaultConfig
from tite.exceptions import ConfigurationError


class ConfigLoader:
    """
    Loads configuration from various sources.
    
    This class handles loading configuration from files, environment
    variables, and merging with default values.
    
    Attributes:
        config_path: Path to configuration file
        env_prefix: Prefix for environment variables
        config: Loaded configuration
    """
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        env_prefix: str = "TITE_",
    ):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to configuration file
            env_prefix: Prefix for environment variables
        """
        self.config_path = config_path
        self.env_prefix = env_prefix
        self.config: Dict[str, Any] = {}
        
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from all sources.
        
        Returns:
            Dict[str, Any]: Loaded configuration
            
        Raises:
            ConfigurationError: If loading fails
        """
        # Start with defaults
        config = DefaultConfig.get_all()
        
        # Load from file if specified
        if self.config_path:
            file_config = self.load_from_file(self.config_path)
            config = self._deep_merge(config, file_config)
            
        # Load from environment
        env_config = self.load_from_env()
        config = self._deep_merge(config, env_config)
        
        self.config = config
        return config
        
    def load_from_file(self, path: Path) -> Dict[str, Any]:
        """
        Load configuration from a file.
        
        Args:
            path: Path to configuration file
            
        Returns:
            Dict[str, Any]: Loaded configuration
            
        Raises:
            ConfigurationError: If file cannot be loaded
        """
        if not path.exists():
            raise ConfigurationError(f"Configuration file not found: {path}")
            
        suffix = path.suffix.lower()
        
        try:
            if suffix == ".yaml" or suffix == ".yml":
                return self._load_yaml(path)
            elif suffix == ".json":
                return self._load_json(path)
            elif suffix == ".toml":
                return self._load_toml(path)
            else:
                raise ConfigurationError(f"Unsupported config format: {suffix}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load config from {path}: {e}")
            
    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """Load YAML file."""
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
            
    def _load_json(self, path: Path) -> Dict[str, Any]:
        """Load JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    def _load_toml(self, path: Path) -> Dict[str, Any]:
        """Load TOML file."""
        import tomllib
        with open(path, "rb") as f:
            return tomllib.load(f)
            
    def load_from_env(self) -> Dict[str, Any]:
        """
        Load configuration from environment variables.
        
        Returns:
            Dict[str, Any]: Configuration from environment
        """
        config = {}
        
        for key, value in os.environ.items():
            if key.startswith(self.env_prefix):
                # Remove prefix
                config_key = key[len(self.env_prefix):].lower()
                
                # Convert to nested dictionary
                parts = config_key.split("__")
                current = config
                
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                    
                # Parse value
                parsed_value = self._parse_env_value(value)
                current[parts[-1]] = parsed_value
                
        return config
        
    def _parse_env_value(self, value: str) -> Any:
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
            float_value = float(value)
            if "." in value:
                return float_value
        except ValueError:
            pass
            
        # List (comma-separated)
        if "," in value and not value.startswith("'"):
            return [item.strip() for item in value.split(",")]
            
        return value
        
    def load_from_string(self, content: str, format: str = "yaml") -> Dict[str, Any]:
        """
        Load configuration from a string.
        
        Args:
            content: Configuration content
            format: Format of the content
            
        Returns:
            Dict[str, Any]: Loaded configuration
            
        Raises:
            ConfigurationError: If content cannot be parsed
        """
        try:
            if format == "yaml":
                return yaml.safe_load(content) or {}
            elif format == "json":
                return json.loads(content)
            elif format == "toml":
                import tomllib
                return tomllib.loads(content)
            else:
                raise ConfigurationError(f"Unsupported format: {format}")
        except Exception as e:
            raise ConfigurationError(f"Failed to parse config: {e}")
            
    def reload(self) -> Dict[str, Any]:
        """
        Reload configuration.
        
        Returns:
            Dict[str, Any]: Reloaded configuration
        """
        return self.load()
        
    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Dot-separated key path
            default: Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        parts = key.split(".")
        current = self.config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
                
        return current
        
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries.
        
        Args:
            base: Base dictionary
            override: Override dictionary
            
        Returns:
            Dict[str, Any]: Merged dictionary
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
                
        return result