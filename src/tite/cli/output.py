"""
Output formatting for Tite CLI.

This module provides functions for formatting and displaying output
with colors, formatting, and structure.
"""

import json
from typing import Any, Dict, List, Optional, Union

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from tite.cli.terminal import colorize, get_terminal_columns, supports_color
from tite.constants import COLORS

# Global console instance
console = Console()


def print_header(text: str, char: str = "=", width: Optional[int] = None) -> None:
    """
    Print a header with decorative characters.
    
    Args:
        text: Header text
        char: Character to use for decoration
        width: Width of the header (defaults to terminal width)
    """
    if width is None:
        width = get_terminal_columns()
    
    text = f" {text} "
    padding = max(0, width - len(text))
    
    left_padding = padding // 2
    right_padding = padding - left_padding
    
    line = char * left_padding + text + char * right_padding
    print(line[:width])


def print_section(text: str, color: str = "blue") -> None:
    """
    Print a section title.
    
    Args:
        text: Section text
        color: Color name
    """
    print()
    print(colorize(f"▸ {text}", color, bold=True))
    print(colorize("─" * min(len(text) + 2, get_terminal_columns()), "dim"))


def print_success(text: str) -> None:
    """
    Print a success message.
    
    Args:
        text: Success message
    """
    console.print(f"[green]✓[/green] {text}")


def print_error(text: str, code: Optional[int] = None) -> None:
    """
    Print an error message.
    
    Args:
        text: Error message
        code: Error code
    """
    if code is not None:
        console.print(f"[red]✗[/red] Error {code}: {text}")
    else:
        console.print(f"[red]✗[/red] {text}")


def print_warning(text: str) -> None:
    """
    Print a warning message.
    
    Args:
        text: Warning message
    """
    console.print(f"[yellow]⚠[/yellow] {text}")


def print_info(text: str) -> None:
    """
    Print an information message.
    
    Args:
        text: Information message
    """
    console.print(f"[blue]ℹ[/blue] {text}")


def print_debug(text: str, verbose: bool = False) -> None:
    """
    Print a debug message.
    
    Args:
        text: Debug message
        verbose: Whether verbose mode is enabled
    """
    if verbose:
        console.print(f"[dim]🔍 {text}[/dim]")


def print_separator(char: str = "─", width: Optional[int] = None) -> None:
    """
    Print a separator line.
    
    Args:
        char: Character to use for the separator
        width: Width of the separator (defaults to terminal width)
    """
    if width is None:
        width = get_terminal_columns()
    console.print(char * width, style="dim")


def print_table(
    title: Optional[str] = None,
    headers: Optional[List[str]] = None,
    rows: Optional[List[List[Any]]] = None,
    columns: Optional[List[str]] = None,
    data: Optional[List[Dict[str, Any]]] = None,
    border_style: str = "dim",
    header_style: str = "bold",
) -> None:
    """
    Print a table.
    
    Args:
        title: Table title
        headers: Column headers
        rows: Table rows
        columns: Column names for data
        data: List of dictionaries
        border_style: Style for borders
        header_style: Style for headers
    """
    table = Table(title=title, border_style=border_style)
    
    # Build table from headers and rows
    if headers and rows:
        for header in headers:
            table.add_column(header, style=header_style)
        
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
    
    # Build table from data
    elif columns and data:
        for column in columns:
            table.add_column(column, style=header_style)
        
        for item in data:
            row = [str(item.get(col, "")) for col in columns]
            table.add_row(*row)
    
    else:
        raise ValueError("Either (headers, rows) or (columns, data) must be provided")
    
    console.print(table)


def print_panel(
    content: str,
    title: Optional[str] = None,
    border_style: str = "blue",
    padding: int = 1,
) -> None:
    """
    Print content in a panel.
    
    Args:
        content: Panel content
        title: Panel title
        border_style: Style for the border
        padding: Padding around content
    """
    panel = Panel(
        content,
        title=title,
        border_style=border_style,
        padding=padding,
    )
    console.print(panel)


