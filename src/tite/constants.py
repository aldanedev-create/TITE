"""
Constants used throughout the Tite application.

This module defines all constant values including default paths,
templates, supported modes, and other configuration values.
"""

from pathlib import Path
from typing import Dict, List, Set

# ============================================================================
# Project Metadata
# ============================================================================

PROJECT_NAME = "Tite"
PROJECT_DESCRIPTION = "A Zero-Configuration Python Project Bootstrapper"
PROJECT_URL = "https://github.com/yourusername/tite"
PROJECT_DOCS = "https://tite.readthedocs.io"
PROJECT_ISSUES = "https://github.com/yourusername/tite/issues"

# ============================================================================
# Version Compatibility
# ============================================================================

MIN_PYTHON_VERSION = (3, 9, 0)
MIN_PYTHON_VERSION_STRING = "3.9.0"

# ============================================================================
# Paths
# ============================================================================

CONFIG_DIR_NAME = ".tite"
CONFIG_FILE_NAME = "tite.toml"
ENV_FILE_NAME = ".env"
ENV_EXAMPLE_FILE_NAME = ".env.example"

# ============================================================================
# Default Templates
# ============================================================================

DEFAULT_TEMPLATE = "default"

# Supported templates for different project types
SUPPORTED_TEMPLATES = {
    "default": "Default Python project structure",
    "library": "Python library project structure",
    "web": "Web application project structure",
    "api": "REST API project structure",
    "cli": "Command-line tool project structure",
    "data": "Data science project structure",
    "ai": "AI/ML project structure",
    "automation": "Automation project structure",
}

# ============================================================================
# Project Modes
# ============================================================================

SUPPORTED_MODES = {
    "default": {
        "name": "Default",
        "description": "Standard Python project setup",
        "template": "default",
    },
    "data": {
        "name": "Data Science",
        "description": "Data science and analytics project",
        "template": "data",
        "packages": ["pandas", "numpy", "matplotlib", "jupyter", "scikit-learn"],
    },
    "ai": {
        "name": "Artificial Intelligence",
        "description": "AI and machine learning project",
        "template": "ai",
        "packages": ["openai", "langchain", "transformers", "torch", "python-dotenv"],
    },
    "automation": {
        "name": "Automation",
        "description": "Automation and scripting project",
        "template": "automation",
        "packages": ["python-dotenv", "pydantic", "requests", "click"],
    },
    "web": {
        "name": "Web Application",
        "description": "Web application with FastAPI or Flask",
        "template": "web",
        "packages": ["fastapi", "uvicorn", "jinja2", "python-dotenv"],
    },
    "api": {
        "name": "REST API",
        "description": "REST API with FastAPI or Flask",
        "template": "api",
        "packages": ["fastapi", "uvicorn", "pydantic", "python-dotenv"],
    },
    "library": {
        "name": "Library",
        "description": "Python library project",
        "template": "library",
        "packages": ["build", "twine", "hatchling"],
    },
    "cli": {
        "name": "Command-Line Tool",
        "description": "CLI tool with Click or Typer",
        "template": "cli",
        "packages": ["click", "rich", "python-dotenv"],
    },
}

# ============================================================================
# Project Structure
# ============================================================================

# Default directory structure for a new project
PROJECT_STRUCTURE: Dict[str, List[str]] = {
    "directories": [
        "src",
        "tests",
        "docs",
        "scripts",
        "data",
        "logs",
    ],
    "files": [
        "README.md",
        "pyproject.toml",
        ".gitignore",
        ".editorconfig",
        "tite.toml",
    ],
}

# Directory structure for different modes
MODE_STRUCTURES: Dict[str, Dict[str, List[str]]] = {
    "default": {
        "directories": ["src", "tests", "logs"],
        "files": ["README.md", "pyproject.toml", ".gitignore", "tite.toml"],
    },
    "library": {
        "directories": ["src", "tests", "docs"],
        "files": ["README.md", "pyproject.toml", "LICENSE", "CHANGELOG.md", ".gitignore", "tite.toml"],
    },
    "web": {
        "directories": ["src", "src/templates", "src/static", "src/static/css", "src/static/js", "tests"],
        "files": ["README.md", "pyproject.toml", ".env.example", ".gitignore", "tite.toml"],
    },
    "api": {
        "directories": ["src", "src/routes", "src/services", "src/models", "src/utils", "tests"],
        "files": ["README.md", "pyproject.toml", ".env.example", "Dockerfile", ".gitignore", "tite.toml"],
    },
    "cli": {
        "directories": ["src", "tests"],
        "files": ["README.md", "pyproject.toml", ".gitignore", "tite.toml"],
    },
    "data": {
        "directories": ["src", "data/raw", "data/processed", "notebooks", "reports", "tests"],
        "files": ["README.md", "pyproject.toml", ".gitignore", "tite.toml"],
    },
    "ai": {
        "directories": ["src", "prompts", "data", "models", "tests"],
        "files": ["README.md", "pyproject.toml", ".env.example", ".gitignore", "tite.toml"],
    },
    "automation": {
        "directories": ["src", "logs", "config", "tests"],
        "files": ["README.md", "pyproject.toml", ".env.example", ".gitignore", "tite.toml"],
    },
}

# ============================================================================
# File Templates
# ============================================================================

