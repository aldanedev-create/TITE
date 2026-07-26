"""
Help and version display for Tite CLI.

This module provides functions for displaying help information,
version information, and command documentation.
"""

import sys
from typing import Optional

from rich.markdown import Markdown
from rich.table import Table

from tite.cli.output import console, print_header, print_welcome
from tite.cli.parser import create_parser
from tite.constants import (
    CLI_DESCRIPTION,
    CLI_NAME,
    PROJECT_DOCS,
    PROJECT_ISSUES,
    PROJECT_URL,
    SUPPORTED_MODES,
    SUPPORTED_TEMPLATES,
)
from tite.version import get_system_info, get_version


def show_help() -> None:
    """
    Display the main help message.
    """
    parser = create_parser()
    parser.print_help()


def show_version() -> None:
    """
    Display version information.
    """
    console.print(f"[bold]{CLI_NAME}[/bold] version [cyan]{get_version()}[/cyan]")
    console.print(f"Python {sys.version.split()[0]}")
    console.print(f"Platform: {sys.platform}")


def show_detailed_help() -> None:
    """
    Display detailed help with examples and additional information.
    """
    console.print()
    print_header(f" {CLI_NAME} - {CLI_DESCRIPTION} ", "=")
    console.print()

    # Basic usage
    console.print("[bold]Usage:[/bold]")
    console.print(f"  {CLI_NAME} <command> [options]")
    console.print()

    # Commands table
    table = Table(title="Commands", border_style="blue")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Example", style="dim")

    commands = [
        ("new", "Create a new Python project", f"{CLI_NAME} new my-app"),
        ("dev", "Start development server", f"{CLI_NAME} dev"),
        ("doctor", "Check project health", f"{CLI_NAME} doctor"),
        ("clean", "Clean build artifacts", f"{CLI_NAME} clean"),
        ("info", "Show project information", f"{CLI_NAME} info"),
        ("config", "View or modify configuration", f"{CLI_NAME} config --list"),
        ("env", "Show environment details", f"{CLI_NAME} env"),
        ("mode", "Work with project modes", f"{CLI_NAME} mode list"),
        ("init", "Initialize Tite in existing project", f"{CLI_NAME} init"),
        ("update", "Update project dependencies", f"{CLI_NAME} update"),
        ("version", "Show version information", f"{CLI_NAME} version"),
    ]

    for cmd, desc, example in commands:
        table.add_row(cmd, desc, example)

    console.print(table)
    console.print()

    # Options
    console.print("[bold]Global Options:[/bold]")
    console.print("  [cyan]--help, -h[/cyan]     Show help message")
    console.print("  [cyan]--version, -v[/cyan]  Show version information")
    console.print("  [cyan]--verbose[/cyan]      Enable verbose output")
    console.print("  [cyan]--no-color[/cyan]     Disable colored output")
    console.print()

    # Modes
    show_modes_help()
    console.print()

    # Templates
    show_templates_help()
    console.print()

    # Examples
    console.print("[bold]Examples:[/bold]")
    console.print(f"  {CLI_NAME} new my-web-app --mode web")
    console.print(f"  {CLI_NAME} new my-library --template library")
    console.print(f"  {CLI_NAME} mode data sales-analysis")
    console.print(f"  {CLI_NAME} dev --host 0.0.0.0 --port 5000")
    console.print()

    # Links
    console.print("[bold]Links:[/bold]")
    console.print(f"  [cyan]Homepage:[/cyan] {PROJECT_URL}")
    console.print(f"  [cyan]Documentation:[/cyan] {PROJECT_DOCS}")
    console.print(f"  [cyan]Issues:[/cyan] {PROJECT_ISSUES}")
    console.print()


