"""
Configuration management for the API application.

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
class APIConfig:
    """
    API application configuration.
    
    Attributes:
        debug: Enable debug mode
        host: Server host address
        port: Server port
        secret_key: Secret key for sessions and security
        api_prefix: API URL prefix
        allowed_hosts: List of allowed host headers
        cors_origins: List of allowed CORS origins
        database_url: Database connection string
        redis_url: Redis connection string
        log_level: Logging level
        rate_limit: Rate limit string (e.g., "100/hour")
        jwt_secret: JWT secret key
        jwt_algorithm: JWT algorithm
        jwt_expiration: JWT expiration time in minutes
    """
    
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    host: str = field(default_factory=lambda: os.getenv("HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", 8000)))
    secret_key: str = field(default_factory=lambda: os.getenv("SECRET_KEY", "dev-secret-key"))
    api_prefix: str = field(default_factory=lambda: os.getenv("API_PREFIX", "/api/v1"))
    
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
    rate_limit: str = field(default_factory=lambda: os.getenv("RATE_LIMIT", "100/hour"))
    
    jwt_secret: str = field(default_factory=lambda: os.getenv(
        "JWT_SECRET",
        "jwt-secret-key-change-in-production"
    ))
    jwt_algorithm: str = field(default_factory=lambda: os.getenv("JWT_ALGORITHM", "HS256"))
    jwt_expiration: int = field(default_factory=lambda: int(os.getenv("JWT_EXPIRATION", "60")))
    
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
            "api_prefix": self.api_prefix,
            "allowed_hosts": self.allowed_hosts,
            "cors_origins": self.cors_origins,
            "database_url": self.database_url,
            "redis_url": self.redis_url,
            "log_level": self.log_level,
            "rate_limit": self.rate_limit,
            "jwt_secret": "***" if self.jwt_secret else None,
            "jwt_algorithm": self.jwt_algorithm,
            "jwt_expiration": self.jwt_expiration,
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
        
        if not self.jwt_secret or self.jwt_secret == "jwt-secret-key-change-in-production":
            import warnings
            warnings.warn("Using default JWT secret in production is insecure!")
        
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            errors.append(f"Invalid log level: {self.log_level}")
        
        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")
        
        return True


def load_config(
    config_path: Optional[Path] = None,
    env_prefix: str = "API_",
) -> APIConfig:
    """
    Load configuration from environment and optional config file.
    
    Args:
        config_path: Optional path to configuration file
        env_prefix: Prefix for environment variables
        
    Returns:
        APIConfig: Loaded configuration
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
                return APIConfig(**data)
            elif suffix == ".toml":
                with open(config_path, "rb") as f:
                    data = tomllib.load(f)
                return APIConfig(**data)
            elif suffix in (".yaml", ".yml"):
                with open(config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                return APIConfig(**data)
        except Exception as e:
            import warnings
            warnings.warn(f"Failed to load config from {config_path}: {e}")
    
    # Load from environment
    return APIConfig()


# Global configuration instance
config = load_config()

# Validate configuration
if config.validate():
    logger = logging.getLogger(__name__)
    logger.info("Configuration loaded successfully")
    logger.info(f"Debug mode: {config.debug}")
    logger.info(f"API Server: http://{config.host}:{config.port}{config.api_prefix}")