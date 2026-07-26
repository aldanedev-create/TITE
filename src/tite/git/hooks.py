"""
Git hooks management for Tite.

This module handles Git hooks for Tite projects including
pre-commit, pre-push, and other hooks.
"""

import stat
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from loguru import logger

from tite.exceptions import FileOperationError


class GitHooks:
    """
    Manages Git hooks.
    
    This class provides functionality for creating, managing,
    and executing Git hooks.
    
    Attributes:
        hooks_dir: Path to hooks directory
        hooks: Dictionary of hook scripts
    """
    
    # Available hooks
    AVAILABLE_HOOKS = [
        "pre-commit",
        "pre-merge-commit",
        "prepare-commit-msg",
        "commit-msg",
        "post-commit",
        "pre-rebase",
        "post-checkout",
        "post-merge",
        "pre-push",
        "pre-receive",
        "update",
        "post-receive",
        "post-update",
        "push-to-checkout",
        "pre-auto-gc",
        "post-rewrite",
    ]
    
    def __init__(self, path: Path):
        """
        Initialize Git hooks manager.
        
        Args:
            path: Repository path
        """
        self.path = Path(path)
        self.hooks_dir = self.path / ".git" / "hooks"
        self.hooks: Dict[str, str] = {}
        self._load_hooks()
        
    def _load_hooks(self) -> None:
        """Load existing hooks."""
        if not self.hooks_dir.exists():
            return
            
        for hook_file in self.hooks_dir.iterdir():
            if hook_file.is_file() and hook_file.name in self.AVAILABLE_HOOKS:
                try:
                    content = hook_file.read_text()
                    self.hooks[hook_file.name] = content
                except Exception:
                    pass
                    
    def add_hook(self, name: str, script: str, executable: bool = True) -> bool:
        """
        Add a hook script.
        
        Args:
            name: Hook name
            script: Hook script content
            executable: Whether to make executable
            
        Returns:
            bool: True if successful
            
        Raises:
            FileOperationError: If hook creation fails
        """
        if name not in self.AVAILABLE_HOOKS:
            logger.warning(f"Unknown hook: {name}")
            
        hook_path = self.hooks_dir / name
        
        try:
            self.hooks_dir.mkdir(parents=True, exist_ok=True)
            hook_path.write_text(script, encoding="utf-8")
            
            if executable:
                hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                
            self.hooks[name] = script
            logger.info(f"Added hook: {name}")
            return True
            
        except Exception as e:
            raise FileOperationError(str(hook_path), "write", str(e))
            
    def remove_hook(self, name: str) -> bool:
        """
        Remove a hook.
        
        Args:
            name: Hook name
            
        Returns:
            bool: True if removed
        """
        hook_path = self.hooks_dir / name
        
        if hook_path.exists():
            hook_path.unlink()
            if name in self.hooks:
                del self.hooks[name]
            logger.info(f"Removed hook: {name}")
            return True
        return False
        
    def get_hook(self, name: str) -> Optional[str]:
        """
        Get hook script content.
        
        Args:
            name: Hook name
            
        Returns:
            Optional[str]: Hook script content
        """
        return self.hooks.get(name)
        
    def has_hook(self, name: str) -> bool:
        """
        Check if a hook exists.
        
        Args:
            name: Hook name
            
        Returns:
            bool: True if hook exists
        """
        return name in self.hooks
        
    def list_hooks(self) -> List[str]:
        """
        List all hooks.
        
        Returns:
            List[str]: List of hook names
        """
        return list(self.hooks.keys())
        
    def install_pre_commit_hook(self) -> bool:
        """
        Install a pre-commit hook.
        
        Returns:
            bool: True if successful
        """
        script = '''#!/usr/bin/env python3
"""
Pre-commit hook for Tite.
Runs code quality checks before committing.
"""

import subprocess
import sys

def run_checks():
    """Run pre-commit checks."""
    checks = [
        ("black", ["--check", "."]),
        ("isort", ["--check", "."]),
        ("flake8", ["."]),
        ("mypy", ["."]),
    ]
    
    failed = False
    
    for tool, args in checks:
        try:
            result = subprocess.run(
                [tool] + args,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"\\n❌ {tool} failed:")
                print(result.stdout)
                print(result.stderr)
                failed = True
        except FileNotFoundError:
            print(f"\\n⚠️  {tool} not found, skipping...")
            
    if failed:
        print("\\n❌ Pre-commit checks failed")
        sys.exit(1)
    else:
        print("\\n✅ Pre-commit checks passed")

if __name__ == "__main__":
    run_checks()
'''
        return self.add_hook("pre-commit", script)
        
    def install_pre_push_hook(self) -> bool:
        """
        Install a pre-push hook.
        
        Returns:
            bool: True if successful
        """
        script = '''#!/usr/bin/env python3
"""
Pre-push hook for Tite.
Runs tests before pushing.
"""

import subprocess
import sys

def run_tests():
    """Run tests before push."""
    try:
        result = subprocess.run(
            ["pytest", "-v", "--tb=short"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("\\n❌ Tests failed:")
            print(result.stdout)
            print(result.stderr)
            sys.exit(1)
        else:
            print("\\n✅ All tests passed")
    except FileNotFoundError:
        print("\\n⚠️  pytest not found, skipping...")

if __name__ == "__main__":
    run_tests()
'''
        return self.add_hook("pre-push", script)
        
    def install_commit_msg_hook(self) -> bool:
        """
        Install a commit-msg hook.
        
        Returns:
            bool: True if successful
        """
        script = '''#!/usr/bin/env python3
"""
Commit message hook for Tite.
Validates commit messages.
"""

import re
import sys

def validate_message(msg):
    """Validate commit message format."""
    # Check for conventional commit format
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(?:\\([^)]+\\))?: .{1,100}$'
    
    if not re.match(pattern, msg):
        print("\\n❌ Invalid commit message format")
        print("Use: type(scope): description")
        print("Types: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert")
        sys.exit(1)

if __name__ == "__main__":
    msg_file = sys.argv[1]
    with open(msg_file, "r") as f:
        msg = f.read().strip()
    validate_message(msg)
'''
        return self.add_hook("commit-msg", script)


