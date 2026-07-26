"""
Configuration manager for Tite.

This module provides a high-level interface for managing configuration
including loading, saving, validation, and access.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union

from tite.config.defaults import DefaultConfig
from tite.config.loader import ConfigLoader
from tite.config.schema import ConfigSchema, ConfigValidationError
from tite.config.writer import ConfigWriter
from tite.exceptions import ConfigurationError


class ConfigManager:
    """
    Manages configuration for Tite projects.
    
    This class provides a unified interface for configuration management
    including loading, saving, validation, and access.
    
    Attributes:
        config_path: Path to configuration file
        loader: Configuration loader
        writer: Configuration writer
        schema: Configuration schema
        config: Current configuration
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        config_path: Optional[Path] = None,
        env_prefix: str = "TITE_",
    ):
        """
        Initialize the configuration manager.
        
        Args:
            project_path: Path to the project directory
            config_path: Path to configuration file
            env_prefix: Prefix for environment variables
        """
        self.project_path = Path(project_path) if project_path else Path.cwd()
        
        if config_path:
            self.config_path = config_path
        else:
            self.config_path = self.project_path / ".tite" / "tite.toml"
            
        self.env_prefix = env_prefix
        self.loader = ConfigLoader(self.config_path, env_prefix)
        self.writer = ConfigWriter()
        self.schema = ConfigSchema()
        self.config: Dict[str, Any] = {}
        
    def load(self) -> Dict[str, Any]:
        """
        Load configuration.
        
        Returns:
            Dict[str, Any]: Loaded configuration
            
        Raises:
            ConfigurationError: If loading fails
        """
        try:
            self.config = self.loader.load()
            
            # Validate configuration
            if not self.schema.validate(self.config):
                errors = self.schema.get_errors()
                raise ConfigValidationError("\n".join(errors))
                
            return self.config
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")
            
    def save(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Save configuration.
        
        Args:
            config: Configuration to save (uses current if None)
            
        Raises:
            ConfigurationError: If saving fails
        """
        if config is not None:
            self.config = config
            
        if not self.config:
            self.config = self.loader.load()
            
        # Validate before saving
        if not self.schema.validate(self.config):
            errors = self.schema.get_errors()
            raise ConfigValidationError("\n".join(errors))
            
        try:
            self.writer.write(self.config_path, self.config)
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Dot-separated key path
            default: Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        if not self.config:
            self.load()
            
        return self.loader.get_value(key, default)
        
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Dot-separated key path
            value: Value to set
        """
        if not self.config:
            self.load()
            
        parts = key.split(".")
        current = self.config
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
            
        current[parts[-1]] = value
        
    def reset(self, key: Optional[str] = None) -> None:
        """
        Reset configuration to defaults.
        
        Args:
            key: Specific key to reset (resets all if None)
        """
        if key:
            # Reset specific key
            default_value = DefaultConfig.get_value(key)
            self.set(key, default_value)
        else:
            # Reset all
            self.config = DefaultConfig.get_all()
            
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get a configuration section.
        
        Args:
            section: Section name
            
        Returns:
            Dict[str, Any]: Section configuration
        """
        return self.get(section, {})
        
    def get_project_config(self) -> Dict[str, Any]:
        """
        Get project configuration.
        
        Returns:
            Dict[str, Any]: Project configuration
        """
        return self.get_section("project")
        
    def get_dev_config(self) -> Dict[str, Any]:
        """
        Get development configuration.
        
        Returns:
            Dict[str, Any]: Development configuration
        """
        return self.get_section("dev")
        
    def get_watcher_config(self) -> Dict[str, Any]:
        """
        Get watcher configuration.
        
        Returns:
            Dict[str, Any]: Watcher configuration
        """
        return self.get_section("watcher")
        
    def get_clean_config(self) -> Dict[str, Any]:
        """
        Get clean configuration.
        
        Returns:
            Dict[str, Any]: Clean configuration
        """
        return self.get_section("clean")
        
    def get_git_config(self) -> Dict[str, Any]:
        """
        Get Git configuration.
        
        Returns:
            Dict[str, Any]: Git configuration
        """
        return self.get_section("git")
        
    def get_testing_config(self) -> Dict[str, Any]:
        """
        Get testing configuration.
        
        Returns:
            Dict[str, Any]: Testing configuration
        """
        return self.get_section("testing")
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        if not self.config:
            self.load()
        return self.config
        
    def merge(self, config: Dict[str, Any]) -> None:
        """
        Merge configuration with current config.
        
        Args:
            config: Configuration to merge
        """
        if not self.config:
            self.load()
            
        self.config = DefaultConfig._deep_merge(self.config, config)
        
    def validate(self) -> bool:
        """
        Validate configuration.
        
        Returns:
            bool: True if valid
            
        Raises:
            ConfigValidationError: If validation fails
        """
        if not self.config:
            self.load()
            
        return self.schema.validate(self.config)