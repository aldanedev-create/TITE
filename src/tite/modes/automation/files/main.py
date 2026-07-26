"""
Main entry point for the automation application.

This module provides the main execution entry for running the
automation scheduler and tasks.
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from src.scheduler import TaskScheduler, AsyncTaskScheduler
from src.utils.logger import setup_logging
from src.tasks.base import BaseTask


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Automation Scheduler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--config", "-c",
        type=Path,
        default=Path("config/schedule.yaml"),
        help="Path to configuration file",
    )
    
    parser.add_argument(
        "--async",
        dest="async_mode",
        action="store_true",
        default=True,
        help="Use async scheduler (default: True)",
    )
    
    parser.add_argument(
        "--sync",
        dest="async_mode",
        action="store_false",
        help="Use sync scheduler",
    )
    
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Start command
    subparsers.add_parser("start", help="Start the scheduler")
    
    # Run task command
    run_parser = subparsers.add_parser("run", help="Run a specific task")
    run_parser.add_argument("task", help="Task name to run")
    run_parser.add_argument("--args", nargs="*", help="Positional arguments")
    run_parser.add_argument("--kwargs", nargs="*", help="Keyword arguments (key=value)")
    
    # List tasks command
    subparsers.add_parser("list", help="List all registered tasks")
    
    # Status command
    subparsers.add_parser("status", help="Show scheduler status")
    
    # Health command
    subparsers.add_parser("health", help="Check health status")
    
    return parser.parse_args()


def run_start(args: argparse.Namespace) -> int:
    """
    Run the start command.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        if args.async_mode:
            scheduler = AsyncTaskScheduler(args.config)
            
            # Run async scheduler
            try:
                asyncio.run(scheduler.start_async())
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                return 0
        else:
            scheduler = TaskScheduler(args.config, asyncio_mode=False)
            scheduler.start()
            
            # Keep running
            try:
                while scheduler.running:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                scheduler.stop()
                
        return 0
        
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        return 1


def run_task(args: argparse.Namespace) -> int:
    """
    Run a specific task.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        # Parse arguments
        task_args = args.args or []
        task_kwargs = {}
        
        if args.kwargs:
            for kwarg in args.kwargs:
                if "=" in kwarg:
                    key, value = kwarg.split("=", 1)
                    task_kwargs[key] = value
                    
        # Load and run task
        import importlib
        
        # Try to import task
        task_name = args.task
        module_name = f"src.tasks.{task_name}"
        
        try:
            module = importlib.import_module(module_name)
            task_class = getattr(module, task_name.title().replace("_", ""))
            task = task_class()
            
            logger.info(f"Running task: {task_name}")
            result = task.run(*task_args, **task_kwargs)
            logger.info(f"Task completed: {task_name}")
            
            if result:
                print(result)
                
            return 0
            
        except ImportError:
            logger.error(f"Task not found: {task_name}")
            return 1
            
    except Exception as e:
        logger.error(f"Task failed: {e}")
        return 1


def run_list(args: argparse.Namespace) -> int:
    """
    List all registered tasks.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        # Discover tasks
        import importlib
        import pkgutil
        import src.tasks
        
        tasks = []
        
        for module_info in pkgutil.iter_modules(src.tasks.__path__):
            if module_info.name.startswith("_"):
                continue
                
            module_name = f"src.tasks.{module_info.name}"
            try:
                module = importlib.import_module(module_name)
                
                # Find task classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, BaseTask) and 
                        attr != BaseTask):
                        tasks.append(attr.__name__)
                        
            except Exception:
                pass
                
        if tasks:
            print("Registered tasks:")
            for task in sorted(tasks):
                print(f"  - {task}")
        else:
            print("No tasks found")
            
        return 0
        
    except Exception as e:
        logger.error(f"Failed to list tasks: {e}")
        return 1


def run_status(args: argparse.Namespace) -> int:
    """
    Show scheduler status.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        scheduler = TaskScheduler(args.config, asyncio_mode=False)
        
        print(f"Scheduler: {'Running' if scheduler.running else 'Stopped'}")
        print(f"Tasks: {len(scheduler.tasks)}")
        print(f"Jobs: {len(scheduler.get_jobs())}")
        
        jobs = scheduler.get_jobs()
        if jobs:
            print("\nScheduled Jobs:")
            for job in jobs:
                next_run = job["next_run_time"]
                print(f"  - {job['id']}: {job['trigger']} (next: {next_run})")
                
        return 0
        
    except Exception as e:
        logger.error(f"Failed to get status: {e}")
        return 1


def run_health(args: argparse.Namespace) -> int:
    """
    Check health status.
    
    Args:
        args: Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        scheduler = TaskScheduler(args.config, asyncio_mode=False)
        
        status = {
            "status": "healthy" if scheduler.running else "stopped",
            "tasks": len(scheduler.tasks),
            "jobs": len(scheduler.get_jobs()),
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        }
        
        if args.async_mode:
            status["mode"] = "async"
        else:
            status["mode"] = "sync"
            
        print(status)
        
        if scheduler.running:
            return 0
        else:
            return 1
            
    except Exception as e:
        print({"status": "unhealthy", "error": str(e)})
        return 1


def main() -> int:
    """
    Main entry point.
    
    Returns:
        int: Exit code
    """
    args = parse_args()
    
    # Setup logging
    setup_logging(level=args.log_level)
    
    # Run command
    if args.command == "start":
        return run_start(args)
    elif args.command == "run":
        return run_task(args)
    elif args.command == "list":
        return run_list(args)
    elif args.command == "status":
        return run_status(args)
    elif args.command == "health":
        return run_health(args)
    else:
        print("Unknown command. Use --help for usage.")
        return 1


if __name__ == "__main__":
    sys.exit(main())