"""
Utility helper functions for the AI application.

This module provides shared utility functions used across the AI application.
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from a string.
    
    Args:
        text: String containing JSON
        
    Returns:
        Optional[Dict[str, Any]]: Extracted JSON or None
    """
    # Try to find JSON in the text
    json_pattern = r'```json\s*([\s\S]*?)\s*```'
    match = re.search(json_pattern, text)
    
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON without code block
    json_pattern = r'\{[\s\S]*\}'
    match = re.search(json_pattern, text)
    
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    return None


def extract_code_blocks(text: str, language: Optional[str] = None) -> List[str]:
    """
    Extract code blocks from a string.
    
    Args:
        text: String containing code blocks
        language: Optional language filter
        
    Returns:
        List[str]: Extracted code blocks
    """
    if language:
        pattern = rf'```{language}\s*([\s\S]*?)\s*```'
    else:
        pattern = r'```(?:\w+)?\s*([\s\S]*?)\s*```'
    
    matches = re.findall(pattern, text)
    return [match.strip() for match in matches]


def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """
    Format a timestamp.
    
    Args:
        timestamp: Timestamp to format (defaults to now)
        
    Returns:
        str: Formatted timestamp
    """
    if timestamp is None:
        timestamp = datetime.utcnow()
    return timestamp.isoformat() + "Z"


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[str]:
    """
    Chunk text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List[str]: List of chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        
        # Try to end at a sentence boundary
        if end < len(text):
            # Look for sentence boundaries
            for boundary in ['. ', '! ', '? ', '\n\n', '\n', ' ']:
                pos = text.rfind(boundary, start, end)
                if pos != -1:
                    end = pos + 1
                    break
        
        chunks.append(text[start:end].strip())
        start = end - chunk_overlap
        
        if start < 0:
            start = 0
    
    return chunks


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Count tokens in text.
    
    Args:
        text: Text to count tokens for
        model: Model to use for token counting
        
    Returns:
        int: Number of tokens
    """
    try:
        import tiktoken
        
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        
        return len(encoding.encode(text))
    except ImportError:
        # Fallback: rough estimate
        return len(text) // 4


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary.
    
    Args:
        data: Dictionary to search
        key: Key to look up
        default: Default value if key not found
        
    Returns:
        Any: Value or default
    """
    return data.get(key, default)


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        base: Base dictionary
        override: Override dictionary (higher priority)
        
    Returns:
        Dict[str, Any]: Merged dictionary
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def sanitize_prompt(prompt: str) -> str:
    """
    Sanitize a prompt by removing potentially harmful content.
    
    Args:
        prompt: Prompt to sanitize
        
    Returns:
        str: Sanitized prompt
    """
    # Remove excessive whitespace
    prompt = re.sub(r'\s+', ' ', prompt).strip()
    
    # Remove potential injection patterns
    injection_patterns = [
        r'ignore previous instructions',
        r'forget all previous',
        r'system:',
        r'role:',
        r'you are now',
        r'as an ai',
    ]
    
    for pattern in injection_patterns:
        prompt = re.sub(pattern, '', prompt, flags=re.IGNORECASE)
    
    return prompt