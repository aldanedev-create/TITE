#!/usr/bin/env python3
"""
Release script for Tite.

This script handles publishing Tite to PyPI and creating GitHub releases.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DIST_DIR = PROJECT_ROOT / "dist"
VERSION_FILE = PROJECT_ROOT / "src" / "tite" / "__init__.py"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"


class ReleaseError(Exception):
    """Exception raised when release fails."""
    pass


def get_current_version() -> str:
    """
    Get current version from __init__.py.
    
    Returns:
        str: Current version string
        
    Raises:
        ReleaseError: If version cannot be read
    """
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            
        for line in content.split("\n"):
            if line.startswith("__version__"):
                # Extract version string
                version = line.split("=")[1].strip().strip('"').strip("'")
                return version
        
        raise ReleaseError("__version__ not found in __init__.py")
        
    except FileNotFoundError:
        raise ReleaseError(f"Version file not found: {VERSION_FILE}")
    except Exception as e:
        raise ReleaseError(f"Failed to read version: {e}")


def update_version(version: str) -> None:
    """
    Update version in __init__.py.
    
    Args:
        version: New version string
        
    Raises:
        ReleaseError: If version cannot be updated
    """
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        lines = content.split("\n")
        updated = False
        
        for i, line in enumerate(lines):
            if line.startswith("__version__"):
                lines[i] = f'__version__ = "{version}"'
                updated = True
                break
        
        if not updated:
            raise ReleaseError("__version__ line not found")
        
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        logger.info(f"Updated version to {version}")
        
    except Exception as e:
        raise ReleaseError(f"Failed to update version: {e}")


def bump_version(version_type: str = "patch") -> str:
    """
    Bump version number.
    
    Args:
        version_type: Type of version bump (major, minor, patch)
        
    Returns:
        str: New version string
        
    Raises:
        ReleaseError: If version cannot be bumped
    """
    current = get_current_version()
    parts = current.split(".")
    
    if len(parts) != 3:
        raise ReleaseError(f"Invalid version format: {current}")
    
    major, minor, patch = map(int, parts)
    
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        raise ReleaseError(f"Invalid version type: {version_type}")
    
    new_version = f"{major}.{minor}.{patch}"
    logger.info(f"Bumping version: {current} -> {new_version}")
    return new_version


def update_changelog(version: str) -> None:
    """
    Update CHANGELOG.md with new version.
    
    Args:
        version: New version string
        
    Raises:
        ReleaseError: If changelog cannot be updated
    """
    if not CHANGELOG_FILE.exists():
        logger.warning("CHANGELOG.md not found")
        return
    
    try:
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if version already exists
        if f"## [{version}]" in content:
            logger.info(f"Version {version} already in changelog")
            return
        
        # Find unreleased section
        unreleased_line = "## [Unreleased]"
        if unreleased_line not in content:
            logger.warning("No [Unreleased] section found in changelog")
            return
        
        # Insert version before unreleased
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.strip() == unreleased_line:
                # Add new version section after unreleased
                insert_pos = i + 1
                lines.insert(insert_pos, "")
                lines.insert(insert_pos + 1, f"## [{version}] - {get_current_date()}")
                lines.insert(insert_pos + 2, "")
                lines.insert(insert_pos + 3, "### Added")
                lines.insert(insert_pos + 4, "- Tite release")
                lines.insert(insert_pos + 5, "")
                break
        
        with open(CHANGELOG_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        logger.info(f"Updated CHANGELOG.md for version {version}")
        
    except Exception as e:
        raise ReleaseError(f"Failed to update changelog: {e}")


def get_current_date() -> str:
    """
    Get current date in YYYY-MM-DD format.
    
    Returns:
        str: Current date
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")


