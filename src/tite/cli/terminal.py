"""
Terminal utilities for Tite.

This module provides terminal-related functions including
size detection, color support, and interactive features.
"""

import os
import shutil
import sys
from typing import Optional, Tuple

from tite.constants import COLORS


def get_terminal_size() -> Tuple[int, int]:
    """
    Get the current terminal size.
    
    Returns:
        Tuple[int, int]: (columns, rows)
        
    Examples:
        >>> get_terminal_size()
        (120, 40)
    """
    try:
        columns, rows = shutil.get_terminal_size()
        return columns, rows
    except Exception:
        return 80, 24


def get_terminal_columns() -> int:
    """
    Get the number of columns in the terminal.
    
    Returns:
        int: Number of columns
        
    Examples:
        >>> get_terminal_columns()
        120
    """
    return get_terminal_size()[0]


def get_terminal_rows() -> int:
    """
    Get the number of rows in the terminal.
    
    Returns:
        int: Number of rows
        
    Examples:
        >>> get_terminal_rows()
        40
    """
    return get_terminal_size()[1]


def supports_color() -> bool:
    """
    Check if the terminal supports colored output.
    
    Returns:
        bool: True if color is supported
        
    Examples:
        >>> supports_color()
        True
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


def colorize(text: str, color: str, bold: bool = False) -> str:
    """
    Apply color to text.
    
    Args:
        text: Text to colorize
        color: Color name (red, green, blue, etc.)
        bold: Whether to make text bold
        
    Returns:
        str: Colorized text
        
    Examples:
        >>> colorize("Hello", "green")
        '\\x1b[32mHello\\x1b[0m'
    """
    if not supports_color():
        return text
    
    if color not in COLORS:
        return text
    
    result = COLORS.get(color, "")
    if bold:
        result += COLORS.get("bold", "")
    
    return f"{result}{text}{COLORS.get('reset', '')}"


def strip_colors(text: str) -> str:
    """
    Remove ANSI color codes from text.
    
    Args:
        text: Text with ANSI color codes
        
    Returns:
        str: Text without color codes
        
    Examples:
        >>> strip_colors('\\x1b[32mHello\\x1b[0m')
        'Hello'
    """
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def clear_screen() -> None:
    """
    Clear the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def clear_line() -> None:
    """
    Clear the current line in the terminal.
    """
    sys.stdout.write('\r\x1b[K')
    sys.stdout.flush()


def move_cursor_up(lines: int = 1) -> None:
    """
    Move the cursor up by the specified number of lines.
    
    Args:
        lines: Number of lines to move up
    """
    sys.stdout.write(f'\x1b[{lines}A')
    sys.stdout.flush()


def move_cursor_down(lines: int = 1) -> None:
    """
    Move the cursor down by the specified number of lines.
    
    Args:
        lines: Number of lines to move down
    """
    sys.stdout.write(f'\x1b[{lines}B')
    sys.stdout.flush()


def move_cursor_to_column(column: int) -> None:
    """
    Move the cursor to the specified column.
    
    Args:
        column: Column number (0-indexed)
    """
    sys.stdout.write(f'\x1b[{column + 1}G')
    sys.stdout.flush()


def hide_cursor() -> None:
    """
    Hide the terminal cursor.
    """
    sys.stdout.write('\x1b[?25l')
    sys.stdout.flush()


def show_cursor() -> None:
    """
    Show the terminal cursor.
    """
    sys.stdout.write('\x1b[?25h')
    sys.stdout.flush()


def get_user_input(prompt: str, default: Optional[str] = None) -> str:
    """
    Get user input with a prompt.
    
    Args:
        prompt: Prompt text
        default: Default value
        
    Returns:
        str: User input
        
    Examples:
        >>> get_user_input("Enter name: ", default="John")
        Enter name: [John] John
    """
    if default is not None:
        prompt = f"{prompt} [{default}] "
    else:
        prompt = f"{prompt} "
    
    user_input = input(prompt)
    return user_input or default or ""