class HookManager:
    """
    Manages Git hooks with templates.
    
    This class provides high-level hook management with
    pre-defined hook templates.
    
    Attributes:
        hooks: GitHooks instance
    """
    
    def __init__(self, path: Path):
        """
        Initialize the hook manager.
        
        Args:
            path: Repository path
        """
        self.hooks = GitHooks(path)
        
    def setup_all_hooks(self) -> Dict[str, bool]:
        """
        Setup all recommended hooks.
        
        Returns:
            Dict[str, bool]: Hook installation status
        """
        results = {}
        
        # Pre-commit hook
        results["pre-commit"] = self.hooks.install_pre_commit_hook()
        
        # Pre-push hook
        results["pre-push"] = self.hooks.install_pre_push_hook()
        
        # Commit message hook
        results["commit-msg"] = self.hooks.install_commit_msg_hook()
        
        return results
        
    def setup_pre_commit_with_python(self) -> bool:
        """
        Setup pre-commit hook with Python tools.
        
        Returns:
            bool: True if successful
        """
        script = f'''#!/usr/bin/env python3
"""
Pre-commit hook with Python tools.
"""

import subprocess
import sys

TOOLS = {{
    "black": ["--check", "."],
    "isort": ["--check", "."],
    "flake8": ["."],
    "mypy": ["."],
    "pytest": ["-v", "--tb=short"],
}}

def run_tool(name, args):
    """Run a tool."""
    try:
        result = subprocess.run(
            [name] + args,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0, result.stdout, result.stderr
    except FileNotFoundError:
        return True, "", f"{{name}} not found"

def main():
    failed = False
    
    for name, args in TOOLS.items():
        success, stdout, stderr = run_tool(name, args)
        if not success:
            print(f"\\n❌ {{name}} failed:")
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)
            failed = True
            
    if failed:
        print("\\n❌ Pre-commit checks failed")
        sys.exit(1)
    else:
        print("\\n✅ All checks passed")

if __name__ == "__main__":
    main()
'''
        return self.hooks.add_hook("pre-commit", script)