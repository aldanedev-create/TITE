"""
Doctor command for Tite.

This module handles health checks for Tite projects, verifying
Python installation, virtual environment, Git, and project structure.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple

from tite.cli.output import print_error, print_info, print_success, print_warning, console
from tite.constants import ERROR_CODES, HEALTH_CHECKS
from tite.core.config import ConfigManager
from tite.core.environment import EnvironmentManager
from tite.core.git import GitManager
from tite.diagnostics.doctor import Doctor
from tite.exceptions import EnvironmentError, ConfigurationError


def run_doctor(args: Dict[str, Any]) -> int:
    """
    Execute the 'doctor' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    fix = args.get("fix", False)
    check = args.get("check")
    verbose = args.get("verbose", False)
    
    project_dir = Path.cwd()
    
    # Check if Tite project
    config_path = project_dir / ".tite" / "tite.toml"
    if not config_path.exists():
        print_warning("Not a Tite project. Use 'tite init' first.")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    console.print()
    console.print("[bold cyan]Tite Doctor[/bold cyan]")
    console.print("[dim]Checking project health...[/dim]")
    console.print()
    
    try:
        # Create doctor
        doctor = Doctor(project_dir, verbose=verbose)
        
        # Run specific check
        if check:
            if check in HEALTH_CHECKS:
                result = doctor.run_check(check)
                result_dict = result.to_dict() if result else {"status": "unknown", "message": "Check not found"}
                display_check_result(check, result_dict, verbose)
            else:
                print_error(f"Unknown check: {check}")
                console.print(f"[dim]Available checks: {', '.join(HEALTH_CHECKS.keys())}[/dim]")
                return ERROR_CODES["ERROR"]
        else:
            # Run all checks
            results = doctor.run_all_checks()
            results_dict = {result.check_name: result.to_dict() for result in results}
            display_all_results(results_dict, verbose)
        
        # Attempt fixes if requested
        if fix:
            console.print()
            print_info("Attempting to fix issues...")
            fixed = doctor.fix_issues()
            if fixed:
                print_success("Issues fixed successfully")
            else:
                print_warning("Could not fix all issues")
        
        # Show summary
        console.print()
        summary = doctor.get_summary()
        status = summary.get("status", "unknown")
        
        if status == "healthy":
            print_success("✅ Project is healthy!")
            console.print(f"[dim]Checks passed: {summary.get('passed', 0)}/{summary.get('total', 0)}[/dim]")
        elif status == "warning":
            print_warning("⚠️ Project has warnings")
            console.print(f"[dim]Checks passed: {summary.get('passed', 0)}/{summary.get('total', 0)}[/dim]")
        else:
            print_error("❌ Project has errors")
            console.print(f"[dim]Checks passed: {summary.get('passed', 0)}/{summary.get('total', 0)}[/dim]")
        
        console.print()
        return ERROR_CODES["SUCCESS"]
        
    except ConfigurationError as e:
        print_error(f"Configuration error: {str(e)}")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    except EnvironmentError as e:
        print_error(f"Environment error: {str(e)}")
        return ERROR_CODES["ENVIRONMENT_ERROR"]
    
    except Exception as e:
        print_error(f"Failed to run doctor: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]


def display_check_result(check_name: str, result: Dict[str, Any], verbose: bool) -> None:
    """
    Display a single check result.
    
    Args:
        check_name: Name of the check
        result: Check result dictionary
        verbose: Enable verbose output
    """
    status = result.get("status", "unknown")
    message = result.get("message", "")
    details = result.get("details", {})
    
    icon = "✅" if status == "passed" else "⚠️" if status == "warning" else "❌"
    color = "green" if status == "passed" else "yellow" if status == "warning" else "red"
    
    console.print(f"[{color}]{icon} {check_name}[/{color}]")
    if message:
        console.print(f"  {message}")
    
    if verbose and details:
        console.print(f"[dim]  Details:[/dim]")
        for key, value in details.items():
            console.print(f"[dim]    {key}: {value}[/dim]")
    
    console.print()


def display_all_results(results: Dict[str, Dict[str, Any]], verbose: bool) -> None:
    """
    Display all check results.
    
    Args:
        results: Dictionary of check results
        verbose: Enable verbose output
    """
    passed = 0
    warnings = 0
    failed = 0
    
    for check_name, result in results.items():
        status = result.get("status", "unknown")
        
        icon = "✅" if status == "passed" else "⚠️" if status == "warning" else "❌"
        color = "green" if status == "passed" else "yellow" if status == "warning" else "red"
        display_name = HEALTH_CHECKS.get(check_name, check_name)
        
        console.print(f"[{color}]{icon} {display_name}[/{color}]")
        
        if status == "passed":
            passed += 1
        elif status == "warning":
            warnings += 1
        else:
            failed += 1
        
        message = result.get("message", "")
        if message:
            console.print(f"  {message}")
        
        if verbose:
            details = result.get("details", {})
            if details:
                console.print(f"[dim]  Details:[/dim]")
                for key, value in details.items():
                    console.print(f"[dim]    {key}: {value}[/dim]")
        
        console.print()
    
    # Summary
    console.print("[bold]Summary:[/bold]")
    console.print(f"  [green]Passed: {passed}[/green]")
    if warnings:
        console.print(f"  [yellow]Warnings: {warnings}[/yellow]")
    if failed:
        console.print(f"  [red]Failed: {failed}[/red]")