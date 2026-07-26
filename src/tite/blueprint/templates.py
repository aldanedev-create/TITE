"""
Blueprint templates for Tite.

This module provides template rendering for blueprints using
Jinja2 with custom filters and functions.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

from tite.exceptions import TemplateNotFoundError, TemplateRenderError


class BlueprintTemplateEngine:
    """
    Template engine for blueprint files.
    
    This class handles rendering templates with Jinja2 and
    provides custom filters and functions for blueprints.
    
    Attributes:
        environment: Jinja2 environment
        template_dir: Template directory
    """
    
    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize the template engine.
        
        Args:
            template_dir: Path to template directory
        """
        if template_dir is None:
            # Find templates directory relative to this file
            current_file = Path(__file__).parent.parent.parent
            template_dir = current_file / "templates"
            
        self.template_dir = Path(template_dir)
        
        # Create Jinja2 environment
        self.environment = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        
        # Add custom filters
        self.environment.filters["snake_case"] = self._to_snake_case
        self.environment.filters["camel_case"] = self._to_camel_case
        self.environment.filters["kebab_case"] = self._to_kebab_case
        self.environment.filters["title_case"] = self._to_title_case
        self.environment.filters["pluralize"] = self._pluralize
        self.environment.filters["upper"] = str.upper
        self.environment.filters["lower"] = str.lower
        
        # Add custom functions
        self.environment.globals.update({
            "now": self._get_current_time,
            "env": self._get_env_var,
            "file_exists": self._file_exists,
            "dir_exists": self._dir_exists,
        })
        
    def render(self, template_content: str, context: Dict[str, Any]) -> str:
        """
        Render template content.
        
        Args:
            template_content: Template content
            context: Template context
            
        Returns:
            str: Rendered content
        """
        try:
            template = self.environment.from_string(template_content)
            return template.render(**context)
        except Exception as e:
            raise TemplateRenderError("blueprint_template", str(e))
            
    def render_file(self, template_path: str, context: Dict[str, Any]) -> str:
        """
        Render a template file.
        
        Args:
            template_path: Path to template file
            context: Template context
            
        Returns:
            str: Rendered content
            
        Raises:
            TemplateNotFoundError: If template is not found
            TemplateRenderError: If rendering fails
        """
        try:
            template = self.environment.get_template(template_path)
            return template.render(**context)
        except TemplateNotFound:
            raise TemplateNotFoundError(template_path)
        except Exception as e:
            raise TemplateRenderError(template_path, str(e))
            
    def render_from_string(self, content: str, context: Dict[str, Any]) -> str:
        """
        Render template from string.
        
        Args:
            content: Template content
            context: Template context
            
        Returns:
            str: Rendered content
        """
        try:
            template = self.environment.from_string(content)
            return template.render(**context)
        except Exception as e:
            raise TemplateRenderError("string_template", str(e))
            
    @staticmethod
    def _to_snake_case(text: str) -> str:
        """Convert text to snake_case."""
        import re
        text = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", text)
        text = re.sub(r"[-\s]", "_", text)
        return text.lower()
        
    @staticmethod
    def _to_camel_case(text: str) -> str:
        """Convert text to camelCase."""
        parts = text.replace("-", "_").replace(" ", "_").split("_")
        if len(parts) <= 1:
            return text
        return parts[0] + "".join(p.title() for p in parts[1:])
        
    @staticmethod
    def _to_kebab_case(text: str) -> str:
        """Convert text to kebab-case."""
        import re
        text = re.sub(r"(?<=[a-z])(?=[A-Z])", "-", text)
        text = re.sub(r"[_\s]", "-", text)
        return text.lower()
        
    @staticmethod
    def _to_title_case(text: str) -> str:
        """Convert text to Title Case."""
        return text.replace("-", " ").replace("_", " ").title()
        
    @staticmethod
    def _pluralize(text: str, count: int = 0) -> str:
        """Pluralize a word."""
        if count == 1:
            return text
        if text.endswith("y"):
            return text[:-1] + "ies"
        if text.endswith("s") or text.endswith("x") or text.endswith("z"):
            return text + "es"
        return text + "s"
        
    @staticmethod
    def _get_current_time() -> str:
        """Get current time string."""
        import datetime
        return datetime.datetime.now().isoformat()
        
    @staticmethod
    def _get_env_var(name: str, default: str = "") -> str:
        """Get environment variable."""
        return os.environ.get(name, default)
        
    def _file_exists(self, path: str) -> bool:
        """Check if file exists."""
        return Path(path).exists()
        
    def _dir_exists(self, path: str) -> bool:
        """Check if directory exists."""
        return Path(path).exists()


class BlueprintTemplate:
    """
    Blueprint template definition.
    
    This class represents a blueprint template with its content
    and metadata.
    
    Attributes:
        name: Template name
        content: Template content
        description: Template description
    """
    
    def __init__(
        self,
        name: str,
        content: str,
        description: str = "",
    ):
        """
        Initialize the blueprint template.
        
        Args:
            name: Template name
            content: Template content
            description: Template description
        """
        self.name = name
        self.content = content
        self.description = description
        
    def render(self, context: Dict[str, Any]) -> str:
        """
        Render the template.
        
        Args:
            context: Template context
            
        Returns:
            str: Rendered content
        """
        engine = BlueprintTemplateEngine()
        return engine.render_from_string(self.content, context)


class TemplateContext:
    """
    Template context builder.
    
    This class helps build template contexts with common variables.
    
    Attributes:
        context: Template context dictionary
    """
    
    def __init__(self, variables: Optional[Dict[str, Any]] = None):
        """
        Initialize the template context.
        
        Args:
            variables: Initial variables
        """
        self.context = variables or {}
        
    def add_project_vars(self, project_name: str, project_path: Path) -> 'TemplateContext':
        """
        Add project variables.
        
        Args:
            project_name: Project name
            project_path: Project path
            
        Returns:
            TemplateContext: Self for chaining
        """
        self.context.update({
            "project_name": project_name,
            "project_path": str(project_path),
            "package_name": project_name.replace("-", "_"),
        })
        return self
        
    def add_user_vars(self) -> 'TemplateContext':
        """
        Add user variables.
        
        Returns:
            TemplateContext: Self for chaining
        """
        import getpass
        import os
        
        self.context.update({
            "user": os.environ.get("USER", getpass.getuser()),
            "email": os.environ.get("EMAIL", f"{getpass.getuser()}@example.com"),
        })
        return self
        
    def add_time_vars(self) -> 'TemplateContext':
        """
        Add time variables.
        
        Returns:
            TemplateContext: Self for chaining
        """
        import datetime
        
        self.context.update({
            "current_year": datetime.datetime.now().year,
            "current_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "current_time": datetime.datetime.now().strftime("%H:%M:%S"),
            "datetime": datetime.datetime.now().isoformat(),
        })
        return self
        
    def add_git_vars(self, project_path: Path) -> 'TemplateContext':
        """
        Add Git variables.
        
        Args:
            project_path: Project path
            
        Returns:
            TemplateContext: Self for chaining
        """
        git_path = project_path / ".git"
        if git_path.exists():
            # Try to get git info
            try:
                import subprocess
                result = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    self.context["git_branch"] = result.stdout.strip()
                    
                result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    self.context["git_commit"] = result.stdout.strip()[:8]
                    
            except Exception:
                pass
                
        return self
        
    def build(self) -> Dict[str, Any]:
        """
        Build the context dictionary.
        
        Returns:
            Dict[str, Any]: Template context
        """
        return self.context