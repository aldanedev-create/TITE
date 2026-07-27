"""
Configuration management for the AI application.

This module handles loading and validating configuration from
environment variables and configuration files.
"""

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class AIConfig:
    """
    AI application configuration.
    
    Attributes:
        provider: LLM provider (openai, anthropic, cohere, etc.)
        model: Model name
        temperature: Temperature for generation
        max_tokens: Maximum tokens for generation
        top_p: Top-p sampling parameter
        frequency_penalty: Frequency penalty
        presence_penalty: Presence penalty
        system_prompt: System prompt to use
        embedding_model: Embedding model for RAG
        vector_db: Vector database type
        chunk_size: Chunk size for document processing
        chunk_overlap: Chunk overlap for document processing
    """
    
    # LLM Configuration
    provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openai"))
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4"))
    temperature: float = field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.7")))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "2000")))
    top_p: float = field(default_factory=lambda: float(os.getenv("TOP_P", "0.9")))
    frequency_penalty: float = field(default_factory=lambda: float(os.getenv("FREQUENCY_PENALTY", "0.0")))
    presence_penalty: float = field(default_factory=lambda: float(os.getenv("PRESENCE_PENALTY", "0.0")))
    
    # System Prompt
    system_prompt: str = field(default_factory=lambda: os.getenv("SYSTEM_PROMPT", "default"))
    
    # RAG Configuration
    embedding_model: str = field(default_factory=lambda: os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    vector_db: str = field(default_factory=lambda: os.getenv("VECTOR_DB", "chromadb"))
    chunk_size: int = field(default_factory=lambda: int(os.getenv("CHUNK_SIZE", "1000")))
    chunk_overlap: int = field(default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "200")))
    
    # Agent Configuration
    agent_type: str = field(default_factory=lambda: os.getenv("AGENT_TYPE", "assistant"))
    max_iterations: int = field(default_factory=lambda: int(os.getenv("MAX_ITERATIONS", "10")))
    verbose: bool = field(default_factory=lambda: os.getenv("VERBOSE", "true").lower() == "true")
    tools: List[str] = field(default_factory=lambda: [
        t.strip() for t in os.getenv("TOOLS", "search,web,code").split(",")
    ])
    
    # Debug
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict[str, Any]: Configuration as dictionary
        """
        return {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "system_prompt": self.system_prompt,
            "embedding_model": self.embedding_model,
            "vector_db": self.vector_db,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "agent_type": self.agent_type,
            "max_iterations": self.max_iterations,
            "verbose": self.verbose,
            "tools": self.tools,
            "debug": self.debug,
            "log_level": self.log_level,
        }
    
    def validate(self) -> bool:
        """
        Validate configuration.
        
        Returns:
            bool: True if configuration is valid
        """
        errors = []
        
        # Validate provider
        valid_providers = ["openai", "anthropic", "cohere", "google", "azure"]
        if self.provider not in valid_providers:
            errors.append(f"Invalid provider: {self.provider}. Must be one of {valid_providers}")
        
        # Validate temperature
        if not 0 <= self.temperature <= 2:
            errors.append(f"Temperature must be between 0 and 2, got {self.temperature}")
        
        # Validate max_tokens
        if self.max_tokens <= 0:
            errors.append(f"Max tokens must be positive, got {self.max_tokens}")
        
        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")
        
        return True


def get_config() -> AIConfig:
    """
    Get the application configuration.
    
    Returns:
        AIConfig: Application configuration
    """
    config = AIConfig()
    config.validate()
    return config