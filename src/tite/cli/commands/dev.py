"""
Development server command for Tite.

This module handles starting the development server with hot reload
functionality, similar to Vite for Python.
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from tite.cli.output import print_error, print_info, print_success, print_warning, console
from tite.cli.progress import Spinner
from tite.constants import ERROR_CODES, WATCH_EXTENSIONS, WATCH_EXCLUDE
from tite.core.config import ConfigManager
from tite.exceptions import ConfigurationError, EnvironmentError


class DevServer:
    """
    Development server with hot reload.
    
    This class manages the development server process and file watching
    for automatic reload on changes.
    """
    
    def __init__(
        self,
        project_dir: Path,
        command: Optional[str] = None,
        host: str = "127.0.0.1",
        port: int = 8000,
        no_reload: bool = False,
    ):
        """
        Initialize the development server.
        
        Args:
            project_dir: Project directory
            command: Command to run (overrides config)
            host: Host to bind to
            port: Port to bind to
            no_reload: Disable auto-reload
        """
        self.project_dir = project_dir
        self.host = host
        self.port = port
        self.no_reload = no_reload
        
        self.process: Optional[subprocess.Popen] = None
        self.observer: Optional[Observer] = None
        self.running = False
        
        # Load configuration
        self.config_manager = ConfigManager(project_dir)
        self.config = self.config_manager.load_config()
        
        # Get command from config or use provided
        self.command = command or self.config.get("dev", {}).get("command", "python src/main.py")
        
        # Get watch paths
        self.watch_paths = self.config.get("watcher", {}).get("paths", ["src", "tests"])
        self.watch_extensions = set(self.config.get("watcher", {}).get("extensions", [".py"]))
        self.watch_exclude = set(self.config.get("watcher", {}).get("ignore", []))
        
        # Combine with defaults
        self.watch_extensions.update(WATCH_EXTENSIONS)
        self.watch_exclude.update(WATCH_EXCLUDE)
        
    def start(self) -> bool:
        """
        Start the development server.
        
        Returns:
            bool: True if started successfully
        """
        console.print()
        console.print(f"[bold]Starting development server...[/bold]")
        console.print(f"  [dim]Command:[/dim] {self.command}")
        console.print(f"  [dim]Host:[/dim] {self.host}")
        console.print(f"  [dim]Port:[/dim] {self.port}")
        console.print(f"  [dim]Auto-reload:[/dim] {'Enabled' if not self.no_reload else 'Disabled'}")
        console.print()
        
        # Change to project directory
        os.chdir(self.project_dir)
        
        # Set environment variables
        env = os.environ.copy()
        env["TITE_DEV"] = "1"
        env["TITE_HOST"] = self.host
        env["TITE_PORT"] = str(self.port)
        
        # Start the process
        self.running = True
        self.start_process(env)
        
        # Start file watcher if reload is enabled
        if not self.no_reload:
            self.start_watcher()
        
        # Handle signals
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        
        # Keep running
        try:
            while self.running:
                time.sleep(0.1)
                if self.process and self.process.poll() is not None:
                    # Process exited
                    if self.process.returncode != 0:
                        console.print()
                        print_warning(f"Process exited with code {self.process.returncode}")
                        console.print("[dim]Press Ctrl+C to stop[/dim]")
                    time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
        
        return True
    
    def start_process(self, env: Dict[str, str]) -> None:
        """
        Start the development process.
        
        Args:
            env: Environment variables
        """
        try:
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            
            # Start output reader thread
            import threading
            thread = threading.Thread(target=self.read_output, daemon=True)
            thread.start()
            
            print_success(f"Server running on http://{self.host}:{self.port}")
            console.print("[dim]Press Ctrl+C to stop[/dim]")
            console.print()
            
        except Exception as e:
            print_error(f"Failed to start process: {str(e)}")
            self.running = False
    
    def read_output(self) -> None:
        """
        Read and display process output.
        """
        if not self.process:
            return
        
        for line in iter(self.process.stdout.readline, ""):
            if line:
                # Check for common patterns to colorize
                if "ERROR" in line or "Error" in line:
                    console.print(f"[red]{line.rstrip()}[/red]")
                elif "WARNING" in line or "Warning" in line:
                    console.print(f"[yellow]{line.rstrip()}[/yellow]")
                elif "INFO" in line or "INFO:" in line:
                    console.print(f"[dim]{line.rstrip()}[/dim]")
                else:
                    console.print(line.rstrip())
    
    def start_watcher(self) -> None:
        """
        Start the file watcher.
        """
        class ChangeHandler(FileSystemEventHandler):
            def __init__(self, server):
                self.server = server
            
            def on_modified(self, event):
                if self.should_restart(event):
                    self.server.restart()
            
            def should_restart(self, event):
                # Check if file should trigger restart
                if event.is_directory:
                    return False
                
                # Check extension
                ext = Path(event.src_path).suffix
                if ext and ext not in self.server.watch_extensions:
                    return False
                
                # Check exclude patterns
                for pattern in self.server.watch_exclude:
                    if pattern in event.src_path:
                        return False
                
                return True
        
        print_info(f"Watching for changes in: {', '.join(self.watch_paths)}")
        
        self.observer = Observer()
        handler = ChangeHandler(self)
        
        for watch_path in self.watch_paths:
            full_path = self.project_dir / watch_path
            if full_path.exists():
                self.observer.schedule(handler, str(full_path), recursive=True)
        
        self.observer.start()
    
    def restart(self) -> None:
        """
        Restart the development server.
        """
        console.print()
        print_info("File change detected. Restarting server...")
        
        # Stop current process
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
        
        # Start new process
        env = os.environ.copy()
        env["TITE_DEV"] = "1"
        env["TITE_HOST"] = self.host
        env["TITE_PORT"] = str(self.port)
        
        self.start_process(env)
    
    def stop(self) -> None:
        """
        Stop the development server.
        """
        console.print()
        print_info("Shutting down development server...")
        
        self.running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
        
        console.print("[dim]Server stopped[/dim]")
    
    def handle_signal(self, signum, frame) -> None:
        """
        Handle termination signals.
        """
        self.stop()
        sys.exit(0)


def run_dev(args: Dict[str, Any]) -> int:
    """
    Execute the 'dev' command.
    
    Args:
        args: Dictionary of command arguments
        
    Returns:
        int: Exit code
    """
    host = args.get("host", "127.0.0.1")
    port = args.get("port", 8000)
    command = args.get("run_command")
    no_reload = args.get("no_reload", False)
    
    project_dir = Path.cwd()
    
    # Check if Tite project
    config_path = project_dir / ".tite" / "tite.toml"
    if not config_path.exists():
        print_warning("Not a Tite project. Use 'tite init' first.")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    try:
        # Create and start dev server
        server = DevServer(
            project_dir=project_dir,
            command=command,
            host=host,
            port=port,
            no_reload=no_reload,
        )
        
        server.start()
        return ERROR_CODES["SUCCESS"]
        
    except ConfigurationError as e:
        print_error(f"Configuration error: {str(e)}")
        return ERROR_CODES["CONFIGURATION_ERROR"]
    
    except EnvironmentError as e:
        print_error(f"Environment error: {str(e)}")
        return ERROR_CODES["ENVIRONMENT_ERROR"]
    
    except Exception as e:
        print_error(f"Failed to start development server: {str(e)}")
        if __debug__:
            import traceback
            traceback.print_exc()
        return ERROR_CODES["ERROR"]