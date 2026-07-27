"""
Core template renderer for Tite.

Provides simple template rendering used directly by CLI commands
(e.g. rendering a .gitignore for `tite init`), on top of the same
Jinja2-based engine used by the blueprint system.
"""

from typing import Any, Dict, Optional

from tite.blueprint.templates import BlueprintTemplateEngine
from tite.constants import DEFAULT_EDITOR_CONFIG, DEFAULT_GIT_IGNORE


class TemplateRenderer:
    """
    Renders individual template snippets (gitignore, editorconfig, etc.)
    and arbitrary Jinja2 template strings.
    """

    def __init__(self) -> None:
        self._engine: Optional[BlueprintTemplateEngine] = None

    @property
    def engine(self) -> BlueprintTemplateEngine:
        """Lazily-constructed Jinja2 template engine (avoids filesystem
        loader setup unless it's actually needed)."""
        if self._engine is None:
            self._engine = BlueprintTemplateEngine()
        return self._engine

    def render_gitignore(self, project_name: str) -> str:
        """
        Render a .gitignore file for a project.

        Args:
            project_name: Name of the project (unused in the default
                template, kept for API symmetry / future customization)

        Returns:
            str: .gitignore content
        """
        return DEFAULT_GIT_IGNORE.lstrip("\n")

    def render_editorconfig(self) -> str:
        """Render a .editorconfig file."""
        return DEFAULT_EDITOR_CONFIG.lstrip("\n")

    def render(self, content: str, context: Dict[str, Any]) -> str:
        """
        Render arbitrary template content with the given context.

        Args:
            content: Template content (Jinja2 syntax)
            context: Variables available to the template

        Returns:
            str: Rendered content
        """
        return self.engine.render(content, context)

    def is_template(self, content: str) -> bool:
        """Check whether content contains Jinja2 template syntax."""
        return "{{" in content or "{%" in content