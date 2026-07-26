"""
Data Science configuration.

This module defines the configuration for Data Science projects.
"""

from typing import Any, Dict


class DataConfig:
    """
    Data Science project configuration.
    
    This class provides default configuration for Data Science projects.
    """
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get the default configuration.
        
        Returns:
            Dict[str, Any]: Default configuration dictionary
        """
        return {
            "project": {
                "name": "",
                "version": "0.1.0",
                "description": "Data science project",
                "python_version": ">=3.9",
                "author": "",
                "email": "",
            },
            "data": {
                "raw_path": "data/raw",
                "processed_path": "data/processed",
                "interim_path": "data/interim",
                "external_path": "data/external",
                "reference_path": "data/reference",
                "formats": ["csv", "parquet", "feather", "hdf5"],
                "compression": "gzip",
            },
            "analysis": {
                "eda": True,
                "statistical_tests": True,
                "correlation_analysis": True,
                "outlier_detection": True,
                "feature_engineering": True,
            },
            "visualization": {
                "theme": "dark",
                "figure_size": [12, 8],
                "dpi": 150,
                "save_format": "png",
                "interactive": True,
            },
            "modeling": {
                "test_size": 0.2,
                "random_state": 42,
                "cross_validation": 5,
                "scoring": "accuracy",
                "hyperparameter_tuning": True,
            },
            "reporting": {
                "format": "markdown",
                "include_code": True,
                "include_plots": True,
                "include_tables": True,
                "export_to_pdf": False,
            },
            "testing": {
                "test_path": "tests",
                "coverage_threshold": 80,
                "dataset_validation": True,
                "model_validation": True,
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "logs/data_pipeline.log",
                "console": True,
            },
        }
        
    @classmethod
    def get_data_paths(cls) -> Dict[str, str]:
        """
        Get data directory paths.
        
        Returns:
            Dict[str, str]: Data directory paths
        """
        config = cls.get_default_config()
        return {
            "raw": config["data"]["raw_path"],
            "processed": config["data"]["processed_path"],
            "interim": config["data"]["interim_path"],
            "external": config["data"]["external_path"],
            "reference": config["data"]["reference_path"],
        }
        
    @classmethod
    def get_analysis_config(cls) -> Dict[str, Any]:
        """
        Get analysis configuration.
        
        Returns:
            Dict[str, Any]: Analysis configuration
        """
        return cls.get_default_config()["analysis"]
        
    @classmethod
    def get_visualization_config(cls) -> Dict[str, Any]:
        """
        Get visualization configuration.
        
        Returns:
            Dict[str, Any]: Visualization configuration
        """
        return cls.get_default_config()["visualization"]
        
    @classmethod
    def get_modeling_config(cls) -> Dict[str, Any]:
        """
        Get modeling configuration.
        
        Returns:
            Dict[str, Any]: Modeling configuration
        """
        return cls.get_default_config()["modeling"]