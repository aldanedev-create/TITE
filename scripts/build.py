#!/usr/bin/env python3
"""
Build script for Tite.

This script handles building the Tite package for distribution,
including wheel and source distribution creation.
"""

import argparse
import logging
import shutil
import subprocess
import sys
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
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
EGG_INFO_DIR = PROJECT_ROOT / "tite.egg-info"


class BuildError(Exception):
    """Exception raised when build fails."""
    pass


def clean_build_artifacts() -> None:
    """
    Clean build artifacts from previous builds.
    
    Raises:
        BuildError: If cleaning fails
    """
    logger.info("Cleaning build artifacts...")
    
    dirs_to_remove = [DIST_DIR, BUILD_DIR, EGG_INFO_DIR]
    
    for dir_path in dirs_to_remove:
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                logger.debug(f"Removed: {dir_path}")
            except Exception as e:
                raise BuildError(f"Failed to remove {dir_path}: {e}")
    
    # Clean Python cache files
    try:
        subprocess.run(
            [sys.executable, "-B", "-c", 
             "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )
        logger.debug("Removed .pyc files")
    except subprocess.CalledProcessError as e:
        logger.warning(f"Failed to clean .pyc files: {e.stderr.decode() if e.stderr else str(e)}")
    
    # Clean __pycache__ directories
    try:
        subprocess.run(
            [sys.executable, "-B", "-c",
             "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__') if p.is_dir()]"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
        )
        logger.debug("Removed __pycache__ directories")
    except subprocess.CalledProcessError as e:
        logger.warning(f"Failed to clean __pycache__: {e.stderr.decode() if e.stderr else str(e)}")
    
    logger.info("Clean completed")


def install_build_dependencies() -> None:
    """
    Install build dependencies.
    
    Raises:
        BuildError: If installation fails
    """
    logger.info("Installing build dependencies...")
    
    dependencies = [
        "build>=0.10.0",
        "hatchling>=1.18.0",
        "twine>=4.0.0",
        "wheel>=0.40.0",
    ]
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] + dependencies,
            check=True,
            capture_output=True,
        )
        logger.debug("Build dependencies installed")
    except subprocess.CalledProcessError as e:
        raise BuildError(f"Failed to install build dependencies: {e.stderr.decode() if e.stderr else str(e)}")


def check_pyproject() -> bool:
    """
    Check if pyproject.toml exists and is valid.
    
    Returns:
        bool: True if valid, False otherwise
    """
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    
    if not pyproject_path.exists():
        logger.error("pyproject.toml not found")
        return False
    
    try:
        import tomllib
        with open(pyproject_path, "rb") as f:
            tomllib.load(f)
        logger.debug("pyproject.toml is valid")
        return True
    except Exception as e:
        logger.error(f"Invalid pyproject.toml: {e}")
        return False


def run_python_build(clean: bool = True) -> Tuple[bool, List[str]]:
    """
    Run Python build process.
    
    Args:
        clean: Whether to clean before building
        
    Returns:
        Tuple[bool, List[str]]: (success, generated_files)
    """
    if clean:
        clean_build_artifacts()
    
    logger.info("Building Tite package...")
    
    try:
        # Use python -m build
        result = subprocess.run(
            [sys.executable, "-m", "build", "--outdir", str(DIST_DIR)],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        
        logger.debug(result.stdout)
        if result.stderr:
            logger.warning(result.stderr)
        
        # Get generated files
        generated_files = []
        if DIST_DIR.exists():
            generated_files = [str(f) for f in DIST_DIR.glob("*")]
        
        logger.info(f"Build successful! Generated {len(generated_files)} files")
        for file in generated_files:
            logger.info(f"  - {Path(file).name}")
        
        return True, generated_files
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Build failed: {e}")
        if e.stdout:
            logger.error(f"Stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Stderr: {e.stderr}")
        return False, []


def build_sdist() -> bool:
    """
    Build only source distribution.
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Building source distribution...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "build", "--sdist", "--outdir", str(DIST_DIR)],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        
        logger.debug(result.stdout)
        if result.stderr:
            logger.warning(result.stderr)
        
        logger.info("Source distribution built successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to build source distribution: {e}")
        if e.stdout:
            logger.error(f"Stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Stderr: {e.stderr}")
        return False


def build_wheel() -> bool:
    """
    Build only wheel distribution.
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Building wheel distribution...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "build", "--wheel", "--outdir", str(DIST_DIR)],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        
        logger.debug(result.stdout)
        if result.stderr:
            logger.warning(result.stderr)
        
        logger.info("Wheel distribution built successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to build wheel distribution: {e}")
        if e.stdout:
            logger.error(f"Stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Stderr: {e.stderr}")
        return False


def verify_build() -> bool:
    """
    Verify the built distributions.
    
    Returns:
        bool: True if verification passes, False otherwise
    """
    logger.info("Verifying build...")
    
    if not DIST_DIR.exists():
        logger.error("Dist directory not found")
        return False
    
    files = list(DIST_DIR.glob("*"))
    if not files:
        logger.error("No distribution files found")
        return False
    
    valid = True
    for file in files:
        if file.suffix == ".whl":
            # Check wheel
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "wheel", "info", str(file)],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                logger.debug(f"Wheel info: {result.stdout}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Invalid wheel: {e}")
                valid = False
        
        elif file.suffix == ".tar.gz" or file.suffix == ".zip":
            # Check sdist - just verify it exists and is readable
            if not file.stat().st_size > 0:
                logger.error(f"Empty source distribution: {file.name}")
                valid = False
    
    if valid:
        logger.info("Build verification passed")
    else:
        logger.error("Build verification failed")
    
    return valid