def print_tree(data: Dict[str, Any], title: Optional[str] = None) -> None:
    """
    Print data as a tree.
    
    Args:
        data: Data to display as tree
        title: Tree title
    """
    tree = Tree(title or "Tree", style="bold")
    
    def add_branch(tree_node, data_item, key=None):
        if isinstance(data_item, dict):
            branch = tree_node.add(f"[blue]{key}[/blue]" if key else "")
            for k, v in data_item.items():
                add_branch(branch, v, k)
        elif isinstance(data_item, list):
            branch = tree_node.add(f"[blue]{key}[/blue]" if key else "")
            for i, v in enumerate(data_item):
                add_branch(branch, v, f"[{i}]")
        else:
            if key:
                tree_node.add(f"[cyan]{key}[/cyan]: [white]{data_item}[/white]")
            else:
                tree_node.add(f"[white]{data_item}[/white]")
    
    add_branch(tree, data)
    console.print(tree)


def print_json(data: Any, indent: int = 2) -> None:
    """
    Print data as formatted JSON.
    
    Args:
        data: Data to print
        indent: JSON indentation
    """
    console.print(json.dumps(data, indent=indent, default=str))


def print_key_value(
    key: str,
    value: Any,
    key_color: str = "cyan",
    value_color: str = "white",
    indent: int = 0,
) -> None:
    """
    Print a key-value pair.
    
    Args:
        key: Key string
        value: Value to display
        key_color: Color for the key
        value_color: Color for the value
        indent: Indentation level
    """
    indent_str = " " * indent
    console.print(f"{indent_str}[{key_color}]{key}[/{key_color}]: [white]{value}[/white]")


def print_list(
    items: List[Any],
    title: Optional[str] = None,
    bullet: str = "•",
    numbered: bool = False,
) -> None:
    """
    Print a list of items.
    
    Args:
        items: List of items to print
        title: List title
        bullet: Bullet character
        numbered: Whether to number the list
    """
    if title:
        console.print(f"[bold]{title}[/bold]")
    
    for i, item in enumerate(items):
        prefix = f"{i + 1}." if numbered else bullet
        console.print(f"  {prefix} {item}")


def print_divider(
    text: Optional[str] = None,
    char: str = "─",
    width: Optional[int] = None,
) -> None:
    """
    Print a divider with optional text.
    
    Args:
        text: Text to center in the divider
        char: Character to use
        width: Width of the divider
    """
    if width is None:
        width = get_terminal_columns()
    
    if text:
        text = f" {text} "
        padding = max(0, width - len(text))
        left = padding // 2
        right = padding - left
        console.print(f"{char * left}{text}{char * right}")
    else:
        console.print(char * width)


def print_welcome() -> None:
    """
    Print the Tite welcome banner.
    """
    console.print()
    console.print("[bold cyan]╔══════════════════════════════════════════╗[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]           [bold white]Tite[/bold white]              [bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]  Zero-Configuration Python Project  [bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]        Bootstrapper                 [bold cyan]║[/bold cyan]")
    console.print("[bold cyan]╚══════════════════════════════════════════╝[/bold cyan]")
    console.print()


def format_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Human-readable size string
        
    Examples:
        >>> format_size(1024)
        '1.00 KB'
        >>> format_size(1048576)
        '1.00 MB'
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Human-readable duration
        
    Examples:
        >>> format_duration(65)
        '1m 5s'
        >>> format_duration(3665)
        '1h 1m 5s'
    """
    if seconds < 0:
        return "0s"
    
    parts = []
    
    hours = int(seconds // 3600)
    if hours:
        parts.append(f"{hours}h")
        seconds %= 3600
    
    minutes = int(seconds // 60)
    if minutes:
        parts.append(f"{minutes}m")
        seconds %= 60
    
    seconds = int(seconds)
    if seconds or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)