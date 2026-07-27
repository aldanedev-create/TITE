"""
Prompt management for the AI application.

This module provides prompt template management, validation, and
rendering for AI applications.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, Template
from loguru import logger


class PromptManager:
    """
    Manages prompt templates and their lifecycle.
    
    Attributes:
        prompt_dir: Directory containing prompt files
        templates: Dictionary of loaded templates
    """
    
    def __init__(self, prompt_dir: Optional[Path] = None):
        """
        Initialize the prompt manager.
        
        Args:
            prompt_dir: Directory containing prompt files
        """
        self.prompt_dir = prompt_dir or Path("prompts")
        self.templates: Dict[str, str] = {}
        self._env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        
        # Load templates
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load all templates from the prompt directory."""
        if not self.prompt_dir.exists():
            logger.warning(f"Prompt directory not found: {self.prompt_dir}")
            return
        
        for file_path in self.prompt_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".txt", ".j2", ".md"]:
                try:
                    content = file_path.read_text(encoding="utf-8")
                    name = str(file_path.relative_to(self.prompt_dir))
                    self.templates[name] = content
                    logger.info(f"Loaded prompt template: {name}")
                except Exception as e:
                    logger.error(f"Failed to load template {file_path}: {e}")
    
    def get_template(self, name: str) -> Optional[str]:
        """
        Get a template by name.
        
        Args:
            name: Template name
            
        Returns:
            Optional[str]: Template content or None
        """
        return self.templates.get(name)
    
    def get_system_prompt(self, name: str = "system.txt") -> Optional[str]:
        """
        Get a system prompt template.
        
        Args:
            name: System prompt name
            
        Returns:
            Optional[str]: System prompt content
        """
        return self.get_template(name)
    
    def render_prompt(self, template_name: str, **kwargs) -> str:
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
        content = self.get_template(template_name)
        if not content:
            raise ValueError(f"Template not found: {template_name}")
        
        try:
            template = self._env.from_string(content)
            return template.render(**kwargs)
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {e}")
            return content
    
    def create_prompt(
        self,
        name: str,
        content: str,
        overwrite: bool = False,
    ) -> None:
        """
        Create a new prompt template.
        
        Args:
            name: Template name
            content: Template content
            overwrite: Whether to overwrite existing
            
        Raises:
            ValueError: If template already exists
        """
        if name in self.templates and not overwrite:
            raise ValueError(f"Template already exists: {name}")
        
        self.templates[name] = content
        
        # Save to file
        template_path = self.prompt_dir / name
        template_path.parent.mkdir(parents=True, exist_ok=True)
        template_path.write_text(content, encoding="utf-8")
        
        logger.info(f"Created prompt template: {name}")
    
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
        template_path = self.prompt_dir / name
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


def create_system_prompt(role: str = "assistant") -> str:
    """
    Create a system prompt for the AI assistant.
    
    Args:
        role: Role of the assistant
        
    Returns:
        str: System prompt
    """
    prompts = {
        "assistant": """You are a helpful AI assistant. You provide accurate, helpful, and safe responses. Always be concise and clear in your answers. If you don't know something, say so.""",
        
        "expert": """You are an expert in your field. Provide detailed, accurate, and well-reasoned responses. Support your answers with evidence and examples. Be thorough but clear.""",
        
        "creative": """You are a creative AI assistant. Think outside the box and provide imaginative, original responses. Be engaging and entertaining while still being helpful.""",
        
        "code": """You are an expert programmer. Write clean, efficient, and well-documented code. Explain your reasoning and provide examples. Follow best practices and style guides.""",
        
        "analyst": """You are a data analyst. Provide clear, data-driven insights. Analyze problems systematically. Use evidence to support your conclusions. Be objective and precise.""",
    }
    
    return prompts.get(role, prompts["assistant"])