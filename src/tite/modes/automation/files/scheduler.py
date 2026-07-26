"""
Scheduler module for automation tasks.

This module provides the main scheduler implementation for running
scheduled and triggered tasks.
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import yaml
from apscheduler.events import (
    EVENT_JOB_ADDED,
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MISSED,
    EVENT_JOB_REMOVED,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from src.handlers.base import BaseHandler
from src.tasks.base import BaseTask
from src.utils.logger import setup_logging


class TaskScheduler:
    """
    Main scheduler for automation tasks.

    This class manages the scheduling and execution of tasks
    using APScheduler.

    Attributes:
        config: Scheduler configuration
        scheduler: APScheduler instance
        tasks: Registered task instances
        handlers: Registered handler instances
        running: Whether the scheduler is running
    """

    def __init__(
        self,
        config_path: Optional[Path] = None,
        asyncio_mode: bool = True,
    ):
        """
        Initialize the task scheduler.

        Args:
            config_path: Path to configuration file
            asyncio_mode: Whether to use asyncio scheduler
        """
        self.config_path = config_path or Path.cwd() / "config" / "schedule.yaml"
        self.asyncio_mode = asyncio_mode
        self.config = self._load_config()
        self.tasks: Dict[str, BaseTask] = {}
        self.handlers: Dict[str, BaseHandler] = {}
        self.running = False

        # Setup logging
        setup_logging()

        # Create scheduler
        if asyncio_mode:
            self.scheduler = AsyncIOScheduler()
        else:
            self.scheduler = BackgroundScheduler()

        # Register event listeners
        self._register_event_listeners()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load scheduler configuration.

        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default scheduler configuration.

        Returns:
            Dict[str, Any]: Default configuration
        """
        return {
            "scheduler": {
                "timezone": "UTC",
                "job_defaults": {
                    "coalesce": False,
                    "max_instances": 3,
                    "misfire_grace_time": 60,
                },
                "executors": {
                    "default": {
                        "type": "threadpool",
                        "max_workers": 10,
                    }
                },
            },
            "tasks": [],
            "handlers": [],
        }

    def _register_event_listeners(self) -> None:
        """Register event listeners for scheduler events."""
        self.scheduler.add_listener(self._on_job_executed, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(self._on_job_error, EVENT_JOB_ERROR)
        self.scheduler.add_listener(self._on_job_missed, EVENT_JOB_MISSED)
        self.scheduler.add_listener(self._on_job_added, EVENT_JOB_ADDED)
        self.scheduler.add_listener(self._on_job_removed, EVENT_JOB_REMOVED)

    def _on_job_executed(self, event) -> None:
        """Handle job execution event."""
        logger.info(f"Job executed: {event.job_id}")

    def _on_job_error(self, event) -> None:
        """Handle job error event."""
        logger.error(f"Job error: {event.job_id} - {event.exception}")

    def _on_job_missed(self, event) -> None:
        """Handle job missed event."""
        logger.warning(f"Job missed: {event.job_id}")

    def _on_job_added(self, event) -> None:
        """Handle job added event."""
        logger.info(f"Job added: {event.job_id}")

    def _on_job_removed(self, event) -> None:
        """Handle job removed event."""
        logger.info(f"Job removed: {event.job_id}")

    def register_task(self, task: BaseTask) -> None:
        """
        Register a task with the scheduler.

        Args:
            task: Task instance to register
        """
        self.tasks[task.name] = task
        logger.info(f"Registered task: {task.name}")

    def register_handler(self, handler: BaseHandler) -> None:
        """
        Register a handler with the scheduler.

        Args:
            handler: Handler instance to register
        """
        self.handlers[handler.name] = handler
        logger.info(f"Registered handler: {handler.name}")

    def add_job(
        self,
        task_name: str,
        trigger: Union[str, Dict[str, Any]],
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        job_id: Optional[str] = None,
        replace_existing: bool = False,
    ) -> None:
        """
        Add a job to the scheduler.

        Args:
            task_name: Name of the task to run
            trigger: Trigger configuration (cron, interval, or date)
            args: Positional arguments for the task
            kwargs: Keyword arguments for the task
            job_id: Unique job ID (auto-generated if None)
            replace_existing: Whether to replace existing job
        """
        if task_name not in self.tasks:
            logger.error(f"Task not found: {task_name}")
            return

        task = self.tasks[task_name]

        # Parse trigger
        trigger_obj = self._parse_trigger(trigger)

        # Add job
        self.scheduler.add_job(
            task.run,
            trigger_obj,
            args=args or [],
            kwargs=kwargs or {},
            id=job_id or f"{task_name}_{datetime.now().timestamp()}",
            replace_existing=replace_existing,
        )

        logger.info(f"Added job: {job_id} for task: {task_name}")

    def _parse_trigger(self, trigger: Union[str, Dict[str, Any]]) -> Any:
        """
        Parse trigger configuration.

        Args:
            trigger: Trigger configuration

        Returns:
            Any: Trigger object
        """
        if isinstance(trigger, str):
            # Cron expression
            return CronTrigger.from_crontab(trigger)

        if isinstance(trigger, dict):
            trigger_type = trigger.get("type", "cron")

            if trigger_type == "cron":
                return CronTrigger(
                    year=trigger.get("year"),
                    month=trigger.get("month"),
                    day=trigger.get("day"),
                    week=trigger.get("week"),
                    day_of_week=trigger.get("day_of_week"),
                    hour=trigger.get("hour"),
                    minute=trigger.get("minute"),
                    second=trigger.get("second"),
                    timezone=trigger.get("timezone"),
                )
            elif trigger_type == "interval":
                return IntervalTrigger(
                    weeks=trigger.get("weeks", 0),
                    days=trigger.get("days", 0),
                    hours=trigger.get("hours", 0),
                    minutes=trigger.get("minutes", 0),
                    seconds=trigger.get("seconds", 0),
                    timezone=trigger.get("timezone"),
                )
            elif trigger_type == "date":
                from apscheduler.triggers.date import DateTrigger

                return DateTrigger(
                    run_date=trigger.get("run_date"),
                    timezone=trigger.get("timezone"),
                )

        raise ValueError(f"Unsupported trigger: {trigger}")

    def load_tasks_from_config(self) -> None:
        """Load tasks from configuration file."""
        tasks_config = self.config.get("tasks", [])

        for task_config in tasks_config:
            name = task_config.get("name")
            if not name:
                continue

            # Import task module
            module_path = task_config.get("module", f"src.tasks.{name}")
            class_name = task_config.get(
                "class", name.title().replace("_", "")
            )

            try:
                import importlib

                module = importlib.import_module(module_path)
                task_class = getattr(module, class_name)

                # Instantiate task
                task = task_class(**task_config.get("params", {}))
                self.register_task(task)

                # Schedule task
                schedule = task_config.get("schedule")
                if schedule:
                    self.add_job(
                        name,
                        schedule,
                        args=task_config.get("args", []),
                        kwargs=task_config.get("kwargs", {}),
                        job_id=task_config.get("job_id", name),
                    )

            except Exception as e:
                logger.error(f"Failed to load task {name}: {e}")

    def start(self) -> None:
        """Start the scheduler."""
        if self.running:
            logger.warning("Scheduler is already running")
            return

        # Load tasks from config
        self.load_tasks_from_config()

        # Start scheduler
        self.scheduler.start()
        self.running = True

        logger.info("Scheduler started")

        # Signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame) -> None:
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}")
        self.stop()
        sys.exit(0)

    def stop(self) -> None:
        """Stop the scheduler."""
        if not self.running:
            return

        self.scheduler.shutdown()
        self.running = False

        logger.info("Scheduler stopped")

    def pause(self) -> None:
        """Pause the scheduler."""
        self.scheduler.pause()
        logger.info("Scheduler paused")

    def resume(self) -> None:
        """Resume the scheduler."""
        self.scheduler.resume()
        logger.info("Scheduler resumed")

    def get_jobs(self) -> List[Dict[str, Any]]:
        """
        Get all scheduled jobs.

        Returns:
            List[Dict[str, Any]]: List of job information
        """
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "trigger": str(job.trigger),
                "next_run_time": job.next_run_time,
                "pending": job.pending,
            })
        return jobs

    def remove_job(self, job_id: str) -> None:
        """
        Remove a job from the scheduler.

        Args:
            job_id: ID of the job to remove
        """
        self.scheduler.remove_job(job_id)
        logger.info(f"Removed job: {job_id}")

    def pause_job(self, job_id: str) -> None:
        """
        Pause a job.

        Args:
            job_id: ID of the job to pause
        """
        self.scheduler.pause_job(job_id)
        logger.info(f"Paused job: {job_id}")

    def resume_job(self, job_id: str) -> None:
        """
        Resume a job.

        Args:
            job_id: ID of the job to resume
        """
        self.scheduler.resume_job(job_id)
        logger.info(f"Resumed job: {job_id}")

    def run_job_now(self, job_id: str) -> None:
        """
        Run a job immediately.

        Args:
            job_id: ID of the job to run
        """
        self.scheduler.run_job(job_id)
        logger.info(f"Running job: {job_id}")


class AsyncTaskScheduler(TaskScheduler):
    """
    Asynchronous task scheduler.

    This class extends TaskScheduler to support async tasks.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the async task scheduler."""
        super().__init__(config_path, asyncio_mode=True)

    async def run_async_task(self, task_name: str, *args, **kwargs) -> Any:
        """
        Run an async task.

        Args:
            task_name: Name of the task
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Any: Task result
        """
        if task_name not in self.tasks:
            logger.error(f"Task not found: {task_name}")
            return None

        task = self.tasks[task_name]
        if hasattr(task, "run_async"):
            return await task.run_async(*args, **kwargs)
        else:
            return task.run(*args, **kwargs)

    async def start_async(self) -> None:
        """Start the scheduler asynchronously."""
        if self.running:
            logger.warning("Scheduler is already running")
            return

        self.load_tasks_from_config()
        self.scheduler.start()
        self.running = True

        logger.info("Async scheduler started")

        # Keep running
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.stop()