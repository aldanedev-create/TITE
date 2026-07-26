"""
Logging utilities for Tite.

This module provides logging configuration and utilities for the
Tite application.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from loguru import logger


class Logger:
    """
    Wrapper around loguru logger with additional functionality.
    
    Attributes:
        logger: loguru logger instance
        level: Current log level
    """
    
    def __init__(self, name: str = "tite", level: str = "INFO"):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            level: Log level
        """
        self.name = name
        self.level = level
        self.logger = logger.bind(name=name)
        self._configure()
        
    def _configure(self) -> None:
        """Configure the logger."""
        # Remove default handler
        logger.remove()
        
        # Add console handler
        logger.add(
            sys.stdout,
            format=self._get_format(),
            level=self.level,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )
        
    def _get_format(self) -> str:
        """Get log format."""
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan> | "
            "<level>{message}</level>"
        )
        
    def set_level(self, level: str) -> None:
        """
        Set log level.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.level = level
        logger.remove()
        logger.add(
            sys.stdout,
            format=self._get_format(),
            level=level,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )
        
    def add_file_handler(self, file_path: Path, level: str = "DEBUG") -> None:
        """
        Add a file handler.
        
        Args:
            file_path: Path to log file
            level: Log level for file
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(file_path),
            format=self._get_format(),
            level=level,
            rotation="1 day",
            retention="30 days",
            compression="gz",
            backtrace=True,
            diagnose=True,
        )
        
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message, **kwargs)
        
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.logger.info(message, **kwargs)
        
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message, **kwargs)
        
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.logger.error(message, **kwargs)
        
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(message, **kwargs)
        
    def exception(self, message: str, **kwargs) -> None:
        """Log exception with traceback."""
        self.logger.exception(message, **kwargs)
        
    def bind(self, **kwargs) -> 'Logger':
        """
        Bind additional context to the logger.
        
        Args:
            **kwargs: Key-value pairs to bind
            
        Returns:
            Logger: New logger instance with bound context
        """
        new_logger = Logger(self.name, self.level)
        new_logger.logger = self.logger.bind(**kwargs)
        return new_logger


def setup_logger(
    name: str = "tite",
    level: str = "INFO",
    log_file: Optional[Path] = None,
) -> Logger:
    """
    Setup the logger.
    
    Args:
        name: Logger name
        level: Log level
        log_file: Path to log file
        
    Returns:
        Logger: Configured logger instance
    """
    logger_instance = Logger(name, level)
    
    if log_file:
        logger_instance.add_file_handler(log_file)
        
    return logger_instance


def get_logger(name: str = "tite") -> Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger: Logger instance
    """
    return Logger(name)