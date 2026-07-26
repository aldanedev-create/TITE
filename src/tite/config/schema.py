"""
Configuration schema for Tite.

This module defines the schema for configuration validation including
field types, required fields, and validation rules.
"""

from typing import Any, Dict, List, Optional, Set, Union


class ConfigField:
    """
    Configuration field definition.
    
    Attributes:
        name: Field name
        type: Field type (string, integer, float, boolean, array, object)
        required: Whether field is required
        default: Default value
        allowed: Allowed values
        pattern: Regex pattern for string fields
        min: Minimum value for numeric fields
        max: Maximum value for numeric fields
        min_length: Minimum length for string/array fields
        max_length: Maximum length for string/array fields
        description: Field description
    """
    
    def __init__(
        self,
        name: str,
        type: str = "string",
        required: bool = False,
        default: Any = None,
        allowed: Optional[List[Any]] = None,
        pattern: Optional[str] = None,
        min: Optional[float] = None,
        max: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        description: str = "",
    ):
        """
        Initialize the config field.
        
        Args:
            name: Field name
            type: Field type
            required: Whether field is required
            default: Default value
            allowed: Allowed values
            pattern: Regex pattern for string fields
            min: Minimum value for numeric fields
            max: Maximum value for numeric fields
            min_length: Minimum length for string/array fields
            max_length: Maximum length for string/array fields
            description: Field description
        """
        self.name = name
        self.type = type
        self.required = required
        self.default = default
        self.allowed = allowed or []
        self.pattern = pattern
        self.min = min
        self.max = max
        self.min_length = min_length
        self.max_length = max_length
        self.description = description
        
    def validate(self, value: Any) -> bool:
        """
        Validate a value against this field.
        
        Args:
            value: Value to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If validation fails
        """
        # Check required
        if self.required and value is None:
            raise ValueError(f"Field '{self.name}' is required")
            
        if value is None:
            return True
            
        # Check type
        if not self._check_type(value):
            raise ValueError(
                f"Field '{self.name}' must be of type '{self.type}'"
            )
            
        # Check allowed values
        if self.allowed and value not in self.allowed:
            raise ValueError(
                f"Field '{self.name}' must be one of: {', '.join(self.allowed)}"
            )
            
        # Check pattern
        if self.pattern and isinstance(value, str):
            import re
            if not re.match(self.pattern, value):
                raise ValueError(
                    f"Field '{self.name}' does not match pattern: {self.pattern}"
                )
                
        # Check min/max
        if self.min is not None and isinstance(value, (int, float)):
            if value < self.min:
                raise ValueError(
                    f"Field '{self.name}' must be >= {self.min}"
                )
                
        if self.max is not None and isinstance(value, (int, float)):
            if value > self.max:
                raise ValueError(
                    f"Field '{self.name}' must be <= {self.max}"
                )
                
        # Check min/max length
        if self.min_length is not None and isinstance(value, (str, list)):
            if len(value) < self.min_length:
                raise ValueError(
                    f"Field '{self.name}' must have length >= {self.min_length}"
                )
                
        if self.max_length is not None and isinstance(value, (str, list)):
            if len(value) > self.max_length:
                raise ValueError(
                    f"Field '{self.name}' must have length <= {self.max_length}"
                )
                
        return True
        
    def _check_type(self, value: Any) -> bool:
        """
        Check if a value matches the expected type.
        
        Args:
            value: Value to check
            
        Returns:
            bool: True if type matches
        """
        type_map = {
            "string": str,
            "integer": int,
            "float": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
            "any": object,
        }
        
        expected_type = type_map.get(self.type, object)
        return isinstance(value, expected_type)
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary.
        
        Returns:
            Dict[str, Any]: Field dictionary
        """
        result = {
            "type": self.type,
            "required": self.required,
        }
        
        if self.default is not None:
            result["default"] = self.default
        if self.allowed:
            result["allowed"] = self.allowed
        if self.pattern:
            result["pattern"] = self.pattern
        if self.min is not None:
            result["min"] = self.min
        if self.max is not None:
            result["max"] = self.max
        if self.min_length is not None:
            result["min_length"] = self.min_length
        if self.max_length is not None:
            result["max_length"] = self.max_length
        if self.description:
            result["description"] = self.description
            
        return result


class ConfigValidationError(Exception):
    """Exception raised when configuration validation fails."""
    pass


class ConfigSchema:
    """
    Configuration schema definition.
    
    This class defines the schema for configuration validation.
    
    Attributes:
        fields: Dictionary of field definitions
        sections: Dictionary of section schemas
    """
    
    def __init__(self):
        """Initialize the configuration schema."""
        self.fields: Dict[str, ConfigField] = {}
        self.sections: Dict[str, 'ConfigSchema'] = {}
        self._build_schema()
        
    def _build_schema(self) -> None:
        """Build the schema."""
        # Project section
        self.add_field("project.name", "string", required=True, description="Project name")
        self.add_field("project.version", "string", required=True, default="0.1.0", description="Project version")
        self.add_field("project.description", "string", description="Project description")
        self.add_field("project.python_version", "string", default=">=3.9", description="Python version requirement")
        self.add_field("project.license", "string", default="MIT", description="Project license")
        self.add_field("project.author", "string", description="Project author")
        self.add_field("project.email", "string", pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 
                      description="Author email")
        
        # Dev section
        self.add_field("dev.command", "string", default="python src/main.py", description="Development command")
        self.add_field("dev.port", "integer", default=8000, min=1, max=65535, description="Development port")
        self.add_field("dev.host", "string", default="127.0.0.1", description="Development host")
        self.add_field("dev.env_file", "string", default=".env", description="Environment file")
        self.add_field("dev.env_prefix", "string", default="APP_", description="Environment variable prefix")
        self.add_field("dev.reload", "boolean", default=True, description="Enable auto-reload")
        self.add_field("dev.debug", "boolean", default=False, description="Enable debug mode")
        
        # Watcher section
        self.add_field("watcher.paths", "array", default=["src", "tests"], description="Watch paths")
        self.add_field("watcher.extensions", "array", default=[".py", ".html", ".css", ".js"], 
                      description="Watch extensions")
        self.add_field("watcher.ignore", "array", default=[".venv", "__pycache__"], description="Ignore patterns")
        self.add_field("watcher.debounce", "integer", default=100, min=0, description="Debounce in milliseconds")
        self.add_field("watcher.restart_on_change", "boolean", default=True, description="Restart on file change")
        
        # Clean section
        self.add_field("clean.include", "array", default=["__pycache__", ".pytest_cache"], description="Clean patterns")
        self.add_field("clean.exclude", "array", default=[".venv"], description="Exclude patterns")
        
        # Git section
        self.add_field("git.init", "boolean", default=True, description="Initialize Git repository")
        self.add_field("git.branch", "string", default="main", description="Default branch name")
        self.add_field("git.remote_url", "string", description="Remote repository URL")
        self.add_field("git.ignore_patterns", "array", default=[".venv", "__pycache__"], 
                      description="Git ignore patterns")
        
        # Testing section
        self.add_field("testing.runner", "string", default="pytest", description="Test runner")
        self.add_field("testing.arguments", "array", default=["-v"], description="Test arguments")
        self.add_field("testing.test_path", "string", default="tests", description="Test directory")
        self.add_field("testing.coverage_threshold", "integer", default=80, min=0, max=100, 
                      description="Coverage threshold")
        
        # Packaging section
        self.add_field("packaging.build_backend", "string", default="hatchling", description="Build backend")
        self.add_field("packaging.include_package_data", "boolean", default=True, 
                      description="Include package data")
        self.add_field("packaging.package_name", "string", description="Package name")
        self.add_field("packaging.package_version", "string", default="0.1.0", description="Package version")
        
        # Logging section
        self.add_field("logging.level", "string", default="INFO", 
                      allowed=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], description="Log level")
        self.add_field("logging.format", "string", default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                      description="Log format")
        self.add_field("logging.file", "string", default="logs/app.log", description="Log file")
        self.add_field("logging.console", "boolean", default=True, description="Log to console")
        self.add_field("logging.rotation", "string", default="1 day", description="Log rotation")
        self.add_field("logging.retention", "string", default="30 days", description="Log retention")
        
        # Database section
        self.add_field("database.enabled", "boolean", default=False, description="Enable database")
        self.add_field("database.engine", "string", default="sqlite", 
                      allowed=["sqlite", "postgresql", "mysql", "mongodb"], description="Database engine")
        self.add_field("database.url", "string", default="sqlite:///app.db", description="Database URL")
        self.add_field("database.pool_size", "integer", default=5, min=1, description="Connection pool size")
        self.add_field("database.max_overflow", "integer", default=10, min=0, description="Max overflow connections")
        
        # API section
        self.add_field("api.prefix", "string", default="/api/v1", description="API prefix")
        self.add_field("api.cors_enabled", "boolean", default=True, description="Enable CORS")
        self.add_field("api.cors_origins", "array", default=["*"], description="CORS allowed origins")
        self.add_field("api.rate_limit_enabled", "boolean", default=False, description="Enable rate limiting")
        self.add_field("api.rate_limit", "string", default="100/hour", description="Rate limit")
        self.add_field("api.docs_enabled", "boolean", default=True, description="Enable API docs")
        
        # Security section
        self.add_field("security.csrf_protection", "boolean", default=True, description="Enable CSRF protection")
        self.add_field("security.session_secure", "boolean", default=False, description="Secure session cookies")
        self.add_field("security.rate_limit", "string", default="100/hour", description="Rate limit")
        self.add_field("security.password_min_length", "integer", default=8, min=4, description="Minimum password length")
        
        # Deployment section
        self.add_field("deployment.platform", "string", default="auto", 
                      allowed=["auto", "heroku", "vercel", "docker", "kubernetes"], description="Deployment platform")
        self.add_field("deployment.health_check_path", "string", default="/health", description="Health check path")
        self.add_field("deployment.metrics_enabled", "boolean", default=True, description="Enable metrics")
        
    def add_field(
        self,
        name: str,
        type: str = "string",
        **kwargs,
    ) -> None:
        """
        Add a field to the schema.
        
        Args:
            name: Field name
            type: Field type
            **kwargs: Additional field attributes
        """
        self.fields[name] = ConfigField(name, type, **kwargs)
        
    def get_field(self, name: str) -> Optional[ConfigField]:
        """
        Get a field by name.
        
        Args:
            name: Field name
            
        Returns:
            Optional[ConfigField]: Field or None
        """
        return self.fields.get(name)
        
    def get_required_fields(self) -> List[str]:
        """
        Get required field names.
        
        Returns:
            List[str]: Required field names
        """
        return [name for name, field in self.fields.items() if field.required]
        
    def validate(self, config: Dict[str, Any]) -> bool:
        """
        Validate configuration against schema.
        
        Args:
            config: Configuration to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ConfigValidationError: If validation fails
        """
        errors = []
        
        for name, field in self.fields.items():
            value = self._get_nested_value(config, name)
            
            try:
                field.validate(value)
            except ValueError as e:
                errors.append(str(e))
                
        if errors:
            raise ConfigValidationError("\n".join(errors))
            
        return True
        
    def _get_nested_value(self, config: Dict[str, Any], key: str) -> Any:
        """
        Get a nested value from configuration.
        
        Args:
            config: Configuration dictionary
            key: Dot-separated key path
            
        Returns:
            Any: Value or None
        """
        parts = key.split(".")
        current = config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
                
        return current
        
    def get_errors(self) -> List[str]:
        """
        Get validation errors from last validation.
        
        Returns:
            List[str]: List of error messages
        """
        return self._last_errors if hasattr(self, "_last_errors") else []