def run_tests() -> bool:
    """
    Run tests before building.
    
    Returns:
        bool: True if tests pass, False otherwise
    """
    logger.info("Running tests...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "--tb=short"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            logger.info("All tests passed")
            return True
        else:
            logger.error("Some tests failed")
            logger.error(result.stdout)
            if result.stderr:
                logger.error(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Test execution failed: {e}")
        return False


def build_documentation() -> bool:
    """
    Build documentation.
    
    Returns:
        bool: True if successful, False otherwise
    """
    docs_dir = PROJECT_ROOT / "docs"
    if not docs_dir.exists():
        logger.warning("Documentation directory not found - skipping")
        return True
    
    logger.info("Building documentation...")
    
    try:
        # Try sphinx
        result = subprocess.run(
            [sys.executable, "-m", "sphinx", "-b", "html", "docs", "docs/_build/html"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            logger.info("Documentation built successfully")
            return True
        else:
            logger.warning("Documentation build failed")
            if result.stderr:
                logger.warning(result.stderr)
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("Sphinx not available - skipping documentation")
        return True


def main():
    """Main entry point for build script."""
    parser = argparse.ArgumentParser(
        description="Build Tite package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              # Build both wheel and sdist
  %(prog)s --wheel      # Build only wheel
  %(prog)s --sdist      # Build only source distribution
  %(prog)s --no-clean   # Build without cleaning
  %(prog)s --test       # Run tests before building
  %(prog)s --docs       # Build documentation
        """
    )
    
    parser.add_argument(
        "--wheel",
        action="store_true",
        help="Build only wheel distribution"
    )
    
    parser.add_argument(
        "--sdist",
        action="store_true",
        help="Build only source distribution"
    )
    
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Skip cleaning before build"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run tests before building"
    )
    
    parser.add_argument(
        "--docs",
        action="store_true",
        help="Build documentation"
    )
    
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip verification after build"
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
        # Install build dependencies
        install_build_dependencies()
        
        # Check pyproject.toml
        if not check_pyproject():
            logger.error("pyproject.toml validation failed")
            sys.exit(1)
        
        # Run tests if requested
        if args.test:
            if not run_tests():
                logger.error("Tests failed - aborting build")
                sys.exit(1)
        
        # Build documentation if requested
        if args.docs:
            build_documentation()
        
        # Build
        clean = not args.no_clean
        
        if args.wheel and args.sdist:
            # Build both
            success, files = run_python_build(clean=clean)
        elif args.wheel:
            # Build only wheel
            if clean:
                clean_build_artifacts()
            success = build_wheel()
        elif args.sdist:
            # Build only sdist
            if clean:
                clean_build_artifacts()
            success = build_sdist()
        else:
            # Build both (default)
            success, files = run_python_build(clean=clean)
        
        if not success:
            logger.error("Build failed")
            sys.exit(1)
        
        # Verify build
        if not args.skip_verify:
            if not verify_build():
                logger.error("Build verification failed")
                sys.exit(1)
        
        logger.info("🎉 Build completed successfully!")
        return 0
        
    except BuildError as e:
        logger.error(f"Build error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Build interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())