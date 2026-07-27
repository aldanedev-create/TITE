"""
Application class for the desktop application.

This module provides the main application class that manages
the application lifecycle and state.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Application:
    """
    Main application class.
    
    This class manages the application state, configuration,
    and provides access to application services.
    """
    
    def __init__(self):
        """
        Initialize the application.
        """
        self.config: Dict[str, Any] = {}
        self.data: Dict[str, Any] = {}
        self._initialized = False
        
        # Load configuration
        self._load_config()
        
        logger.info("Application initialized")
    
    def _load_config(self) -> None:
        """
        Load application configuration.
        """
        # Load from environment
        self.config.update({
            "debug": os.getenv("DEBUG", "false").lower() == "true",
            "theme": os.getenv("THEME", "dark"),
            "language": os.getenv("LANGUAGE", "en"),
        })
        
        # Load from config file
        config_path = self._get_config_path()
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
                logger.info(f"Loaded config from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}")
        
        # Load user data
        data_path = self._get_data_path()
        if data_path.exists():
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                logger.info(f"Loaded data from {data_path}")
            except Exception as e:
                logger.warning(f"Failed to load data: {e}")
    
    def _get_config_path(self) -> Path:
        """
        Get the configuration file path.
        
        Returns:
            Path: Configuration file path
        """
        # Platform-specific config directories
        if os.name == "nt":  # Windows
            base_dir = Path(os.environ.get("APPDATA", "~")) / "{{ project_name }}"
        elif os.name == "posix":  # Linux/macOS
            base_dir = Path.home() / ".config" / "{{ project_name }}"
        else:
            base_dir = Path.cwd() / ".config"
        
        return base_dir / "config.json"
    
    def _get_data_path(self) -> Path:
        """
        Get the data file path.
        
        Returns:
            Path: Data file path
        """
        if os.name == "nt":  # Windows
            base_dir = Path(os.environ.get("APPDATA", "~")) / "{{ project_name }}"
        elif os.name == "posix":  # Linux/macOS
            base_dir = Path.home() / ".local" / "share" / "{{ project_name }}"
        else:
            base_dir = Path.cwd() / ".data"
        
        return base_dir / "data.json"
    
    def save_config(self) -> None:
        """
        Save application configuration.
        """
        config_path = self._get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved config to {config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def save_data(self) -> None:
        """
        Save application data.
        """
        data_path = self._get_data_path()
        data_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved data to {data_path}")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
        self.save_config()
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """
        Get a data value.
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Any: Data value
        """
        return self.data.get(key, default)
    
    def set_data(self, key: str, value: Any) -> None:
        """
        Set a data value.
        
        Args:
            key: Data key
            value: Data value
        """
        self.data[key] = value
        self.save_data()
    
    def quit(self) -> None:
        """
        Quit the application.
        """
        logger.info("Application quitting...")
        self.save_config()
        self.save_data()


# Global application instance
_app: Optional[Application] = None


def get_app() -> Application:
    """
    Get the global application instance.
    
    Returns:
        Application: Application instance
    """
    global _app
    if _app is None:
        _app = Application()
    return _app