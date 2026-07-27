"""
Development server for Tite.

This module provides the main development server with hot reload
capabilities, similar to Vite for Python.
"""

import os
import signal
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from tite.dev.watcher import FileWatcher
from tite.dev.runner import ProcessRunner
from tite.dev.reload import Reloader
from tite.dev.browser import BrowserLauncher
from tite.core.config import ConfigManager


class DevServer:
    """
    Development server with hot reload.

    This class manages the development server process, file watching,
    and automatic reloading on file changes.

    Attributes:
        project_path: Path to the project
        config: Server configuration
        runner: Process runner
        watcher: File watcher
        reloader: Reloader
        browser: Browser launcher
        running: Whether the server is running
    """

    def __init__(
        self,
        project_path: Optional[Path] = None,
        config: Optional[Dict[str, Any]] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        command: Optional[str] = None,
        no_reload: bool = False,
        no_browser: bool = False,
        verbose: bool = False,
    ):
        """
        Initialize the development server.

        Args:
            project_path: Path to the project
            config: Server configuration
            host: Host to bind to
            port: Port to bind to
            command: Command to run
            no_reload: Disable auto-reload
            no_browser: Don't open browser
            verbose: Enable verbose output
        """
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.no_reload = no_reload
        self.no_browser = no_browser
        self.verbose = verbose
        self.running = False

        # Load configuration
        self.config_manager = ConfigManager(self.project_path)
        self.config = config or self._load_config()

        # Ensure "dev" section exists in config
        if "dev" not in self.config:
            self.config["dev"] = {}

        # Override with command-line arguments
        if host:
            self.config["dev"]["host"] = host
        if port:
            self.config["dev"]["port"] = port
        if command:
            self.config["dev"]["command"] = command

        # Get settings
        self.host = self.config["dev"].get("host", "127.0.0.1")
        self.port = self.config["dev"].get("port", 8000)
        self.command = self.config["dev"].get("command", "python src/main.py")
        self.env_file = self.config["dev"].get("env_file", ".env")
        self.env_prefix = self.config["dev"].get("env_prefix", "APP_")
        self.debug = self.config["dev"].get("debug", False)

        # Initialize components
        self.runner = ProcessRunner(
            cwd=self.project_path,
            env_file=self.env_file,
            env_prefix=self.env_prefix,
        )

        watcher_config = self.config.get("watcher", {})
        self.watcher = FileWatcher(
            paths=watcher_config.get("paths", ["src", "tests"]),
            extensions=watcher_config.get("extensions", [".py"]),
            ignore=watcher_config.get("ignore", []),
            debounce=watcher_config.get("debounce", 100),
        )

        self.reloader = Reloader(
            restart_on_change=watcher_config.get("restart_on_change", True),
        )

        self.browser = BrowserLauncher()

        # Setup signal handlers safely
        if threading.current_thread() is threading.main_thread():
            try:
                signal.signal(signal.SIGINT, self._signal_handler)
                signal.signal(signal.SIGTERM, self._signal_handler)
            except (ValueError, OSError):
                pass

    def _load_config(self) -> Dict[str, Any]:
        """
        Load server configuration.

        Returns:
            Dict[str, Any]: Server configuration
        """
        try:
            return self.config_manager.load()
        except Exception as e:
            logger.warning(f"Failed to load config: {e}")
            return {
                "dev": {
                    "command": "python src/main.py",
                    "port": 8000,
                    "host": "127.0.0.1",
                    "env_file": ".env",
                    "env_prefix": "APP_",
                    "debug": False,
                },
                "watcher": {
                    "paths": ["src", "tests"],
                    "extensions": [".py", ".html", ".css", ".js"],
                    "ignore": [".venv", "__pycache__", "*.egg-info"],
                    "debounce": 100,
                    "restart_on_change": True,
                },
            }

    def start(self) -> None:
        """
        Start the development server.
        """
        if self.running:
            logger.warning("Server is already running")
            return

        logger.info("Starting development server...")
        logger.info(f"  Command: {self.command}")
        logger.info(f"  Host: {self.host}")
        logger.info(f"  Port: {self.port}")
        logger.info(f"  Auto-reload: {'Enabled' if not self.no_reload else 'Disabled'}")
        logger.info(f"  Debug: {self.debug}")
        logger.info(f"  Project: {self.project_path}")

        self.running = True

        # Set environment variables
        os.environ["TITE_DEV"] = "1"
        os.environ["TITE_HOST"] = str(self.host)
        os.environ["TITE_PORT"] = str(self.port)
        os.environ["TITE_DEBUG"] = str(self.debug)

        # Start the process
        self._start_process()

        # Start file watcher if reload is enabled
        if not self.no_reload:
            self._start_watcher()

        # Open browser
        if not self.no_browser:
            self.browser.open(f"http://{self.host}:{self.port}")

        # Keep the server running
        try:
            while self.running:
                time.sleep(0.1)

                # Check if process is still running
                if self.runner.is_alive():
                    continue

                # Process exited
                exit_code = self.runner.get_exit_code()
                if exit_code is not None and exit_code != 0:
                    logger.error(f"Process exited with code {exit_code}")

                # Restart if auto-reload is enabled
                if not self.no_reload and self.running:
                    logger.info("Process exited, restarting...")
                    self._start_process()

        except KeyboardInterrupt:
            self.stop()

    def _start_process(self) -> None:
        """
        Start the development process.
        """
        try:
            env = self._get_environment()
            self.runner.start(self.command, env=env)
            logger.info(f"Server running on http://{self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to start process: {e}")
            self.running = False

    def _get_environment(self) -> Dict[str, str]:
        """
        Get environment variables for the process.

        Returns:
            Dict[str, str]: Environment variables
        """
        env = os.environ.copy()

        # Add Tite-specific variables
        env["TITE_DEV"] = "1"
        env["TITE_HOST"] = str(self.host)
        env["TITE_PORT"] = str(self.port)
        env["TITE_DEBUG"] = str(self.debug)

        # Load from .env file safely
        env_file = self.project_path / self.env_file
        if env_file.exists():
            try:
                from dotenv import dotenv_values
                loaded_env = dotenv_values(env_file)
                env.update({k: str(v) if v is not None else "" for k, v in loaded_env.items()})
            except ImportError:
                logger.debug("python-dotenv not installed, skipping .env loading")

        return env

    def _start_watcher(self) -> None:
        """
        Start the file watcher.
        """
        def on_change(events: List[Dict[str, Any]]):
            if not self.running:
                return

            logger.info("File change detected, reloading...")

            # Stop the current process
            self.runner.stop()

            # Start a new process
            self._start_process()

        self.watcher.on_change = on_change
        self.watcher.start()

    def _signal_handler(self, signum: int, frame: Any) -> None:
        """
        Handle termination signals.
        """
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)

    def stop(self) -> None:
        """
        Stop the development server.
        """
        if not self.running:
            return

        logger.info("Stopping development server...")
        self.running = False

        # Stop watcher
        if hasattr(self, "watcher"):
            self.watcher.stop()

        # Stop process
        if hasattr(self, "runner"):
            self.runner.stop()

        logger.info("Server stopped")

    def restart(self) -> None:
        """
        Restart the development server.
        """
        logger.info("Restarting development server...")
        self.stop()
        time.sleep(0.5)
        self.start()

    def get_status(self) -> Dict[str, Any]:
        """
        Get server status.

        Returns:
            Dict[str, Any]: Server status
        """
        return {
            "running": self.running,
            "host": self.host,
            "port": self.port,
            "command": self.command,
            "reload_enabled": not self.no_reload,
            "process_running": self.runner.is_alive(),
            "pid": self.runner.get_pid(),
            "uptime": self.runner.get_uptime(),
        }