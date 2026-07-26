"""
Custom exceptions for the Tite application.

This module defines all custom exception classes used throughout Tite.
"""

from typing import Any, Dict, Optional


class TiteError(Exception):
    """
    Base exception class for all Tite errors.
    
    This is the parent class for all custom exceptions in Tite.
    All Tite exceptions should inherit from this class.
    
    Attributes:
        code: Error code (int)
        message: Error message (str)
        details: Additional error details (dict)
    """
    
    def __init__(
        self,
        message: str = "An error occurred in Tite",
        code: int = 1,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a Tite error.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
        """
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)
    
    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message} (code: {self.code}, details: {self.details})"
        return f"{self.message} (code: {self.code})"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert error to dictionary.
        
        Returns:
            Dict[str, Any]: Error as dictionary
        """
        return {
            "error": self.message,
            "code": self.code,
            "details": self.details,
        }


class ProjectExistsError(TiteError):
    """
    Raised when trying to create a project that already exists.
    
    This exception is raised when the user attempts to create a new project
    in a directory that already contains a project.
    """
    
    def __init__(
        self,
        project_name: str,
        message: Optional[str] = None,
        code: int = 4,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a ProjectExistsError."""
        if message is None:
            message = f"Project '{project_name}' already exists"
        super().__init__(message, code, details)
        self.project_name = project_name


class InvalidProjectNameError(TiteError):
    """
    Raised when a project name is invalid.
    
    This exception is raised when the user provides an invalid project name,
    such as one containing special characters or starting with a number.
    """
    
    def __init__(
        self,
        project_name: str,
        reason: Optional[str] = None,
        code: int = 3,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize an InvalidProjectNameError."""
        if reason:
            message = f"Invalid project name '{project_name}': {reason}"
        else:
            message = f"Invalid project name '{project_name}'"
        super().__init__(message, code, details)
        self.project_name = project_name


class TemplateNotFoundError(TiteError):
    """
    Raised when a template is not found.
    
    This exception is raised when the user specifies a template that
    does not exist in the templates directory.
    """
    
    def __init__(
        self,
        template_name: str,
        message: Optional[str] = None,
        code: int = 5,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a TemplateNotFoundError."""
        if message is None:
            message = f"Template '{template_name}' not found"
        super().__init__(message, code, details)
        self.template_name = template_name


class ModeNotFoundError(TiteError):
    """
    Raised when a mode is not found.
    
    This exception is raised when the user specifies a mode that
    does not exist in the supported modes.
    """
    
    def __init__(
        self,
        mode_name: str,
        message: Optional[str] = None,
        code: int = 6,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a ModeNotFoundError."""
        if message is None:
            message = f"Mode '{mode_name}' not found"
        super().__init__(message, code, details)
        self.mode_name = mode_name


class EnvironmentError(TiteError):
    """
    Raised when there is an environment-related error.
    
    This exception is raised when there are issues with the Python
    environment, such as missing Python, virtual environment problems,
    or dependency conflicts.
    """
    
    def __init__(
        self,
        message: str,
        code: int = 7,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize an EnvironmentError."""
        super().__init__(message, code, details)


class ConfigurationError(TiteError):
    """
    Raised when there is a configuration error.
    
    This exception is raised when configuration files are invalid,
    missing required settings, or have incorrect values.
    """
    
    def __init__(
        self,
        message: str,
        code: int = 8,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a ConfigurationError."""
        super().__init__(message, code, details)


class DependencyError(TiteError):
    """
    Raised when there is a dependency error.
    
    This exception is raised when required dependencies are missing,
    have incompatible versions, or fail to install.
    """
    
    def __init__(
        self,
        dependency_name: str,
        message: Optional[str] = None,
        code: int = 9,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a DependencyError."""
        if message is None:
            message = f"Dependency error for '{dependency_name}'"
        super().__init__(message, code, details)
        self.dependency_name = dependency_name


class FileOperationError(TiteError):
    """
    Raised when a file operation fails.
    
    This exception is raised when file operations such as creation,
    deletion, reading, or writing fail.
    """
    
    def __init__(
        self,
        file_path: str,
        operation: str,
        message: Optional[str] = None,
        code: int = 10,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a FileOperationError."""
        if message is None:
            message = f"Failed to {operation} '{file_path}'"
        super().__init__(message, code, details)
        self.file_path = file_path
        self.operation = operation


class GitError(TiteError):
    """
    Raised when a Git operation fails.
    
    This exception is raised when Git operations such as initialization,
    committing, or tagging fail.
    """
    
    def __init__(
        self,
        operation: str,
        message: Optional[str] = None,
        code: int = 11,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a GitError."""
        if message is None:
            message = f"Git error during '{operation}'"
        super().__init__(message, code, details)
        self.operation = operation


class NetworkError(TiteError):
    """
    Raised when a network operation fails.
    
    This exception is raised when network operations such as downloads,
    API calls, or package installations fail.
    """
    
    def __init__(
        self,
        url: str,
        message: Optional[str] = None,
        code: int = 12,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a NetworkError."""
        if message is None:
            message = f"Network error accessing '{url}'"
        super().__init__(message, code, details)
        self.url = url


class PermissionError(TiteError):
    """
    Raised when there is a permission error.
    
    This exception is raised when the user does not have sufficient
    permissions to perform an operation.
    """
    
    def __init__(
        self,
        path: str,
        message: Optional[str] = None,
        code: int = 13,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a PermissionError."""
        if message is None:
            message = f"Permission denied for '{path}'"
        super().__init__(message, code, details)
        self.path = path


class CommandNotFoundError(TiteError):
    """
    Raised when a command is not found.
    
    This exception is raised when the user enters an invalid command.
    """
    
    def __init__(
        self,
        command: str,
        message: Optional[str] = None,
        code: int = 2,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a CommandNotFoundError."""
        if message is None:
            message = f"Command '{command}' not found"
        super().__init__(message, code, details)
        self.command = command


class ValidationError(TiteError):
    """
    Raised when validation fails.
    
    This exception is raised when data validation fails, such as
    invalid configuration values or malformed input.
    """
    
    def __init__(
        self,
        field: str,
        message: Optional[str] = None,
        code: int = 8,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a ValidationError."""
        if message is None:
            message = f"Validation error for '{field}'"
        super().__init__(message, code, details)
        self.field = field


class TemplateRenderError(TiteError):
    """
    Raised when template rendering fails.
    
    This exception is raised when Jinja2 template rendering fails,
    such as when variables are missing or invalid.
    """
    
    def __init__(
        self,
        template_name: str,
        message: Optional[str] = None,
        code: int = 5,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a TemplateRenderError."""
        if message is None:
            message = f"Failed to render template '{template_name}'"
        super().__init__(message, code, details)
        self.template_name = template_name


class StateError(TiteError):
    """
    Raised when the application is in an invalid state.
    
    This exception is raised when the application attempts to perform
    an operation that is not valid in the current state.
    """
    
    def __init__(
        self,
        state: str,
        operation: str,
        message: Optional[str] = None,
        code: int = 1,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a StateError."""
        if message is None:
            message = f"Cannot perform '{operation}' in state '{state}'"
        super().__init__(message, code, details)
        self.state = state
        self.operation = operation


# ============================================================================
# Error Code Mapping
# ============================================================================

ERROR_CODE_MAP = {
    "ProjectExistsError": 4,
    "InvalidProjectNameError": 3,
    "TemplateNotFoundError": 5,
    "ModeNotFoundError": 6,
    "EnvironmentError": 7,
    "ConfigurationError": 8,
    "DependencyError": 9,
    "FileOperationError": 10,
    "GitError": 11,
    "NetworkError": 12,
    "PermissionError": 13,
    "CommandNotFoundError": 2,
    "ValidationError": 8,
    "TemplateRenderError": 5,
    "StateError": 1,
}


def get_error_code(exception_class: type) -> int:
    """
    Get the error code for an exception class.
    
    Args:
        exception_class: Exception class
        
    Returns:
        int: Error code
        
    Examples:
        >>> get_error_code(ProjectExistsError)
        4
    """
    return ERROR_CODE_MAP.get(exception_class.__name__, 1)


def get_exception_class(error_code: int) -> Optional[type]:
    """
    Get the exception class for an error code.
    
    Args:
        error_code: Error code
        
    Returns:
        Optional[type]: Exception class or None if not found
        
    Examples:
        >>> get_exception_class(4)
        <class 'tite.exceptions.ProjectExistsError'>
    """
    for name, code in ERROR_CODE_MAP.items():
        if code == error_code:
            # Get the class from globals
            return globals().get(name)
    return None