"""
Update command for Tite.

This module handles updating project dependencies and configuration.
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

from tite.cli.output import print_error, print_info, print_success, print_warning, console
from tite.cli.progress import Spinner, ProgressContext
from tite.constants import ERROR_CODES
from tite.core.config import ConfigManager
from tite.core.environment import EnvironmentManager
from tite.exceptions import ConfigurationError, EnvironmentError


def run_update(args: Dict[str, Any]) -> int:
    """
    Execute the 'update' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    package = args.get("package")
    major = args.get("major", False)
    dry_run = args.get("dry_run", False)
    
    project_dir = Path.cwd()
    
    # Check if Tite project
    config_path = project_dir / ".tite" / "tite.toml"
    if not config_path.exists():
        print_warning("Not a Tite project. Use 'tite init' first.")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    console.print()
    console.print("[bold cyan]Tite Update[/bold cyan]")
    if dry_run:
        console.print("[dim]Dry run mode - no changes will be made[/dim]")
    console.print()
    
    try:
        # Load config
        config_manager = ConfigManager(project_dir)
        config = config_manager.load_config()
        
        # Get project name
        project_name = config.get("project", {}).get("name", project_dir.name)
        
        # Check virtual environment
        env_manager = EnvironmentManager(project_dir)
        if not env_manager.venv_exists():
            print_warning("Virtual environment not found")
            from tite.cli.terminal import confirm_action
            if confirm_action("Create virtual environment?", default=True):
                env_manager.create_venv()
            else:
                return ERROR_CODES["ENVIRONMENT_ERROR"]
        
        # Activate virtual environment
        python_path = env_manager.get_python_path()
        pip_path = env_manager.get_pip_path()
        
        if not python_path.exists() or not pip_path.exists():
            print_error("Virtual environment is incomplete")
            return ERROR_CODES["ENVIRONMENT_ERROR"]
        
        # Get current dependencies
        current_deps = get_installed_packages(pip_path)
        
        # Update dependencies
        if package:
            # Update specific package
            update_package(pip_path, package, major, dry_run)
        else:
            # Update all dependencies
            update_all_dependencies(pip_path, config, dry_run)
        
        # Update lock file
        if not dry_run:
            update_lock_file(pip_path, project_dir)
        
        # Show updated packages
        console.print()
        updated_deps = get_installed_packages(pip_path)
        display_changes(current_deps, updated_deps)
        
        print_success("Dependencies updated successfully")
        return ERROR_CODES["SUCCESS"]
        
    except ConfigurationError as e:
        print_error(f"Configuration error: {str(e)}")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    except EnvironmentError as e:
        print_error(f"Environment error: {str(e)}")
        return ERROR_CODES["ENVIRONMENT_ERROR"]
    
    except Exception as e:
        print_error(f"Failed to update: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]


def get_installed_packages(pip_path: Path) -> Dict[str, str]:
    """
    Get installed packages and their versions.
    
    Args:
        pip_path: Path to pip executable
        
    Returns:
        Dict[str, str]: Package name to version mapping
    """
    try:
        result = subprocess.run(
            [str(pip_path), "list", "--format=freeze"],
            capture_output=True,
            text=True,
            check=True,
        )
        
        packages = {}
        for line in result.stdout.strip().split("\n"):
            if "==" in line:
                name, version = line.split("==", 1)
                packages[name.lower()] = version
        
        return packages
        
    except subprocess.CalledProcessError:
        return {}


def update_package(pip_path: Path, package: str, major: bool, dry_run: bool) -> None:
    """
    Update a specific package.
    
    Args:
        pip_path: Path to pip executable
        package: Package name
        major: Allow major version updates
        dry_run: Dry run mode
    """
    print_info(f"Updating package: {package}")
    
    if major:
        cmd = [str(pip_path), "install", "--upgrade", package]
    else:
        cmd = [str(pip_path), "install", "--upgrade", f"{package}<{get_next_major(package)}"]
    
    if dry_run:
        console.print(f"[dim]Would run: {' '.join(cmd)}[/dim]")
        return
    
    try:
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        print_success(f"Updated {package}")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to update {package}: {e.stderr}")


def update_all_dependencies(pip_path: Path, config: Dict[str, Any], dry_run: bool) -> None:
    """
    Update all dependencies.
    
    Args:
        pip_path: Path to pip executable
        config: Configuration dictionary
        dry_run: Dry run mode
    """
    # Get dependencies from config
    deps = config.get("project", {}).get("dependencies", {})
    
    if not deps:
        print_info("No dependencies found to update")
        return
    
    print_info(f"Updating {len(deps)} dependencies...")
    
    with ProgressContext("Updating dependencies", total=len(deps)) as progress:
        for dep, version in deps.items():
            progress.update(description=f"Updating {dep}...")
            
            if dry_run:
                console.print(f"[dim]Would update: {dep} {version}[/dim]")
            else:
                try:
                    subprocess.run(
                        [str(pip_path), "install", "--upgrade", dep],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                except subprocess.CalledProcessError:
                    print_warning(f"Failed to update {dep}")
            
            progress.update(advance=1)


def update_lock_file(pip_path: Path, project_dir: Path) -> None:
    """
    Update the lock file.
    
    Args:
        pip_path: Path to pip executable
        project_dir: Project directory
    """
    lock_path = project_dir / "requirements.txt"
    
    try:
        subprocess.run(
            [str(pip_path), "freeze", ">", str(lock_path)],
            shell=True,
            check=True,
            capture_output=True,
        )
        print_info(f"Updated lock file: {lock_path}")
    except subprocess.CalledProcessError:
        print_warning("Failed to update lock file")


def get_next_major(package: str) -> str:
    """
    Get the next major version constraint.
    
    Args:
        package: Package name
        
    Returns:
        str: Version constraint
    """
    # This is a simplified version - in practice, you'd query PyPI
    return "100.0.0"


def display_changes(old: Dict[str, str], new: Dict[str, str]) -> None:
    """
    Display changes between old and new packages.
    
    Args:
        old: Old package versions
        new: New package versions
    """
    added = set(new.keys()) - set(old.keys())
    removed = set(old.keys()) - set(new.keys())
    updated = set(new.keys()) & set(old.keys())
    
    changed = []
    for pkg in updated:
        if old.get(pkg) != new.get(pkg):
            changed.append((pkg, old.get(pkg), new.get(pkg)))
    
    if added:
        console.print("[bold]Added:[/bold]")
        for pkg in added:
            console.print(f"  [green]+ {pkg} {new.get(pkg)}[/green]")
    
    if removed:
        console.print("[bold]Removed:[/bold]")
        for pkg in removed:
            console.print(f"  [red]- {pkg} {old.get(pkg)}[/red]")
    
    if changed:
        console.print("[bold]Updated:[/bold]")
        for pkg, old_v, new_v in changed:
            console.print(f"  [yellow]~ {pkg} {old_v} -> {new_v}[/yellow]")
    
    if not added and not removed and not changed:
        console.print("[dim]No changes[/dim]")