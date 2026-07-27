"""
Blueprint command for Tite.

Builds a new project from a declarative blueprint file (YAML/JSON/TOML)
using tite.blueprint.parser.BlueprintParser and
tite.blueprint.builder.BlueprintBuilder.
"""

from pathlib import Path
from typing import Any, Dict

from tite.blueprint.builder import BlueprintBuilder
from tite.blueprint.parser import BlueprintParser
from tite.cli.output import console, print_error, print_info, print_success
from tite.cli.progress import ProgressContext
from tite.constants import ERROR_CODES
from tite.exceptions import ConfigurationError, TiteError


def run_blueprint(args: Dict[str, Any]) -> int:
    """
    Execute the 'blueprint' command.

    Args:
        args: Dictionary of command arguments

    Returns:
        int: Exit code
    """
    blueprint_file = args.get("file")
    name_override = args.get("name")
    path_override = args.get("path")
    dry_run = args.get("dry_run", False)
    var_overrides = args.get("var") or []

    blueprint_path = Path(blueprint_file)
    if not blueprint_path.exists():
        print_error(f"Blueprint file not found: {blueprint_path}")
        return ERROR_CODES["ERROR"]

    # Parse (and validate) the blueprint up front.
    try:
        parser = BlueprintParser()
        blueprint = parser.parse_file(blueprint_path)
    except ConfigurationError as e:
        print_error(f"Invalid blueprint: {str(e)}")
        return ERROR_CODES["CONFIGURATION_ERROR"]

    # Parse --var KEY=VALUE overrides.
    variables: Dict[str, str] = {}
    for item in var_overrides:
        if "=" not in item:
            print_error(f"Invalid --var value (expected KEY=VALUE): {item}")
            return ERROR_CODES["ERROR"]
        key, value = item.split("=", 1)
        variables[key.strip()] = value.strip()

    project_name = name_override or blueprint.get("name") or blueprint_path.stem
    base_dir = Path(path_override) if path_override else Path.cwd()
    project_path = base_dir / project_name

    console.print()
    console.print(f"[bold]Building project from blueprint:[/bold] {blueprint_path.name}")
    console.print(f"  [dim]Name:[/dim] {project_name}")
    console.print(f"  [dim]Location:[/dim] {project_path}")
    console.print()

    if dry_run:
        print_info("Blueprint is valid. Dry run: no files were created.")
        return ERROR_CODES["SUCCESS"]

    if project_path.exists() and any(project_path.iterdir()):
        print_error(f"Directory already exists and is not empty: {project_path}")
        return ERROR_CODES["PROJECT_EXISTS"]

    try:
        project_path.mkdir(parents=True, exist_ok=True)
        builder = BlueprintBuilder(project_path, blueprint=blueprint, variables=variables)

        with ProgressContext(f"Building {project_name}", total=1) as progress:
            results = builder.build()
            progress.update(advance=1, description="Done")

        print_success(f"Project '{project_name}' created successfully!")
        console.print()
        console.print(f"  [dim]Directories created:[/dim] {len(results['created_dirs'])}")
        console.print(f"  [dim]Files created:[/dim] {len(results['created_files'])}")
        if results["installed_packages"]:
            console.print(f"  [dim]Packages installed:[/dim] {len(results['installed_packages'])}")
        if results["executed_commands"]:
            console.print(f"  [dim]Commands executed:[/dim] {len(results['executed_commands'])}")
        console.print()
        console.print("Next steps:")
        console.print(f"  cd {project_name}")
        console.print()

        return ERROR_CODES["SUCCESS"]

    except TiteError as e:
        print_error(str(e))
        return ERROR_CODES["ERROR"]
    except Exception as e:
        print_error(f"Failed to build project: {str(e)}")
        return ERROR_CODES["ERROR"]