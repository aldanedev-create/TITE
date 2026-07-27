"""
Reloader for Tite.

This module provides reloading functionality for the development
server, handling graceful restarts and state management.
"""

import signal
import sys
import time
from typing import Any, Callable, Dict, List, Optional

from loguru import logger


class Reloader:
    """
    Manages reloading of the development server.

    This class handles graceful reloads of the development server,
    managing process lifecycle and state.

    Attributes:
        restart_on_change: Whether to restart on file change
        reload_delay: Delay before reload in seconds
        max_reloads: Maximum number of reloads
        _reload_count: Number of reloads performed
        _last_reload: Timestamp of the last reload
    """

    def __init__(
        self,
        restart_on_change: bool = True,
        reload_delay: float = 0.5,
        max_reloads: int = 100,
    ):
        """
        Initialize the reloader.

        Args:
            restart_on_change: Whether to restart on file change
            reload_delay: Delay before reload in seconds
            max_reloads: Maximum number of reloads
        """
        self.restart_on_change = restart_on_change
        self.reload_delay = reload_delay
        self.max_reloads = max_reloads
        self._reload_count = 0
        self._last_reload = 0.0
        self._reload_callbacks: List[Callable] = []
        self._pre_reload_callbacks: List[Callable] = []
        self._post_reload_callbacks: List[Callable] = []

    def reload(self, reason: str = "manual") -> bool:
        """
        Trigger a reload.

        Args:
            reason: Reason for reload

        Returns:
            bool: True if reload was triggered
        """
        if not self.restart_on_change:
            logger.info("Reload disabled, ignoring change")
            return False

        # Check reload limit
        if self._reload_count >= self.max_reloads:
            logger.warning(f"Maximum reloads ({self.max_reloads}) reached")
            return False

        # Check reload cooldown
        current_time = time.time()
        if current_time - self._last_reload < self.reload_delay:
            logger.debug("Reload cooldown active, skipping")
            return False

        logger.info(f"Reloading server (reason: {reason})")

        # Run pre-reload callbacks
        for callback in self._pre_reload_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Pre-reload callback failed: {e}")

        # Increment reload count
        self._reload_count += 1
        self._last_reload = current_time

        # Run reload callbacks
        for callback in self._reload_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Reload callback failed: {e}")

        # Run post-reload callbacks
        for callback in self._post_reload_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Post-reload callback failed: {e}")

        return True

    def on_reload(self, callback: Callable) -> None:
        """
        Register a reload callback.

        Args:
            callback: Callback to run on reload
        """
        self._reload_callbacks.append(callback)

    def on_pre_reload(self, callback: Callable) -> None:
        """
        Register a pre-reload callback.

        Args:
            callback: Callback to run before reload
        """
        self._pre_reload_callbacks.append(callback)

    def on_post_reload(self, callback: Callable) -> None:
        """
        Register a post-reload callback.

        Args:
            callback: Callback to run after reload
        """
        self._post_reload_callbacks.append(callback)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get reload statistics.

        Returns:
            Dict[str, Any]: Reload statistics
        """
        return {
            "reload_count": self._reload_count,
            "max_reloads": self.max_reloads,
            "last_reload": self._last_reload,
            "restart_on_change": self.restart_on_change,
            "reload_delay": self.reload_delay,
        }

    def reset(self) -> None:
        """
        Reset reload statistics.
        """
        self._reload_count = 0
        self._last_reload = 0.0

    def enable(self) -> None:
        """
        Enable auto-reload.
        """
        self.restart_on_change = True
        logger.info("Auto-reload enabled")

    def disable(self) -> None:
        """
        Disable auto-reload.
        """
        self.restart_on_change = False
        logger.info("Auto-reload disabled")


class GracefulReloader(Reloader):
    """
    Graceful reloader with signal handling.

    This class extends Reloader with graceful shutdown and
    reload using SIGTERM and SIGUSR2 signals.
    """

    def __init__(
        self,
        restart_on_change: bool = True,
        reload_delay: float = 0.5,
        max_reloads: int = 100,
        graceful_timeout: float = 5.0,
    ):
        """
        Initialize the graceful reloader.

        Args:
            restart_on_change: Whether to restart on file change
            reload_delay: Delay before reload in seconds
            max_reloads: Maximum number of reloads
            graceful_timeout: Timeout for graceful shutdown
        """
        super().__init__(restart_on_change, reload_delay, max_reloads)
        self.graceful_timeout = graceful_timeout
        self._shutting_down = False
        self._shutdown_callbacks: List[Callable] = []

        # Setup cross-platform signal handlers safely
        try:
            if hasattr(signal, "SIGTERM"):
                signal.signal(signal.SIGTERM, self._signal_handler)
            if hasattr(signal, "SIGUSR2"):
                signal.signal(signal.SIGUSR2, self._signal_handler)
        except (ValueError, AttributeError):
            # Handles non-main thread execution or OS signal limitations
            pass

    def on_shutdown(self, callback: Callable) -> None:
        """
        Register a shutdown callback.

        Args:
            callback: Callback to run on graceful shutdown
        """
        self._shutdown_callbacks.append(callback)

    def _signal_handler(self, signum: int, frame: Any) -> None:
        """
        Handle signals.

        Args:
            signum: Signal number
            frame: Current frame
        """
        if hasattr(signal, "SIGTERM") and signum == signal.SIGTERM:
            logger.info("Received SIGTERM, shutting down gracefully...")
            self.shutdown()
        elif hasattr(signal, "SIGUSR2") and signum == signal.SIGUSR2:
            logger.info("Received SIGUSR2, reloading...")
            self.reload("SIGUSR2")

    def shutdown(self) -> None:
        """
        Gracefully shut down.
        """
        if self._shutting_down:
            return

        self._shutting_down = True
        logger.info("Initiating graceful shutdown...")

        # Run shutdown callbacks
        for callback in self._shutdown_callbacks + self._post_reload_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Shutdown callback failed: {e}")

        # Wait for graceful shutdown
        if self.graceful_timeout > 0:
            time.sleep(self.graceful_timeout)

        sys.exit(0)