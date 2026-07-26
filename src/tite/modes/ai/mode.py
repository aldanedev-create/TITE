"""
AI/ML mode definition.

This module defines the AI/Machine Learning mode for Tite, including
its configuration, structure, and default packages.
"""

from typing import Any, Dict, List

from tite.modes.ai.structure import AIStructure
from tite.modes.ai.config import AIConfig
from tite.modes.ai.packages import AI_PACKAGES


class AIMode:
    """
    AI/ML mode for Tite.
    
    This class defines the AI/ML mode configuration including
    structure, packages, and default settings for AI projects.
    """
    
    name = "ai"
    display_name = "Artificial Intelligence"
    description = "AI and machine learning project with OpenAI, LangChain, and PyTorch"
    template = "ai"
    
    @classmethod
    def get_structure(cls) -> Dict[str, List[str]]:
        """
        Get the directory structure for the AI mode.
        
        Returns:
            Dict[str, List[str]]: Directory structure
        """
        return AIStructure.get_structure()
        
    @classmethod
    def get_packages(cls) -> List[str]:
        """
        Get the default packages for the AI mode.
        
        Returns:
            List[str]: List of package names
        """
        return AI_PACKAGES
        
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """
        Get the default configuration for the AI mode.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return AIConfig.get_default_config()
        
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