"""
Init command for Tite.

This module handles initializing Tite in an existing Python project.
"""

from pathlib import Path
from typing import Dict, Any

from tite.cli.output import print_error, print_info, print_success, print_warning, console
from tite.cli.terminal import confirm_action
from tite.constants import ERROR_CODES
from tite.core.filesystem import FileSystemManager
from tite.core.config import ConfigManager
from tite.core.templates import TemplateRenderer
from tite.exceptions import ConfigurationError, FileOperationError


def run_init(args: Dict[str, Any]) -> int:
    """
    Execute the 'init' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    project_path = args.get("path", Path.cwd())
    force = args.get("force", False)
    
    project_dir = Path(project_path)
    
    # Check if directory exists
    if not project_dir.exists():
        print_error(f"Directory not found: {project_dir}")
        return ERROR_CODES["FILE_OPERATION_ERROR"]
    
    # Check if already a Tite project
    config_path = project_dir / ".tite" / "tite.toml"
    if config_path.exists() and not force:
        print_warning("Tite is already initialized in this directory")
        if not confirm_action("Reinitialize Tite?", default=False):
            print_info("Initialization cancelled")
            return ERROR_CODES["SUCCESS"]
    
    # Check if it's a Python project
    has_python = False
    has_pyproject = False
    has_setup = False
    
    for file in project_dir.iterdir():
        if file.suffix == ".py":
            has_python = True
        if file.name == "pyproject.toml":
            has_pyproject = True
        if file.name in ("setup.py", "setup.cfg"):
            has_setup = True
    
    if not has_python and not has_pyproject and not has_setup:
        print_warning("No Python files or project configuration found")
        if not confirm_action("Continue initialization anyway?", default=False):
            print_info("Initialization cancelled")
            return ERROR_CODES["SUCCESS"]
    
    console.print()
    console.print(f"[bold]Initializing Tite in:[/bold] {project_dir}")
    console.print()
    
    try:
        # Create Tite configuration
        config_manager = ConfigManager(project_dir)
        
        # Detect project info
        project_name = project_dir.name
        python_version = detect_python_version(project_dir)
        
        # Create Tite config
        config = {
            "project": {
                "name": project_name,
                "version": "0.1.0",
                "python_version": python_version,
            },
            "dev": {
                "command": detect_dev_command(project_dir),
                "port": 8000,
                "host": "127.0.0.1",
            },
            "watcher": {
                "paths": ["src", "tests"],
                "extensions": [".py"],
            },
        }
        
        config_manager.create_config(config)
        
        # Create .tite directory
        tite_dir = project_dir / ".tite"
        tite_dir.mkdir(exist_ok=True)
        
        # Create tite.toml
        config_manager.save_config()
        
        # Create .gitignore if it doesn't exist
        gitignore_path = project_dir / ".gitignore"
        if not gitignore_path.exists():
            renderer = TemplateRenderer()
            gitignore_content = renderer.render_gitignore(project_name)
            gitignore_path.write_text(gitignore_content)
            print_info("Created .gitignore")
        
        # Check if virtual environment exists
        venv_path = project_dir / ".venv"
        if not venv_path.exists():
            print_warning("No virtual environment found")
            if confirm_action("Create virtual environment?", default=True):
                from tite.core.environment import EnvironmentManager
                env_manager = EnvironmentManager(project_dir)
                env_manager.create_venv()
                print_success("Virtual environment created")
        
        # Check if Git is initialized
        git_path = project_dir / ".git"
        if not git_path.exists():
            print_warning("Git repository not found")
            if confirm_action("Initialize Git repository?", default=True):
                from tite.core.git import GitManager
                git_manager = GitManager(project_dir)
                git_manager.init()
                print_success("Git repository initialized")
        
        console.print()
        print_success(f"Tite initialized successfully in {project_dir}")
        console.print()
        
        console.print("[bold]Next steps:[/bold]")
        console.print("  [cyan]tite config --list[/cyan]  # View configuration")
        console.print("  [cyan]tite doctor[/cyan]  # Check project health")
        console.print("  [cyan]tite dev[/cyan]  # Start development server")
        console.print()
        
        return ERROR_CODES["SUCCESS"]
        
    except ConfigurationError as e:
        print_error(f"Configuration error: {str(e)}")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    except FileOperationError as e:
        print_error(f"File operation error: {str(e)}")
        return ERROR_CODES["FILE_OPERATION_ERROR"]
    
    except Exception as e:
        print_error(f"Failed to initialize Tite: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]


def detect_python_version(project_dir: Path) -> str:
    """
    Detect Python version from project.
    
    Args:
        project_dir: Project directory
        
    Returns:
        str: Python version string
    """
    # Check pyproject.toml
    pyproject_path = project_dir / "pyproject.toml"
    if pyproject_path.exists():
        try:
            import tomllib
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                requires = data.get("project", {}).get("requires-python", "")
                if requires:
                    return requires
        except Exception:
            pass
    
    # Check .python-version
    python_version_path = project_dir / ".python-version"
    if python_version_path.exists():
        try:
            return python_version_path.read_text().strip()
        except Exception:
            pass
    
    # Default
    return ">=3.9"


def detect_dev_command(project_dir: Path) -> str:
    """
    Detect development command.
    
    Args:
        project_dir: Project directory
        
    Returns:
        str: Development command
    """
    # Check for main.py
    if (project_dir / "src" / "main.py").exists():
        return "python src/main.py"
    
    # Check for app.py
    if (project_dir / "src" / "app.py").exists():
        return "python src/app.py"
    
    # Check for manage.py (Django)
    if (project_dir / "manage.py").exists():
        return "python manage.py runserver"
    
    # Default
    return "python src/main.py"