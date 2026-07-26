"""
Config command for Tite.

This module handles viewing, setting, and managing Tite configuration.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from tite.cli.output import print_error, print_info, print_success, print_warning, console, print_key_value
from tite.constants import ERROR_CODES
from tite.core.config import ConfigManager
from tite.exceptions import ConfigurationError


def run_config(args: Dict[str, Any]) -> int:
    """
    Execute the 'config' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    get_key = args.get("get")
    set_key_value = args.get("set")
    list_config = args.get("list", False)
    reset_key = args.get("reset")
    
    project_dir = Path.cwd()
    
    # Check if Tite project
    config_path = project_dir / ".tite" / "tite.toml"
    if not config_path.exists():
        print_warning("Not a Tite project. Use 'tite init' first.")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    try:
        config_manager = ConfigManager(project_dir)
        config = config_manager.load_config()
        
        # Get specific value
        if get_key:
            value = get_nested_value(config, get_key)
            if value is None:
                print_error(f"Key '{get_key}' not found")
                return ERROR_CODES["CONFIGURATION_ERROR"]
            
            if isinstance(value, dict):
                console.print(json.dumps(value, indent=2))
            else:
                console.print(value)
            return ERROR_CODES["SUCCESS"]
        
        # Set specific value
        if set_key_value:
            key, value = set_key_value
            config = set_nested_value(config, key, value)
            config_manager.save_config(config)
            print_success(f"Set '{key}' = {value}")
            return ERROR_CODES["SUCCESS"]
        
        # Reset specific value
        if reset_key:
            # Get default config
            default_config = ConfigManager.get_default_config()
            default_value = get_nested_value(default_config, reset_key)
            
            if default_value is None:
                print_error(f"Key '{reset_key}' not found in defaults")
                return ERROR_CODES["CONFIGURATION_ERROR"]
            
            config = set_nested_value(config, reset_key, default_value)
            config_manager.save_config(config)
            print_success(f"Reset '{reset_key}' to default")
            return ERROR_CODES["SUCCESS"]
        
        # List all config
        if list_config or not get_key and not set_key_value and not reset_key:
            display_config(config)
            return ERROR_CODES["SUCCESS"]
        
        # Default: show help
        console.print("[dim]Use --list to show all configuration[/dim]")
        console.print("[dim]Use --get <key> to get a value[/dim]")
        console.print("[dim]Use --set <key> <value> to set a value[/dim]")
        console.print("[dim]Use --reset <key> to reset to default[/dim]")
        
        return ERROR_CODES["SUCCESS"]
        
    except ConfigurationError as e:
        print_error(f"Configuration error: {str(e)}")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    except Exception as e:
        print_error(f"Failed to manage configuration: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]


def get_nested_value(config: Dict[str, Any], key: str) -> Any:
    """
    Get a nested value from configuration.
    
    Args:
        config: Configuration dictionary
        key: Dot-separated key path
        
    Returns:
        Any: Value or None if not found
    """
    parts = key.split(".")
    current = config
    
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    
    return current


def set_nested_value(config: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
    """
    Set a nested value in configuration.
    
    Args:
        config: Configuration dictionary
        key: Dot-separated key path
        value: Value to set
        
    Returns:
        Dict[str, Any]: Updated configuration
    """
    parts = key.split(".")
    current = config
    
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    
    # Try to parse value as appropriate type
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.isdigit():
        value = int(value)
    elif value.replace(".", "").isdigit():
        value = float(value)
    
    current[parts[-1]] = value
    return config


def display_config(config: Dict[str, Any]) -> None:
    """
    Display configuration.
    
    Args:
        config: Configuration dictionary
    """
    console.print()
    console.print("[bold cyan]Tite Configuration[/bold cyan]")
    console.print()
    
    display_config_section(config, "", 0)


def display_config_section(data: Dict[str, Any], prefix: str = "", depth: int = 0) -> None:
    """
    Recursively display configuration section.
    
    Args:
        data: Configuration data
        prefix: Current key prefix
        depth: Current depth
    """
    indent = "  " * depth
    
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            if depth > 0:
                console.print(f"{indent}[bold]{key}:[/bold]")
            else:
                console.print(f"[bold]{key}:[/bold]")
            display_config_section(value, full_key, depth + 1)
        else:
            display_value = value
            if isinstance(value, bool):
                display_value = "true" if value else "false"
            elif isinstance(value, list):
                display_value = ", ".join(str(v) for v in value)
            
            console.print(f"{indent}  [cyan]{key}[/cyan]: [white]{display_value}[/white]")