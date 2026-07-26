"""
Terminal utilities for Tite.

This module provides terminal manipulation and formatting utilities.
"""

import os
import re
import shutil
import sys
from typing import Optional, Tuple


class TerminalUtils:
    """
    Utility class for terminal operations.
    
    This class provides static methods for terminal manipulation,
    color support, and formatting.
    """
    
    # ANSI color codes
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_black": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m",
    }
    
    @staticmethod
    def get_terminal_size() -> Tuple[int, int]:
        """
        Get the terminal size.
        
        Returns:
            Tuple[int, int]: (columns, rows)
        """
        try:
            columns, rows = shutil.get_terminal_size()
            return columns, rows
        except Exception:
            return 80, 24
            
    @staticmethod
    def get_terminal_width() -> int:
        """Get terminal width in columns."""
        return TerminalUtils.get_terminal_size()[0]
        
    @staticmethod
    def get_terminal_height() -> int:
        """Get terminal height in rows."""
        return TerminalUtils.get_terminal_size()[1]
        
    @staticmethod
    def supports_color() -> bool:
        """
        Check if the terminal supports color.
        
        Returns:
            bool: True if color is supported
        """
        if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
            return True
            
        # Check for NO_COLOR environment variable
        if os.environ.get("NO_COLOR"):
            return False
            
        # Check for TERM environment variable
        term = os.environ.get("TERM", "")
        if term in ("dumb", ""):
            return False
            
        return True
        
    @staticmethod
    def colorize(text: str, color: str, bold: bool = False) -> str:
        """
        Apply color to text.
        
        Args:
            text: Text to colorize
            color: Color name
            bold: Whether to make text bold
            
        Returns:
            str: Colorized text
        """
        if not TerminalUtils.supports_color():
            return text
            
        if color not in TerminalUtils.COLORS:
            return text
            
        result = TerminalUtils.COLORS.get(color, "")
        if bold:
            result += TerminalUtils.COLORS.get("bold", "")
            
        return f"{result}{text}{TerminalUtils.COLORS.get('reset', '')}"
        
    @staticmethod
    def strip_colors(text: str) -> str:
        """
        Remove ANSI color codes from text.
        
        Args:
            text: Text with ANSI color codes
            
        Returns:
            str: Text without color codes
        """
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
        
    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    @staticmethod
    def clear_line() -> None:
        """Clear the current line in the terminal."""
        sys.stdout.write('\r\x1b[K')
        sys.stdout.flush()
        
    @staticmethod
    def move_cursor_up(lines: int = 1) -> None:
        """Move the cursor up by the specified number of lines."""
        sys.stdout.write(f'\x1b[{lines}A')
        sys.stdout.flush()
        
    @staticmethod
    def move_cursor_down(lines: int = 1) -> None:
        """Move the cursor down by the specified number of lines."""
        sys.stdout.write(f'\x1b[{lines}B')
        sys.stdout.flush()
        
    @staticmethod
    def move_cursor_to_column(column: int) -> None:
        """Move the cursor to the specified column."""
        sys.stdout.write(f'\x1b[{column + 1}G')
        sys.stdout.flush()
        
    @staticmethod
    def hide_cursor() -> None:
        """Hide the terminal cursor."""
        sys.stdout.write('\x1b[?25l')
        sys.stdout.flush()
        
    @staticmethod
    def show_cursor() -> None:
        """Show the terminal cursor."""
        sys.stdout.write('\x1b[?25h')
        sys.stdout.flush()
        
    @staticmethod
    def get_user_input(prompt: str, default: Optional[str] = None) -> str:
        """
        Get user input with a prompt.
        
        Args:
            prompt: Prompt text
            default: Default value
            
        Returns:
            str: User input
        """
        if default is not None:
            prompt = f"{prompt} [{default}] "
        else:
            prompt = f"{prompt} "
            
        user_input = input(prompt)
        return user_input or default or ""
        
    @staticmethod
    def confirm_action(message: str, default: bool = False) -> bool:
        """
        Ask for confirmation.
        
        Args:
            message: Confirmation message
            default: Default value
            
        Returns:
            bool: True if confirmed
        """
        if default:
            prompt = f"{message} [Y/n] "
        else:
            prompt = f"{message} [y/N] "
            
        response = input(prompt).strip().lower()
        if not response:
            return default
        return response in ("y", "yes", "ye", "yep", "yeah")
        
    @staticmethod
    def is_interactive() -> bool:
        """Check if the terminal is interactive."""
        return sys.stdin.isatty() and sys.stdout.isatty()


def get_terminal_size() -> Tuple[int, int]:
    """Get terminal size."""
    return TerminalUtils.get_terminal_size()


def clear_screen() -> None:
    """Clear the terminal screen."""
    TerminalUtils.clear_screen()


def colorize(text: str, color: str, bold: bool = False) -> str:
    """Apply color to text."""
    return TerminalUtils.colorize(text, color, bold)


def strip_colors(text: str) -> str:
    """Remove ANSI color codes from text."""
    return TerminalUtils.strip_colors(text)