def check_git_status() -> bool:
    """
    Check git status.
    
    Returns:
        bool: True if clean, False if dirty
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        
        if result.stdout.strip():
            logger.warning("Git working directory is not clean:")
            logger.warning(result.stdout)
            return False
        
        return True
        
    except subprocess.CalledProcessError:
        logger.warning("Not in a git repository")
        return True


def git_commit_and_tag(version: str, message: Optional[str] = None) -> bool:
    """
    Commit changes and create git tag.
    
    Args:
        version: Version to tag
        message: Commit message
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Add files
        subprocess.run(
            ["git", "add", VERSION_FILE, CHANGELOG_FILE],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )
        
        # Commit
        if message is None:
            message = f"Release version {version}"
        
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )
        
        # Create tag
        tag = f"v{version}"
        subprocess.run(
            ["git", "tag", "-a", tag, "-m", f"Release {version}"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )
        
        logger.info(f"Created commit and tag: {tag}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Git operation failed: {e}")
        if e.stdout:
            logger.error(e.stdout)
        if e.stderr:
            logger.error(e.stderr)
        return False


def check_pypi_credentials() -> bool:
    """
    Check if PyPI credentials are available.
    
    Returns:
        bool: True if credentials available
    """
    # Check token
    token = os.environ.get("PYPI_TOKEN")
    if token:
        return True
    
    # Check .pypirc
    pypirc = Path.home() / ".pypirc"
    if pypirc.exists():
        return True
    
    logger.warning("No PyPI credentials found")
    return False


def upload_to_pypi(repository: str = "pypi") -> bool:
    """
    Upload distributions to PyPI.
    
    Args:
        repository: PyPI repository to upload to
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Uploading to {repository}...")
    
    if not DIST_DIR.exists():
        logger.error("Dist directory not found. Run build first.")
        return False
    
    dist_files = list(DIST_DIR.glob("*"))
    if not dist_files:
        logger.error("No distribution files found")
        return False
    
    try:
        # Check token
        token = os.environ.get("PYPI_TOKEN")
        if token:
            # Use token with twine
            cmd = [
                sys.executable, "-m", "twine", "upload",
                "--repository", repository,
                "--username", "__token__",
                "--password", token,
            ] + [str(f) for f in dist_files]
        else:
            # Use twine with .pypirc
            cmd = [
                sys.executable, "-m", "twine", "upload",
                "--repository", repository,
            ] + [str(f) for f in dist_files]
        
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        
        logger.info(f"Successfully uploaded to {repository}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Upload failed: {e}")
        if e.stdout:
            logger.error(e.stdout)
        if e.stderr:
            logger.error(e.stderr)
        return False


def create_github_release(version: str, token: Optional[str] = None) -> bool:
    """
    Create GitHub release.
    
    Args:
        version: Version to release
        token: GitHub token
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Creating GitHub release...")
    
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            logger.warning("No GitHub token found. Skipping GitHub release.")
            return False
    
    try:
        # Get changelog for version
        changelog = ""
        if CHANGELOG_FILE.exists():
            with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract version section
            version_header = f"## [{version}]"
            version_underline = f"## {version}"
            
            lines = content.split("\n")
            start_idx = None
            end_idx = None
            
            for i, line in enumerate(lines):
                if line.strip().startswith(version_header) or line.strip().startswith(version_underline):
                    start_idx = i + 1
                elif start_idx is not None and line.strip().startswith("## [") and i > start_idx:
                    end_idx = i
                    break
            
            if start_idx is not None and end_idx is not None:
                changelog = "\n".join(lines[start_idx:end_idx]).strip()
            elif start_idx is not None:
                changelog = "\n".join(lines[start_idx:]).strip()
        
        # Create release using GitHub CLI
        tag = f"v{version}"
        cmd = [
            "gh", "release", "create",
            tag,
            "--title", f"Tite {version}",
            "--notes", changelog or f"Tite {version} release",
            "--target", "main",
        ]
        
        # Add assets
        if DIST_DIR.exists():
            for file in DIST_DIR.glob("*"):
                cmd.append(str(file))
        
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            logger.info("GitHub release created successfully")
            return True
        else:
            logger.error(f"GitHub release failed: {result.stderr}")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Try using GitHub API with curl
        return create_github_release_api(version, token)
    except Exception as e:
        logger.error(f"Failed to create GitHub release: {e}")
        return False


def create_github_release_api(version: str, token: str) -> bool:
    """
    Create GitHub release using API.
    
    Args:
        version: Version to release
        token: GitHub token
        
    Returns:
        bool: True if successful, False otherwise
    """
    import requests
    
    try:
        url = "https://api.github.com/repos/yourusername/tite/releases"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        
        data = {
            "tag_name": f"v{version}",
            "target_commitish": "main",
            "name": f"Tite {version}",
            "body": f"Tite {version} release",
            "draft": False,
            "prerelease": False,
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            logger.info("GitHub release created successfully (API)")
            return True
        else:
            logger.error(f"GitHub API error: {response.status_code} - {response.text}")
            return False
            
    except ImportError:
        logger.warning("requests not installed. Skipping GitHub release.")
        return False
    except Exception as e:
        logger.error(f"GitHub API failed: {e}")
        return False


def build_package() -> bool:
    """
    Build the package.
    
    Returns:
        bool: True if successful, False otherwise
    """
    build_script = PROJECT_ROOT / "scripts" / "build.py"
    if not build_script.exists():
        logger.error("Build script not found")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(build_script), "--skip-verify"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        
        if result.returncode != 0:
            logger.error("Build failed")
            if result.stdout:
                logger.error(result.stdout)
            if result.stderr:
                logger.error(result.stderr)
            return False
        
        logger.info("Build successful")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Build failed: {e}")
        return False


def main():
    """Main entry point for release script."""
    parser = argparse.ArgumentParser(
        description="Release Tite package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                 # Release current version
  %(prog)s --bump patch    # Bump patch version and release
  %(prog)s --bump minor    # Bump minor version and release
  %(prog)s --bump major    # Bump major version and release
  %(prog)s --dry-run       # Dry run (no actual changes)
  %(prog)s --no-git        # Skip git operations
  %(prog)s --no-pypi       # Skip PyPI upload
  %(prog)s --no-github     # Skip GitHub release
        """
    )
    
    parser.add_argument(
        "--bump",
        choices=["patch", "minor", "major"],
        help="Bump version before release"
    )
    
    parser.add_argument(
        "--version",
        help="Specific version to release (overrides bump)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run (no actual changes)"
    )
    
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Skip git operations"
    )
    
    parser.add_argument(
        "--no-pypi",
        action="store_true",
        help="Skip PyPI upload"
    )
    
    parser.add_argument(
        "--no-github",
        action="store_true",
        help="Skip GitHub release"
    )
    
    parser.add_argument(
        "--repository",
        default="pypi",
        help="PyPI repository to upload to (default: pypi)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Determine version
        if args.version:
            version = args.version
        elif args.bump:
            version = bump_version(args.bump)
        else:
            version = get_current_version()
        
        logger.info(f"Preparing release {version}")
        
        if args.dry_run:
            logger.info("🔍 DRY RUN - No changes will be made")
        
        # Check git status
        if not args.dry_run and not args.no_git:
            if not check_git_status():
                response = input("Continue with uncommitted changes? [y/N] ")
                if response.lower() != "y":
                    logger.info("Release cancelled")
                    return 0
        
        # Update version
        if not args.dry_run:
            if args.bump or args.version:
                update_version(version)
                update_changelog(version)
        
        # Build package
        logger.info("Building package...")
        if not build_package():
            logger.error("Build failed. Release cancelled.")
            return 1
        
        # Git commit and tag
        if not args.dry_run and not args.no_git:
            logger.info("Committing changes...")
            if not git_commit_and_tag(version):
                logger.error("Git commit/tag failed")
                return 1
        
        # Upload to PyPI
        if not args.dry_run and not args.no_pypi:
            if check_pypi_credentials():
                if not upload_to_pypi(args.repository):
                    logger.error("PyPI upload failed")
                    return 1
            else:
                logger.warning("No PyPI credentials. Skipping upload.")
        
        # Create GitHub release
        if not args.dry_run and not args.no_github:
            if not create_github_release(version):
                logger.warning("GitHub release creation failed or skipped")
        
        # Push changes
        if not args.dry_run and not args.no_git:
            try:
                subprocess.run(
                    ["git", "push", "origin", "main"],
                    cwd=PROJECT_ROOT,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "push", "origin", "--tags"],
                    cwd=PROJECT_ROOT,
                    check=True,
                    capture_output=True,
                )
                logger.info("Pushed changes and tags to remote")
            except subprocess.CalledProcessError:
                logger.warning("Failed to push changes. Push manually.")
        
        logger.info(f"🎉 Release {version} completed successfully!")
        
        if args.dry_run:
            logger.info("🔍 DRY RUN completed. No changes were made.")
        
        return 0
        
    except ReleaseError as e:
        logger.error(f"Release error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Release interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())