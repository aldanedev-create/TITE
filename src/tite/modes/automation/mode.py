"""
Automation mode definition.

This module defines the Automation mode for Tite, including
its configuration, structure, and default packages.
"""

from typing import Any, Dict, List

from tite.modes.automation.structure import AutomationStructure
from tite.modes.automation.config import AutomationConfig
from tite.modes.automation.packages import AUTOMATION_PACKAGES


class AutomationMode:
    """
    Automation mode for Tite.
    
    This class defines the Automation mode configuration including
    structure, packages, and default settings for automation projects.
    """
    
    name = "automation"
    display_name = "Automation"
    description = "Automation and scripting project with task scheduling and logging"
    template = "automation"
    
    @classmethod
    def get_structure(cls) -> Dict[str, List[str]]:
        """
        Get the directory structure for the automation mode.
        
        Returns:
            Dict[str, List[str]]: Directory structure
        """
        return AutomationStructure.get_structure()
        
    @classmethod
    def get_packages(cls) -> List[str]:
        """
        Get the default packages for the automation mode.
        
        Returns:
            List[str]: List of package names
        """
        return AUTOMATION_PACKAGES
        
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """
        Get the default configuration for the automation mode.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return AutomationConfig.get_default_config()
        
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """
        Convert the mode to a dictionary.
        
        Returns:
            Dict[str, Any]: Mode definition
        """
        return {
            "name": cls.name,
            "display_name": cls.display_name,
            "description": cls.description,
            "template": cls.template,
            "packages": cls.get_packages(),
            "structure": cls.get_structure(),
            "config": cls.get_config(),
        }