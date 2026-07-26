"""
Blueprint schema for Tite.

This module defines the schema for blueprint definitions including
field types, validation rules, and schema management.
"""

from typing import Any, Dict, List, Optional, Set, Union


class SchemaType:
    """Schema field types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    ANY = "any"


class SchemaField:
    """
    Schema field definition.
    
    Attributes:
        name: Field name
        type: Field type
        required: Whether field is required
        default: Default value
        allowed: Allowed values
        pattern: Regex pattern for string fields
        description: Field description
    """
    
    def __init__(
        self,
        name: str,
        type: str = SchemaType.STRING,
        required: bool = False,
        default: Any = None,
        allowed: Optional[List[Any]] = None,
        pattern: Optional[str] = None,
        description: str = "",
    ):
        """
        Initialize the schema field.
        
        Args:
            name: Field name
            type: Field type
            required: Whether field is required
            default: Default value
            allowed: Allowed values
            pattern: Regex pattern for string fields
            description: Field description
        """
        self.name = name
        self.type = type
        self.required = required
        self.default = default
        self.allowed = allowed or []
        self.pattern = pattern
        self.description = description
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary.
        
        Returns:
            Dict[str, Any]: Field as dictionary
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
        if self.description:
            result["description"] = self.description
            
        return result


class BlueprintSchema:
    """
    Blueprint schema definition.
    
    This class defines the schema for blueprint files including
    required fields, field types, and validation rules.
    
    Attributes:
        fields: Dictionary of field definitions
        version: Schema version
    """
    
    # Default schema for blueprints
    DEFAULT_SCHEMA = {
        "name": {
            "type": SchemaType.STRING,
            "required": True,
            "description": "Blueprint name",
        },
        "version": {
            "type": SchemaType.STRING,
            "required": False,
            "default": "1.0.0",
            "pattern": r'^\d+\.\d+\.\d+$',
            "description": "Blueprint version",
        },
        "description": {
            "type": SchemaType.STRING,
            "required": False,
            "description": "Blueprint description",
        },
        "template": {
            "type": SchemaType.STRING,
            "required": False,
            "description": "Template to use",
        },
        "variables": {
            "type": SchemaType.OBJECT,
            "required": False,
            "default": {},
            "description": "Variables for substitution",
        },
        "directories": {
            "type": SchemaType.ARRAY,
            "required": False,
            "default": [],
            "description": "Directories to create",
        },
        "files": {
            "type": SchemaType.OBJECT,
            "required": False,
            "default": {},
            "description": "Files to create",
        },
        "template_files": {
            "type": SchemaType.ARRAY,
            "required": False,
            "default": [],
            "description": "Template files to copy",
        },
        "packages": {
            "type": SchemaType.ARRAY,
            "required": False,
            "default": [],
            "description": "Packages to install",
        },
        "commands": {
            "type": SchemaType.ARRAY,
            "required": False,
            "default": [],
            "description": "Commands to execute",
        },
        "dependencies": {
            "type": SchemaType.ARRAY,
            "required": False,
            "default": [],
            "description": "Blueprint dependencies",
        },
    }
    
    def __init__(self, schema: Optional[Dict[str, Any]] = None):
        """
        Initialize the blueprint schema.
        
        Args:
            schema: Schema definition (uses default if None)
        """
        self.fields: Dict[str, SchemaField] = {}
        self.version = "1.0.0"
        
        schema = schema or self.DEFAULT_SCHEMA
        
        for field_name, field_config in schema.items():
            self.fields[field_name] = SchemaField(
                name=field_name,
                type=field_config.get("type", SchemaType.STRING),
                required=field_config.get("required", False),
                default=field_config.get("default"),
                allowed=field_config.get("allowed"),
                pattern=field_config.get("pattern"),
                description=field_config.get("description", ""),
            )
            
    def get_field(self, name: str) -> Optional[SchemaField]:
        """
        Get a field definition.
        
        Args:
            name: Field name
            
        Returns:
            Optional[SchemaField]: Field definition or None
        """
        return self.fields.get(name)
        
    def get_required_fields(self) -> List[str]:
        """
        Get required field names.
        
        Returns:
            List[str]: Required field names
        """
        return [name for name, field in self.fields.items() if field.required]
        
    def get_field_default(self, name: str) -> Any:
        """
        Get field default value.
        
        Args:
            name: Field name
            
        Returns:
            Any: Default value or None
        """
        field = self.get_field(name)
        return field.default if field else None
        
    def validate_field(self, name: str, value: Any) -> bool:
        """
        Validate a field value.
        
        Args:
            name: Field name
            value: Field value
            
        Returns:
            bool: True if valid
        """
        field = self.get_field(name)
        if not field:
            return False
            
        # Check type
        if not self._check_type(value, field.type):
            return False
            
        # Check allowed values
        if field.allowed and value not in field.allowed:
            return False
            
        return True
        
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if a value matches an expected type."""
        if expected_type == SchemaType.STRING:
            return isinstance(value, str)
        elif expected_type == SchemaType.INTEGER:
            return isinstance(value, int)
        elif expected_type == SchemaType.FLOAT:
            return isinstance(value, (int, float))
        elif expected_type == SchemaType.BOOLEAN:
            return isinstance(value, bool)
        elif expected_type == SchemaType.ARRAY:
            return isinstance(value, list)
        elif expected_type == SchemaType.OBJECT:
            return isinstance(value, dict)
        elif expected_type == SchemaType.ANY:
            return True
        return False
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert schema to dictionary.
        
        Returns:
            Dict[str, Any]: Schema as dictionary
        """
        return {
            "version": self.version,
            "fields": {
                name: field.to_dict()
                for name, field in self.fields.items()
            },
        }


class BlueprintSchemaValidationError(Exception):
    """Exception raised when schema validation fails."""
    pass