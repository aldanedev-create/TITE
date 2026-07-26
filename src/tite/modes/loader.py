"""
Mode loader for Tite.

This module handles loading mode definitions from various sources
including built-in modes, files, and packages.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from tite.modes.registry import ModeRegistry
from tite.exceptions import ConfigurationError, ModeNotFoundError


class ModeLoader:
    """
    Loads mode definitions from various sources.
    
    This class handles loading modes from built-in definitions,
    files, and external packages.
    
    Attributes:
        registry: Mode registry
    """
    
    def __init__(self, registry: Optional[ModeRegistry] = None):
        """
        Initialize the mode loader.
        
        Args:
            registry: Mode registry (creates new if None)
        """
        self.registry = registry or ModeRegistry()
        self.loaded_modes: Dict[str, Dict[str, Any]] = {}
        
    def load_mode(self, mode_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a mode by name.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            Optional[Dict[str, Any]]: Mode definition or None
        """
        # Check if already loaded
        if mode_name in self.loaded_modes:
            return self.loaded_modes[mode_name]
            
        # Check registry
        mode = self.registry.get_mode(mode_name)
        if mode:
            self.loaded_modes[mode_name] = mode
            return mode
            
        # Try to load from file
        mode_from_file = self.load_mode_from_file(mode_name)
        if mode_from_file:
            self.loaded_modes[mode_name] = mode_from_file
            return mode_from_file
            
        # Try to load from package
        mode_from_package = self.load_mode_from_package(mode_name)
        if mode_from_package:
            self.loaded_modes[mode_name] = mode_from_package
            return mode_from_package
            
        return None
        
    def load_mode_from_file(self, mode_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a mode from a file.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            Optional[Dict[str, Any]]: Mode definition or None
        """
        # Search in common locations
        search_paths = [
            Path.cwd() / ".tite" / "modes" / f"{mode_name}.yaml",
            Path.cwd() / ".tite" / "modes" / f"{mode_name}.yml",
            Path.cwd() / ".tite" / "modes" / f"{mode_name}.json",
            Path.cwd() / "modes" / f"{mode_name}.yaml",
            Path.cwd() / "modes" / f"{mode_name}.yml",
            Path.cwd() / "modes" / f"{mode_name}.json",
        ]
        
        for path in search_paths:
            if path.exists():
                try:
                    return self._parse_mode_file(path)
                except Exception:
                    continue
                    
        return None
        
    def load_mode_from_package(self, mode_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a mode from an installed package.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            Optional[Dict[str, Any]]: Mode definition or None
        """
        try:
            # Try to import the mode package
            import importlib
            package_name = f"tite_mode_{mode_name}"
            module = importlib.import_module(package_name)
            
            # Look for mode definition
            if hasattr(module, "MODE"):
                return module.MODE
                
            if hasattr(module, "get_mode"):
                return module.get_mode()
                
        except ImportError:
            pass
            
        return None
        
    def _parse_mode_file(self, path: Path) -> Dict[str, Any]:
        """
        Parse a mode definition file.
        
        Args:
            path: Path to the file
            
        Returns:
            Dict[str, Any]: Mode definition
            
        Raises:
            ConfigurationError: If file cannot be parsed
        """
        suffix = path.suffix.lower()
        
        try:
            if suffix == ".yaml" or suffix == ".yml":
                with open(path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            elif suffix == ".json":
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                raise ConfigurationError(f"Unsupported mode file format: {suffix}")
        except Exception as e:
            raise ConfigurationError(f"Failed to parse mode file {path}: {e}")
            
    def load_all_modes(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all available modes.
        
        Returns:
            Dict[str, Dict[str, Any]]: All mode definitions
        """
        # Load from registry
        for mode_name in self.registry.get_mode_names():
            self.load_mode(mode_name)
            
        # Load from files
        file_modes = self._find_mode_files()
        for mode_name, path in file_modes.items():
            try:
                mode = self._parse_mode_file(path)
                self.loaded_modes[mode_name] = mode
            except Exception:
                pass
                
        return self.loaded_modes
        
    def _find_mode_files(self) -> Dict[str, Path]:
        """
        Find all mode definition files.
        
        Returns:
            Dict[str, Path]: Mode name to file path mapping
        """
        mode_files = {}
        
        search_dirs = [
            Path.cwd() / ".tite" / "modes",
            Path.cwd() / "modes",
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
                
            for ext in [".yaml", ".yml", ".json"]:
                for path in search_dir.glob(f"*{ext}"):
                    mode_name = path.stem
                    if mode_name not in mode_files:
                        mode_files[mode_name] = path
                        
        return mode_files
        
    def reload_mode(self, mode_name: str) -> Optional[Dict[str, Any]]:
        """
        Reload a mode definition.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            Optional[Dict[str, Any]]: Reloaded mode definition
        """
        # Remove from cache
        if mode_name in self.loaded_modes:
            del self.loaded_modes[mode_name]
            
        # Reload
        return self.load_mode(mode_name)
        
    def get_mode_template(self, mode_name: str) -> Optional[str]:
        """
        Get the template name for a mode.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            Optional[str]: Template name or None
        """
        mode = self.load_mode(mode_name)
        if mode:
            return mode.get("template")
        return None
        
    def get_mode_packages(self, mode_name: str) -> List[str]:
        """
        Get the packages for a mode.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            List[str]: List of package names
        """
        mode = self.load_mode(mode_name)
        if mode:
            return mode.get("packages", [])
        return []