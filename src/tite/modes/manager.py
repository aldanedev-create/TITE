"""
Mode manager for Tite.

This module handles the creation, management, and execution of project modes.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from tite.modes.registry import ModeRegistry
from tite.modes.loader import ModeLoader
from tite.modes.validator import ModeValidator
from tite.core.bootstrap import BootstrapManager
from tite.core.project import ProjectManager
from tite.exceptions import ModeNotFoundError, ConfigurationError


class ModeManager:
    """
    Manages project modes.
    
    This class handles loading, validating, and executing modes for
    project creation and management.
    
    Attributes:
        registry: Mode registry
        loader: Mode loader
        validator: Mode validator
    """
    
    def __init__(self):
        """Initialize the mode manager."""
        self.registry = ModeRegistry()
        self.loader = ModeLoader(self.registry)
        self.validator = ModeValidator()
        
    def create_project(
        self,
        mode_name: str,
        project_name: str,
        project_path: Path,
        force: bool = False,
        variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a project using a specific mode.
        
        Args:
            mode_name: Name of the mode to use
            project_name: Name of the project
            project_path: Path where the project will be created
            force: Whether to force overwrite
            variables: Variables for template substitution
            
        Returns:
            Dict[str, Any]: Creation results
            
        Raises:
            ModeNotFoundError: If mode is not found
            ConfigurationError: If mode configuration is invalid
        """
        # Load mode
        mode = self.loader.load_mode(mode_name)
        if not mode:
            raise ModeNotFoundError(mode_name)
            
        # Validate mode
        self.validator.validate(mode)
        
        # Get mode configuration
        mode_config = self._get_mode_config(mode, variables or {})
        
        # Create project
        bootstrap = BootstrapManager(
            project_name=project_name,
            project_path=project_path,
            template=mode_config.get("template", "default"),
            mode=mode_name,
            force=force,
        )
        
        # Override structure if mode provides it
        if "structure" in mode_config:
            bootstrap.structure = mode_config["structure"]
            
        # Override files if mode provides them
        if "files" in mode_config:
            bootstrap.files = mode_config["files"]
            
        # Create the project
        results = {
            "mode": mode_name,
            "project": project_name,
            "path": str(project_path),
            "created": [],
            "packages_installed": [],
        }
        
        # Create structure
        bootstrap.create_structure()
        results["created"].extend(bootstrap.created_dirs)
        
        # Generate files
        bootstrap.generate_files()
        results["created"].extend(bootstrap.created_files)
        
        # Create virtual environment
        bootstrap.create_venv()
        
        # Install mode packages
        packages = mode_config.get("packages", [])
        if packages:
            bootstrap.install_packages(packages)
            results["packages_installed"] = packages
            
        # Initialize Git
        bootstrap.init_git()
        
        # Run post-hooks
        bootstrap.run_post_hooks()
        
        return results
        
    def list_modes(self) -> List[Dict[str, Any]]:
        """
        List all available modes.
        
        Returns:
            List[Dict[str, Any]]: List of mode information
        """
        return self.registry.list_modes()
        
    def get_mode_info(self, mode_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific mode.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            Optional[Dict[str, Any]]: Mode information or None
        """
        return self.registry.get_mode_info(mode_name)
        
    def _get_mode_config(
        self,
        mode: Dict[str, Any],
        variables: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Get mode configuration with variables applied.
        
        Args:
            mode: Mode definition
            variables: Variables for substitution
            
        Returns:
            Dict[str, Any]: Mode configuration
        """
        config = {
            "template": mode.get("template", "default"),
            "packages": mode.get("packages", []),
            "structure": mode.get("structure", {}),
            "files": mode.get("files", {}),
            "commands": mode.get("commands", []),
            "variables": {**mode.get("variables", {}), **variables},
        }
        
        return config
        
    def get_mode_packages(self, mode_name: str) -> List[str]:
        """
        Get packages for a specific mode.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            List[str]: List of package names
            
        Raises:
            ModeNotFoundError: If mode is not found
        """
        mode = self.loader.load_mode(mode_name)
        if not mode:
            raise ModeNotFoundError(mode_name)
        return mode.get("packages", [])
        
    def get_mode_structure(self, mode_name: str) -> Dict[str, List[str]]:
        """
        Get directory structure for a specific mode.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            Dict[str, List[str]]: Directory structure
            
        Raises:
            ModeNotFoundError: If mode is not found
        """
        mode = self.loader.load_mode(mode_name)
        if not mode:
            raise ModeNotFoundError(mode_name)
        return mode.get("structure", {})
        
    def get_mode_files(self, mode_name: str) -> Dict[str, str]:
        """
        Get files for a specific mode.
        
        Args:
            mode_name: Name of the mode
            
        Returns:
            Dict[str, str]: File paths to content
            
        Raises:
            ModeNotFoundError: If mode is not found
        """
        mode = self.loader.load_mode(mode_name)
        if not mode:
            raise ModeNotFoundError(mode_name)
        return mode.get("files", {})