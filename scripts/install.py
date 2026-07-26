#!/usr/bin/env python3
"""
Install script for Tite.

This script handles installation of Tite and its dependencies.
"""

import argparse
import logging
import os
import platform
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from typing import List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
VENV_DIR = PROJECT_ROOT / ".venv"
DIST_DIR = PROJECT_ROOT / "dist"


class InstallError(Exception):
    """Exception raised when installation fails."""
    pass


def get_python_version() -> Tuple[int, int]:
    """
    Get Python version.
    
    Returns:
        Tuple[int, int]: (major, minor) version
    """
    version = sys.version_info
    return version.major, version.minor


def check_python_version(required_major: int = 3, required_minor: int = 9) -> bool:
    """
    Check Python version compatibility.
    
    Args:
        required_major: Required major version
        required_minor: Required minor version
        
    Returns:
        bool: True if compatible
    """
    major, minor = get_python_version()
    
    if major < required_major or (major == required_major and minor < required_minor):
        logger.error(f"Python {required_major}.{required_minor}+ is required")
        logger.error(f"Current version: {major}.{minor}")
        return False
    
    logger.info(f"Python version: {major}.{minor} (compatible)")
    return True


def create_virtual_env(force: bool = False) -> bool:
    """
    Create virtual environment.
    
    Args:
        force: Force recreation of virtual environment
        
    Returns:
        bool: True if successful
    """
    if VENV_DIR.exists():
        if force:
            logger.info("Removing existing virtual environment...")
            shutil.rmtree(VENV_DIR)
        else:
            logger.info("Virtual environment already exists. Use --force to recreate.")
            return True
    
    logger.info("Creating virtual environment...")
    
    try:
        # Create virtual environment
        builder = venv.EnvBuilder(
            system_site_packages=False,
            clear=True,
            with_pip=True,
        )
        builder.create(VENV_DIR)
        
        logger.info(f"Virtual environment created at: {VENV_DIR}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create virtual environment: {e}")
        return False


def get_pip_path() -> Path:
    """
    Get path to pip in virtual environment.
    
    Returns:
        Path: Path to pip
    """
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "pip.exe"
    else:
        return VENV_DIR / "bin" / "pip"


def get_python_path() -> Path:
    """
    Get path to Python in virtual environment.
    
    Returns:
        Path: Path to Python
    """
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    else:
        return VENV_DIR / "bin" / "python"


