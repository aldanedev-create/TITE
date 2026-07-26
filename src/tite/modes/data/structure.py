"""
Data Science structure definition.

This module defines the directory structure for Data Science projects.
"""

from typing import Dict, List


class DataStructure:
    """
    Data Science project structure.
    
    This class defines the directory and file structure for
    Data Science projects created with Tite.
    """
    
    @classmethod
    def get_structure(cls) -> Dict[str, List[str]]:
        """
        Get the directory structure.
        
        Returns:
            Dict[str, List[str]]: Directory structure
        """
        return {
            "directories": [
                "src",
                "data/raw",
                "data/processed",
                "data/interim",
                "data/external",
                "data/reference",
                "notebooks",
                "notebooks/exploratory",
                "notebooks/final",
                "reports",
                "reports/figures",
                "reports/tables",
                "tests",
                "tests/unit",
                "tests/integration",
                "scripts",
                "config",
            ],
            "files": [
                "src/__init__.py",
                "src/data_loader.py",
                "src/data_processor.py",
                "src/analyzer.py",
                "src/visualizer.py",
                "src/model.py",
                "src/pipeline.py",
                "src/utils.py",
                "src/main.py",
                "notebooks/exploratory/01_data_exploration.ipynb",
                "notebooks/exploratory/02_feature_engineering.ipynb",
                "notebooks/exploratory/03_modeling.ipynb",
                "notebooks/final/analysis_report.ipynb",
                "reports/final_report.md",
                "reports/methodology.md",
                "tests/unit/test_data_loader.py",
                "tests/unit/test_processor.py",
                "tests/unit/test_analyzer.py",
                "tests/integration/test_pipeline.py",
                "scripts/download_data.py",
                "scripts/run_pipeline.py",
                "config/settings.py",
                "config/data_sources.yaml",
                "requirements.txt",
                "environment.yml",
                "README.md",
                ".env.example",
                ".gitignore",
            ],
        }
        
    @classmethod
    def get_directories(cls) -> List[str]:
        """
        Get only the directories.
        
        Returns:
            List[str]: List of directory paths
        """
        return cls.get_structure()["directories"]
        
    @classmethod
    def get_files(cls) -> List[str]:
        """
        Get only the files.
        
        Returns:
            List[str]: List of file paths
        """
        return cls.get_structure()["files"]
        
    @classmethod
    def get_source_files(cls) -> List[str]:
        """
        Get Python source files.
        
        Returns:
            List[str]: List of Python file paths
        """
        return [f for f in cls.get_files() if f.endswith(".py")]
        
    @classmethod
    def get_notebooks(cls) -> List[str]:
        """
        Get Jupyter notebook files.
        
        Returns:
            List[str]: List of notebook file paths
        """
        return [f for f in cls.get_files() if f.endswith(".ipynb")]
        
    @classmethod
    def get_config_files(cls) -> List[str]:
        """
        Get configuration files.
        
        Returns:
            List[str]: List of config file paths
        """
        return [
            "config/settings.py",
            "config/data_sources.yaml",
            "requirements.txt",
            "environment.yml",
            "README.md",
            ".env.example",
            ".gitignore",
        ]