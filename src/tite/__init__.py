"""
Tite - A Zero-Configuration Python Project Bootstrapper for Modern Software Development.

Tite is a command-line tool that automates Python project initialization,
providing a production-ready development environment in seconds.

Key features:
    - Zero configuration required
    - Framework agnostic (works with any Python framework)
    - Automatic virtual environment setup
    - Git repository initialization
    - Project structure generation
    - Development server with hot reload
    - Health checks and diagnostics
    - Domain-specific modes (Data Science, AI, Automation)

Examples:
    >>> from tite import create_project
    >>> create_project("my-app")
    Project 'my-app' created successfully!
"""

__version__ = "0.1.4"
__author__ = "Aldane Hutchinson"
__email__ = "aldanehutchinson5@gmail.com"
__license__ = "MIT"

from tite.constants import (
    DEFAULT_TEMPLATE,
    PROJECT_STRUCTURE,
    SUPPORTED_MODES,
)
from tite.exceptions import (
    ConfigurationError,
    EnvironmentError,
    InvalidProjectNameError,
    ModeNotFoundError,
    ProjectExistsError,
    TemplateNotFoundError,
    TiteError,
)
from tite.version import get_version

__all__ = [
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "get_version",
    
    # Constants
    "DEFAULT_TEMPLATE",
    "PROJECT_STRUCTURE",
    "SUPPORTED_MODES",
    
    # Exceptions
    "TiteError",
    "ProjectExistsError",
    "InvalidProjectNameError",
    "TemplateNotFoundError",
    "ModeNotFoundError",
    "EnvironmentError",
    "ConfigurationError",
]