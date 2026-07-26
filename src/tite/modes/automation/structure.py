"""
Automation structure definition.

This module defines the directory structure for Automation projects.
"""

from typing import Dict, List


class AutomationStructure:
    """
    Automation project structure.
    
    This class defines the directory and file structure for
    Automation projects created with Tite.
    """
    
    @classmethod
    def get_structure(cls) -> Dict[str, List[str]]:
        """
        Get the directory structure.
        
        Returns:
            Dict[str, List[str]]: Directory structure
        """
        return {
            "directories": [
                "src",
                "src/tasks",
                "src/schedulers",
                "src/handlers",
                "src/utils",
                "config",
                "logs",
                "data",
                "scripts",
                "tests",
                "tests/unit",
                "tests/integration",
            ],
            "files": [
                "src/__init__.py",
                "src/tasks/__init__.py",
                "src/tasks/base.py",
                "src/tasks/data_processing.py",
                "src/tasks/notification.py",
                "src/tasks/file_ops.py",
                "src/tasks/backup.py",
                "src/tasks/cleanup.py",
                "src/tasks/reporting.py",
                "src/schedulers/__init__.py",
                "src/schedulers/manager.py",
                "src/schedulers/cron.py",
                "src/schedulers/interval.py",
                "src/handlers/__init__.py",
                "src/handlers/base.py",
                "src/handlers/email.py",
                "src/handlers/slack.py",
                "src/handlers/telegram.py",
                "src/handlers/webhook.py",
                "src/handlers/logging.py",
                "src/utils/__init__.py",
                "src/utils/logger.py",
                "src/utils/helpers.py",
                "src/utils/validators.py",
                "src/utils/retry.py",
                "src/main.py",
                "src/cli.py",
                "config/__init__.py",
                "config/settings.py",
                "config/tasks.yaml",
                "config/handlers.yaml",
                "config/schedule.yaml",
                "scripts/start.sh",
                "scripts/stop.sh",
                "scripts/restart.sh",
                "scripts/setup.sh",
                "tests/unit/__init__.py",
                "tests/unit/test_tasks.py",
                "tests/unit/test_scheduler.py",
                "tests/unit/test_handlers.py",
                "tests/integration/__init__.py",
                "tests/integration/test_pipeline.py",
                "README.md",
                "pyproject.toml",
                "requirements.txt",
                ".env.example",
                ".gitignore",
            ],
        }
        
    @classmethod
    def get_directories(cls) -> List[str]:
        """
        Get only the directories.
        
        Returns:
            List[str]: List of directory paths
        """
        return cls.get_structure()["directories"]
        
    @classmethod
    def get_files(cls) -> List[str]:
        """
        Get only the files.
        
        Returns:
            List[str]: List of file paths
        """
        return cls.get_structure()["files"]
        
    @classmethod
    def get_source_files(cls) -> List[str]:
        """
        Get Python source files.
        
        Returns:
            List[str]: List of Python file paths
        """
        return [f for f in cls.get_files() if f.endswith(".py")]
        
    @classmethod
    def get_task_files(cls) -> List[str]:
        """
        Get task-related files.
        
        Returns:
            List[str]: List of task file paths
        """
        return [
            "src/tasks/base.py",
            "src/tasks/data_processing.py",
            "src/tasks/notification.py",
            "src/tasks/file_ops.py",
            "src/tasks/backup.py",
            "src/tasks/cleanup.py",
            "src/tasks/reporting.py",
        ]
        
    @classmethod
    def get_config_files(cls) -> List[str]:
        """
        Get configuration files.
        
        Returns:
            List[str]: List of config file paths
        """
        return [
            "config/settings.py",
            "config/tasks.yaml",
            "config/handlers.yaml",
            "config/schedule.yaml",
            "requirements.txt",
            "README.md",
            ".env.example",
            ".gitignore",
        ]