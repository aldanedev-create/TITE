"""
Prompt management for AI/ML applications.

This module provides prompt template management, validation, and
rendering for AI/ML applications.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from jinja2 import Environment, FileSystemLoader, Template
from loguru import logger

from src.utils.validators import validate_prompt


class PromptTemplate:
    """
    Prompt template with variables and rendering.
    
    Attributes:
        name: Template name
        content: Template content
        variables: Required variables
        version: Template version
    """
    
    def __init__(
        self,
        name: str,
        content: str,
        variables: Optional[List[str]] = None,
        version: str = "1.0.0",
    ):
        """
        Initialize the prompt template.
        
        Args:
            name: Template name
            content: Template content
            variables: Required variables
            version: Template version
        """
        self.name = name
        self.content = content
        self.variables = variables or []
        self.version = version
        self._env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        
    def render(self, **kwargs) -> str:
        """
        Render the template with variables.
        
        Args:
            **kwargs: Variables for rendering
            
        Returns:
            str: Rendered prompt
            
        Raises:
            ValueError: If required variables are missing
        """
        # Validate required variables
        missing = [v for v in self.variables if v not in kwargs]
        if missing:
            raise ValueError(f"Missing required variables: {missing}")
            
        # Render template
        template = self._env.from_string(self.content)
        return template.render(**kwargs)
        
    def validate(self) -> bool:
        """
        Validate the template.
        
        Returns:
            bool: True if valid
        """
        try:
            validate_prompt(self.content)
            return True
        except Exception as e:
            logger.error(f"Template validation failed: {e}")
            return False
            
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary.
        
        Returns:
            Dict[str, Any]: Template dictionary
        """
        return {
            "name": self.name,
            "content": self.content,
            "variables": self.variables,
            "version": self.version,
        }
        
    @classmethod
    def from_file(cls, path: Path) -> 'PromptTemplate':
        """
        Load a template from a file.
        
        Args:
            path: Path to the template file
            
        Returns:
            PromptTemplate: Loaded template
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not path.exists():
            raise FileNotFoundError(f"Template file not found: {path}")
            
        content = path.read_text(encoding="utf-8")
        
        # Extract variables from content
        variables = re.findall(r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}', content)
        variables = list(set(variables))
        
        return cls(
            name=path.stem,
            content=content,
            variables=variables,
        )


class PromptManager:
    """
    Manages prompt templates and their lifecycle.
    
    Attributes:
        prompt_dir: Directory containing prompt files
        templates: Dictionary of loaded templates
        environment: Jinja2 environment
    """
    
    def __init__(self, prompt_dir: Optional[Path] = None):
        """
        Initialize the prompt manager.
        
        Args:
            prompt_dir: Directory containing prompt files
        """
        self.prompt_dir = prompt_dir or Path("prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        self._env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        
        # Load templates
        self.load_templates()
        
    def load_templates(self) -> None:
        """Load all templates from the prompt directory."""
        if not self.prompt_dir.exists():
            logger.warning(f"Prompt directory not found: {self.prompt_dir}")
            return
            
        for file_path in self.prompt_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".txt", ".j2", ".md"]:
                try:
                    template = PromptTemplate.from_file(file_path)
                    self.templates[template.name] = template
                    logger.info(f"Loaded prompt template: {template.name}")
                except Exception as e:
                    logger.error(f"Failed to load template {file_path}: {e}")
                    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """
        Get a template by name.
        
        Args:
            name: Template name
            
        Returns:
            Optional[PromptTemplate]: Template or None
        """
        return self.templates.get(name)
        
    def get_system_prompt(self, name: str = "system") -> Optional[str]:
        """
        Get a system prompt template.
        
        Args:
            name: System prompt name
            
        Returns:
            Optional[str]: System prompt content
        """
        template = self.get_template(f"system/{name}")
        if template:
            return template.content
        return None
        
    def get_user_prompt(self, name: str = "default") -> Optional[str]:
        """
        Get a user prompt template.
        
        Args:
            name: User prompt name
            
        Returns:
            Optional[str]: User prompt content
        """
        template = self.get_template(f"user/{name}")
        if template:
            return template.content
        return None
        
    def render_prompt(
        self,
        template_name: str,
        **kwargs,
    ) -> str:
        """
        Render a prompt template.
        
        Args:
            template_name: Name of the template
            **kwargs: Variables for rendering
            
        Returns:
            str: Rendered prompt
            
        Raises:
            ValueError: If template not found
        """
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template not found: {template_name}")
            
        return template.render(**kwargs)
        
    def create_prompt(
        self,
        name: str,
        content: str,
        variables: Optional[List[str]] = None,
        overwrite: bool = False,
    ) -> PromptTemplate:
        """
        Create a new prompt template.
        
        Args:
            name: Template name
            content: Template content
            variables: Required variables
            overwrite: Whether to overwrite existing
            
        Returns:
            PromptTemplate: Created template
            
        Raises:
            ValueError: If template already exists
        """
        if name in self.templates and not overwrite:
            raise ValueError(f"Template already exists: {name}")
            
        template = PromptTemplate(
            name=name,
            content=content,
            variables=variables,
        )
        
        # Validate
        if not template.validate():
            raise ValueError("Invalid template")
            
        self.templates[name] = template
        
        # Save to file
        template_path = self.prompt_dir / f"{name}.txt"
        template_path.parent.mkdir(parents=True, exist_ok=True)
        template_path.write_text(content, encoding="utf-8")
        
        logger.info(f"Created prompt template: {name}")
        return template
        
    def delete_template(self, name: str) -> bool:
        """
        Delete a template.
        
        Args:
            name: Template name
            
        Returns:
            bool: True if deleted
        """
        if name not in self.templates:
            return False
            
        del self.templates[name]
        
        # Delete file
        template_path = self.prompt_dir / f"{name}.txt"
        if template_path.exists():
            template_path.unlink()
            
        logger.info(f"Deleted prompt template: {name}")
        return True
        
    def list_templates(self) -> List[str]:
        """
        List all template names.
        
        Returns:
            List[str]: List of template names
        """
        return list(self.templates.keys())
        
    def export_templates(self, output_path: Path) -> None:
        """
        Export all templates to a file.
        
        Args:
            output_path: Path to output file
        """
        data = {
            name: template.to_dict()
            for name, template in self.templates.items()
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Exported templates to: {output_path}")
        
    def import_templates(self, input_path: Path) -> None:
        """
        Import templates from a file.
        
        Args:
            input_path: Path to input file
        """
        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {input_path}")
            
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        for name, template_data in data.items():
            template = PromptTemplate(
                name=name,
                content=template_data["content"],
                variables=template_data.get("variables", []),
                version=template_data.get("version", "1.0.0"),
            )
            self.templates[name] = template
            
        logger.info(f"Imported {len(data)} templates from: {input_path}")


class PromptValidator:
    """
    Validates prompts for safety and quality.
    """
    
    @staticmethod
    def validate_safety(prompt: str) -> bool:
        """
        Validate prompt for safety.
        
        Args:
            prompt: Prompt to validate
            
        Returns:
            bool: True if safe
        """
        # Check for common injection patterns
        injection_patterns = [
            r"ignore previous instructions",
            r"forget all previous",
            r"system:",
            r"role:",
            r"you are now",
            r"as an ai",
        ]
        
        prompt_lower = prompt.lower()
        for pattern in injection_patterns:
            if pattern in prompt_lower:
                logger.warning(f"Potential injection pattern found: {pattern}")
                return False
                
        return True
        
    @staticmethod
    def validate_length(prompt: str, max_length: int = 4000) -> bool:
        """
        Validate prompt length.
        
        Args:
            prompt: Prompt to validate
            max_length: Maximum length
            
        Returns:
            bool: True if within length limit
        """
        return len(prompt) <= max_length
        
    @staticmethod
    def validate_format(prompt: str) -> bool:
        """
        Validate prompt format.
        
        Args:
            prompt: Prompt to validate
            
        Returns:
            bool: True if valid format
        """
        # Check for balanced braces
        open_braces = prompt.count("{")
        close_braces = prompt.count("}")
        
        if open_braces != close_braces:
            logger.warning("Unbalanced braces in prompt")
            return False
            
        return True
        
    @classmethod
    def validate(cls, prompt: str) -> Dict[str, bool]:
        """
        Run all validations.
        
        Args:
            prompt: Prompt to validate
            
        Returns:
            Dict[str, bool]: Validation results
        """
        return {
            "safe": cls.validate_safety(prompt),
            "length": cls.validate_length(prompt),
            "format": cls.validate_format(prompt),
        }