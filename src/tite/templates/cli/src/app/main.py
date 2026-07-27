"""
Main entry point for the CLI application.

This module sets up the command-line interface using Click or Typer.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Try to import Click first, fallback to argparse
try:
    import click
    HAS_CLICK = True
except ImportError:
    import argparse
    HAS_CLICK = False

# Import local modules
from app.config import load_config, Config
from app.commands import register_commands


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/cli.log", mode="a", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)

# Global config
config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the application configuration.
    
    Returns:
        Config: Application configuration
    """
    global config
    if config is None:
        config = load_config()
    return config


if HAS_CLICK:
    # Click-based CLI
    @click.group()
    @click.option("--config", "-c", type=click.Path(exists=True), help="Path to config file")
    @click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
    @click.option("--quiet", "-q", is_flag=True, help="Suppress output")
    @click.pass_context
    def cli(ctx: click.Context, config: Optional[str], verbose: bool, quiet: bool):
        """
        {{ project_description }}
        
        A command-line tool for managing {{ project_name }} operations.
        """
        ctx.ensure_object(dict)
        ctx.obj["config_path"] = config
        ctx.obj["verbose"] = verbose
        ctx.obj["quiet"] = quiet
        
        # Load configuration
        cfg = load_config(config)
        ctx.obj["config"] = cfg
        
        # Set log level
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        elif quiet:
            logging.getLogger().setLevel(logging.ERROR)
    
    @cli.command()
    @click.option("--name", "-n", default="World", help="Name to greet")
    @click.pass_context
    def hello(ctx: click.Context, name: str):
        """Say hello to someone."""
        cfg = ctx.obj["config"]
        verbose = ctx.obj["verbose"]
        
        if verbose:
            logger.debug(f"Greeting {name} with config: {cfg}")
        
        click.echo(f"Hello, {name}!")
        
        if cfg and cfg.get("greeting"):
            click.echo(f"  {cfg['greeting']}")
    
    @cli.command()
    @click.option("--count", "-c", type=int, default=1, help="Number of times to repeat")
    @click.pass_context
    def status(ctx: click.Context, count: int):
        """Show application status."""
        cfg = ctx.obj["config"]
        
        click.echo("Application Status:")
        click.echo(f"  Name: {{ project_name }}")
        click.echo(f"  Version: 0.1.0")
        click.echo(f"  Config loaded: {'Yes' if cfg else 'No'}")
        
        if cfg:
            click.echo("  Configuration:")
            for key, value in cfg.items():
                click.echo(f"    {key}: {value}")

else:
    # Argparse-based CLI (fallback)
    def create_parser():
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            description="{{ project_description }}",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s hello --name John
  %(prog)s status
  %(prog)s --verbose
            """
        )
        
        parser.add_argument(
            "--config", "-c",
            help="Path to config file",
        )
        
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Enable verbose output",
        )
        
        parser.add_argument(
            "--quiet", "-q",
            action="store_true",
            help="Suppress output",
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Command to run")
        
        # Hello command
        hello_parser = subparsers.add_parser("hello", help="Say hello to someone")
        hello_parser.add_argument("--name", "-n", default="World", help="Name to greet")
        
        # Status command
        subparsers.add_parser("status", help="Show application status")
        
        return parser
    
    def main():
        """Main entry point for argparse-based CLI."""
        parser = create_parser()
        args = parser.parse_args()
        
        # Set log level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        elif args.quiet:
            logging.getLogger().setLevel(logging.ERROR)
        
        # Load config
        cfg = load_config(args.config)
        
        if args.command == "hello":
            print(f"Hello, {args.name}!")
            if cfg and cfg.get("greeting"):
                print(f"  {cfg['greeting']}")
        
        elif args.command == "status":
            print("Application Status:")
            print(f"  Name: {{ project_name }}")
            print(f"  Version: 0.1.0")
            print(f"  Config loaded: {'Yes' if cfg else 'No'}")
            if cfg:
                print("  Configuration:")
                for key, value in cfg.items():
                    print(f"    {key}: {value}")
        
        else:
            parser.print_help()


def main():
    """Main entry point for the CLI application."""
    if HAS_CLICK:
        cli()
    else:
        # Argparse fallback
        main_argparse()

if __name__ == "__main__":
    sys.exit(main())