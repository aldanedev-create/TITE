"""
Environment command for Tite.

This module displays detailed information about the Python environment
including virtual environment status, Python version, and installed packages.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

from tite.cli.output import print_error, print_info, print_warning, console, print_table, print_key_value
from tite.constants import ERROR_CODES
from tite.core.environment import EnvironmentManager
from tite.exceptions import EnvironmentError


def run_env(args: Dict[str, Any]) -> int:
    """
    Execute the 'env' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    output_json = args.get("json", False)
    show_packages = args.get("show_packages", False)
    show_vars = args.get("show_vars", False)
    
    project_dir = Path.cwd()
    
    console.print()
    console.print("[bold cyan]Environment Information[/bold cyan]")
    console.print()
    
    try:
        env_manager = EnvironmentManager(project_dir)
        
        # Collect environment information
        env_info = collect_environment_info(env_manager, show_packages, show_vars)
        
        # Output
        if output_json:
            console.print(json.dumps(env_info, indent=2, default=str))
        else:
            display_environment_info(env_info, show_packages, show_vars)
        
        return ERROR_CODES["SUCCESS"]
        
    except EnvironmentError as e:
        print_error(f"Environment error: {str(e)}")
        return ERROR_CODES["ENVIRONMENT_ERROR"]
    
    except Exception as e:
        print_error(f"Failed to get environment info: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]


def collect_environment_info(
    env_manager: EnvironmentManager,
    show_packages: bool = False,
    show_vars: bool = False,
) -> Dict[str, Any]:
    """
    Collect environment information.
    
    Args:
        env_manager: Environment manager instance
        show_packages: Include package information
        show_vars: Include environment variables
        
    Returns:
        Dict[str, Any]: Environment information
    """
    info = {
        "python": {},
        "virtualenv": {},
        "system": {},
        "packages": {},
        "variables": {},
    }
    
    # Python information
    info["python"] = {
        "version": sys.version,
        "version_info": {
            "major": sys.version_info.major,
            "minor": sys.version_info.minor,
            "micro": sys.version_info.micro,
        },
        "executable": sys.executable,
        "path": sys.path,
    }
    
    # Virtual environment
    info["virtualenv"] = {
        "exists": env_manager.venv_exists(),
        "path": str(env_manager.venv_path) if env_manager.venv_exists() else None,
        "active": env_manager.is_venv_active(),
        "python_path": str(env_manager.get_python_path()) if env_manager.venv_exists() else None,
    }
    
    # System information
    import platform
    info["system"] = {
        "platform": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
    }
    
    # Packages
    if show_packages:
        try:
            info["packages"] = env_manager.get_installed_packages()
        except Exception:
            info["packages"] = {}
    
    # Environment variables
    if show_vars:
        # Filter environment variables
        filtered_vars = {}
        for key, value in os.environ.items():
            # Exclude sensitive variables
            if any(sensitive in key.lower() for sensitive in ["key", "token", "secret", "password", "auth"]):
                filtered_vars[key] = "***"
            else:
                filtered_vars[key] = value
        info["variables"] = filtered_vars
    
    return info


def display_environment_info(
    info: Dict[str, Any],
    show_packages: bool = False,
    show_vars: bool = False,
) -> None:
    """
    Display environment information.
    
    Args:
        info: Environment information dictionary
        show_packages: Show packages
        show_vars: Show environment variables
    """
    # Python info
    console.print("[bold]Python:[/bold]")
    python = info.get("python", {})
    print_key_value("Version", python.get("version", "N/A"))
    print_key_value("Executable", python.get("executable", "N/A"))
    print_key_value("Path Count", len(python.get("path", [])))
    console.print()
    
    # Virtual environment
    console.print("[bold]Virtual Environment:[/bold]")
    venv = info.get("virtualenv", {})
    status = "Active" if venv.get("active") else "Exists" if venv.get("exists") else "Not found"
    print_key_value("Status", status)
    if venv.get("path"):
        print_key_value("Path", venv.get("path"))
    if venv.get("python_path"):
        print_key_value("Python Path", venv.get("python_path"))
    console.print()
    
    # System info
    console.print("[bold]System:[/bold]")
    system = info.get("system", {})
    print_key_value("Platform", system.get("platform", "N/A"))
    print_key_value("Release", system.get("release", "N/A"))
    print_key_value("Machine", system.get("machine", "N/A"))
    print_key_value("Processor", system.get("processor", "N/A"))
    print_key_value("Hostname", system.get("hostname", "N/A"))
    console.print()
    
    # Packages
    if show_packages:
        console.print("[bold]Installed Packages:[/bold]")
        packages = info.get("packages", {})
        if packages:
            # Sort by name
            sorted_packages = sorted(packages.items())
            
            # Display in columns
            table_data = []
            for name, version in sorted_packages:
                table_data.append([name, version])
            
            print_table(
                headers=["Package", "Version"],
                rows=table_data,
            )
        else:
            console.print("  [dim]No packages found[/dim]")
        console.print()
    
    # Environment variables
    if show_vars:
        console.print("[bold]Environment Variables:[/bold]")
        variables = info.get("variables", {})
        
        # Show only first 20 variables
        for i, (key, value) in enumerate(sorted(variables.items())):
            if i >= 20:
                console.print(f"  [dim]... and {len(variables) - 20} more[/dim]")
                break
            print_key_value(key, value, indent=2)
        
        if not variables:
            console.print("  [dim]No environment variables[/dim]")
        console.print()
    
    # Summary
    console.print("[bold]Summary:[/bold]")
    console.print(f"  Python: {info.get('python', {}).get('version', 'N/A').split()[0]}")
    console.print(f"  Virtual Environment: {info.get('virtualenv', {}).get('status', 'N/A')}")
    console.print(f"  Platform: {info.get('system', {}).get('platform', 'N/A')}")
    console.print()