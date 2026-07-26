"""
Mode validator for Tite.

This module handles validating mode definitions for correctness
and completeness.
"""

from typing import Any, Dict, List, Optional

from tite.exceptions import ValidationError


class ModeValidator:
    """
    Validates mode definitions.
    
    This class checks mode definitions for required fields,
    correct types, and valid values.
    """
    
    REQUIRED_FIELDS = ["name", "description", "template"]
    OPTIONAL_FIELDS = ["packages", "structure", "files", "variables", "commands"]
    
    def validate(self, mode: Dict[str, Any]) -> bool:
        """
        Validate a mode definition.
        
        Args:
            mode: Mode definition to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If mode is invalid
        """
        errors = []
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in mode:
                errors.append(f"Missing required field: {field}")
                
        # Check field types
        if "name" in mode and not isinstance(mode["name"], str):
            errors.append("name must be a string")
            
        if "description" in mode and not isinstance(mode["description"], str):
            errors.append("description must be a string")
            
        if "template" in mode and not isinstance(mode["template"], str):
            errors.append("template must be a string")
            
        if "packages" in mode:
            if not isinstance(mode["packages"], list):
                errors.append("packages must be a list")
            else:
                for pkg in mode["packages"]:
                    if not isinstance(pkg, str):
                        errors.append("each package must be a string")
                        
        if "structure" in mode:
            if not isinstance(mode["structure"], dict):
                errors.append("structure must be a dictionary")
            else:
                self._validate_structure(mode["structure"], errors)
                
        if "files" in mode:
            if not isinstance(mode["files"], dict):
                errors.append("files must be a dictionary")
            else:
                for key, value in mode["files"].items():
                    if not isinstance(key, str):
                        errors.append("file keys must be strings")
                    if not isinstance(value, str):
                        errors.append("file values must be strings")
                        
        if "variables" in mode:
            if not isinstance(mode["variables"], dict):
                errors.append("variables must be a dictionary")
                
        if "commands" in mode:
            if not isinstance(mode["commands"], list):
                errors.append("commands must be a list")
            else:
                for cmd in mode["commands"]:
                    if not isinstance(cmd, (str, dict)):
                        errors.append("each command must be a string or dictionary")
                        
        if errors:
            raise ValidationError("mode", "\n".join(errors))
            
        return True
        
    def _validate_structure(self, structure: Dict[str, Any], errors: List[str]) -> None:
        """
        Validate the structure field.
        
        Args:
            structure: Structure dictionary
            errors: List to append errors to
        """
        if "directories" in structure:
            if not isinstance(structure["directories"], list):
                errors.append("structure.directories must be a list")
            else:
                for dir_path in structure["directories"]:
                    if not isinstance(dir_path, str):
                        errors.append("each directory path must be a string")
                        
        if "files" in structure:
            if not isinstance(structure["files"], list):
                errors.append("structure.files must be a list")
            else:
                for file_path in structure["files"]:
                    if not isinstance(file_path, str):
                        errors.append("each file path must be a string")
                        
    def validate_mode_name(self, name: str) -> bool:
        """
        Validate a mode name.
        
        Args:
            name: Mode name to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If name is invalid
        """
        if not name:
            raise ValidationError("mode_name", "Mode name cannot be empty")
            
        if len(name) < 1 or len(name) > 50:
            raise ValidationError("mode_name", "Mode name must be between 1 and 50 characters")
            
        import re
        if not re.match(r'^[a-z][a-z0-9\-_]*$', name):
            raise ValidationError(
                "mode_name",
                "Mode name must start with a letter and contain only "
                "lowercase letters, numbers, hyphens, and underscores"
            )
            
        return True
        
    def validate_template(self, template_name: str) -> bool:
        """
        Validate a template name.
        
        Args:
            template_name: Template name to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If template name is invalid
        """
        if not template_name:
            raise ValidationError("template", "Template name cannot be empty")
            
        import re
        if not re.match(r'^[a-z][a-z0-9\-_]*$', template_name):
            raise ValidationError(
                "template",
                "Template name must start with a letter and contain only "
                "lowercase letters, numbers, hyphens, and underscores"
            )
            
        return True
        
    def validate_package(self, package: str) -> bool:
        """
        Validate a package name.
        
        Args:
            package: Package name to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If package name is invalid
        """
        if not package:
            raise ValidationError("package", "Package name cannot be empty")
            
        # Check for valid package name format
        import re
        if not re.match(r'^[a-zA-Z0-9\-_\.]+$', package):
            raise ValidationError(
                "package",
                f"Invalid package name: {package}"
            )
            
        return True
        
    def get_validation_errors(self, mode: Dict[str, Any]) -> List[str]:
        """
        Get validation errors for a mode without raising an exception.
        
        Args:
            mode: Mode definition to validate
            
        Returns:
            List[str]: List of error messages
        """
        errors = []
        
        try:
            self.validate(mode)
        except ValidationError as e:
            errors = str(e).split("\n")
            
        return errors