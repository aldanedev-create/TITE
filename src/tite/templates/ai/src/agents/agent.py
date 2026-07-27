"""
Agent implementations for the AI application.

This module provides agent implementations including assistant,
RAG, and chain agents.
"""

import logging
from typing import Any, Dict, List, Optional

from src.models.model import LLMModel
from src.prompts import PromptManager, create_system_prompt

logger = logging.getLogger(__name__)


class BaseAgent:
    """
    Base agent class.
    
    Attributes:
        model: LLM model
        prompt_manager: Prompt manager
        verbose: Whether to log verbose output
        max_iterations: Maximum iterations for the agent
    """
    
    def __init__(
        self,
        model: LLMModel,
        prompt_manager: Optional[PromptManager] = None,
        verbose: bool = True,
        max_iterations: int = 10,
    ):
        """
        Initialize the agent.
        
        Args:
            model: LLM model
            prompt_manager: Prompt manager
            verbose: Whether to log verbose output
            max_iterations: Maximum iterations for the agent
        """
        self.model = model
        self.prompt_manager = prompt_manager or PromptManager()
        self.verbose = verbose
        self.max_iterations = max_iterations
        self.history: List[Dict[str, str]] = []
    
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the agent with input text.
        
        Args:
            input_text: Input text
            **kwargs: Additional arguments
            
        Returns:
            str: Agent response
        """
        raise NotImplementedError("Subclasses must implement run()")


class AssistantAgent(BaseAgent):
    """
    Assistant agent that provides general assistance.
    
    This agent uses a system prompt to provide general assistance
    with conversation history support.
    """
    
    def __init__(
        self,
        model: LLMModel,
        prompt_manager: Optional[PromptManager] = None,
        system_prompt: Optional[str] = None,
        verbose: bool = True,
        max_iterations: int = 10,
        max_history: int = 20,
    ):
        """
        Initialize the assistant agent.
        
        Args:
            model: LLM model
            prompt_manager: Prompt manager
            system_prompt: System prompt to use
            verbose: Whether to log verbose output
            max_iterations: Maximum iterations
            max_history: Maximum history length
        """
        super().__init__(model, prompt_manager, verbose, max_iterations)
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        self.max_history = max_history
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt."""
        # Try to load from prompt manager
        prompt = self.prompt_manager.get_system_prompt()
        if prompt:
            return prompt
        
        # Use default
        return create_system_prompt("assistant")
    
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the assistant agent.
        
        Args:
            input_text: User input
            **kwargs: Additional arguments
            
        Returns:
            str: Agent response
        """
        if self.verbose:
            logger.info(f"Assistant running with input: {input_text}")
        
        # Add user message to history
        self.history.append({"role": "user", "content": input_text})
        
        # Generate response
        response = self.model.generate(
            prompt=input_text,
            system_prompt=self.system_prompt,
            **kwargs
        )
        
        # Add response to history
        self.history.append({"role": "assistant", "content": response})
        
        # Trim history if needed
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        if self.verbose:
            logger.info(f"Assistant response: {response[:100]}...")
        
        return response
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.history = []
        logger.info("History cleared")


class RAGAgent(BaseAgent):
    """
    RAG (Retrieval-Augmented Generation) agent.
    
    This agent retrieves relevant documents and uses them to
    generate informed responses.
    """
    
    def __init__(
        self,
        model: LLMModel,
        embedding_model: Optional[EmbeddingModel] = None,
        prompt_manager: Optional[PromptManager] = None,
        vector_db: Optional[Any] = None,
        system_prompt: Optional[str] = None,
        verbose: bool = True,
        max_iterations: int = 10,
        top_k: int = 5,
    ):
        """
        Initialize the RAG agent.
        
        Args:
            model: LLM model
            embedding_model: Embedding model
            prompt_manager: Prompt manager
            vector_db: Vector database
            system_prompt: System prompt
            verbose: Whether to log verbose output
            max_iterations: Maximum iterations
            top_k: Number of documents to retrieve
        """
        super().__init__(model, prompt_manager, verbose, max_iterations)
        from src.models.model import EmbeddingModel as EmbModel
        self.embedding_model = embedding_model or EmbModel()
        self.vector_db = vector_db
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        self.top_k = top_k
        self.documents: List[Dict[str, Any]] = []
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt."""
        return """You are a helpful AI assistant with access to relevant documents. Use the provided context to answer questions accurately. If the context doesn't contain enough information, say so."""
    
    def add_documents(self, documents: List[str]) -> None:
        """
        Add documents to the knowledge base.
        
        Args:
            documents: List of document strings
        """
        for doc in documents:
            embedding = self.embedding_model.embed(doc)
            self.documents.append({
                "content": doc,
                "embedding": embedding,
            })
        logger.info(f"Added {len(documents)} documents")
    
    def _retrieve(self, query: str) -> List[str]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Query text
            
        Returns:
            List[str]: Relevant documents
        """
        # If using vector DB, query it
        if self.vector_db:
            # Placeholder for vector DB query
            return []
        
        # Simple similarity search
        if not self.documents:
            return []
        
        query_embedding = self.embedding_model.embed(query)
        
        # Calculate similarity scores
        similarities = []
        for doc in self.documents:
            similarity = self._cosine_similarity(query_embedding, doc["embedding"])
            similarities.append((similarity, doc["content"]))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in similarities[:self.top_k]]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import math
        
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0
        
        return dot / (norm_a * norm_b)
    
    def run(self, input_text: str, **kwargs) -> str:
        """
        Run the RAG agent.
        
        Args:
            input_text: User input
            **kwargs: Additional arguments
            
        Returns:
            str: Agent response
        """
        if self.verbose:
            logger.info(f"RAG agent running with input: {input_text}")
        
        # Retrieve relevant documents
        context = self._retrieve(input_text)
        
        # Build prompt with context
        prompt = input_text
        if context:
            context_text = "\n\n".join(context)
            prompt = f"Context:\n{context_text}\n\nQuestion: {input_text}"
        
        # Generate response
        response = self.model.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
            **kwargs
        )
        
        if self.verbose:
            logger.info(f"RAG agent response: {response[:100]}...")
        
        return response