"""
Core process manager for Tite.

Runs shell commands within a project directory. Returns real
subprocess.CompletedProcess objects so callers can use .returncode,
.stdout, and .stderr directly.
"""

import subprocess
from pathlib import Path
from typing import List, Optional, Union


class ProcessManager:
    """
    Runs subprocesses scoped to a project directory.

    Attributes:
        project_path: Default working directory for commands
    """

    def __init__(self, project_path: Union[str, Path]):
        """
        Initialize the process manager.

        Args:
            project_path: Default working directory for commands
        """
        self.project_path = Path(project_path)

    def run(
        self,
        cmd: Union[str, List[str]],
        cwd: Optional[Union[str, Path]] = None,
        capture_output: bool = True,
        check: bool = False,
        shell: Optional[bool] = None,
        env: Optional[dict] = None,
    ) -> subprocess.CompletedProcess:
        """
        Run a command.

        Args:
            cmd: Command and arguments (list) or a shell command string
            cwd: Working directory (defaults to project_path)
            capture_output: Whether to capture stdout/stderr
            check: Whether to raise on non-zero exit code
            shell: Whether to run through the shell (defaults to True
                only if cmd is a string)
            env: Environment variables to use for the subprocess

        Returns:
            subprocess.CompletedProcess: Result of the command
        """
        if shell is None:
            shell = isinstance(cmd, str)

        return subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else str(self.project_path),
            capture_output=capture_output,
            text=True,
            check=check,
            shell=shell,
            env=env,
        )