# Template files that should be copied with variable substitution
TEMPLATE_FILES = {
    "README.md": "README.md.j2",
    "pyproject.toml": "pyproject.toml.j2",
    "tite.toml": "tite.toml.j2",
    ".gitignore": ".gitignore.j2",
    ".editorconfig": ".editorconfig.j2",
    "src/main.py": "main.py.j2",
    "tests/test_main.py": "test_main.py.j2",
}

# ============================================================================
# CLI Configuration
# ============================================================================

CLI_NAME = "tite"
CLI_DESCRIPTION = "Zero-Configuration Python Project Bootstrapper"
CLI_EPILOG = """
Examples:
    tite new my-app              Create a new Python project
    tite dev                     Start development server
    tite doctor                  Check project health
    tite clean                   Clean build artifacts
    tite info                    Show project information
    tite config                  View configuration
    tite env                     Show environment details
    tite mode list               List available modes
    tite mode data sales-app     Create a data science project
    tite mode ai chatbot         Create an AI project

For more information, visit: https://tite.readthedocs.io
"""

# ============================================================================
# Development Server Configuration
# ============================================================================

DEFAULT_DEV_HOST = "127.0.0.1"
DEFAULT_DEV_PORT = 8000
DEFAULT_DEV_COMMAND = "python src/main.py"

# File extensions to watch in development
WATCH_EXTENSIONS = {".py", ".html", ".css", ".js", ".json", ".yaml", ".yml", ".toml"}

# Directories to exclude from watching
WATCH_EXCLUDE = {
    ".venv",
    "venv",
    "__pycache__",
    "*.egg-info",
    "logs",
    "*.log",
    "build",
    "dist",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
}

# ============================================================================
# Clean Patterns
# ============================================================================

CLEAN_PATTERNS = {
    "directories": [
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".hypothesis",
        ".tox",
        ".nox",
        "build",
        "dist",
        "*.egg-info",
    ],
    "files": [
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.so",
        "*.log",
        "*.pid",
        "*.pid.lock",
        ".coverage",
        "coverage.xml",
        "*.cover",
    ],
}

# ============================================================================
# Git Configuration
# ============================================================================

DEFAULT_GIT_IGNORE = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so
*.pyd
*.pyo

# Virtual environments
.venv/
venv/
ENV/
env/
env.bak/

# Distribution / packaging
build/
dist/
*.egg-info/
*.egg
*.egg-info/
MANIFEST
.eggs/

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.pytest_cache/
.mypy_cache/
.ruff_cache/
.hypothesis/

# Environment variables
.env
.env.local
.env.*.local
.envrc
.direnv/

# IDE / Editor
.idea/
.vscode/
*.iml
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Tite specific
.tite/
*.tite.lock

# Logs
logs/
*.log
*.pid
*.pid.lock

# Databases
*.db
*.sqlite
*.sqlite3

# Secrets
*.key
*.pem
*.crt
*.csr
*.p12
*.pfx
*.p8
*.p7b
*.cer
*.der
*.gpg
*.asc
"""

# ============================================================================
# Editor Config
# ============================================================================

DEFAULT_EDITOR_CONFIG = """
# EditorConfig is awesome: https://EditorConfig.org

# Top-most EditorConfig file
root = true

# Unix-style newlines with a newline ending every file
[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4
max_line_length = 88

# Python files
[*.py]
indent_style = space
indent_size = 4
max_line_length = 88

# TOML files
[*.toml]
indent_style = space
indent_size = 2

# YAML files
[*.{yaml,yml}]
indent_style = space
indent_size = 2

# Markdown files
[*.{md,markdown}]
indent_style = space
indent_size = 4
max_line_length = 120
trim_trailing_whitespace = false
"""

# ============================================================================
# Colors (ANSI)
# ============================================================================

COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
}

# ============================================================================
# Logging
# ============================================================================

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "logs/tite.log"

# ============================================================================
# API Configuration
# ============================================================================

DEFAULT_API_PREFIX = "/api/v1"
DEFAULT_API_RATE_LIMIT = "100/hour"

# ============================================================================
# Testing
# ============================================================================

TEST_PATHS = ["tests"]
TEST_PATTERNS = ["test_*.py", "*_test.py"]
TEST_CLASSES = ["Test*"]
TEST_FUNCTIONS = ["test_*"]

# ============================================================================
# Health Checks
# ============================================================================

HEALTH_CHECKS = {
    "python": "Check Python version",
    "environment": "Check virtual environment",
    "git": "Check Git repository",
    "project_files": "Check project files",
    "dependencies": "Check dependencies",
    "configuration": "Check configuration",
}

# ============================================================================
# Package Managers
# ============================================================================

SUPPORTED_PACKAGE_MANAGERS = {
    "pip": "pip",
    "poetry": "poetry",
    "pipenv": "pipenv",
    "hatch": "hatch",
    "pdm": "pdm",
}

# ============================================================================
# Error Codes
# ============================================================================

ERROR_CODES = {
    "SUCCESS": 0,
    "ERROR": 1,
    "INVALID_COMMAND": 2,
    "INVALID_PROJECT_NAME": 3,
    "PROJECT_EXISTS": 4,
    "TEMPLATE_NOT_FOUND": 5,
    "MODE_NOT_FOUND": 6,
    "ENVIRONMENT_ERROR": 7,
    "CONFIGURATION_ERROR": 8,
    "DEPENDENCY_ERROR": 9,
    "FILE_OPERATION_ERROR": 10,
    "GIT_ERROR": 11,
    "NETWORK_ERROR": 12,
    "PERMISSION_ERROR": 13,
}