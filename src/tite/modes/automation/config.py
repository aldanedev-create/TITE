"""
Automation configuration.

This module defines the configuration for Automation projects.
"""

from typing import Any, Dict, List


class AutomationConfig:
    """
    Automation project configuration.
    
    This class provides default configuration for Automation projects.
    """
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get the default configuration.
        
        Returns:
            Dict[str, Any]: Default configuration dictionary
        """
        return {
            "project": {
                "name": "",
                "version": "0.1.0",
                "description": "Automation project",
                "python_version": ">=3.9",
                "author": "",
                "email": "",
            },
            "scheduler": {
                "type": "apscheduler",
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
                "job_stores": {
                    "default": {
                        "type": "sqlalchemy",
                        "url": "sqlite:///jobs.sqlite",
                    }
                },
            },
            "tasks": {
                "retry_count": 3,
                "retry_delay": 60,
                "timeout": 300,
                "parallel": False,
                "max_workers": 5,
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "logs/automation.log",
                "console": True,
                "rotation": "1 day",
                "retention": "30 days",
                "compression": "gz",
            },
            "notifications": {
                "enabled": True,
                "channels": {
                    "email": {
                        "smtp_host": "smtp.gmail.com",
                        "smtp_port": 587,
                        "use_tls": True,
                        "from_email": "noreply@example.com",
                    },
                    "slack": {
                        "webhook_url": "",
                    },
                    "telegram": {
                        "bot_token": "",
                        "chat_id": "",
                    },
                    "webhook": {
                        "url": "",
                        "method": "POST",
                        "headers": {},
                    },
                },
            },
            "data": {
                "storage_path": "data",
                "archive_path": "data/archive",
                "backup_path": "data/backup",
                "formats": ["json", "csv", "parquet", "sqlite"],
                "compression": "gzip",
            },
            "monitoring": {
                "enabled": True,
                "metrics": ["runtime", "success_rate", "error_rate"],
                "alert_threshold": 0.1,
                "check_interval": 60,
                "health_check_path": "/health",
            },
            "security": {
                "encryption": True,
                "key_rotation_days": 90,
                "audit_logging": True,
                "allowed_hosts": [],
            },
            "testing": {
                "test_path": "tests",
                "coverage_threshold": 80,
                "mock_external_services": True,
            },
        }
        
    @classmethod
    def get_scheduler_config(cls) -> Dict[str, Any]:
        """
        Get scheduler configuration.
        
        Returns:
            Dict[str, Any]: Scheduler configuration
        """
        return cls.get_default_config()["scheduler"]
        
    @classmethod
    def get_task_config(cls) -> Dict[str, Any]:
        """
        Get task configuration.
        
        Returns:
            Dict[str, Any]: Task configuration
        """
        return cls.get_default_config()["tasks"]
        
    @classmethod
    def get_notification_config(cls) -> Dict[str, Any]:
        """
        Get notification configuration.
        
        Returns:
            Dict[str, Any]: Notification configuration
        """
        return cls.get_default_config()["notifications"]
        
    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """
        Get logging configuration.
        
        Returns:
            Dict[str, Any]: Logging configuration
        """
        return cls.get_default_config()["logging"]
        
    @classmethod
    def get_data_config(cls) -> Dict[str, Any]:
        """
        Get data configuration.
        
        Returns:
            Dict[str, Any]: Data configuration
        """
        return cls.get_default_config()["data"]