"""
Configuration management for the web application.

This module handles loading and validating configuration from
environment variables and configuration files.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class AppConfig:
    """
    Application configuration.
    
    Attributes:
        debug: Enable debug mode
        host: Server host address
        port: Server port
        secret_key: Secret key for sessions and security
        allowed_hosts: List of allowed host headers
        cors_origins: List of allowed CORS origins
        database_url: Database connection string
        redis_url: Redis connection string
        log_level: Logging level
        static_dir: Static files directory
        templates_dir: Templates directory
    """
    
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    host: str = field(default_factory=lambda: os.getenv("HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", 8000)))
    secret_key: str = field(default_factory=lambda: os.getenv("SECRET_KEY", "dev-secret-key"))
    
    allowed_hosts: List[str] = field(default_factory=lambda: [
        h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    ])
    
    cors_origins: List[str] = field(default_factory=lambda: [
        o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",")
    ])
    
    database_url: str = field(default_factory=lambda: os.getenv(
        "DATABASE_URL",
        "sqlite:///app.db"
    ))
    
    redis_url: str = field(default_factory=lambda: os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    ))
    
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    
    static_dir: Path = field(default_factory=lambda: Path(__file__).parent / "static")
    templates_dir: Path = field(default_factory=lambda: Path(__file__).parent / "templates")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict[str, Any]: Configuration as dictionary
        """
        return {
            "debug": self.debug,
            "host": self.host,
            "port": self.port,
            "secret_key": "***" if self.secret_key else None,
            "allowed_hosts": self.allowed_hosts,
            "cors_origins": self.cors_origins,
            "database_url": self.database_url,
            "redis_url": self.redis_url,
            "log_level": self.log_level,
            "static_dir": str(self.static_dir),
            "templates_dir": str(self.templates_dir),
        }
    
    def validate(self) -> bool:
        """
        Validate configuration.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        errors = []
        
        if not isinstance(self.debug, bool):
            errors.append("debug must be a boolean")
        
        if not isinstance(self.port, int) or not (0 < self.port < 65536):
            errors.append("port must be between 1 and 65535")
        
        if not self.host:
            errors.append("host cannot be empty")
        
        if not self.secret_key or self.secret_key == "dev-secret-key":
            import warnings
            warnings.warn("Using default secret key in production is insecure!")
        
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            errors.append(f"Invalid log level: {self.log_level}")
        
        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")
        
        return True


def load_config(
    config_path: Optional[Path] = None,
    env_prefix: str = "APP_",
) -> AppConfig:
    """
    Load configuration from environment and optional config file.
    
    Args:
        config_path: Optional path to configuration file
        env_prefix: Prefix for environment variables
        
    Returns:
        AppConfig: Loaded configuration
    """
    if config_path and config_path.exists():
        # Load from file if supported
        import json
        import tomllib
        import yaml
        
        suffix = config_path.suffix.lower()
        
        try:
            if suffix == ".json":
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return AppConfig(**data)
            elif suffix == ".toml":
                with open(config_path, "rb") as f:
                    data = tomllib.load(f)
                return AppConfig(**data)
            elif suffix in (".yaml", ".yml"):
                with open(config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                return AppConfig(**data)
        except Exception as e:
            import warnings
            warnings.warn(f"Failed to load config from {config_path}: {e}")
    
    # Load from environment
    return AppConfig()


# Global configuration instance
config = load_config()

# Validate configuration
if config.validate():
    logger = logging.getLogger(__name__)
    logger.info("Configuration loaded successfully")
    logger.info(f"Debug mode: {config.debug}")
    logger.info(f"Server: http://{config.host}:{config.port}")