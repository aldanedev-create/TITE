"""
Blueprint validator for Tite.

This module provides validation for blueprint definitions including
schema validation, required fields, and custom validation rules.
"""

from typing import Any, Dict, List, Optional, Set, Union

from tite.blueprint.schema import BlueprintSchema, SchemaType


class ValidationResult:
    """
    Result of blueprint validation.
    
    Attributes:
        valid: Whether the validation passed
        errors: List of error messages
        warnings: List of warning messages
    """
    
    def __init__(self):
        """Initialize validation result."""
        self.valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def add_error(self, error: str) -> None:
        """
        Add an error.
        
        Args:
            error: Error message
        """
        self.errors.append(error)
        self.valid = False
        
    def add_warning(self, warning: str) -> None:
        """
        Add a warning.
        
        Args:
            warning: Warning message
        """
        self.warnings.append(warning)
        
    def merge(self, other: 'ValidationResult') -> None:
        """
        Merge another validation result.
        
        Args:
            other: Other validation result
        """
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        if not other.valid:
            self.valid = False
            
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary.
        
        Returns:
            Dict[str, Any]: Validation result as dictionary
        """
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
        }


class BlueprintValidator:
    """
    Validates blueprint definitions.
    
    This class handles validating blueprint definitions against a schema
    and applying custom validation rules.
    
    Attributes:
        schema: Blueprint schema
        result: Validation result
    """
    
    def __init__(self, schema: Optional[BlueprintSchema] = None):
        """
        Initialize the blueprint validator.
        
        Args:
            schema: Blueprint schema (uses default if None)
        """
        self.schema = schema or BlueprintSchema()
        self.result = ValidationResult()
        self._validators: List[callable] = []
        
    def validate(self, blueprint: Dict[str, Any]) -> bool:
        """
        Validate a blueprint.
        
        Args:
            blueprint: Blueprint to validate
            
        Returns:
            bool: True if valid
        """
        self.result = ValidationResult()
        
        # Validate against schema
        self._validate_schema(blueprint)
        
        # Run custom validators
        for validator in self._validators:
            validator(blueprint, self.result)
            
        return self.result.valid
        
    def _validate_schema(self, blueprint: Dict[str, Any]) -> None:
        """
        Validate blueprint against schema.
        
        Args:
            blueprint: Blueprint to validate
        """
        # Check required fields
        required = self.schema.get_required_fields()
        for field in required:
            if field not in blueprint:
                self.result.add_error(f"Required field missing: {field}")
                
        # Validate field types
        for field, value in blueprint.items():
            if field in self.schema.fields:
                field_schema = self.schema.fields[field]
                self._validate_field(field, value, field_schema)
                
    def _validate_field(self, field: str, value: Any, field_schema: Any) -> None:
        """
        Validate a single field.
        
        Args:
            field: Field name
            value: Field value
            field_schema: Field schema (a SchemaField instance)
        """
        field_type = field_schema.type
        required = field_schema.required
        allowed_values = field_schema.allowed
        pattern = field_schema.pattern
        
        # Check required
        if required and value is None:
            self.result.add_error(f"Required field is empty: {field}")
            return
            
        # Check type
        if value is not None and not self._check_type(value, field_type):
            self.result.add_error(f"Invalid type for field '{field}': expected {field_type}")
            
        # Check allowed values
        if allowed_values and value not in allowed_values:
            self.result.add_error(f"Invalid value for field '{field}': {value}")
            
        # Check pattern
        if pattern and isinstance(value, str):
            import re
            if not re.match(pattern, value):
                self.result.add_error(f"Invalid format for field '{field}': {value}")
                
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """
        Check if a value matches an expected type.
        
        Args:
            value: Value to check
            expected_type: Expected type
            
        Returns:
            bool: True if type matches
        """
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
        
    def add_validator(self, validator: callable) -> None:
        """
        Add a custom validator.
        
        Args:
            validator: Validator function that takes (blueprint, result)
        """
        self._validators.append(validator)
        
    def get_errors(self) -> List[str]:
        """
        Get validation errors.
        
        Returns:
            List[str]: List of error messages
        """
        return self.result.errors
        
    def get_warnings(self) -> List[str]:
        """
        Get validation warnings.
        
        Returns:
            List[str]: List of warning messages
        """
        return self.result.warnings
        
    def is_valid(self) -> bool:
        """
        Check if the validation passed.
        
        Returns:
            bool: True if valid
        """
        return self.result.valid


# Built-in validators

def validate_blueprint_name(blueprint: Dict[str, Any], result: ValidationResult) -> None:
    """
    Validate blueprint name.
    
    Args:
        blueprint: Blueprint definition
        result: Validation result
    """
    name = blueprint.get("name")
    if name:
        import re
        if not re.match(r'^[a-zA-Z0-9\-_]+$', name):
            result.add_error(f"Invalid blueprint name: {name}")


def validate_blueprint_version(blueprint: Dict[str, Any], result: ValidationResult) -> None:
    """
    Validate blueprint version.
    
    Args:
        blueprint: Blueprint definition
        result: Validation result
    """
    version = blueprint.get("version")
    if version:
        import re
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            result.add_error(f"Invalid version format: {version}")


def validate_blueprint_dependencies(blueprint: Dict[str, Any], result: ValidationResult) -> None:
    """
    Validate blueprint dependencies.
    
    Args:
        blueprint: Blueprint definition
        result: Validation result
    """
    deps = blueprint.get("dependencies", [])
    if not isinstance(deps, list):
        result.add_error("Dependencies must be a list")
        
    for dep in deps:
        if not isinstance(dep, str):
            result.add_error(f"Invalid dependency: {dep}")