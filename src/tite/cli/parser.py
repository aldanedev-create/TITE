"""
Command-line argument parser for Tite.

This module handles parsing and validation of command-line arguments.
"""

import argparse
import re
from typing import Dict, List, Optional, Tuple, Union

from tite.constants import CLI_DESCRIPTION, CLI_EPILOG, CLI_NAME
from tite.exceptions import InvalidProjectNameError


def create_parser() -> argparse.ArgumentParser:
    """
    Create the main argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog=CLI_NAME,
        description=CLI_DESCRIPTION,
        epilog=CLI_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Global options
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show version information"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    # Subparsers for commands
    subparsers = parser.add_subparsers(
        dest="command",
        title="Commands",
        description="Available Tite commands",
        help="Command to execute",
    )
    
    # 'new' command
    new_parser = subparsers.add_parser(
        "new",
        help="Create a new Python project",
        description="Create a new Python project with Tite",
    )
    new_parser.add_argument(
        "name",
        help="Name of the project to create"
    )
    new_parser.add_argument(
        "--template", "-t",
        default="default",
        help="Template to use (default: default)"
    )
    new_parser.add_argument(
        "--mode", "-m",
        help="Mode to use (data, ai, automation, web, api, library, cli)"
    )
    new_parser.add_argument(
        "--path", "-p",
        help="Path to create the project in (default: current directory)"
    )
    new_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force creation even if directory exists"
    )
    new_parser.add_argument(
        "--no-git",
        action="store_true",
        help="Skip Git initialization"
    )
    new_parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Skip virtual environment creation"
    )
    
    # 'dev' command
    dev_parser = subparsers.add_parser(
        "dev",
        help="Start development server",
        description="Start development server with hot reload",
    )
    dev_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    dev_parser.add_argument(
        "--port", "-p",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    dev_parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable automatic reload on file changes"
    )
    dev_parser.add_argument(
        "--command",
        help="Command to run (overrides tite.toml)"
    )
    
    # 'doctor' command
    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Check project health",
        description="Run health checks on the project",
    )
    doctor_parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to fix issues automatically"
    )
    doctor_parser.add_argument(
        "--check",
        choices=["python", "env", "git", "files", "deps", "config"],
        help="Run a specific check only"
    )
    doctor_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed information"
    )
    
    # 'clean' command
    clean_parser = subparsers.add_parser(
        "clean",
        help="Clean build artifacts and cache",
        description="Remove build artifacts, cache files, and temporary files",
    )
    clean_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be cleaned without actually deleting"
    )
    clean_parser.add_argument(
        "--all",
        action="store_true",
        help="Clean everything including virtual environment"
    )
    clean_parser.add_argument(
        "--type",
        choices=["cache", "build", "logs", "all"],
        default="all",
        help="Type of files to clean (default: all)"
    )
    
    # 'info' command
    info_parser = subparsers.add_parser(
        "info",
        help="Show project information",
        description="Display detailed information about the project",
    )
    info_parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    info_parser.add_argument(
        "--section",
        choices=["project", "env", "deps", "git", "config"],
        help="Show a specific section only"
    )
    
    # 'config' command
    config_parser = subparsers.add_parser(
        "config",
        help="View or modify configuration",
        description="Display or update Tite configuration",
    )
    config_parser.add_argument(
        "--get",
        help="Get a configuration value (e.g., 'project.name')"
    )
    config_parser.add_argument(
        "--set",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="Set a configuration value"
    )
    config_parser.add_argument(
        "--list",
        action="store_true",
        help="List all configuration values"
    )
    config_parser.add_argument(
        "--reset",
        help="Reset a configuration value to default"
    )
    
    # 'env' command
    env_parser = subparsers.add_parser(
        "env",
        help="Show environment details",
        description="Display information about the Python environment",
    )
    env_parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    env_parser.add_argument(
        "--show-packages",
        action="store_true",
        help="Show installed packages"
    )
    env_parser.add_argument(
        "--show-vars",
        action="store_true",
        help="Show environment variables"
    )
    
    # 'mode' command
    mode_parser = subparsers.add_parser(
        "mode",
        help="Work with project modes",
        description="List, create, or manage project modes",
    )
    mode_parser.add_argument(
        "mode",
        nargs="?",
        help="Mode to use (data, ai, automation, web, api, library, cli, list)"
    )
    mode_parser.add_argument(
        "name",
        nargs="?",
        help="Name of the project to create with the mode"
    )
    mode_parser.add_argument(
        "--list",
        action="store_true",
        help="List available modes"
    )
    mode_parser.add_argument(
        "--path", "-p",
        help="Path to create the project in"
    )
    mode_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force creation even if directory exists"
    )
    
    # 'init' command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize Tite in an existing project",
        description="Add Tite configuration to an existing Python project",
    )
    init_parser.add_argument(
        "--path", "-p",
        help="Path to the existing project"
    )
    init_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force initialization even if Tite is already configured"
    )
    
    # 'update' command
    update_parser = subparsers.add_parser(
        "update",
        help="Update project dependencies",
        description="Update dependencies and lock file",
    )
    update_parser.add_argument(
        "--package", "-p",
        help="Update a specific package only"
    )
    update_parser.add_argument(
        "--major",
        action="store_true",
        help="Allow major version updates"
    )
    update_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without actually updating"
    )
    
    # 'version' command
    version_parser = subparsers.add_parser(
        "version",
        help="Show version information",
        description="Display detailed version information",
    )
    version_parser.add_argument(
        "--short",
        action="store_true",
        help="Show only the version number"
    )
    
    return parser


def validate_project_name(name: str) -> bool:
    """
    Validate a project name.
    
    Args:
        name: Project name to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        InvalidProjectNameError: If the name is invalid
    """
    if not name:
        raise InvalidProjectNameError(name, "Project name cannot be empty")
    
    # Check length
    if len(name) < 1:
        raise InvalidProjectNameError(name, "Project name must be at least 1 character")
    
    if len(name) > 100:
        raise InvalidProjectNameError(name, "Project name must be at most 100 characters")
    
    # Check for valid characters (alphanumeric, hyphen, underscore)
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\-_]*$', name):
        raise InvalidProjectNameError(
            name,
            "Project name must start with a letter or number and contain only "
            "letters, numbers, hyphens, and underscores"
        )
    
    # Check if it's a reserved name
    reserved_names = {
        "tite", "python", "test", "tests", "src", "lib", "bin", "docs",
        "scripts", "data", "logs", "config", "dist", "build", "venv",
        ".venv", "__pycache__", ".git", ".hg", ".svn",
    }
    
    if name.lower() in reserved_names:
        raise InvalidProjectNameError(
            name,
            f"'{name}' is a reserved name"
        )
    
    return True


def parse_arguments(args: List[str]) -> Tuple[str, Dict[str, Union[str, bool, int]]]:
    """
    Parse command-line arguments.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Tuple[str, Dict]: Command name and parsed arguments
        
    Raises:
        CommandNotFoundError: If the command is not found
    """
    parser = create_parser()
    
    if not args:
        parser.print_help()
        return "help", {}
    
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return "help", {}
    
    # Convert args to dictionary, filtering out None values
    args_dict = {
        k: v for k, v in vars(parsed_args).items()
        if v is not None and k != "command"
    }
    
    # Validate project name if present
    if "name" in args_dict and parsed_args.command in ("new", "mode"):
        try:
            validate_project_name(args_dict["name"])
        except InvalidProjectNameError as e:
            raise e
    
    return parsed_args.command, args_dict


def parse_key_value(key_value: str) -> Tuple[str, str]:
    """
    Parse a key=value string.
    
    Args:
        key_value: String in format "key=value"
        
    Returns:
        Tuple[str, str]: (key, value)
        
    Raises:
        ValueError: If the string is not in the correct format
    """
    if "=" not in key_value:
        raise ValueError(f"Expected 'key=value', got '{key_value}'")
    
    key, value = key_value.split("=", 1)
    return key.strip(), value.strip()


def parse_nested_key(key: str) -> List[str]:
    """
    Parse a nested key (e.g., "project.name" -> ["project", "name"]).
    
    Args:
        key: Nested key string
        
    Returns:
        List[str]: Split key parts
    """
    return key.split(".")