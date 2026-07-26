"""
Mode command for Tite.

This module handles the creation of projects using pre-configured modes
and listing available modes.
"""

from pathlib import Path
from typing import Dict, Any, Optional

from tite.cli.output import print_error, print_info, print_success, console
from tite.cli.progress import ProgressContext
from tite.constants import ERROR_CODES, SUPPORTED_MODES
from tite.core.bootstrap import BootstrapManager
from tite.exceptions import ModeNotFoundError, ProjectExistsError


def run_mode(args: Dict[str, Any]) -> int:
    """
    Execute the 'mode' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    mode_name = args.get("mode")
    project_name = args.get("name")
    list_modes = args.get("list", False)
    project_path = args.get("path", Path.cwd())
    force = args.get("force", False)
    
    # List modes
    if list_modes or mode_name == "list":
        return list_available_modes()
    
    # Validate mode
    if not mode_name:
        print_error("Mode name is required")
        print_info("Use 'tite mode list' to see available modes")
        return ERROR_CODES["MODE_NOT_FOUND"]
    
    if mode_name not in SUPPORTED_MODES:
        print_error(f"Mode '{mode_name}' not found")
        print_info("Use 'tite mode list' to see available modes")
        return ERROR_CODES["MODE_NOT_FOUND"]
    
    # Validate project name
    if not project_name:
        print_error("Project name is required")
        return ERROR_CODES["INVALID_PROJECT_NAME"]
    
    # Get mode info
    mode_info = SUPPORTED_MODES[mode_name]
    template = mode_info.get("template", "default")
    
    # Build project path
    project_dir = Path(project_path) / project_name
    
    # Check if project already exists
    if project_dir.exists() and not force:
        print_error(f"Project '{project_name}' already exists at {project_dir}")
        print_info("Use --force to overwrite")
        return ERROR_CODES["PROJECT_EXISTS"]
    
    # Show what we're about to do
    console.print()
    console.print(f"[bold]Creating project with mode:[/bold] {mode_name}")
    console.print(f"[bold]Mode description:[/bold] {mode_info.get('description', '')}")
    console.print(f"[bold]Project:[/bold] {project_name}")
    console.print(f"[bold]Location:[/bold] {project_dir}")
    console.print()
    
    try:
        # Create project with progress
        with ProgressContext(f"Creating {mode_name} project {project_name}", total=5) as progress:
            progress.update(description="Initializing project structure...")
            
            # Create bootstrap manager
            bootstrap = BootstrapManager(
                project_name=project_name,
                project_path=project_dir,
                template=template,
                mode=mode_name,
                force=force,
            )
            
            progress.update(advance=1, description="Creating directories...")
            bootstrap.create_structure()
            
            progress.update(advance=1, description="Generating files...")
            bootstrap.generate_files()
            
            progress.update(advance=1, description="Creating virtual environment...")
            bootstrap.create_venv()
            
            progress.update(advance=1, description="Installing mode packages...")
            
            # Install mode-specific packages
            packages = mode_info.get("packages", [])
            if packages:
                bootstrap.install_packages(packages)
            
            progress.update(advance=1, description="Finalizing setup...")
            bootstrap.run_post_hooks()
        
        # Show success message
        console.print()
        print_success(f"Project '{project_name}' created with {mode_name} mode!")
        console.print()
        
        # Show next steps
        console.print("[bold]Next steps:[/bold]")
        console.print(f"  [cyan]cd {project_name}[/cyan]")
        console.print("  [cyan]source .venv/bin/activate[/cyan]  # On Windows: .venv\\Scripts\\activate")
        console.print("  [cyan]tite dev[/cyan]  # Start development server")
        console.print()
        
        # Show mode-specific packages
        if packages:
            console.print("[dim]Mode packages installed:[/dim]")
            for pkg in packages:
                console.print(f"  [dim]- {pkg}[/dim]")
        
        return ERROR_CODES["SUCCESS"]
        
    except ModeNotFoundError as e:
        print_error(str(e))
        return ERROR_CODES["MODE_NOT_FOUND"]
    
    except ProjectExistsError as e:
        print_error(str(e))
        return ERROR_CODES["PROJECT_EXISTS"]
    
    except Exception as e:
        print_error(f"Failed to create project: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]


def list_available_modes() -> int:
    """
    List all available modes.
    
    Returns:
        int: Exit code
    """
    console.print()
    console.print("[bold cyan]Available Tite Modes:[/bold cyan]")
    console.print()
    
    for mode_name, mode_info in SUPPORTED_MODES.items():
        if mode_name == "default":
            continue
        
        description = mode_info.get("description", "")
        template = mode_info.get("template", "default")
        packages = mode_info.get("packages", [])
        
        console.print(f"[bold]{mode_name}[/bold]")
        console.print(f"  [dim]Description:[/dim] {description}")
        console.print(f"  [dim]Template:[/dim] {template}")
        if packages:
            console.print(f"  [dim]Packages:[/dim] {', '.join(packages)}")
        console.print()
    
    console.print("[dim]Usage: tite mode <mode> <project-name>[/dim]")
    console.print("[dim]Example: tite mode data sales-analysis[/dim]")
    
    return ERROR_CODES["SUCCESS"]