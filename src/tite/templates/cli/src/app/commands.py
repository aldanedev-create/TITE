"""
Command definitions for the CLI application.

This module contains the command implementations and registration.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def register_commands() -> Dict[str, Any]:
    """
    Register all available commands.
    
    Returns:
        Dict[str, Any]: Dictionary of command names to functions
    """
    return {
        "hello": hello_command,
        "status": status_command,
        "config": config_command,
    }


def hello_command(args: Dict[str, Any]) -> int:
    """
    Hello command implementation.
    
    Args:
        args: Command arguments
        
    Returns:
        int: Exit code
    """
    name = args.get("name", "World")
    config = args.get("config", {})
    verbose = args.get("verbose", False)
    
    if verbose:
        logger.debug(f"Hello command called with name={name}, config={config}")
    
    print(f"Hello, {name}!")
    
    if config and config.get("greeting"):
        print(f"  {config['greeting']}")
    
    return 0


def status_command(args: Dict[str, Any]) -> int:
    """
    Status command implementation.
    
    Args:
        args: Command arguments
        
    Returns:
        int: Exit code
    """
    config = args.get("config", {})
    
    print("Application Status:")
    print(f"  Name: {{ project_name }}")
    print(f"  Version: 0.1.0")
    print(f"  Config loaded: {'Yes' if config else 'No'}")
    
    if config:
        print("  Configuration:")
        for key, value in config.items():
            print(f"    {key}: {value}")
    
    return 0


def config_command(args: Dict[str, Any]) -> int:
    """
    Config command implementation.
    
    Args:
        args: Command arguments
        
    Returns:
        int: Exit code
    """
    config = args.get("config", {})
    action = args.get("action", "show")
    key = args.get("key")
    value = args.get("value")
    
    if action == "show":
        print("Configuration:")
        if config:
            for k, v in config.items():
                print(f"  {k}: {v}")
        else:
            print("  No configuration loaded")
    
    elif action == "get":
        if key:
            if config and key in config:
                print(f"{key}: {config[key]}")
            else:
                print(f"Key '{key}' not found")
        else:
            print("No key specified")
    
    elif action == "set":
        if key and value:
            print(f"Setting {key}={value}")
            # In a real implementation, this would save the config
        else:
            print("Both key and value are required")
    
    return 0


def register_click_commands(cli) -> None:
    """
    Register commands with Click CLI.
    
    Args:
        cli: Click group instance
    """
    import click
    
    @cli.command()
    @click.option("--name", "-n", default="World", help="Name to greet")
    @click.pass_context
    def hello(ctx: click.Context, name: str):
        """Say hello to someone."""
        config = ctx.obj.get("config", {})
        verbose = ctx.obj.get("verbose", False)
        
        if verbose:
            logger.debug(f"Hello command called with name={name}")
        
        click.echo(f"Hello, {name}!")
        if config and config.get("greeting"):
            click.echo(f"  {config['greeting']}")
    
    @cli.command()
    @click.pass_context
    def status(ctx: click.Context):
        """Show application status."""
        config = ctx.obj.get("config", {})
        
        click.echo("Application Status:")
        click.echo(f"  Name: {{ project_name }}")
        click.echo(f"  Version: 0.1.0")
        click.echo(f"  Config loaded: {'Yes' if config else 'No'}")
        if config:
            click.echo("  Configuration:")
            for key, value in config.items():
                click.echo(f"    {key}: {value}")
    
    @cli.group()
    def config():
        """Manage configuration."""
        pass
    
    @config.command("show")
    @click.pass_context
    def config_show(ctx: click.Context):
        """Show current configuration."""
        config = ctx.obj.get("config", {})
        click.echo("Configuration:")
        if config:
            for key, value in config.items():
                click.echo(f"  {key}: {value}")
        else:
            click.echo("  No configuration loaded")
    
    @config.command("get")
    @click.argument("key")
    @click.pass_context
    def config_get(ctx: click.Context, key: str):
        """Get a configuration value."""
        config = ctx.obj.get("config", {})
        if key in config:
            click.echo(f"{key}: {config[key]}")
        else:
            click.echo(f"Key '{key}' not found", err=True)
    
    @config.command("set")
    @click.argument("key")
    @click.argument("value")
    @click.pass_context
    def config_set(ctx: click.Context, key: str, value: str):
        """Set a configuration value."""
        click.echo(f"Setting {key}={value}")
        # In a real implementation, this would save the config