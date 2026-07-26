"""
New project command for Tite.

This module handles the creation of new Python projects with Tite.
"""

import shutil
from pathlib import Path
from typing import Dict, Any, Optional

from tite.cli.output import print_error, print_info, print_success, print_warning, console
from tite.cli.progress import Spinner, ProgressContext
from tite.constants import ERROR_CODES, DEFAULT_TEMPLATE, SUPPORTED_MODES
from tite.core.bootstrap import BootstrapManager
from tite.core.filesystem import FileSystemManager
from tite.core.templates import TemplateRenderer
from tite.core.config import ConfigManager
from tite.exceptions import (
    ProjectExistsError,
    InvalidProjectNameError,
    TemplateNotFoundError,
    ModeNotFoundError,
)


def run_new(args: Dict[str, Any]) -> int:
    """
    Execute the 'new' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    project_name = args.get("name")
    template = args.get("template", DEFAULT_TEMPLATE)
    mode = args.get("mode")
    project_path = args.get("path", Path.cwd())
    force = args.get("force", False)
    no_git = args.get("no_git", False)
    no_venv = args.get("no_venv", False)
    
    # Validate project name
    if not project_name:
        print_error("Project name is required")
        return ERROR_CODES["INVALID_PROJECT_NAME"]
    
    # Handle mode if specified
    if mode:
        if mode not in SUPPORTED_MODES:
            print_error(f"Mode '{mode}' not found")
            return ERROR_CODES["MODE_NOT_FOUND"]
        
        # Override template with mode's template
        template = SUPPORTED_MODES[mode].get("template", template)
        print_info(f"Using mode: {mode}")
    
    # Build full project path
    project_dir = Path(project_path) / project_name
    
    # Check if project already exists
    if project_dir.exists() and not force:
        print_error(f"Project '{project_name}' already exists at {project_dir}")
        print_info("Use --force to overwrite")
        return ERROR_CODES["PROJECT_EXISTS"]
    
    # Show what we're about to do
    console.print()
    console.print(f"[bold]Creating project:[/bold] {project_name}")
    console.print(f"[bold]Location:[/bold] {project_dir}")
    console.print(f"[bold]Template:[/bold] {template}")
    if mode:
        console.print(f"[bold]Mode:[/bold] {mode}")
    console.print()
    
    try:
        # Create project with progress
        with ProgressContext(f"Creating project {project_name}", total=6) as progress:
            progress.update(description="Initializing project structure...")
            
            # Create bootstrap manager
            bootstrap = BootstrapManager(
                project_name=project_name,
                project_path=project_dir,
                template=template,
                mode=mode,
                force=force,
            )
            
            progress.update(advance=1, description="Creating directories...")
            
            # Create project structure
            bootstrap.create_structure()
            
            progress.update(advance=1, description="Generating files...")
            
            # Generate files from templates
            bootstrap.generate_files()
            
            progress.update(advance=1, description="Creating virtual environment...")
            
            # Create virtual environment
            if not no_venv:
                bootstrap.create_venv()
            
            progress.update(advance=1, description="Initializing Git repository...")
            
            # Initialize Git
            if not no_git:
                bootstrap.init_git()
            
            progress.update(advance=1, description="Installing dependencies...")
            
            # Install base dependencies
            bootstrap.install_dependencies()
            
            progress.update(advance=1, description="Finalizing setup...")
            
            # Run post-creation hooks
            bootstrap.run_post_hooks()
        
        # Show success message
        console.print()
        print_success(f"Project '{project_name}' created successfully!")
        console.print()
        
        # Show next steps
        console.print("[bold]Next steps:[/bold]")
        console.print(f"  [cyan]cd {project_name}[/cyan]")
        if not no_venv:
            console.print("  [cyan]source .venv/bin/activate[/cyan]  # On Windows: .venv\\Scripts\\activate")
        console.print("  [cyan]tite dev[/cyan]  # Start development server")
        console.print()
        console.print("[dim]For more information: tite --help[/dim]")
        
        return ERROR_CODES["SUCCESS"]
        
    except ProjectExistsError as e:
        print_error(str(e))
        return ERROR_CODES["PROJECT_EXISTS"]
    
    except InvalidProjectNameError as e:
        print_error(str(e))
        return ERROR_CODES["INVALID_PROJECT_NAME"]
    
    except TemplateNotFoundError as e:
        print_error(str(e))
        return ERROR_CODES["TEMPLATE_NOT_FOUND"]
    
    except ModeNotFoundError as e:
        print_error(str(e))
        return ERROR_CODES["MODE_NOT_FOUND"]
    
    except Exception as e:
        print_error(f"Failed to create project: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]