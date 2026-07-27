"""
File watcher for Tite.

This module provides file watching functionality with support
for patterns, debouncing, and change events.
"""

import fnmatch
import threading
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
    with timer-based debouncing support.
    """

    def __init__(
        self,
        debounce: int = 100,
        extensions: Optional[List[str]] = None,
        ignore_patterns: Optional[List[str]] = None,
        on_change: Optional[Callable[[List[Dict[str, Any]]], None]] = None,
    ):
        """
        Initialize the file change handler.

        Args:
            debounce: Debounce time in milliseconds
            extensions: File extensions to watch (e.g. ['.py', '.html'])
            ignore_patterns: Glob or folder patterns to ignore
            on_change: Callback for file changes
        """
        self.debounce = debounce / 1000.0  # Convert to seconds
        # Normalize extensions to ensure leading dot
        self.extensions = {
            ext if ext.startswith(".") else f".{ext}"
            for ext in (extensions or [])
        }
        self.ignore_patterns = set(ignore_patterns or [])
        self.on_change = on_change

        self._lock = threading.Lock()
        self._timer: Optional[threading.Timer] = None
        self._pending_events: Dict[str, Dict[str, Any]] = {}

    def on_any_event(self, event: Any) -> None:
        """
        Handle any file system event.

        Args:
            event: File system event
        """
        if event.is_directory or not self._should_handle(event):
            return

        event_data = {
            "path": event.src_path,
            "event_type": event.event_type,
            "is_directory": event.is_directory,
        }

        with self._lock:
            # Deduplicate by path
            self._pending_events[event.src_path] = event_data

            # Reset timer on each incoming event (true debouncing)
            if self._timer is not None:
                self._timer.cancel()

            self._timer = threading.Timer(self.debounce, self._flush_events)
            self._timer.start()

    def _flush_events(self) -> None:
        """
        Trigger callback with collected events after debounce quiet window.
        """
        with self._lock:
            events_to_send = list(self._pending_events.values())
            self._pending_events.clear()
            self._timer = None

        if events_to_send and self.on_change:
            try:
                self.on_change(events_to_send)
            except Exception as e:
                logger.error(f"Error executing watcher on_change callback: {e}")

    def _should_handle(self, event: Any) -> bool:
        """
        Check if an event should be handled based on extensions and ignore patterns.
        """
        path = Path(event.src_path)

        # Check extension
        if self.extensions:
            if path.suffix.lower() not in self.extensions:
                return False

        # Check ignore patterns across normalized path parts
        path_str = str(path).replace("\\", "/")
        path_parts = path.parts

        if self.ignore_patterns:
            for pattern in self.ignore_patterns:
                # Match full path glob pattern
                if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path.name, pattern):
                    return False
                # Match explicit directory/file path components (e.g. .venv, __pycache__)
                clean_pattern = pattern.strip("/*")
                if clean_pattern in path_parts:
                    return False

        return True


class FileWatcher:
    """
    Watches files for changes.

    Manages the file system observer and handles file change events
    with debouncing and filtering.
    """

    def __init__(
        self,
        paths: Optional[List[str]] = None,
        extensions: Optional[List[str]] = None,
        ignore: Optional[List[str]] = None,
        debounce: int = 100,
        recursive: bool = True,
        on_change: Optional[Callable[[List[Dict[str, Any]]], None]] = None,
    ):
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
        if path not in self.paths:
            self.paths.append(path)
            if self.running:
                self.restart()

    def remove_path(self, path: str) -> None:
        if path in self.paths:
            self.paths.remove(path)
            if self.running:
                self.restart()

    def add_extension(self, extension: str) -> None:
        if extension not in self.extensions:
            self.extensions.append(extension)
            if self.running:
                self.restart()

    def remove_extension(self, extension: str) -> None:
        if extension in self.extensions:
            self.extensions.remove(extension)
            if self.running:
                self.restart()

    def add_ignore(self, pattern: str) -> None:
        if pattern not in self.ignore:
            self.ignore.append(pattern)
            if self.running:
                self.restart()

    def remove_ignore(self, pattern: str) -> None:
        if pattern in self.ignore:
            self.ignore.remove(pattern)
            if self.running:
                self.restart()

    def get_watched_paths(self) -> List[str]:
        """
        Get all watched paths.
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
        """
        target = str(Path(path).resolve())
        return any(
            str(Path(p).resolve()) == target for p in self.get_watched_paths()
        )