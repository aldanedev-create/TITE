"""
Mode registry for Tite.

This module provides a registry for all available project modes.
"""

from typing import Any, Dict, List, Optional


class ModeRegistry:
    """
    Registry for project modes.
    
    This class maintains a registry of all available modes and their
    configurations.
    
    Attributes:
        modes: Dictionary of mode definitions
    """
    
    def __init__(self):
        """Initialize the mode registry."""
        self.modes: Dict[str, Dict[str, Any]] = {}
        self._register_builtin_modes()
        
    def _register_builtin_modes(self) -> None:
        """Register built-in modes."""
        # Data Science mode
        self.register_mode(
            "data",
            name="Data Science",
            description="Data science and analytics project with pandas, numpy, and jupyter",
            template="data",
            packages=[
                "pandas>=2.0.0",
                "numpy>=1.24.0",
                "jupyter>=1.0.0",
                "matplotlib>=3.7.0",
                "scikit-learn>=1.2.0",
                "seaborn>=0.12.0",
                "plotly>=5.14.0",
                "scipy>=1.10.0",
                "statsmodels>=0.14.0",
                "ipykernel>=6.0.0",
            ],
            structure={
                "directories": [
                    "src",
                    "data/raw",
                    "data/processed",
                    "data/interim",
                    "data/external",
                    "notebooks",
                    "reports",
                    "reports/figures",
                    "tests",
                ],
                "files": [
                    "src/data_loader.py",
                    "src/data_processor.py",
                    "src/analyzer.py",
                    "src/visualizer.py",
                    "src/main.py",
                    "notebooks/exploration.ipynb",
                    "reports/final_report.md",
                    "tests/test_data_loader.py",
                    "tests/test_processor.py",
                    "README.md",
                    "pyproject.toml",
                    ".env.example",
                    ".gitignore",
                ],
            },
            variables={
                "data_sources": ["csv", "excel", "sqlite", "postgresql"],
                "analysis_types": ["exploratory", "statistical", "predictive"],
            },
        )
        
        # AI/ML mode
        self.register_mode(
            "ai",
            name="Artificial Intelligence",
            description="AI and machine learning project with OpenAI, LangChain, and PyTorch",
            template="ai",
            packages=[
                "openai>=1.0.0",
                "langchain>=0.3.0",
                "transformers>=4.30.0",
                "torch>=2.0.0",
                "tensorflow>=2.13.0",
                "sentence-transformers>=2.2.0",
                "huggingface-hub>=0.16.0",
                "datasets>=2.14.0",
                "tokenizers>=0.13.0",
                "accelerate>=0.24.0",
                "bitsandbytes>=0.41.0",
                "python-dotenv>=1.0.0",
                "pydantic>=2.0.0",
                "tiktoken>=0.5.0",
                "chromadb>=0.4.0",
            ],
            structure={
                "directories": [
                    "src",
                    "src/models",
                    "src/agents",
                    "src/prompts",
                    "src/tools",
                    "src/utils",
                    "data",
                    "data/training",
                    "data/evaluation",
                    "data/fine_tuning",
                    "models",
                    "models/checkpoints",
                    "models/fine_tuned",
                    "prompts",
                    "prompts/system",
                    "prompts/user",
                    "tests",
                    "tests/unit",
                    "tests/integration",
                ],
                "files": [
                    "src/models/base.py",
                    "src/models/llm.py",
                    "src/models/embedding.py",
                    "src/agents/base.py",
                    "src/agents/assistant.py",
                    "src/prompts/manager.py",
                    "src/tools/base.py",
                    "src/tools/search.py",
                    "src/utils/helpers.py",
                    "src/utils/logger.py",
                    "src/main.py",
                    "src/app.py",
                    "prompts/system/default.txt",
                    "prompts/user/default.txt",
                    "tests/unit/test_models.py",
                    "tests/unit/test_agents.py",
                    "tests/integration/test_pipeline.py",
                    "README.md",
                    "pyproject.toml",
                    ".env.example",
                    ".gitignore",
                ],
            },
            variables={
                "llm_providers": ["openai", "anthropic", "cohere", "local"],
                "model_sizes": ["small", "medium", "large", "xl"],
                "embedding_models": ["text-embedding-3-small", "text-embedding-3-large"],
                "vector_dbs": ["chromadb", "pinecone", "weaviate", "qdrant"],
            },
        )
        
        # Automation mode
        self.register_mode(
            "automation",
            name="Automation",
            description="Automation and scripting project with task scheduling and logging",
            template="automation",
            packages=[
                "python-dotenv>=1.0.0",
                "pydantic>=2.0.0",
                "requests>=2.31.0",
                "click>=8.0.0",
                "schedule>=1.2.0",
                "apscheduler>=3.10.0",
                "python-telegram-bot>=20.0.0",
                "selenium>=4.15.0",
                "beautifulsoup4>=4.12.0",
                "lxml>=4.9.0",
                "pandas>=2.0.0",
                "openpyxl>=3.1.0",
                "paramiko>=3.0.0",
                "cryptography>=41.0.0",
                "rich>=13.0.0",
                "loguru>=0.7.0",
                "watchdog>=3.0.0",
            ],
            structure={
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
                ],
                "files": [
                    "src/tasks/base.py",
                    "src/tasks/data_processing.py",
                    "src/tasks/notification.py",
                    "src/tasks/file_ops.py",
                    "src/schedulers/manager.py",
                    "src/handlers/base.py",
                    "src/handlers/email.py",
                    "src/handlers/slack.py",
                    "src/utils/logger.py",
                    "src/utils/helpers.py",
                    "src/main.py",
                    "src/cli.py",
                    "config/settings.py",
                    "config/tasks.yaml",
                    "scripts/start.sh",
                    "scripts/stop.sh",
                    "tests/test_tasks.py",
                    "tests/test_scheduler.py",
                    "README.md",
                    "pyproject.toml",
                    ".env.example",
                    ".gitignore",
                ],
            },
            variables={
                "task_types": ["scheduled", "triggered", "continuous"],
                "notification_channels": ["email", "slack", "telegram", "webhook"],
                "log_levels": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            },
        )
        
    def register_mode(
        self,
        name: str,
        **kwargs: Any,
    ) -> None:
        """
        Register a new mode.
        
        Args:
            name: Mode name (key)
            **kwargs: Mode configuration
        """
        self.modes[name] = kwargs
        
    def get_mode(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a mode by name.
        
        Args:
            name: Mode name
            
        Returns:
            Optional[Dict[str, Any]]: Mode configuration or None
        """
        return self.modes.get(name)
        
    def list_modes(self) -> List[Dict[str, Any]]:
        """
        List all modes.
        
        Returns:
            List[Dict[str, Any]]: List of mode information
        """
        return [
            {
                "name": name,
                "display_name": info.get("name", name),
                "description": info.get("description", ""),
                "packages": info.get("packages", []),
                "template": info.get("template", "default"),
            }
            for name, info in self.modes.items()
        ]
        
    def get_mode_names(self) -> List[str]:
        """
        Get all mode names.
        
        Returns:
            List[str]: List of mode names
        """
        return list(self.modes.keys())
        
    def mode_exists(self, name: str) -> bool:
        """
        Check if a mode exists.
        
        Args:
            name: Mode name
            
        Returns:
            bool: True if mode exists
        """
        return name in self.modes