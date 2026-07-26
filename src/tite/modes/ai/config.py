"""
AI/ML configuration.

This module defines the configuration for AI/ML projects.
"""

from typing import Any, Dict, List


class AIConfig:
    """
    AI/ML project configuration.
    
    This class provides default configuration for AI/ML projects.
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
                "description": "AI/ML project",
                "python_version": ">=3.9",
                "author": "",
                "email": "",
            },
            "models": {
                "llm": {
                    "provider": "openai",
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "top_p": 0.9,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0,
                    "streaming": False,
                },
                "embedding": {
                    "provider": "openai",
                    "model": "text-embedding-3-small",
                    "dimensions": 1536,
                },
                "vision": {
                    "provider": "openai",
                    "model": "gpt-4-vision-preview",
                },
                "speech": {
                    "provider": "openai",
                    "model": "whisper-1",
                },
            },
            "agents": {
                "type": "assistant",
                "max_iterations": 10,
                "verbose": True,
                "tools": ["search", "web", "code", "data"],
                "memory": {
                    "type": "vector",
                    "persist": True,
                    "max_messages": 1000,
                },
            },
            "prompts": {
                "system_template": "prompts/system/default.txt",
                "user_template": "prompts/user/default.txt",
                "few_shot_examples": "prompts/few_shot/examples.txt",
                "max_tokens": 2000,
                "temperature": 0.7,
            },
            "rag": {
                "enabled": True,
                "chunk_size": 1000,
                "chunk_overlap": 200,
                "vector_db": {
                    "type": "chromadb",
                    "persist_directory": "data/embeddings",
                    "collection_name": "default",
                },
                "retrieval": {
                    "top_k": 5,
                    "similarity_threshold": 0.7,
                },
            },
            "training": {
                "batch_size": 32,
                "epochs": 10,
                "learning_rate": 0.001,
                "optimizer": "adam",
                "loss_function": "cross_entropy",
                "early_stopping": True,
                "patience": 3,
                "validation_split": 0.2,
                "checkpoint_dir": "models/checkpoints",
            },
            "evaluation": {
                "metrics": ["accuracy", "precision", "recall", "f1", "bleu", "rouge"],
                "test_split": 0.2,
                "batch_size": 64,
                "output_dir": "models/evaluation",
            },
            "deployment": {
                "platform": "local",
                "api": {
                    "enabled": True,
                    "port": 8000,
                    "host": "127.0.0.1",
                },
                "model_serving": {
                    "framework": "fastapi",
                    "workers": 4,
                },
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "logs/ai.log",
                "console": True,
                "rotation": "1 day",
                "retention": "30 days",
            },
            "monitoring": {
                "enabled": True,
                "metrics": ["latency", "tokens", "cost", "success_rate"],
                "alerts": {
                    "latency_threshold": 5.0,
                    "error_rate_threshold": 0.1,
                    "cost_threshold": 100.0,
                },
            },
            "security": {
                "api_key_required": True,
                "rate_limiting": {
                    "enabled": True,
                    "requests_per_minute": 60,
                },
                "allowed_origins": ["*"],
            },
        }
        
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """Get model configuration."""
        return cls.get_default_config()["models"]
        
    @classmethod
    def get_agent_config(cls) -> Dict[str, Any]:
        """Get agent configuration."""
        return cls.get_default_config()["agents"]
        
    @classmethod
    def get_prompt_config(cls) -> Dict[str, Any]:
        """Get prompt configuration."""
        return cls.get_default_config()["prompts"]
        
    @classmethod
    def get_rag_config(cls) -> Dict[str, Any]:
        """Get RAG configuration."""
        return cls.get_default_config()["rag"]
        
    @classmethod
    def get_training_config(cls) -> Dict[str, Any]:
        """Get training configuration."""
        return cls.get_default_config()["training"]