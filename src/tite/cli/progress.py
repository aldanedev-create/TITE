"""
Progress indicators for Tite CLI.

This module provides progress bar and spinner functionality
for long-running operations.
"""

import sys
import threading
import time
from typing import Any, Callable, Iterator, Optional, Union

from rich.progress import (
    BarColumn,
    Progress,
    ProgressColumn,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from tite.cli.output import console
from tite.cli.terminal import clear_line, supports_color


def create_progress() -> Progress:
    """
    Create a Rich progress bar instance.
    
    Returns:
        Progress: Configured progress bar
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        refresh_per_second=10,
    )


class Spinner:
    """
    A simple spinner for indicating progress.
    
    This class provides a visual spinner that runs in a separate thread.
    
    Attributes:
        message: Message to display next to the spinner
        spinner_chars: Characters to cycle through
        delay: Delay between updates in seconds
    
    Examples:
        >>> with Spinner("Loading..."):
        ...     time.sleep(2)
    """
    
    def __init__(
        self,
        message: str = "Loading...",
        spinner_chars: str = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
        delay: float = 0.1,
    ):
        """
        Initialize the spinner.
        
        Args:
            message: Message to display
            spinner_chars: Characters to cycle through
            delay: Delay between updates in seconds
        """
        self.message = message
        self.spinner_chars = spinner_chars
        self.delay = delay
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
    def _spin(self) -> None:
        """Run the spinner animation."""
        i = 0
        while self.running:
            char = self.spinner_chars[i % len(self.spinner_chars)]
            sys.stdout.write(f"\r{char} {self.message}")
            sys.stdout.flush()
            time.sleep(self.delay)
            i += 1
        
        # Clear the line when done
        clear_line()
        
    def start(self) -> None:
        """Start the spinner."""
        if self.thread and self.thread.is_alive():
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self) -> None:
        """Stop the spinner."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)
        clear_line()
        
    def update_message(self, message: str) -> None:
        """
        Update the spinner message.
        
        Args:
            message: New message
        """
        self.message = message
        
    def __enter__(self) -> 'Spinner':
        """Enter context manager."""
        self.start()
        return self
        
    def __exit__(self, *args: Any) -> None:
        """Exit context manager."""
        self.stop()


class ProgressBar:
    """
    A simple progress bar implementation.
    
    Attributes:
        total: Total number of items
        current: Current progress
        bar_length: Length of the progress bar in characters
        prefix: Text before the progress bar
        suffix: Text after the progress bar
        fill_char: Character for filled portion
        empty_char: Character for empty portion
    """
    
    def __init__(
        self,
        total: int,
        prefix: str = "",
        suffix: str = "",
        bar_length: int = 50,
        fill_char: str = "█",
        empty_char: str = "░",
    ):
        """
        Initialize the progress bar.
        
        Args:
            total: Total number of items
            prefix: Text before the progress bar
            suffix: Text after the progress bar
            bar_length: Length of the progress bar in characters
            fill_char: Character for filled portion
            empty_char: Character for empty portion
        """
        self.total = total
        self.current = 0
        self.prefix = prefix
        self.suffix = suffix
        self.bar_length = bar_length
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.enabled = supports_color()
        
    def update(self, current: Optional[int] = None, step: int = 1) -> None:
        """
        Update the progress bar.
        
        Args:
            current: Current progress value
            step: Increment by this amount if current is None
        """
        if current is not None:
            self.current = min(current, self.total)
        else:
            self.current = min(self.current + step, self.total)
        
        self._render()
        
    def _render(self) -> None:
        """Render the progress bar."""
        if not self.enabled:
            return
        
        percent = self.current / self.total
        filled_length = int(self.bar_length * percent)
        
        bar = self.fill_char * filled_length + self.empty_char * (self.bar_length - filled_length)
        
        sys.stdout.write(
            f"\r{self.prefix} |{bar}| {percent:.1%} {self.suffix}"
        )
        sys.stdout.flush()
        
        if self.current >= self.total:
            sys.stdout.write("\n")
        
    def reset(self) -> None:
        """Reset the progress bar."""
        self.current = 0
        self._render()


class ProgressCounter:
    """
    A counter that displays progress.
    
    This class is useful for displaying progress when the total
    is not known in advance.
    
    Attributes:
        message: Message to display
        count: Current count
        unit: Unit name (e.g., "files", "items")
    """
    
    def __init__(self, message: str = "Processing", unit: str = "items"):
        """
        Initialize the progress counter.
        
        Args:
            message: Message to display
            unit: Unit name
        """
        self.message = message
        self.unit = unit
        self.count = 0
        self.enabled = supports_color()
        
    def increment(self, step: int = 1) -> None:
        """
        Increment the counter.
        
        Args:
            step: Amount to increment by
        """
        self.count += step
        self._render()
        
    def _render(self) -> None:
        """Render the counter."""
        if not self.enabled:
            return
        
        sys.stdout.write(f"\r{self.message}: {self.count} {self.unit}")
        sys.stdout.flush()
        
    def finish(self) -> None:
        """Finish and show final count."""
        self._render()
        sys.stdout.write("\n")
        sys.stdout.flush()


def with_progress(
    items: Iterator[Any],
    description: str = "Processing",
    total: Optional[int] = None,
) -> Iterator[Any]:
    """
    Generator wrapper that shows progress when iterating.
    
    Args:
        items: Items to iterate over
        description: Progress description
        total: Total number of items (optional)
        
    Yields:
        Any: Items from the iterator
        
    Examples:
        >>> for item in with_progress(files, "Processing files", len(files)):
        ...     process(item)
    """
    with create_progress() as progress:
        task = progress.add_task(description, total=total or len(items))
        
        for item in items:
            yield item
            progress.update(task, advance=1)


def progress_indicator(func: Callable, message: str = "Processing...") -> Any:
    """
    Decorator that shows a spinner while a function runs.
    
    Args:
        func: Function to run
        message: Message to display
        
    Returns:
        Any: Function result
        
    Examples:
        >>> @progress_indicator
        ... def long_running_function():
        ...     time.sleep(2)
        ...     return "Done"
    """
    def wrapper(*args, **kwargs):
        with Spinner(message):
            return func(*args, **kwargs)
    return wrapper


def track_progress(
    iterator: Iterator,
    description: str = "Processing",
    total: Optional[int] = None,
) -> Iterator:
    """
    Track progress of an iterator.
    
    This is a simpler alternative to with_progress.
    
    Args:
        iterator: Iterator to track
        description: Progress description
        total: Total number of items
        
    Yields:
        Any: Items from the iterator
    """
    return with_progress(iterator, description, total)


class ProgressContext:
    """
    Context manager for showing progress.
    
    This class provides a more flexible way to show progress.
    
    Attributes:
        description: Progress description
        total: Total number of steps
        progress: Rich Progress instance
        task: Task ID
    """
    
    def __init__(self, description: str = "Processing", total: Optional[int] = None):
        """
        Initialize the progress context.
        
        Args:
            description: Progress description
            total: Total number of steps
        """
        self.description = description
        self.total = total
        self.progress = None
        self.task = None
        
    def __enter__(self):
        """Enter context manager."""
        self.progress = create_progress()
        self.progress.start()
        self.task = self.progress.add_task(self.description, total=self.total)
        return self
        
    def __exit__(self, *args):
        """Exit context manager."""
        if self.progress:
            self.progress.stop()
            
    def update(self, advance: int = 1, description: Optional[str] = None) -> None:
        """
        Update the progress.
        
        Args:
            advance: Amount to advance by
            description: Optional new description
        """
        if self.progress and self.task is not None:
            self.progress.update(self.task, advance=advance)
            if description:
                self.progress.update(self.task, description=description)
                
    def set_total(self, total: int) -> None:
        """
        Set the total number of steps.
        
        Args:
            total: Total number of steps
        """
        self.total = total
        if self.progress and self.task is not None:
            self.progress.update(self.task, total=total)