def show_modes_help() -> None:
    """
    Display help for available modes.
    """
    table = Table(title="Available Modes", border_style="green")
    table.add_column("Mode", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Template", style="dim")

    for mode_name, mode_info in SUPPORTED_MODES.items():
        if mode_name == "default":
            continue
        template = mode_info.get("template", "default")
        table.add_row(mode_name, mode_info.get("description", ""), template)

    console.print(table)


def show_templates_help() -> None:
    """
    Display help for available templates.
    """
    table = Table(title="Available Templates", border_style="yellow")
    table.add_column("Template", style="cyan")
    table.add_column("Description", style="white")

    for template_name, description in SUPPORTED_TEMPLATES.items():
        table.add_row(template_name, description)

    console.print(table)


def show_command_help(command: str) -> None:
    """
    Display help for a specific command.

    Args:
        command: Command name
    """
    parser = create_parser()
    subparsers = parser._subparsers._group_actions[0].choices

    if command not in subparsers:
        console.print(f"[red]Unknown command: {command}[/red]")
        show_help()
        return

    parser.print_usage()
    console.print()
    subparsers[command].print_help()


def show_quick_help(error_message: Optional[str] = None) -> None:
    """
    Display quick help after an error.

    Args:
        error_message: Optional error message to display
    """
    if error_message:
        console.print(f"[red]Error:[/red] {error_message}")
        console.print()

    console.print(f"[bold]Try:[/bold] {CLI_NAME} --help for more information")
    console.print()
    console.print("[dim]Quick commands:[/dim]")
    console.print(f"  {CLI_NAME} new <project-name>    Create a new project")
    console.print(f"  {CLI_NAME} dev                  Start development server")
    console.print(f"  {CLI_NAME} doctor               Check project health")
    console.print(f"  {CLI_NAME} mode list            List available modes")


def show_version_info() -> None:
    """
    Display detailed version information.
    """
    console.print()
    print_header(f" {CLI_NAME} Version {get_version()} ", "=")
    console.print()

    info = get_system_info()

    table = Table(border_style="blue")
    table.add_column("Component", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Tite", get_version())
    table.add_row("Python", info["python_version"])
    table.add_row("Platform", info["platform"])
    table.add_row("Release", info.get("platform_release", "N/A"))
    table.add_row("Architecture", info.get("architecture", "N/A"))
    table.add_row("Implementation", info.get("implementation", "N/A"))

    console.print(table)
    console.print()


def show_welcome() -> None:
    """
    Display the welcome message.
    """
    print_welcome()
    console.print("[dim]Type --help for usage information[/dim]")
    console.print()


def show_help_panel(topic: str) -> None:
    """
    Display help for a specific topic.

    Args:
        topic: Help topic
    """
    topics = {
        "getting-started": """
# Getting Started with Tite

## Installation
```bash
pip install tite
```

## Create a project
```bash
tite new my-app
cd my-app
```

## Start developing
```bash
tite dev
```

Run `tite doctor` any time to check your project's health.
""",
        "modes": """
# Tite Modes

Modes are domain-specific presets applied on top of a template, e.g.:

```bash
tite mode data sales-analysis
tite mode ai chatbot-assistant
tite mode automation backup-tool
```

Run `tite mode list` to see all available modes.
""",
        "templates": """
# Tite Templates

Templates control the base project structure. Use `--template` with `tite new`:

```bash
tite new my-api --template api
```

Run `tite --help` to see the full list of supported templates.
""",
        "commands": """
# Tite Commands

- `tite new <name>` - Create a new project
- `tite dev` - Start the development server
- `tite doctor` - Run health checks
- `tite clean` - Remove cache and build artifacts
- `tite info` - Show project information
- `tite config` - View or modify configuration
- `tite env` - Show environment details
- `tite mode <mode> <name>` - Create a project with a domain-specific preset
""",
    }

    if topic not in topics:
        console.print(f"[red]Unknown help topic: {topic}[/red]")
        console.print(f"[dim]Available topics: {', '.join(topics.keys())}[/dim]")
        return

    console.print(Markdown(topics[topic]))