"""
Blueprint parser for Tite.

This module handles parsing blueprint definitions from various formats
including YAML, JSON, and TOML.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from tite.blueprint.schema import BlueprintSchema
from tite.blueprint.validator import BlueprintValidator
from tite.exceptions import ConfigurationError, ValidationError


class BlueprintParser:
    """
    Parses blueprint definitions from files or dictionaries.
    
    This class handles loading and parsing blueprint definitions from
    various formats and validating them against the blueprint schema.
    
    Attributes:
        schema: Blueprint schema for validation
        validator: Blueprint validator instance
    """
    
    def __init__(self):
        """Initialize the blueprint parser."""
        self.schema = BlueprintSchema()
        self.validator = BlueprintValidator(self.schema)
        
    def parse_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Parse a blueprint from a file.
        
        Args:
            file_path: Path to the blueprint file
            
        Returns:
            Dict[str, Any]: Parsed blueprint definition
            
        Raises:
            ConfigurationError: If file cannot be parsed
            ValidationError: If blueprint is invalid
        """
        path = Path(file_path)
        
        if not path.exists():
            raise ConfigurationError(f"Blueprint file not found: {path}")
            
        # Determine format from extension
        suffix = path.suffix.lower()
        
        try:
            if suffix == ".yaml" or suffix == ".yml":
                data = self._parse_yaml(path)
            elif suffix == ".json":
                data = self._parse_json(path)
            elif suffix == ".toml":
                data = self._parse_toml(path)
            else:
                # Try to parse as YAML first, then JSON
                try:
                    data = self._parse_yaml(path)
                except Exception:
                    try:
                        data = self._parse_json(path)
                    except Exception:
                        raise ConfigurationError(f"Unsupported blueprint format: {suffix}")
                        
            # Validate the blueprint
            self.validator.validate(data)
            
            return data
            
        except Exception as e:
            raise ConfigurationError(f"Failed to parse blueprint: {e}")
            
    def parse_string(self, content: str, format: str = "yaml") -> Dict[str, Any]:
        """
        Parse a blueprint from a string.
        
        Args:
            content: Blueprint content
            format: Format of the content (yaml, json, toml)
            
        Returns:
            Dict[str, Any]: Parsed blueprint definition
            
        Raises:
            ConfigurationError: If content cannot be parsed
            ValidationError: If blueprint is invalid
        """
        try:
            if format == "yaml":
                data = yaml.safe_load(content)
            elif format == "json":
                data = json.loads(content)
            elif format == "toml":
                import tomllib
                data = tomllib.loads(content)
            else:
                raise ConfigurationError(f"Unsupported format: {format}")
                
            # Validate the blueprint
            self.validator.validate(data)
            
            return data
            
        except Exception as e:
            raise ConfigurationError(f"Failed to parse blueprint: {e}")
            
    def _parse_yaml(self, path: Path) -> Dict[str, Any]:
        """Parse YAML file."""
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
            
    def _parse_json(self, path: Path) -> Dict[str, Any]:
        """Parse JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    def _parse_toml(self, path: Path) -> Dict[str, Any]:
        """Parse TOML file."""
        import tomllib
        with open(path, "rb") as f:
            return tomllib.load(f)
            
    def parse_blueprint_name(self, name: str) -> Dict[str, str]:
        """
        Parse a blueprint name into components.
        
        Args:
            name: Blueprint name (e.g., "project:web", "mode:data")
            
        Returns:
            Dict[str, str]: Parsed components
        """
        result = {"type": "blueprint", "name": name}
        
        if ":" in name:
            type_part, name_part = name.split(":", 1)
            result["type"] = type_part
            result["name"] = name_part
            
        return result
        
    def get_blueprint_template(self, blueprint: Dict[str, Any]) -> Optional[str]:
        """
        Get the template name from a blueprint.
        
        Args:
            blueprint: Blueprint definition
            
        Returns:
            Optional[str]: Template name or None
        """
        return blueprint.get("template")
        
    def get_blueprint_variables(self, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get variables from a blueprint.
        
        Args:
            blueprint: Blueprint definition
            
        Returns:
            Dict[str, Any]: Blueprint variables
        """
        return blueprint.get("variables", {})
        
    def get_blueprint_commands(self, blueprint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get commands from a blueprint.
        
        Args:
            blueprint: Blueprint definition
            
        Returns:
            List[Dict[str, Any]]: Blueprint commands
        """
        return blueprint.get("commands", [])
        
    def get_blueprint_files(self, blueprint: Dict[str, Any]) -> Dict[str, str]:
        """
        Get files from a blueprint.
        
        Args:
            blueprint: Blueprint definition
            
        Returns:
            Dict[str, str]: File paths to content
        """
        return blueprint.get("files", {})
        
    def get_blueprint_dependencies(self, blueprint: Dict[str, Any]) -> List[str]:
        """
        Get dependencies from a blueprint.
        
        Args:
            blueprint: Blueprint definition
            
        Returns:
            List[str]: Dependency names
        """
        return blueprint.get("dependencies", [])


class BlueprintVariableParser:
    """
    Parses and substitutes variables in blueprint content.
    """
    
    def __init__(self, variables: Optional[Dict[str, Any]] = None):
        """
        Initialize the variable parser.
        
        Args:
            variables: Variables to use for substitution
        """
        self.variables = variables or {}
        
    def parse_variables(self, content: str) -> str:
        """
        Parse and substitute variables in content.
        
        Args:
            content: Content containing variable placeholders
            
        Returns:
            str: Content with variables substituted
        """
        # Pattern for {{ variable }}
        pattern = r'\{\{\s*([^}]+)\s*\}\}'
        
        def replace_variable(match):
            var_name = match.group(1).strip()
            
            # Handle nested access
            if "." in var_name:
                parts = var_name.split(".")
                value = self.variables
                for part in parts:
                    if isinstance(value, dict):
                        value = value.get(part)
                    else:
                        return match.group(0)
                return str(value) if value is not None else match.group(0)
                
            # Simple variable
            value = self.variables.get(var_name)
            return str(value) if value is not None else match.group(0)
            
        return re.sub(pattern, replace_variable, content)
        
    def parse_variables_in_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and substitute variables in a dictionary.
        
        Args:
            data: Dictionary containing variable placeholders
            
        Returns:
            Dict[str, Any]: Dictionary with variables substituted
        """
        result = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.parse_variables(value)
            elif isinstance(value, dict):
                result[key] = self.parse_variables_in_dict(value)
            elif isinstance(value, list):
                result[key] = self.parse_variables_in_list(value)
            else:
                result[key] = value
                
        return result
        
    def parse_variables_in_list(self, data: List[Any]) -> List[Any]:
        """
        Parse and substitute variables in a list.
        
        Args:
            data: List containing variable placeholders
            
        Returns:
            List[Any]: List with variables substituted
        """
        result = []
        
        for item in data:
            if isinstance(item, str):
                result.append(self.parse_variables(item))
            elif isinstance(item, dict):
                result.append(self.parse_variables_in_dict(item))
            elif isinstance(item, list):
                result.append(self.parse_variables_in_list(item))
            else:
                result.append(item)
                
        return result
        
    def add_variables(self, variables: Dict[str, Any]) -> None:
        """
        Add more variables.
        
        Args:
            variables: Variables to add
        """
        self.variables.update(variables)
        
    def set_variable(self, key: str, value: Any) -> None:
        """
        Set a single variable.
        
        Args:
            key: Variable name
            value: Variable value
        """
        self.variables[key] = value
        
    def get_variable(self, key: str, default: Any = None) -> Any:
        """
        Get a variable value.
        
        Args:
            key: Variable name
            default: Default value if not found
            
        Returns:
            Any: Variable value
        """
        return self.variables.get(key, default)