def confirm_action(
    message: str,
    default: bool = False,
    yes_text: str = "yes",
    no_text: str = "no",
) -> bool:
    """
    Ask for confirmation.
    
    Args:
        message: Confirmation message
        default: Default value (True for yes, False for no)
        yes_text: Text for yes option
        no_text: Text for no option
        
    Returns:
        bool: True if confirmed, False otherwise
        
    Examples:
        >>> confirm_action("Continue?")
        Continue? [y/N]
        False
    """
    if default:
        prompt = f"{message} [{yes_text.upper()}/{no_text}] "
    else:
        prompt = f"{message} [{yes_text}/{no_text.upper()}] "
    
    while True:
        response = input(prompt).strip().lower()
        if not response:
            return default
        if response in ("y", "yes", "ye", "yep", "yeah"):
            return True
        if response in ("n", "no", "nope"):
            return False
        print("Please answer yes or no.")


def select_from_list(
    items: list,
    title: str = "Select an option",
    default: Optional[int] = None,
) -> Optional[int]:
    """
    Interactive selection from a list.
    
    Args:
        items: List of items to select from
        title: Title to display
        default: Default selection index
        
    Returns:
        Optional[int]: Selected index or None if cancelled
    """
    if not items:
        return None
    
    print(f"\n{title}:")
    
    for i, item in enumerate(items):
        prefix = "> " if i == default else "  "
        print(f"{prefix}{i + 1}. {item}")
    
    while True:
        try:
            response = input(f"\nSelect option (1-{len(items)}): ").strip()
            if not response and default is not None:
                return default
            
            selection = int(response) - 1
            if 0 <= selection < len(items):
                return selection
            print(f"Please enter a number between 1 and {len(items)}")
            
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            return None


def wait_for_keypress(message: str = "Press any key to continue...") -> None:
    """
    Wait for a keypress.
    
    Args:
        message: Message to display
    """
    import select
    import sys
    
    print(message, end="", flush=True)
    
    if sys.stdin.isatty():
        if os.name == "nt":
            import msvcrt
            msvcrt.getch()
        else:
            import termios
            import tty
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    else:
        input()
    
    print("\r" + " " * len(message) + "\r", end="", flush=True)


def is_interactive() -> bool:
    """
    Check if the terminal is interactive.
    
    Returns:
        bool: True if interactive, False otherwise
    """
    return sys.stdin.isatty() and sys.stdout.isatty()


def get_terminal_title() -> Optional[str]:
    """
    Get the terminal window title.
    
    Returns:
        Optional[str]: Terminal title or None if unavailable
    """
    try:
        if os.name == "nt":
            import ctypes
            import ctypes.wintypes
            
            class WINDOWINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.wintypes.DWORD),
                    ("rcWindow", ctypes.wintypes.RECT),
                    ("rcClient", ctypes.wintypes.RECT),
                    ("dwStyle", ctypes.wintypes.DWORD),
                    ("dwExStyle", ctypes.wintypes.DWORD),
                    ("dwWindowStatus", ctypes.wintypes.DWORD),
                    ("cxWindowBorders", ctypes.wintypes.UINT),
                    ("cyWindowBorders", ctypes.wintypes.UINT),
                    ("atomWindowType", ctypes.wintypes.ATOM),
                    ("wCreatorVersion", ctypes.wintypes.WORD),
                ]
            
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            
            length = user32.GetWindowTextLengthW(hwnd) + 1
            buffer = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hwnd, buffer, length)
            
            return buffer.value if buffer.value else None
        else:
            # Try xterm title
            import subprocess
            result = subprocess.run(
                ["xprop", "-id", os.environ.get("WINDOWID", ""), "WM_NAME"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and "=" in result.stdout:
                return result.stdout.split("=", 1)[1].strip().strip('"')
            return None
            
    except Exception:
        return None


def set_terminal_title(title: str) -> None:
    """
    Set the terminal window title.
    
    Args:
        title: Title to set
    """
    try:
        if os.name == "nt":
            import ctypes
            user32 = ctypes.windll.user32
            user32.SetConsoleTitleW(title)
        else:
            sys.stdout.write(f"\x1b]0;{title}\x07")
            sys.stdout.flush()
    except Exception:
        pass