def install_dependencies(
    extra: Optional[str] = None,
    dev: bool = False,
    upgrade: bool = False,
) -> bool:
    """
    Install dependencies in virtual environment.
    
    Args:
        extra: Extra dependencies to install (e.g., "fastapi")
        dev: Install development dependencies
        upgrade: Upgrade pip
        
    Returns:
        bool: True if successful
    """
    pip_path = get_pip_path()
    
    if not pip_path.exists():
        logger.error("pip not found in virtual environment")
        return False
    
    # Upgrade pip
    if upgrade:
        logger.info("Upgrading pip...")
        try:
            subprocess.run(
                [str(pip_path), "install", "--upgrade", "pip"],
                check=True,
                capture_output=True,
            )
            logger.info("pip upgraded successfully")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to upgrade pip: {e}")
    
    # Build pip install command
    cmd = [str(pip_path), "install"]
    
    if dev:
        # Install in editable mode with dev dependencies
        logger.info("Installing in development mode...")
        cmd.extend(["-e", str(PROJECT_ROOT)])
        cmd.extend(["-e", f"{PROJECT_ROOT}[dev]"])
    elif extra:
        # Install with extra dependencies
        logger.info(f"Installing with extra: {extra}")
        cmd.extend(["-e", f"{PROJECT_ROOT}[{extra}]"])
    else:
        # Install in editable mode
        logger.info("Installing Tite in editable mode...")
        cmd.extend(["-e", str(PROJECT_ROOT)])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        
        logger.info("Dependencies installed successfully")
        if result.stdout:
            logger.debug(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        if e.stdout:
            logger.error(e.stdout)
        if e.stderr:
            logger.error(e.stderr)
        return False


def install_wheel() -> bool:
    """
    Install from wheel distribution.
    
    Returns:
        bool: True if successful
    """
    if not DIST_DIR.exists():
        logger.error("Dist directory not found. Run build.py first.")
        return False
    
    wheels = list(DIST_DIR.glob("*.whl"))
    if not wheels:
        logger.error("No wheel files found in dist directory")
        return False
    
    # Use the most recent wheel
    wheel = max(wheels, key=lambda f: f.stat().st_mtime)
    
    pip_path = get_pip_path()
    if not pip_path.exists():
        logger.error("pip not found in virtual environment")
        return False
    
    logger.info(f"Installing from wheel: {wheel.name}")
    
    try:
        subprocess.run(
            [str(pip_path), "install", str(wheel)],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )
        
        logger.info("Wheel installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install wheel: {e}")
        if e.stdout:
            logger.error(e.stdout)
        if e.stderr:
            logger.error(e.stderr)
        return False


def verify_installation() -> bool:
    """
    Verify Tite installation.
    
    Returns:
        bool: True if installation is working
    """
    python_path = get_python_path()
    
    if not python_path.exists():
        logger.error("Python not found in virtual environment")
        return False
    
    try:
        # Try importing tite
        result = subprocess.run(
            [str(python_path), "-c", "import tite; print(tite.__version__)"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        
        version = result.stdout.strip()
        logger.info(f"✅ Tite installed successfully! Version: {version}")
        
        # Try running tite --help
        result = subprocess.run(
            [str(python_path), "-m", "tite", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            logger.info("✅ Tite CLI is working")
        else:
            logger.warning("Tite CLI may not be properly configured")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Installation verification failed: {e}")
        if e.stdout:
            logger.error(e.stdout)
        if e.stderr:
            logger.error(e.stderr)
        return False


def show_activation_instructions() -> None:
    """
    Show instructions for activating virtual environment.
    """
    logger.info("\n" + "=" * 60)
    logger.info("✅ Tite installed successfully!")
    logger.info("=" * 60)
    
    if platform.system() == "Windows":
        activate_path = VENV_DIR / "Scripts" / "activate"
        logger.info(f"\nTo activate the virtual environment:")
        logger.info(f"  {activate_path}")
    else:
        activate_path = VENV_DIR / "bin" / "activate"
        logger.info(f"\nTo activate the virtual environment:")
        logger.info(f"  source {activate_path}")
    
    logger.info("\nOr use the Python directly:")
    logger.info(f"  {get_python_path()}")
    
    logger.info("\nTo install Tite globally:")
    logger.info("  pip install tite")
    
    logger.info("\nTo start using Tite:")
    logger.info("  tite new my-project")


def setup_development_environment() -> bool:
    """
    Setup full development environment.
    
    Returns:
        bool: True if successful
    """
    logger.info("Setting up development environment...")
    
    # Create virtual environment
    if not create_virtual_env(force=True):
        return False
    
    # Install development dependencies
    if not install_dependencies(dev=True, upgrade=True):
        return False
    
    # Install pre-commit hooks
    python_path = get_python_path()
    if python_path.exists():
        try:
            # Install pre-commit
            subprocess.run(
                [str(python_path), "-m", "pip", "install", "pre-commit"],
                check=True,
                capture_output=True,
            )
            
            # Install hooks
            subprocess.run(
                [str(python_path), "-m", "pre_commit", "install"],
                cwd=PROJECT_ROOT,
                check=True,
                capture_output=True,
            )
            
            logger.info("Pre-commit hooks installed")
        except subprocess.CalledProcessError:
            logger.warning("Failed to install pre-commit hooks")
    
    # Verify installation
    if not verify_installation():
        return False
    
    show_activation_instructions()
    return True


def install_global() -> bool:
    """
    Install Tite globally using pip.
    
    Returns:
        bool: True if successful
    """
    logger.info("Installing Tite globally...")
    
    try:
        # Check if tite is already installed
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "tite"],
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            logger.info("Tite is already installed")
            response = input("Reinstall? [y/N] ")
            if response.lower() != "y":
                return True
        
        # Install from current directory
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", str(PROJECT_ROOT)],
            check=True,
            capture_output=True,
        )
        
        # Verify
        result = subprocess.run(
            [sys.executable, "-m", "tite", "--help"],
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            logger.info("✅ Tite installed globally successfully!")
            return True
        else:
            logger.warning("Tite installed but CLI may not be accessible")
            return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install globally: {e}")
        if e.stdout:
            logger.error(e.stdout)
        if e.stderr:
            logger.error(e.stderr)
        return False


def main():
    """Main entry point for install script."""
    parser = argparse.ArgumentParser(
        description="Install Tite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Install in virtual environment
  %(prog)s --dev              # Setup development environment
  %(prog)s --global           # Install globally
  %(prog)s --extra fastapi    # Install with extra dependencies
  %(prog)s --wheel            # Install from wheel distribution
        """
    )
    
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Setup development environment"
    )
    
    parser.add_argument(
        "--global",
        action="store_true",
        dest="global_install",
        help="Install globally (system-wide)"
    )
    
    parser.add_argument(
        "--extra",
        help="Install with extra dependencies (e.g., fastapi, flask)"
    )
    
    parser.add_argument(
        "--wheel",
        action="store_true",
        help="Install from wheel distribution"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force recreation of virtual environment"
    )
    
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip verification after installation"
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
        # Check Python version
        if not check_python_version():
            return 1
        
        # Global installation
        if args.global_install:
            if install_global():
                logger.info("🎉 Global installation completed successfully!")
                return 0
            else:
                return 1
        
        # Development environment
        if args.dev:
            if setup_development_environment():
                return 0
            else:
                return 1
        
        # Create virtual environment
        if not create_virtual_env(force=args.force):
            return 1
        
        # Install from wheel
        if args.wheel:
            if not install_wheel():
                return 1
        else:
            # Install with dependencies
            if args.extra:
                if not install_dependencies(extra=args.extra):
                    return 1
            else:
                if not install_dependencies(dev=False):
                    return 1
        
        # Verify installation
        if not args.no_verify:
            if not verify_installation():
                logger.warning("Installation verification failed")
        
        show_activation_instructions()
        logger.info("🎉 Installation completed successfully!")
        return 0
        
    except InstallError as e:
        logger.error(f"Installation error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Installation interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())