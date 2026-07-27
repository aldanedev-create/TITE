"""
Bootstrap manager for Tite.

This is the main orchestrator used by `tite new` and `tite mode` to
actually create a project: directories, rendered template files,
virtual environment, Git repository, and dependency installation.
"""

import datetime
import getpass
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from tite.constants import MODE_STRUCTURES, PROJECT_STRUCTURE, SUPPORTED_MODES, SUPPORTED_TEMPLATES
from tite.core.config import ConfigManager
from tite.core.environment import EnvironmentManager
from tite.core.filesystem import FileSystemManager
from tite.core.git import GitManager
from tite.core.installer import PackageInstaller
from tite.core.templates import TemplateRenderer
from tite.exceptions import InvalidProjectNameError, TemplateNotFoundError

# Directories/files that are build artifacts, never part of a template
_SKIP_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".git"}
_SKIP_FILE_SUFFIXES = {".pyc", ".pyo"}


class BootstrapManager:
    """
    Orchestrates creation of a new Tite project.

    Attributes:
        project_name: Name of the project
        project_path: Full path where the project will be created
        template: Template name to use
        mode: Optional mode name (data, ai, automation, etc.)
        force: Whether to overwrite an existing directory
        structure: Optional explicit {"directories": [...], "files": [...]}
            override (set externally, e.g. by ModeManager)
        files: Optional explicit {relative_path: content} override
            (set externally, e.g. by ModeManager)
        created_dirs: Directories created by create_structure()
        created_files: Files created by generate_files()
    """

    def __init__(
        self,
        project_name: str,
        project_path: Union[str, Path],
        template: str = "default",
        mode: Optional[str] = None,
        force: bool = False,
    ):
        """
        Initialize the bootstrap manager.

        Args:
            project_name: Name of the project
            project_path: Full path where the project will be created
            template: Template name to use
            mode: Optional mode name
            force: Whether to overwrite an existing directory

        Raises:
            InvalidProjectNameError: If the project name is invalid
        """
        if not project_name or not project_name.strip():
            raise InvalidProjectNameError(project_name or "")

        self.project_name = project_name
        self.project_path = Path(project_path)
        self.template = template or "default"
        self.mode = mode
        self.force = force

        # Optional externally-assigned overrides (see tite.modes.manager)
        self.structure: Optional[Dict[str, List[str]]] = None
        self.files: Optional[Dict[str, str]] = None

        self.created_dirs: List[str] = []
        self.created_files: List[str] = []

        self._tite_pkg_dir = Path(__file__).resolve().parent.parent
        self._templates_root = self._tite_pkg_dir / "templates"

        self._file_manager = FileSystemManager(self.project_path)
        self._renderer = TemplateRenderer()

    # ------------------------------------------------------------------
    # Structure / files
    # ------------------------------------------------------------------

    def create_structure(self) -> None:
        """Create the project directory and its subdirectories."""
        self.created_dirs = []

        self.project_path.mkdir(parents=True, exist_ok=True)
        self.created_dirs.append(str(self.project_path))

        directories = self._resolve_directories()
        for rel_dir in directories:
            full_path = self.project_path / rel_dir
            self._file_manager.create_directory(full_path, exist_ok=True)
            self.created_dirs.append(str(full_path))

    def generate_files(self) -> None:
        """Generate project files from the template (and mode overlay)."""
        self.created_files = []
        context = self._build_context()

        # Explicit override (e.g. set by ModeManager) takes priority.
        if self.files:
            for rel_path, content in self.files.items():
                content = self._maybe_render(content, context)
                target = self._file_manager.write_file(rel_path, content)
                self.created_files.append(str(target))
            return

        # Default: copy the template directory tree.
        template_dir = self._resolve_template_dir(self.template)
        self._copy_tree(template_dir, context)

        # Layer mode-specific extra files on top, if this mode ships any.
        mode_files_dir = self._tite_pkg_dir / "modes" / (self.mode or "") / "files"
        if self.mode and mode_files_dir.is_dir():
            self._copy_tree(mode_files_dir, context)

    # ------------------------------------------------------------------
    # Environment / Git / dependencies
    # ------------------------------------------------------------------

    def create_venv(self) -> None:
        """Create the project's virtual environment."""
        env_manager = EnvironmentManager(self.project_path)
        env_manager.create_venv()

    def init_git(self) -> None:
        """Initialize a Git repository for the project."""
        git_manager = GitManager(self.project_path)
        git_manager.init()

    def install_dependencies(self) -> bool:
        """
        Install base dependencies for the project.

        For mode-based projects created via `tite new --mode ...`, this
        installs the mode's packages. Plain template projects have no
        extra dependencies beyond what's in the generated pyproject.toml.
        """
        if self.mode and self.mode in SUPPORTED_MODES:
            packages = SUPPORTED_MODES[self.mode].get("packages", [])
            if packages:
                return self.install_packages(packages)
        return True

    def install_packages(self, packages: List[str]) -> bool:
        """Install a specific list of packages into the project's venv."""
        installer = PackageInstaller(self.project_path)
        return installer.install_packages(packages)

    def run_post_hooks(self) -> None:
        """
        Run any post-creation hooks.

        No hooks are defined by default; this exists so the CLI's
        creation pipeline always has a final step to call.
        """
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_directories(self) -> List[str]:
        if self.structure and self.structure.get("directories"):
            return list(self.structure["directories"])

        if self.mode and self.mode in MODE_STRUCTURES:
            return list(MODE_STRUCTURES[self.mode]["directories"])

        if self.template in MODE_STRUCTURES:
            return list(MODE_STRUCTURES[self.template]["directories"])

        return list(PROJECT_STRUCTURE["directories"])

    def _resolve_template_dir(self, template: str) -> Path:
        candidate = self._templates_root / template
        if candidate.is_dir():
            return candidate

        default_dir = self._templates_root / "default"
        if default_dir.is_dir():
            return default_dir

        raise TemplateNotFoundError(template)

    def _build_context(self) -> Dict[str, Any]:
        package_name = self.project_name.replace("-", "_").replace(" ", "_").lower()
        now = datetime.datetime.now()
        user = os.environ.get("USER", self._safe_getuser())
        return {
            "project_name": self.project_name,
            "package_name": package_name,
            "project_path": str(self.project_path),
            "template": self.template,
            "mode": self.mode or "",
            "current_year": now.year,
            "current_date": now.strftime("%Y-%m-%d"),
            "user": user,
            "author_name": user,
            "author_email": os.environ.get("EMAIL", f"{user}@example.com"),
            "project_description": f"A {self.template} project created with Tite",
        }

    @staticmethod
    def _safe_getuser() -> str:
        try:
            return getpass.getuser()
        except Exception:
            return "user"

    def _maybe_render(self, content: str, context: Dict[str, Any]) -> str:
        if self._renderer.is_template(content):
            return self._renderer.render(content, context)
        return content

    def _copy_tree(self, source_root: Path, context: Dict[str, Any]) -> None:
        """Copy a template directory tree into the project, rendering
        any file whose content contains Jinja2 syntax, and substituting
        the literal 'package_name' path segment with the real package
        name (used by the library template)."""
        for source_path in source_root.rglob("*"):
            rel_parts = source_path.relative_to(source_root).parts
            if any(part in _SKIP_DIR_NAMES for part in rel_parts):
                continue
            if source_path.is_dir():
                continue
            if source_path.suffix in _SKIP_FILE_SUFFIXES:
                continue

            dest_parts = [
                context["package_name"] if part == "package_name" else part
                for part in rel_parts
            ]

            # The Tite config file always lives at .tite/tite.toml (this is
            # what ConfigManager, doctor, clean, info, and update all look
            # for), regardless of where it sits in the template tree.
            if dest_parts == ["tite.toml"]:
                dest_parts = [".tite", "tite.toml"]

            dest_path = self.project_path.joinpath(*dest_parts)

            try:
                text = source_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, ValueError):
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, dest_path)
                self.created_files.append(str(dest_path))
                continue

            rendered = self._maybe_render(text, context)
            target = self._file_manager.write_file(dest_path, rendered)
            self.created_files.append(str(target))