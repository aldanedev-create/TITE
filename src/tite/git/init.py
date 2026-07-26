"""
Git initialization for Tite.

This module handles Git repository initialization and basic
setup for Tite projects.
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from loguru import logger

from tite.exceptions import GitError


class GitInit:
    """
    Git initialization operations.
    
    This class handles Git repository initialization with
    proper configuration and setup.
    
    Attributes:
        path: Repository path
        initialized: Whether the repository is initialized
    """
    
    def __init__(self, path: Path):
        """
        Initialize Git operations.
        
        Args:
            path: Repository path
        """
        self.path = Path(path)
        self.initialized = self._check_initialized()
        
    def _check_initialized(self) -> bool:
        """
        Check if Git is initialized.
        
        Returns:
            bool: True if Git is initialized
        """
        return (self.path / ".git").exists()
        
    def init(
        self,
        bare: bool = False,
        template: Optional[Path] = None,
        initial_branch: str = "main",
    ) -> bool:
        """
        Initialize a Git repository.
        
        Args:
            bare: Whether to create a bare repository
            template: Template directory
            initial_branch: Initial branch name
            
        Returns:
            bool: True if successful
            
        Raises:
            GitError: If initialization fails
        """
        if self.initialized:
            logger.info("Git repository already initialized")
            return True
            
        logger.info(f"Initializing Git repository: {self.path}")
        
        try:
            cmd = ["git", "init"]
            
            if bare:
                cmd.append("--bare")
                
            if template:
                cmd.extend(["--template", str(template)])
                
            if initial_branch:
                cmd.extend(["--initial-branch", initial_branch])
                
            result = subprocess.run(
                cmd,
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True,
            )
            
            self.initialized = True
            logger.info("Git repository initialized")
            
            # Configure basic settings
            self._configure()
            
            return True
            
        except subprocess.CalledProcessError as e:
            raise GitError("init", f"Failed to initialize Git: {e.stderr}")
            
    def _configure(self) -> None:
        """Configure basic Git settings."""
        try:
            # Set user info if not set
            self._set_user_config()
            
            # Set default branch
            self._set_default_branch()
            
        except Exception as e:
            logger.warning(f"Failed to configure Git: {e}")
            
    def _set_user_config(self) -> None:
        """Set user configuration."""
        try:
            # Check if user.name is set
            result = subprocess.run(
                ["git", "config", "--local", "user.name"],
                cwd=self.path,
                capture_output=True,
                text=True,
            )
            
            if not result.stdout.strip():
                # Set default user
                import getpass
                import os
                
                user = os.environ.get("GIT_AUTHOR_NAME") or getpass.getuser()
                email = os.environ.get("GIT_AUTHOR_EMAIL") or f"{user}@example.com"
                
                self._run_git_config("user.name", user)
                self._run_git_config("user.email", email)
                
        except Exception:
            pass
            
    def _set_default_branch(self) -> None:
        """Set default branch name."""
        try:
            self._run_git_config("init.defaultBranch", "main")
        except Exception:
            pass
            
    def _run_git_config(self, key: str, value: str) -> None:
        """
        Run git config command.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        try:
            subprocess.run(
                ["git", "config", "--local", key, value],
                cwd=self.path,
                capture_output=True,
                check=True,
            )
        except Exception:
            pass
            
    def is_initialized(self) -> bool:
        """
        Check if Git is initialized.
        
        Returns:
            bool: True if Git is initialized
        """
        return self.initialized
        
    def get_git_version(self) -> Optional[str]:
        """
        Get Git version.
        
        Returns:
            Optional[str]: Git version string
        """
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except Exception:
            return None


class GitInitializer:
    """
    Advanced Git initialization with templates.
    
    This class provides advanced Git initialization with
    template support and custom configurations.
    
    Attributes:
        init: GitInit instance
    """
    
    def __init__(self, path: Path):
        """
        Initialize the Git initializer.
        
        Args:
            path: Repository path
        """
        self.init = GitInit(path)
        
    def init_with_template(self, template: Dict[str, str]) -> bool:
        """
        Initialize Git with template configuration.
        
        Args:
            template: Template configuration
            
        Returns:
            bool: True if successful
        """
        if not self.init.init():
            return False
            
        # Apply template
        for key, value in template.items():
            try:
                subprocess.run(
                    ["git", "config", "--local", key, value],
                    cwd=self.init.path,
                    capture_output=True,
                    check=True,
                )
            except Exception:
                pass
                
        return True
        
    def init_standard(self) -> bool:
        """
        Initialize with standard configuration.
        
        Returns:
            bool: True if successful
        """
        template = {
            "core.autocrlf": "input" if sys.platform != "win32" else "true",
            "core.ignorecase": "true" if sys.platform == "win32" else "false",
            "core.precomposeunicode": "true" if sys.platform == "darwin" else "false",
            "pull.rebase": "false",
            "fetch.prune": "true",
            "init.defaultBranch": "main",
        }
        return self.init_with_template(template)
        
    def init_github(self, remote_url: str, branch: str = "main") -> bool:
        """
        Initialize with GitHub configuration.
        
        Args:
            remote_url: GitHub repository URL
            branch: Default branch name
            
        Returns:
            bool: True if successful
        """
        template = {
            "init.defaultBranch": branch,
            "remote.origin.url": remote_url,
            "remote.origin.fetch": f"+refs/heads/*:refs/remotes/origin/*",
            "branch.{branch}.remote": "origin",
            "branch.{branch}.merge": f"refs/heads/{branch}",
        }
        
        # Replace branch placeholder
        template = {k.replace("{branch}", branch): v for k, v in template.items()}
        
        return self.init_with_template(template)
        
    def init_gitlab(self, remote_url: str, branch: str = "main") -> bool:
        """
        Initialize with GitLab configuration.
        
        Args:
            remote_url: GitLab repository URL
            branch: Default branch name
            
        Returns:
            bool: True if successful
        """
        return self.init_github(remote_url, branch)