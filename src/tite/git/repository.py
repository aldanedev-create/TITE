"""
Git repository management for Tite.

This module provides high-level Git repository operations including
cloning, branching, committing, and status checking.
"""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from tite.exceptions import GitError


class GitRepository:
    """
    Manages Git repository operations.
    
    This class provides a high-level interface for Git operations
    including status, commit, branch, and remote management.
    
    Attributes:
        path: Repository path
    """
    
    def __init__(self, path: Path):
        """
        Initialize the Git repository.
        
        Args:
            path: Repository path
        """
        self.path = Path(path)
        
    def _run_git(self, args: List[str], check: bool = True) -> Tuple[int, str, str]:
        """
        Run a git command.
        
        Args:
            args: Command arguments
            check: Whether to check return code
            
        Returns:
            Tuple[int, str, str]: (return_code, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.path,
                capture_output=True,
                text=True,
                check=check,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr
            
    def is_initialized(self) -> bool:
        """Check if the repository is initialized."""
        return (self.path / ".git").exists()
        
    def get_branch(self) -> Optional[str]:
        """
        Get the current branch name.
        
        Returns:
            Optional[str]: Current branch name
        """
        if not self.is_initialized():
            return None
            
        rc, stdout, _ = self._run_git(["branch", "--show-current"])
        if rc == 0 and stdout:
            return stdout.strip()
        return None
        
    def get_remote(self, name: str = "origin") -> Optional[str]:
        """
        Get remote URL.
        
        Args:
            name: Remote name
            
        Returns:
            Optional[str]: Remote URL
        """
        if not self.is_initialized():
            return None
            
        rc, stdout, _ = self._run_git(["remote", "get-url", name])
        if rc == 0 and stdout:
            return stdout.strip()
        return None
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get repository status.
        
        Returns:
            Dict[str, Any]: Status information
        """
        status = {
            "initialized": self.is_initialized(),
            "branch": self.get_branch(),
            "remote": self.get_remote(),
            "changes": [],
            "untracked": [],
            "commits_ahead": 0,
            "commits_behind": 0,
        }
        
        if not status["initialized"]:
            return status
            
        # Get status
        rc, stdout, _ = self._run_git(["status", "--porcelain"])
        if rc == 0:
            for line in stdout.strip().split("\n"):
                if not line:
                    continue
                if line.startswith("??"):
                    status["untracked"].append(line[3:])
                else:
                    status["changes"].append(line)
                    
        # Get commit counts
        rc, stdout, _ = self._run_git(["rev-list", "--count", "HEAD...origin/HEAD"])
        if rc == 0:
            try:
                ahead, behind = stdout.strip().split("\t")
                status["commits_ahead"] = int(ahead)
                status["commits_behind"] = int(behind)
            except ValueError:
                pass
                
        return status
        
    def add(self, files: Optional[List[str]] = None) -> bool:
        """
        Add files to staging.
        
        Args:
            files: Files to add (all if None)
            
        Returns:
            bool: True if successful
        """
        args = ["add"]
        if files:
            args.extend(files)
        else:
            args.append(".")
            
        rc, _, stderr = self._run_git(args)
        if rc != 0:
            logger.error(f"Failed to add files: {stderr}")
            return False
        return True
        
    def commit(self, message: str, all_files: bool = False) -> bool:
        """
        Commit changes.
        
        Args:
            message: Commit message
            all_files: Whether to add all files first
            
        Returns:
            bool: True if successful
        """
        if all_files:
            if not self.add():
                return False
                
        rc, _, stderr = self._run_git(["commit", "-m", message])
        if rc != 0:
            logger.error(f"Failed to commit: {stderr}")
            return False
        return True
        
    def push(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """
        Push changes.
        
        Args:
            remote: Remote name
            branch: Branch name (uses current if None)
            
        Returns:
            bool: True if successful
        """
        if branch is None:
            branch = self.get_branch()
            if not branch:
                logger.error("No branch to push")
                return False
                
        rc, _, stderr = self._run_git(["push", remote, branch])
        if rc != 0:
            logger.error(f"Failed to push: {stderr}")
            return False
        return True
        
    def pull(self, remote: str = "origin", branch: Optional[str] = None) -> bool:
        """
        Pull changes.
        
        Args:
            remote: Remote name
            branch: Branch name (uses current if None)
            
        Returns:
            bool: True if successful
        """
        if branch is None:
            branch = self.get_branch()
            if not branch:
                logger.error("No branch to pull")
                return False
                
        rc, _, stderr = self._run_git(["pull", remote, branch])
        if rc != 0:
            logger.error(f"Failed to pull: {stderr}")
            return False
        return True
        
    def create_branch(self, name: str, checkout: bool = True) -> bool:
        """
        Create a branch.
        
        Args:
            name: Branch name
            checkout: Whether to checkout the new branch
            
        Returns:
            bool: True if successful
        """
        rc, _, stderr = self._run_git(["branch", name])
        if rc != 0:
            logger.error(f"Failed to create branch: {stderr}")
            return False
            
        if checkout:
            return self.checkout(name)
        return True
        
    def checkout(self, name: str) -> bool:
        """
        Checkout a branch.
        
        Args:
            name: Branch name
            
        Returns:
            bool: True if successful
        """
        rc, _, stderr = self._run_git(["checkout", name])
        if rc != 0:
            logger.error(f"Failed to checkout: {stderr}")
            return False
        return True
        
    def clone(self, url: str, path: Optional[Path] = None) -> bool:
        """
        Clone a repository.
        
        Args:
            url: Repository URL
            path: Destination path
            
        Returns:
            bool: True if successful
        """
        dest = path or self.path
        rc, _, stderr = self._run_git(["clone", url, str(dest)])
        if rc != 0:
            logger.error(f"Failed to clone: {stderr}")
            return False
        return True
        
    def get_log(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get commit log.
        
        Args:
            count: Number of commits
            
        Returns:
            List[Dict[str, Any]]: Commit log entries
        """
        if not self.is_initialized():
            return []
            
        format_str = "%H|%an|%ae|%ai|%s"
        rc, stdout, _ = self._run_git(["log", f"-{count}", f"--format={format_str}"])
        
        commits = []
        if rc == 0:
            for line in stdout.strip().split("\n"):
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) >= 5:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4],
                    })
        return commits


class RepositoryManager:
    """
    Manages Git repositories with higher-level operations.
    
    This class provides additional functionality for repository
    management including cloning, initialization, and maintenance.
    
    Attributes:
        repo: GitRepository instance
    """
    
    def __init__(self, path: Path):
        """
        Initialize the repository manager.
        
        Args:
            path: Repository path
        """
        self.repo = GitRepository(path)
        
    def init_from_template(self, template: Dict[str, Any]) -> bool:
        """
        Initialize from a template.
        
        Args:
            template: Template configuration
            
        Returns:
            bool: True if successful
        """
        # Create repository
        from tite.git.init import GitInitializer
        initializer = GitInitializer(self.repo.path)
        initializer.init_standard()
        
        # Configure from template
        for key, value in template.items():
            self.repo._run_git(["config", "--local", key, value])
            
        return True
        
    def setup_gitflow(self) -> bool:
        """
        Setup GitFlow branching model.
        
        Returns:
            bool: True if successful
        """
        # Create branches
        branches = ["develop", "feature", "release", "hotfix"]
        for branch in branches:
            if branch not in ["develop"]:
                self.repo.create_branch(branch, checkout=False)
                
        # Set default branch
        self.repo.checkout("main")
        
        # Configure GitFlow
        self.repo._run_git(["config", "--local", "gitflow.branch.main", "main"])
        self.repo._run_git(["config", "--local", "gitflow.branch.develop", "develop"])
        
        return True
        
    def get_summary(self) -> Dict[str, Any]:
        """
        Get repository summary.
        
        Returns:
            Dict[str, Any]: Repository summary
        """
        status = self.repo.get_status()
        summary = {
            "path": str(self.repo.path),
            "initialized": status["initialized"],
            "branch": status["branch"],
            "remote": status["remote"],
            "changes": len(status["changes"]),
            "untracked": len(status["untracked"]),
            "commits_ahead": status["commits_ahead"],
            "commits_behind": status["commits_behind"],
            "last_commit": None,
        }
        
        # Get last commit
        commits = self.repo.get_log(1)
        if commits:
            summary["last_commit"] = commits[0]
            
        return summary