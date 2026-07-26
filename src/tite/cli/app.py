"""
Main CLI application entry point for Tite.

This module defines the main command-line interface for Tite,
handling command routing and execution.
"""

import sys
from typing import Optional

from tite.cli.help import show_help, show_version
from tite.cli.parser import parse_arguments
from tite.cli.output import print_error, print_success, print_info, console
from tite.constants import CLI_NAME, CLI_DESCRIPTION, ERROR_CODES
from tite.exceptions import TiteError, CommandNotFoundError


def main(args: Optional[list] = None) -> int:
    """
    Main entry point for the Tite CLI.
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        int: Exit code (0 for success, non-zero for errors)
        
    Examples:
        >>> main(["new", "my-project"])
        0
        
        >>> main(["--help"])
        0
    """
    if args is None:
        args = sys.argv[1:]
    
    # Handle help and version flags
    if not args or args[0] in ("-h", "--help"):
        show_help()
        return ERROR_CODES["SUCCESS"]
    
    if args[0] in ("-v", "--version"):
        show_version()
        return ERROR_CODES["SUCCESS"]
    
    try:
        # Parse and execute command
        command, command_args = parse_arguments(args)
        
        if command == "new":
            from tite.cli.commands.new import run_new
            return run_new(command_args)
        
        elif command == "dev":
            from tite.cli.commands.dev import run_dev
            return run_dev(command_args)
        
        elif command == "doctor":
            from tite.cli.commands.doctor import run_doctor
            return run_doctor(command_args)
        
        elif command == "clean":
            from tite.cli.commands.clean import run_clean
            return run_clean(command_args)
        
        elif command == "info":
            from tite.cli.commands.info import run_info
            return run_info(command_args)
        
        elif command == "config":
            from tite.cli.commands.config import run_config
            return run_config(command_args)
        
        elif command == "env":
            from tite.cli.commands.env import run_env
            return run_env(command_args)
        
        elif command == "mode":
            from tite.cli.commands.mode import run_mode
            return run_mode(command_args)
        
        elif command == "init":
            from tite.cli.commands.init import run_init
            return run_init(command_args)
        
        elif command == "update":
            from tite.cli.commands.update import run_update
            return run_update(command_args)
        
        elif command == "version":
            from tite.cli.commands.version import run_version
            return run_version(command_args)
        
        else:
            raise CommandNotFoundError(command=command)
    
    except TiteError as e:
        print_error(e.message, code=e.code)
        if e.details:
            console.print(f"[dim]Details: {e.details}[/dim]")
        return e.code
    
    except KeyboardInterrupt:
        print_info("Operation cancelled by user")
        return ERROR_CODES["SUCCESS"]
    
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]


if __name__ == "__main__":
    sys.exit(main())