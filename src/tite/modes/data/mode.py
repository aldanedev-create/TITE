"""
Data Science mode definition.

This module defines the Data Science mode for Tite, including
its configuration, structure, and default packages.
"""

from typing import Any, Dict, List

from tite.modes.data.structure import DataStructure
from tite.modes.data.config import DataConfig
from tite.modes.data.packages import DATA_PACKAGES


class DataMode:
    """
    Data Science mode for Tite.
    
    This class defines the Data Science mode configuration including
    structure, packages, and default settings.
    """
    
    name = "data"
    display_name = "Data Science"
    description = "Data science and analytics project with pandas, numpy, and jupyter"
    template = "data"
    
    @classmethod
    def get_structure(cls) -> Dict[str, List[str]]:
        """
        Get the directory structure for the data science mode.
        
        Returns:
            Dict[str, List[str]]: Directory structure
        """
        return DataStructure.get_structure()
        
    @classmethod
    def get_packages(cls) -> List[str]:
        """
        Get the default packages for the data science mode.
        
        Returns:
            List[str]: List of package names
        """
        return DATA_PACKAGES
        
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """
        Get the default configuration for the data science mode.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return DataConfig.get_default_config()
        
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