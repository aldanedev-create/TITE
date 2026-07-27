"""
Core configuration manager for Tite.

This module adapts tite.config.manager.ConfigManager to the interface
expected by the CLI commands and diagnostics (load_config/save_config/
create_config), while keeping the original load/save methods available
since some callers use those directly.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union

from tite.config.manager import ConfigManager as _BaseConfigManager
from tite.config.defaults import DefaultConfig


class ConfigManager(_BaseConfigManager):
    """
    Project configuration manager used by CLI commands.

    Extends the lower-level tite.config.manager.ConfigManager with the
    method names the rest of the codebase expects.
    """

    def __init__(self, project_path: Optional[Union[str, Path]] = None, **kwargs):
        super().__init__(project_path=Path(project_path) if project_path else None, **kwargs)

    def load_config(self) -> Dict[str, Any]:
        """Load and return the project configuration."""
        return self.load()

    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Persist the project configuration."""
        self.save(config)

    def create_config(self, config: Dict[str, Any]) -> None:
        """
        Set the in-memory configuration to be written out by save_config().

        This does not write to disk itself; call save_config() afterwards
        to persist it (matching how `tite init` uses these two methods).
        """
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config = config

    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Return the default configuration values."""
        return DefaultConfig.get_all()