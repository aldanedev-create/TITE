"""
Default configuration values for Tite.

This module defines the default configuration values used by Tite
for project creation and management.
"""

from typing import Any, Dict, List


class DefaultConfig:
    """
    Default configuration values for Tite.
    
    This class provides the default configuration values used when
    creating new projects or when configuration files are missing.
    """
    
    # Project defaults
    PROJECT = {
        "name": "",
        "version": "0.1.0",
        "description": "A Python project created with Tite",
        "python_version": ">=3.9",
        "license": "MIT",
        "author": "",
        "email": "",
    }
    
    # Development server defaults
    DEV = {
        "command": "python src/main.py",
        "port": 8000,
        "host": "127.0.0.1",
        "env_file": ".env",
        "env_prefix": "APP_",
        "reload": True,
        "debug": False,
    }
    
    # File watcher defaults
    WATCHER = {
        "paths": ["src", "tests"],
        "extensions": [".py", ".html", ".css", ".js", ".json", ".yaml", ".yml", ".toml"],
        "ignore": [
            ".venv",
            "venv",
            "__pycache__",
            "*.egg-info",
            "logs",
            "*.log",
            "build",
            "dist",
            ".git",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            ".hypothesis",
            ".tox",
            ".nox",
        ],
        "debounce": 100,
        "restart_on_change": True,
    }
    
    # Clean patterns
    CLEAN = {
        "include": [
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            ".hypothesis",
            ".tox",
            ".nox",
            "build",
            "dist",
            "*.egg-info",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "*.so",
            "*.log",
            "*.pid",
            "*.pid.lock",
            ".coverage",
            "coverage.xml",
            "*.cover",
            "htmlcov",
        ],
        "exclude": [
            ".venv",
            "venv",
            ".git",
        ],
    }
    
    # Git defaults
    GIT = {
        "init": True,
        "branch": "main",
        "remote_url": "",
        "ignore_patterns": [
            ".venv",
            "venv",
            "__pycache__",
            "*.pyc",
            ".env",
            ".env.local",
            ".env.*.local",
            "dist",
            "build",
            "*.egg-info",
            "*.log",
            "*.db",
            "*.sqlite",
            "*.sqlite3",
            "*.pid",
            "*.pid.lock",
            ".DS_Store",
            "Thumbs.db",
            ".idea",
            ".vscode",
            "*.iml",
            "*.swp",
            "*.swo",
        ],
    }
    
    # Testing defaults
    TESTING = {
        "runner": "pytest",
        "arguments": ["-v", "--cov=src", "--cov-report=html", "--cov-report=term-missing"],
        "test_path": "tests",
        "coverage_threshold": 80,
    }
    
    # Packaging defaults
    PACKAGING = {
        "build_backend": "hatchling",
        "include_package_data": True,
        "package_name": "",
        "package_version": "0.1.0",
    }
    
    # Documentation defaults
    DOCS = {
        "builder": "sphinx",
        "source_dir": "docs",
        "build_dir": "docs/_build",
        "format": "html",
        "theme": "sphinx_rtd_theme",
    }
    
    # Logging defaults
    LOGGING = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/app.log",
        "console": True,
        "rotation": "1 day",
        "retention": "30 days",
        "compression": "gz",
    }
    
    # Database defaults
    DATABASE = {
        "enabled": False,
        "engine": "sqlite",
        "url": "sqlite:///app.db",
        "pool_size": 5,
        "max_overflow": 10,
        "echo": False,
    }
    
    # API defaults
    API = {
        "prefix": "/api/v1",
        "cors_enabled": True,
        "cors_origins": ["*"],
        "rate_limit_enabled": False,
        "rate_limit": "100/hour",
        "docs_enabled": True,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }
    
    # Security defaults
    SECURITY = {
        "csrf_protection": True,
        "session_secure": False,
        "rate_limit": "100/hour",
        "password_min_length": 8,
        "allowed_hosts": ["localhost", "127.0.0.1"],
    }
    
    # Deployment defaults
    DEPLOYMENT = {
        "platform": "auto",
        "environments": ["development", "staging", "production"],
        "health_check_path": "/health",
        "metrics_enabled": True,
    }
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """
        Get all default configuration.
        
        Returns:
            Dict[str, Any]: All default configuration
        """
        return {
            "project": cls.PROJECT,
            "dev": cls.DEV,
            "watcher": cls.WATCHER,
            "clean": cls.CLEAN,
            "git": cls.GIT,
            "testing": cls.TESTING,
            "packaging": cls.PACKAGING,
            "docs": cls.DOCS,
            "logging": cls.LOGGING,
            "database": cls.DATABASE,
            "api": cls.API,
            "security": cls.SECURITY,
            "deployment": cls.DEPLOYMENT,
        }
        
    @classmethod
    def get_section(cls, section: str) -> Dict[str, Any]:
        """
        Get a specific section of defaults.
        
        Args:
            section: Section name
            
        Returns:
            Dict[str, Any]: Section defaults
            
        Raises:
            ValueError: If section doesn't exist
        """
        sections = {
            "project": cls.PROJECT,
            "dev": cls.DEV,
            "watcher": cls.WATCHER,
            "clean": cls.CLEAN,
            "git": cls.GIT,
            "testing": cls.TESTING,
            "packaging": cls.PACKAGING,
            "docs": cls.DOCS,
            "logging": cls.LOGGING,
            "database": cls.DATABASE,
            "api": cls.API,
            "security": cls.SECURITY,
            "deployment": cls.DEPLOYMENT,
        }
        
        if section not in sections:
            raise ValueError(f"Unknown section: {section}")
            
        return sections[section]
        
    @classmethod
    def get_value(cls, key: str) -> Any:
        """
        Get a specific default value.
        
        Args:
            key: Dot-separated key path
            
        Returns:
            Any: Default value
            
        Raises:
            ValueError: If key doesn't exist
        """
        parts = key.split(".")
        current = cls.get_all()
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                raise ValueError(f"Unknown key: {key}")
                
        return current
        
    @classmethod
    def merge_with(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge defaults with a configuration.
        
        Args:
            config: Configuration to merge
            
        Returns:
            Dict[str, Any]: Merged configuration
        """
        defaults = cls.get_all()
        return cls._deep_merge(defaults, config)
        
    @classmethod
    def _deep_merge(cls, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries.
        
        Args:
            base: Base dictionary
            override: Override dictionary
            
        Returns:
            Dict[str, Any]: Merged dictionary
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = cls._deep_merge(result[key], value)
            else:
                result[key] = value
                
        return result