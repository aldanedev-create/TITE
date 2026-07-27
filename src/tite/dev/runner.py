"""
Process runner for Tite.

This module handles running and managing subprocesses for the
development server.
"""

import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO

from loguru import logger


class ProcessRunner:
    """
    Manages a subprocess for the development server.

    This class handles starting, stopping, and monitoring a
    subprocess with output streaming and environment management.

    Attributes:
        cwd: Working directory
        env_file: Environment file
        env_prefix: Environment variable prefix
        process: Subprocess instance
        running: Whether the process is running
        _stdout_thread: Thread for reading stdout
        _stderr_thread: Thread for reading stderr
    """

    def __init__(
        self,
        cwd: Optional[Path] = None,
        env_file: Optional[str] = None,
        env_prefix: Optional[str] = None,
    ):
        """
        Initialize the process runner.

        Args:
            cwd: Working directory
            env_file: Environment file
            env_prefix: Environment variable prefix
        """
        self.cwd = Path(cwd) if cwd else Path.cwd()
        self.env_file = env_file or ".env"
        self.env_prefix = env_prefix or "APP_"
        self.process: Optional[subprocess.Popen] = None
        self.running = False
        self._stdout_thread: Optional[threading.Thread] = None
        self._stderr_thread: Optional[threading.Thread] = None
        self._start_time: Optional[float] = None
        self._exit_code: Optional[int] = None

    def start(
        self,
        command: str,
        env: Optional[Dict[str, str]] = None,
        shell: bool = True,
    ) -> bool:
        """
        Start the process.

        Args:
            command: Command to run
            env: Environment variables
            shell: Whether to use shell

        Returns:
            bool: True if started successfully
        """
        if self.running and self.is_alive():
            logger.warning("Process is already running")
            return False

        logger.info(f"Starting process: {command}")

        # Prepare environment
        env_vars = self._get_environment(env)

        try:
            # Set process group creation flags for proper process tree termination
            kwargs: Dict[str, Any] = {
                "cwd": self.cwd,
                "env": env_vars,
                "shell": shell,
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
                "text": True,
                "bufsize": 1,
            }

            if sys.platform == "win32":
                kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            else:
                kwargs["start_new_session"] = True

            # Start process
            self.process = subprocess.Popen(command, **kwargs)

            self.running = True
            self._start_time = time.time()
            self._exit_code = None

            # Start output readers
            if self.process.stdout:
                self._stdout_thread = threading.Thread(
                    target=self._read_output,
                    args=(self.process.stdout, "stdout"),
                    daemon=True,
                )
                self._stdout_thread.start()

            if self.process.stderr:
                self._stderr_thread = threading.Thread(
                    target=self._read_output,
                    args=(self.process.stderr, "stderr"),
                    daemon=True,
                )
                self._stderr_thread.start()

            logger.info(f"Process started (PID: {self.process.pid})")
            return True

        except Exception as e:
            logger.error(f"Failed to start process: {e}")
            self.running = False
            return False

    def _read_output(self, stream: TextIO, name: str) -> None:
        """
        Read output from a stream safely.

        Args:
            stream: Stream to read from
            name: Stream name (stdout/stderr)
        """
        try:
            for line in iter(stream.readline, ""):
                if not line:
                    break
                clean_line = line.rstrip()
                if name == "stdout":
                    logger.info(clean_line)
                else:
                    logger.error(clean_line)
        except (ValueError, IOError):
            # Handles stream closure during process teardown
            pass
        finally:
            try:
                stream.close()
            except Exception:
                pass

    def _get_environment(self, extra_env: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Get environment variables for the process.

        Args:
            extra_env: Extra environment variables

        Returns:
            Dict[str, str]: Environment variables
        """
        env = os.environ.copy()

        # Load from .env file
        env_file_path = self.cwd / self.env_file
        if env_file_path.exists():
            try:
                from dotenv import dotenv_values
                loaded_env = dotenv_values(env_file_path)
                # Convert None values to empty strings safely
                env.update({k: v if v is not None else "" for k, v in loaded_env.items()})
            except ImportError:
                logger.debug("python-dotenv not installed, skipping .env loading")

        # Add prefix-specific variables
        if self.env_prefix:
            prefixed = {}
            for key, value in list(env.items()):
                if key.startswith(self.env_prefix):
                    new_key = key[len(self.env_prefix):]
                    prefixed[new_key] = value
            env.update(prefixed)

        # Add extra environment variables
        if extra_env:
            env.update(extra_env)

        return env

    def stop(self, timeout: float = 5.0) -> bool:
        """
        Stop the process and all child sub-processes across platforms.

        Args:
            timeout: Timeout for graceful shutdown

        Returns:
            bool: True if stopped successfully
        """
        if not self.running or not self.process:
            self.running = False
            return True

        logger.info("Stopping process...")

        try:
            pid = self.process.pid

            if sys.platform == "win32":
                # Windows taskkill kills the process tree forcefully or gracefully
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            else:
                # Send SIGTERM to process group on POSIX
                try:
                    pgid = os.getpgid(pid)
                    os.killpg(pgid, signal.SIGTERM)
                except ProcessLookupError:
                    pass

            # Wait for exit
            try:
                self.process.wait(timeout=timeout)
                self._exit_code = self.process.returncode
            except subprocess.TimeoutExpired:
                logger.warning("Process did not stop gracefully, killing process group...")
                if sys.platform != "win32":
                    try:
                        pgid = os.getpgid(pid)
                        os.killpg(pgid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                self.process.kill()
                self.process.wait()
                self._exit_code = self.process.returncode

        except Exception as e:
            logger.error(f"Failed to stop process: {e}")
            self.running = False
            return False

        self.running = False
        logger.info(f"Process stopped (exit code: {self._exit_code})")
        return True

    def restart(self, command: str, env: Optional[Dict[str, str]] = None) -> bool:
        """
        Restart the process.

        Args:
            command: Command to run
            env: Environment variables

        Returns:
            bool: True if restarted successfully
        """
        self.stop()
        time.sleep(0.5)
        return self.start(command, env)

    def is_alive(self) -> bool:
        """
        Check if the process is alive.

        Returns:
            bool: True if process is running
        """
        if not self.process or not self.running:
            return False

        alive = self.process.poll() is None
        if not alive and self.running:
            self.running = False
            self._exit_code = self.process.returncode

        return alive

    def get_pid(self) -> Optional[int]:
        """
        Get the process PID.

        Returns:
            Optional[int]: Process PID or None
        """
        if self.process:
            return self.process.pid
        return None

    def get_exit_code(self) -> Optional[int]:
        """
        Get the process exit code.

        Returns:
            Optional[int]: Exit code or None
        """
        if self.process:
            code = self.process.poll()
            if code is not None:
                self._exit_code = code
        return self._exit_code

    def get_uptime(self) -> Optional[float]:
        """
        Get process uptime in seconds.

        Returns:
            Optional[float]: Uptime in seconds or None
        """
        if self._start_time and self.is_alive():
            return time.time() - self._start_time
        return None

    def send_signal(self, signal_type: int) -> bool:
        """
        Send a signal to the process.

        Args:
            signal_type: Signal to send

        Returns:
            bool: True if signal was sent
        """
        if not self.process or not self.is_alive():
            return False

        try:
            if sys.platform != "win32":
                pgid = os.getpgid(self.process.pid)
                os.killpg(pgid, signal_type)
            else:
                self.process.send_signal(signal_type)
            return True
        except Exception as e:
            logger.error(f"Failed to send signal: {e}")
            return False