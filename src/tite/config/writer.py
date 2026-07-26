"""
Configuration writer for Tite.

This module handles writing configuration to various formats
including YAML, JSON, and TOML.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from tite.exceptions import ConfigurationError


class ConfigWriter:
    """
    Writes configuration to files.
    
    This class handles writing configuration to files in various
    formats with proper formatting and structure.
    """
    
    def __init__(self):
        """Initialize the configuration writer."""
        pass
        
    def write(
        self,
        path: Path,
        config: Dict[str, Any],
        format: Optional[str] = None,
    ) -> None:
        """
        Write configuration to a file.
        
        Args:
            path: Path to write to
            config: Configuration to write
            format: Format to use (auto-detected from extension if None)
            
        Raises:
            ConfigurationError: If writing fails
        """
        # Auto-detect format
        if format is None:
            suffix = path.suffix.lower()
            if suffix == ".yaml" or suffix == ".yml":
                format = "yaml"
            elif suffix == ".json":
                format = "json"
            elif suffix == ".toml":
                format = "toml"
            else:
                format = "yaml"
                
        try:
            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write based on format
            if format == "yaml":
                self._write_yaml(path, config)
            elif format == "json":
                self._write_json(path, config)
            elif format == "toml":
                self._write_toml(path, config)
            else:
                raise ConfigurationError(f"Unsupported format: {format}")
                
        except Exception as e:
            raise ConfigurationError(f"Failed to write config to {path}: {e}")
            
    def _write_yaml(self, path: Path, config: Dict[str, Any]) -> None:
        """
        Write YAML configuration.
        
        Args:
            path: Path to write to
            config: Configuration to write
        """
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(
                config,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )
            
    def _write_json(self, path: Path, config: Dict[str, Any]) -> None:
        """
        Write JSON configuration.
        
        Args:
            path: Path to write to
            config: Configuration to write
        """
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                config,
                f,
                indent=2,
                ensure_ascii=False,
                sort_keys=False,
            )
            
    def _write_toml(self, path: Path, config: Dict[str, Any]) -> None:
        """
        Write TOML configuration.
        
        Args:
            path: Path to write to
            config: Configuration to write
        """
        import tomli_w
        
        with open(path, "wb") as f:
            tomli_w.dump(config, f)
            
    def write_string(
        self,
        config: Dict[str, Any],
        format: str = "yaml",
    ) -> str:
        """
        Write configuration to a string.
        
        Args:
            config: Configuration to write
            format: Format to use
            
        Returns:
            str: Configuration string
            
        Raises:
            ConfigurationError: If writing fails
        """
        try:
            if format == "yaml":
                return yaml.dump(config, default_flow_style=False, allow_unicode=True)
            elif format == "json":
                return json.dumps(config, indent=2, ensure_ascii=False)
            elif format == "toml":
                import tomli_w
                return tomli_w.dumps(config)
            else:
                raise ConfigurationError(f"Unsupported format: {format}")
        except Exception as e:
            raise ConfigurationError(f"Failed to write config to string: {e}")
            
    def write_to_project(
        self,
        project_path: Path,
        config: Dict[str, Any],
        format: str = "toml",
    ) -> None:
        """
        Write configuration to a project.
        
        Args:
            project_path: Path to the project
            config: Configuration to write
            format: Format to use
        """
        config_path = project_path / ".tite" / f"tite.{format}"
        self.write(config_path, config, format)
        
    def merge_and_write(
        self,
        path: Path,
        config: Dict[str, Any],
        format: Optional[str] = None,
    ) -> None:
        """
        Merge with existing configuration and write.
        
        Args:
            path: Path to write to
            config: Configuration to merge
            format: Format to use
            
        Raises:
            ConfigurationError: If reading/writing fails
        """
        # Try to read existing config
        existing = {}
        if path.exists():
            from tite.config.loader import ConfigLoader
            loader = ConfigLoader()
            try:
                existing = loader.load_from_file(path)
            except Exception:
                pass
                
        # Merge configurations
        merged = self._deep_merge(existing, config)
        
        # Write merged config
        self.write(path, merged, format)
        
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
        
    def create_default_config(self, project_name: str) -> Dict[str, Any]:
        """
        Create a default configuration for a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Dict[str, Any]: Default configuration
        """
        from tite.config.defaults import DefaultConfig
        
        config = DefaultConfig.get_all()
        config["project"]["name"] = project_name
        return config