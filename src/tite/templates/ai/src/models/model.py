"""
Model implementations for the AI application.

This module provides LLM model implementations with support for
multiple providers including OpenAI, Anthropic, and more.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class LLMModel:
    """
    LLM model wrapper with support for multiple providers.
    
    Attributes:
        provider: Provider name (openai, anthropic, cohere, etc.)
        model: Model name
        temperature: Temperature for generation
        max_tokens: Maximum tokens for generation
        top_p: Top-p sampling parameter
        frequency_penalty: Frequency penalty
        presence_penalty: Presence penalty
    """
    
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 0.9,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
    ):
        """
        Initialize the LLM model.
        
        Args:
            provider: Provider name
            model: Model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens for generation
            top_p: Top-p sampling parameter
            frequency_penalty: Frequency penalty
            presence_penalty: Presence penalty
        """
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        
        self._client = self._initialize_client()
        
        logger.info(f"Initialized LLM model: {provider}/{model}")
    
    def _initialize_client(self):
        """
        Initialize the client for the specified provider.
        
        Returns:
            Client instance
        """
        if self.provider == "openai":
            try:
                import openai
                openai.api_key = os.getenv("OPENAI_API_KEY")
                return openai
            except ImportError:
                raise ImportError("openai package is required for OpenAI provider")
        
        elif self.provider == "anthropic":
            try:
                import anthropic
                return anthropic.Anthropic(
                    api_key=os.getenv("ANTHROPIC_API_KEY")
                )
            except ImportError:
                raise ImportError("anthropic package is required for Anthropic provider")
        
        elif self.provider == "cohere":
            try:
                import cohere
                return cohere.Client(os.getenv("COHERE_API_KEY"))
            except ImportError:
                raise ImportError("cohere package is required for Cohere provider")
        
        elif self.provider == "google":
            try:
                import google.generativeai as genai
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                return genai
            except ImportError:
                raise ImportError("google-generativeai package is required for Google provider")
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            **kwargs: Additional generation parameters
            
        Returns:
            str: Generated response
        """
        logger.debug(f"Generating response with {self.provider}/{self.model}")
        
        if self.provider == "openai":
            return self._generate_openai(prompt, system_prompt, **kwargs)
        elif self.provider == "anthropic":
            return self._generate_anthropic(prompt, system_prompt, **kwargs)
        elif self.provider == "cohere":
            return self._generate_cohere(prompt, **kwargs)
        elif self.provider == "google":
            return self._generate_google(prompt, system_prompt, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _generate_openai(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate using OpenAI API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            top_p=kwargs.get("top_p", self.top_p),
            frequency_penalty=kwargs.get("frequency_penalty", self.frequency_penalty),
            presence_penalty=kwargs.get("presence_penalty", self.presence_penalty),
        )
        return response.choices[0].message.content
    
    def _generate_anthropic(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate using Anthropic API."""
        response = self._client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", self.temperature),
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    
    def _generate_cohere(self, prompt: str, **kwargs) -> str:
        """Generate using Cohere API."""
        response = self._client.generate(
            model=self.model,
            prompt=prompt,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
        )
        return response.generations[0].text
    
    def _generate_google(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate using Google Gemini API."""
        model = self._client.GenerativeModel(self.model)
        
        if system_prompt:
            model = self._client.GenerativeModel(
                self.model,
                system_instruction=system_prompt
            )
        
        response = model.generate_content(prompt)
        return response.text


class EmbeddingModel:
    """
    Embedding model wrapper for RAG applications.
    
    Attributes:
        provider: Provider name
        model: Model name
    """
    
    def __init__(
        self,
        provider: str = "openai",
        model: str = "text-embedding-3-small",
    ):
        """
        Initialize the embedding model.
        
        Args:
            provider: Provider name
            model: Model name
        """
        self.provider = provider
        self.model = model
        self._client = self._initialize_client()
        
        logger.info(f"Initialized embedding model: {provider}/{model}")
    
    def _initialize_client(self):
        """Initialize the client for the specified provider."""
        if self.provider == "openai":
            try:
                import openai
                openai.api_key = os.getenv("OPENAI_API_KEY")
                return openai
            except ImportError:
                raise ImportError("openai package is required for OpenAI provider")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def embed(self, text: str) -> List[float]:
        """
        Get embedding for a text.
        
        Args:
            text: Text to embed
            
        Returns:
            List[float]: Embedding vector
        """
        if self.provider == "openai":
            response = self._client.embeddings.create(
                model=self.model,
                input=text,
            )
            return response.data[0].embedding
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        return [self.embed(text) for text in texts]