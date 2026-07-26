"""
File watcher for Tite.

This module provides file watching functionality with support
for patterns, debouncing, and change events.
"""

import fnmatch
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

from loguru import logger
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileChangeHandler(FileSystemEventHandler):
    """
    Handles file system change events.
    
    This class processes file change events and triggers callbacks
    with debouncing support.
    
    Attributes:
        debounce: Debounce time in milliseconds
        extensions: File extensions to watch
        ignore_patterns: Patterns to ignore
        on_change: Callback for file changes
        _last_event: Timestamp of the last event
    """
    
    def __init__(
        self,
        debounce: int = 100,
        extensions: Optional[List[str]] = None,
        ignore_patterns: Optional[List[str]] = None,
        on_change: Optional[Callable] = None,
    ):
        """
        Initialize the file change handler.
        
        Args:
            debounce: Debounce time in milliseconds
            extensions: File extensions to watch
            ignore_patterns: Patterns to ignore
            on_change: Callback for file changes
        """
        self.debounce = debounce / 1000.0  # Convert to seconds
        self.extensions = set(extensions or [])
        self.ignore_patterns = set(ignore_patterns or [])
        self.on_change = on_change
        self._last_event = 0.0
        self._pending_events: List[Dict[str, Any]] = []
        
    def on_any_event(self, event: Any) -> None:
        """
        Handle any file system event.
        
        Args:
            event: File system event
        """
        # Skip directory events
        if event.is_directory:
            return
            
        # Check if we should handle this event
        if not self._should_handle(event):
            return
            
        # Debounce events
        current_time = time.time()
        if current_time - self._last_event < self.debounce:
            # Update the last event time
            self._last_event = current_time
            return
            
        self._last_event = current_time
        
        # Process the event
        event_data = {
            "path": event.src_path,
            "event_type": event.event_type,
            "is_directory": event.is_directory,
        }
        
        self._pending_events.append(event_data)
        
        # Trigger callback
        if self.on_change:
            self.on_change(self._pending_events)
            
        # Clear pending events
        self._pending_events = []
        
    def _should_handle(self, event: Any) -> bool:
        """
        Check if an event should be handled.
        
        Args:
            event: File system event
            
        Returns:
            bool: True if event should be handled
        """
        path = Path(event.src_path)
        
        # Check extension
        if self.extensions:
            ext = path.suffix.lower()
            if ext not in self.extensions:
                return False
                
        # Check ignore patterns
        if self.ignore_patterns:
            for pattern in self.ignore_patterns:
                if fnmatch.fnmatch(str(path), pattern):
                    return False
                if pattern in str(path):
                    return False
                    
        return True


class FileWatcher:
    """
    Watches files for changes.
    
    This class manages the file system observer and handles
    file change events with debouncing and filtering.
    
    Attributes:
        paths: Paths to watch
        extensions: File extensions to watch
        ignore: Patterns to ignore
        debounce: Debounce time in milliseconds
        recursive: Whether to watch recursively
        observer: File system observer
        handler: File change handler
        on_change: Callback for file changes
    """
    
    def __init__(
        self,
        paths: Optional[List[str]] = None,
        extensions: Optional[List[str]] = None,
        ignore: Optional[List[str]] = None,
        debounce: int = 100,
        recursive: bool = True,
        on_change: Optional[Callable] = None,
    ):
        """
        Initialize the file watcher.
        
        Args:
            paths: Paths to watch
            extensions: File extensions to watch
            ignore: Patterns to ignore
            debounce: Debounce time in milliseconds
            recursive: Whether to watch recursively
            on_change: Callback for file changes
        """
        self.paths = paths or ["src", "tests"]
        self.extensions = extensions or [".py", ".html", ".css", ".js"]
        self.ignore = ignore or [".venv", "__pycache__", "*.egg-info", "logs", "*.log"]
        self.debounce = debounce
        self.recursive = recursive
        self.on_change = on_change
        self.observer: Optional[Observer] = None
        self.handler: Optional[FileChangeHandler] = None
        self.running = False
        
    def start(self) -> None:
        """
        Start watching files.
        """
        if self.running:
            logger.warning("File watcher is already running")
            return
            
        logger.info("Starting file watcher...")
        logger.info(f"  Watching: {', '.join(self.paths)}")
        logger.info(f"  Extensions: {', '.join(self.extensions)}")
        logger.info(f"  Debounce: {self.debounce}ms")
        
        # Create handler
        self.handler = FileChangeHandler(
            debounce=self.debounce,
            extensions=self.extensions,
            ignore_patterns=self.ignore,
            on_change=self.on_change,
        )
        
        # Create observer
        self.observer = Observer()
        
        # Schedule watches
        for path_pattern in self.paths:
            path = Path(path_pattern)
            
            if path.is_absolute():
                watch_path = path
            else:
                watch_path = Path.cwd() / path
                
            if not watch_path.exists():
                logger.warning(f"Watch path does not exist: {watch_path}")
                continue
                
            self.observer.schedule(
                self.handler,
                str(watch_path),
                recursive=self.recursive,
            )
            
        # Start observer
        self.observer.start()
        self.running = True
        logger.info("File watcher started")
        
    def stop(self) -> None:
        """
        Stop watching files.
        """
        if not self.running:
            return
            
        logger.info("Stopping file watcher...")
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            
        self.running = False
        logger.info("File watcher stopped")
        
    def restart(self) -> None:
        """
        Restart the file watcher.
        """
        self.stop()
        self.start()
        
    def add_path(self, path: str) -> None:
        """
        Add a path to watch.
        
        Args:
            path: Path to watch
        """
        if path not in self.paths:
            self.paths.append(path)
            self.restart()
            
    def remove_path(self, path: str) -> None:
        """
        Remove a path from watch.
        
        Args:
            path: Path to remove
        """
        if path in self.paths:
            self.paths.remove(path)
            self.restart()
            
    def add_extension(self, extension: str) -> None:
        """
        Add an extension to watch.
        
        Args:
            extension: Extension to add
        """
        if extension not in self.extensions:
            self.extensions.append(extension)
            self.restart()
            
    def remove_extension(self, extension: str) -> None:
        """
        Remove an extension from watch.
        
        Args:
            extension: Extension to remove
        """
        if extension in self.extensions:
            self.extensions.remove(extension)
            self.restart()
            
    def add_ignore(self, pattern: str) -> None:
        """
        Add an ignore pattern.
        
        Args:
            pattern: Pattern to ignore
        """
        if pattern not in self.ignore:
            self.ignore.append(pattern)
            self.restart()
            
    def remove_ignore(self, pattern: str) -> None:
        """
        Remove an ignore pattern.
        
        Args:
            pattern: Pattern to remove
        """
        if pattern in self.ignore:
            self.ignore.remove(pattern)
            self.restart()
            
    def get_watched_paths(self) -> List[str]:
        """
        Get all watched paths.
        
        Returns:
            List[str]: Watched paths
        """
        if not self.observer:
            return []
            
        watched = []
        for watch in self.observer.watches:
            watched.append(watch.path)
        return watched
        
    def is_watching(self, path: str) -> bool:
        """
        Check if a path is being watched.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path is being watched
        """
        return str(path) in self.get_watched_paths()