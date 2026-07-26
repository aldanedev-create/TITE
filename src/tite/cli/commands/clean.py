"""
Clean command for Tite.

This module handles cleaning build artifacts, cache files, and
temporary files from Tite projects.
"""

import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional

from tite.cli.output import print_error, print_info, print_success, print_warning, console
from tite.cli.progress import ProgressContext
from tite.constants import ERROR_CODES, CLEAN_PATTERNS
from tite.core.config import ConfigManager
from tite.core.filesystem import FileSystemManager
from tite.exceptions import FileOperationError


def run_clean(args: Dict[str, Any]) -> int:
    """
    Execute the 'clean' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    dry_run = args.get("dry_run", False)
    clean_all = args.get("all", False)
    clean_type = args.get("type", "all")
    
    project_dir = Path.cwd()
    
    # Check if Tite project
    config_path = project_dir / ".tite" / "tite.toml"
    if not config_path.exists():
        print_warning("Not a Tite project. Use 'tite init' first.")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    console.print()
    console.print("[bold cyan]Tite Clean[/bold cyan]")
    if dry_run:
        console.print("[dim]Dry run mode - no files will be deleted[/dim]")
    console.print()
    
    try:
        # Load config
        config_manager = ConfigManager(project_dir)
        config = config_manager.load_config()
        
        # Get clean patterns from config or use defaults
        clean_config = config.get("clean", {})
        include_patterns = clean_config.get("include", CLEAN_PATTERNS["directories"] + CLEAN_PATTERNS["files"])
        exclude_patterns = clean_config.get("exclude", [".venv", "venv"])
        
        # Determine what to clean
        if clean_all:
            # Clean everything including venv
            exclude_patterns = []
        
        if clean_type == "cache":
            patterns = ["__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".hypothesis"]
        elif clean_type == "build":
            patterns = ["build", "dist", "*.egg-info", "*.pyc", "*.pyo", "*.pyd"]
        elif clean_type == "logs":
            patterns = ["*.log", "*.pid", "*.pid.lock"]
        else:
            patterns = include_patterns
        
        # Find files to clean
        files_to_remove = find_files_to_clean(
            project_dir,
            patterns,
            exclude_patterns,
        )
        
        if not files_to_remove:
            print_info("Nothing to clean")
            return ERROR_CODES["SUCCESS"]
        
        # Show what will be deleted
        console.print(f"[bold]Found {len(files_to_remove)} items to clean:[/bold]")
        for path in files_to_remove[:20]:  # Show first 20
            console.print(f"  [dim]{path}[/dim]")
        
        if len(files_to_remove) > 20:
            console.print(f"  [dim]... and {len(files_to_remove) - 20} more[/dim]")
        
        console.print()
        
        if dry_run:
            console.print("[dim]Dry run completed - no files were deleted[/dim]")
            return ERROR_CODES["SUCCESS"]
        
        # Ask for confirmation
        if not dry_run:
            from tite.cli.terminal import confirm_action
            if not confirm_action("Delete these files?", default=False):
                print_info("Clean cancelled")
                return ERROR_CODES["SUCCESS"]
        
        # Delete files
        with ProgressContext("Cleaning project", total=len(files_to_remove)) as progress:
            deleted_count = 0
            for file_path in files_to_remove:
                try:
                    if file_path.is_dir():
                        shutil.rmtree(file_path)
                    else:
                        file_path.unlink()
                    deleted_count += 1
                    progress.update(advance=1)
                except Exception as e:
                    console.print(f"[yellow]Failed to delete {file_path}: {e}[/yellow]")
        
        console.print()
        print_success(f"Cleaned {deleted_count} items")
        
        return ERROR_CODES["SUCCESS"]
        
    except FileOperationError as e:
        print_error(f"File operation error: {str(e)}")
        return ERROR_CODES["FILE_OPERATION_ERROR"]
    
    except Exception as e:
        print_error(f"Failed to clean: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]


def find_files_to_clean(
    project_dir: Path,
    patterns: List[str],
    exclude_patterns: List[str],
) -> List[Path]:
    """
    Find files to clean based on patterns.
    
    Args:
        project_dir: Project directory
        patterns: Patterns to include
        exclude_patterns: Patterns to exclude
        
    Returns:
        List[Path]: List of files to clean
    """
    files_to_remove = []
    
    for pattern in patterns:
        # Handle directory patterns
        if pattern.endswith("/"):
            pattern = pattern[:-1]
            for path in project_dir.rglob(pattern):
                if path.is_dir() and should_exclude(path, exclude_patterns):
                    files_to_remove.append(path)
        # Handle file patterns
        else:
            for path in project_dir.rglob(pattern):
                if should_exclude(path, exclude_patterns):
                    files_to_remove.append(path)
    
    # Remove duplicates
    return list(set(files_to_remove))


def should_exclude(path: Path, exclude_patterns: List[str]) -> bool:
    """
    Check if a path should be excluded.
    
    Args:
        path: Path to check
        exclude_patterns: Patterns to exclude
        
    Returns:
        bool: True if should be excluded
    """
    path_str = str(path)
    for pattern in exclude_patterns:
        if pattern in path_str:
            return False
    return True