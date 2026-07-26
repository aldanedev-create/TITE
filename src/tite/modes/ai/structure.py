"""
AI/ML structure definition.

This module defines the directory structure for AI/ML projects.
"""

from typing import Dict, List


class AIStructure:
    """
    AI/ML project structure.
    
    This class defines the directory and file structure for
    AI/ML projects created with Tite.
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
                "src/models",
                "src/agents",
                "src/prompts",
                "src/tools",
                "src/utils",
                "data",
                "data/training",
                "data/evaluation",
                "data/fine_tuning",
                "data/embeddings",
                "models",
                "models/checkpoints",
                "models/fine_tuned",
                "models/embeddings",
                "prompts",
                "prompts/system",
                "prompts/user",
                "prompts/few_shot",
                "prompts/templates",
                "tests",
                "tests/unit",
                "tests/integration",
                "tests/evaluation",
                "scripts",
                "config",
                "logs",
                "notebooks",
            ],
            "files": [
                "src/__init__.py",
                "src/models/__init__.py",
                "src/models/base.py",
                "src/models/llm.py",
                "src/models/embedding.py",
                "src/models/vision.py",
                "src/models/speech.py",
                "src/models/multimodal.py",
                "src/agents/__init__.py",
                "src/agents/base.py",
                "src/agents/assistant.py",
                "src/agents/chain.py",
                "src/agents/rag.py",
                "src/agents/agentic.py",
                "src/prompts/__init__.py",
                "src/prompts/manager.py",
                "src/prompts/template.py",
                "src/prompts/validator.py",
                "src/tools/__init__.py",
                "src/tools/base.py",
                "src/tools/search.py",
                "src/tools/web.py",
                "src/tools/code.py",
                "src/tools/data.py",
                "src/utils/__init__.py",
                "src/utils/logger.py",
                "src/utils/helpers.py",
                "src/utils/validators.py",
                "src/utils/retry.py",
                "src/utils/cache.py",
                "src/main.py",
                "src/app.py",
                "src/api.py",
                "src/cli.py",
                "prompts/system/default.txt",
                "prompts/system/assistant.txt",
                "prompts/system/rag.txt",
                "prompts/user/default.txt",
                "prompts/user/query.txt",
                "prompts/few_shot/examples.txt",
                "prompts/templates/base.j2",
                "prompts/templates/chain.j2",
                "tests/unit/__init__.py",
                "tests/unit/test_models.py",
                "tests/unit/test_agents.py",
                "tests/unit/test_prompts.py",
                "tests/integration/__init__.py",
                "tests/integration/test_pipeline.py",
                "tests/evaluation/__init__.py",
                "tests/evaluation/test_metrics.py",
                "tests/evaluation/test_benchmark.py",
                "scripts/download_models.py",
                "scripts/fine_tune.py",
                "scripts/evaluate.py",
                "scripts/benchmark.py",
                "scripts/export.py",
                "config/settings.py",
                "config/models.yaml",
                "config/agents.yaml",
                "config/prompts.yaml",
                "config/evaluation.yaml",
                "notebooks/exploration.ipynb",
                "notebooks/training.ipynb",
                "notebooks/evaluation.ipynb",
                "README.md",
                "pyproject.toml",
                "requirements.txt",
                ".env.example",
                ".gitignore",
            ],
        }
        
    @classmethod
    def get_directories(cls) -> List[str]:
        """Get only the directories."""
        return cls.get_structure()["directories"]
        
    @classmethod
    def get_files(cls) -> List[str]:
        """Get only the files."""
        return cls.get_structure()["files"]
        
    @classmethod
    def get_model_files(cls) -> List[str]:
        """Get model-related files."""
        return [
            "src/models/base.py",
            "src/models/llm.py",
            "src/models/embedding.py",
            "src/models/vision.py",
            "src/models/speech.py",
            "src/models/multimodal.py",
        ]
        
    @classmethod
    def get_agent_files(cls) -> List[str]:
        """Get agent-related files."""
        return [
            "src/agents/base.py",
            "src/agents/assistant.py",
            "src/agents/chain.py",
            "src/agents/rag.py",
            "src/agents/agentic.py",
        ]
        
    @classmethod
    def get_prompt_files(cls) -> List[str]:
        """Get prompt-related files."""
        return [
            "src/prompts/manager.py",
            "src/prompts/template.py",
            "src/prompts/validator.py",
            "prompts/system/default.txt",
            "prompts/system/assistant.txt",
            "prompts/system/rag.txt",
            "prompts/user/default.txt",
            "prompts/few_shot/examples.txt",
            "prompts/templates/base.j2",
        ]