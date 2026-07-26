"""
Info command for Tite.

This module displays detailed information about the project including
project metadata, dependencies, Git status, and environment details.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from tite.cli.output import print_error, print_info, print_success, print_warning, console, print_table, print_key_value
from tite.constants import ERROR_CODES
from tite.core.config import ConfigManager
from tite.core.environment import EnvironmentManager
from tite.core.git import GitManager
from tite.exceptions import ConfigurationError


def run_info(args: Dict[str, Any]) -> int:
    """
    Execute the 'info' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    output_json = args.get("json", False)
    section = args.get("section")
    
    project_dir = Path.cwd()
    
    # Check if Tite project
    config_path = project_dir / ".tite" / "tite.toml"
    if not config_path.exists():
        print_warning("Not a Tite project. Use 'tite init' first.")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    try:
        # Collect information
        info = collect_project_info(project_dir)
        
        # Filter by section
        if section:
            if section in info:
                info = {section: info[section]}
            else:
                print_error(f"Section '{section}' not found")
                console.print(f"[dim]Available sections: {', '.join(info.keys())}[/dim]")
                return ERROR_CODES["ERROR"]
        
        # Output
        if output_json:
            console.print(json.dumps(info, indent=2, default=str))
        else:
            display_info(info)
        
        return ERROR_CODES["SUCCESS"]
        
    except ConfigurationError as e:
        print_error(f"Configuration error: {str(e)}")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    except Exception as e:
        print_error(f"Failed to get project info: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]


def collect_project_info(project_dir: Path) -> Dict[str, Any]:
    """
    Collect all project information.
    
    Args:
        project_dir: Project directory
        
    Returns:
        Dict[str, Any]: Project information
    """
    info = {}
    
    # Load config
    config_manager = ConfigManager(project_dir)
    config = config_manager.load_config()
    
    # Project info
    info["project"] = {
        "name": config.get("project", {}).get("name", project_dir.name),
        "version": config.get("project", {}).get("version", "0.1.0"),
        "description": config.get("project", {}).get("description", ""),
        "python_version": config.get("project", {}).get("python_version", ">=3.9"),
    }
    
    # Environment info
    env_manager = EnvironmentManager(project_dir)
    info["environment"] = {
        "python_path": str(env_manager.get_python_path()) if env_manager.venv_exists() else None,
        "venv_exists": env_manager.venv_exists(),
        "python_version": env_manager.get_python_version() if env_manager.venv_exists() else None,
        "packages": get_packages_info(env_manager) if env_manager.venv_exists() else None,
    }
    
    # Git info
    git_manager = GitManager(project_dir)
    info["git"] = {
        "initialized": git_manager.is_initialized(),
        "branch": git_manager.get_current_branch() if git_manager.is_initialized() else None,
        "remote": git_manager.get_remote_url() if git_manager.is_initialized() else None,
        "status": git_manager.get_status() if git_manager.is_initialized() else None,
    }
    
    # Config info
    info["config"] = config
    
    # File info
    info["files"] = get_file_info(project_dir)
    
    return info


def get_packages_info(env_manager: EnvironmentManager) -> Dict[str, str]:
    """
    Get information about installed packages.
    
    Args:
        env_manager: Environment manager instance
        
    Returns:
        Dict[str, str]: Package name to version mapping
    """
    try:
        return env_manager.get_installed_packages()
    except Exception:
        return {}


def get_file_info(project_dir: Path) -> Dict[str, Any]:
    """
    Get information about project files.
    
    Args:
        project_dir: Project directory
        
    Returns:
        Dict[str, Any]: File information
    """
    info = {
        "total_files": 0,
        "total_size": 0,
        "python_files": 0,
        "python_lines": 0,
    }
    
    for file_path in project_dir.rglob("*"):
        if file_path.is_file():
            info["total_files"] += 1
            info["total_size"] += file_path.stat().st_size
            
            if file_path.suffix == ".py":
                info["python_files"] += 1
                try:
                    lines = len(file_path.read_text().split("\n"))
                    info["python_lines"] += lines
                except Exception:
                    pass
    
    return info


def display_info(info: Dict[str, Any]) -> None:
    """
    Display project information.
    
    Args:
        info: Project information dictionary
    """
    console.print()
    console.print("[bold cyan]Project Information[/bold cyan]")
    console.print()
    
    # Project section
    if "project" in info:
        console.print("[bold]Project:[/bold]")
        project = info["project"]
        print_key_value("Name", project.get("name", "N/A"))
        print_key_value("Version", project.get("version", "N/A"))
        if project.get("description"):
            print_key_value("Description", project.get("description"))
        print_key_value("Python Version", project.get("python_version", "N/A"))
        console.print()
    
    # Environment section
    if "environment" in info:
        console.print("[bold]Environment:[/bold]")
        env = info["environment"]
        print_key_value("Virtual Environment", "Exists" if env.get("venv_exists") else "Not found")
        if env.get("python_version"):
            print_key_value("Python Version", env.get("python_version"))
        if env.get("python_path"):
            print_key_value("Python Path", env.get("python_path"))
        
        # Packages
        packages = env.get("packages", {})
        if packages:
            console.print(f"  [dim]Packages: {len(packages)}[/dim]")
        console.print()
    
    # Git section
    if "git" in info:
        console.print("[bold]Git:[/bold]")
        git = info["git"]
        print_key_value("Initialized", "Yes" if git.get("initialized") else "No")
        if git.get("branch"):
            print_key_value("Branch", git.get("branch"))
        if git.get("remote"):
            print_key_value("Remote", git.get("remote"))
        console.print()
    
    # Files section
    if "files" in info:
        console.print("[bold]Files:[/bold]")
        files = info["files"]
        print_key_value("Total Files", files.get("total_files", 0))
        print_key_value("Total Size", format_size(files.get("total_size", 0)))
        print_key_value("Python Files", files.get("python_files", 0))
        print_key_value("Python Lines", files.get("python_lines", 0))
        console.print()


def format_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Human-readable size
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB"]
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"