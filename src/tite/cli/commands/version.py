"""
Version command for Tite.

This module displays version information for Tite and its dependencies.
"""

from typing import Dict, Any

from tite.cli.output import console, print_info, print_key_value
from tite.constants import ERROR_CODES
from tite.version import get_version, get_system_info, get_package_version, format_version_info


def run_version(args: Dict[str, Any]) -> int:
    """
    Execute the 'version' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    short = args.get("short", False)
    
    if short:
        # Only show version number
        console.print(get_version())
        return ERROR_CODES["SUCCESS"]
    
    # Show detailed version info
    console.print()
    console.print("[bold cyan]Tite Version Information[/bold cyan]")
    console.print()
    
    # Tite version
    console.print("[bold]Tite:[/bold]")
    print_key_value("Version", get_version())
    
    # Dependencies
    console.print()
    console.print("[bold]Dependencies:[/bold]")
    
    dependencies = [
        "click",
        "rich",
        "watchdog",
        "pathspec",
        "colorama",
        "python-dotenv",
        "questionary",
    ]
    
    for dep in dependencies:
        version = get_package_version(dep)
        if version:
            print_key_value(dep, version)
        else:
            print_key_value(dep, "Not installed", value_color="red")
    
    # System info
    console.print()
    console.print("[bold]System:[/bold]")
    system_info = get_system_info()
    for key, value in system_info.items():
        if isinstance(value, str):
            print_key_value(key.replace("_", " ").title(), value)
    
    console.print()
    
    # Python version
    console.print(f"Python: {system_info.get('python_version', 'N/A')}")
    
    console.print()
    return ERROR_CODES["SUCCESS"]