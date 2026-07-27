"""
Utility helper functions for the API.

This module provides shared utility functions used across the API application.
"""

import hashlib
import json
import os
import re
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def generate_id() -> str:
    """
    Generate a unique ID.
    
    Returns:
        str: Unique ID (UUID4)
    """
    return str(uuid.uuid4())


def generate_timestamp() -> str:
    """
    Generate ISO format timestamp.
    
    Returns:
        str: ISO format timestamp
    """
    return datetime.utcnow().isoformat() + "Z"


def hash_string(text: str, algorithm: str = "sha256") -> str:
    """
    Hash a string using the specified algorithm.
    
    Args:
        text: String to hash
        algorithm: Hash algorithm (sha256, md5, sha1)
        
    Returns:
        str: Hashed string
    """
    if algorithm == "sha256":
        return hashlib.sha256(text.encode()).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(text.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_uuid(uuid_string: str) -> bool:
    """
    Validate UUID format.
    
    Args:
        uuid_string: UUID string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def parse_json_safe(data: Union[str, bytes, bytearray]) -> Optional[Dict[str, Any]]:
    """
    Safely parse JSON data.
    
    Args:
        data: JSON string to parse
        
    Returns:
        Optional[Dict[str, Any]]: Parsed data or None if invalid
    """
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return None


def to_camel_case(text: str) -> str:
    """
    Convert snake_case to camelCase.
    
    Args:
        text: snake_case string
        
    Returns:
        str: camelCase string
    """
    components = text.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def to_snake_case(text: str) -> str:
    """
    Convert camelCase to snake_case.
    
    Args:
        text: camelCase string
        
    Returns:
        str: snake_case string
    """
    pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
    return pattern.sub("_", text).lower()


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


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


class PaginationHelper:
    """
    Helper class for pagination.
    """

    def __init__(self, page: int = 1, per_page: int = 20, max_per_page: int = 100):
        """
        Initialize pagination helper.
        
        Args:
            page: Current page number (1-indexed)
            per_page: Number of items per page
            max_per_page: Maximum items per page
        """
        self.page = max(1, page)
        self.per_page = min(max(1, per_page), max_per_page)
        self.offset = (self.page - 1) * self.per_page
    
    def get_offset(self) -> int:
        """
        Get the offset for database queries.
        
        Returns:
            int: Offset value
        """
        return self.offset
    
    def get_limit(self) -> int:
        """
        Get the limit for database queries.
        
        Returns:
            int: Limit value
        """
        return self.per_page
    
    def get_pagination_metadata(self, total: int) -> Dict[str, Any]:
        """
        Get pagination metadata.
        
        Args:
            total: Total number of items
            
        Returns:
            Dict[str, Any]: Pagination metadata
        """
        total_pages = (total + self.per_page - 1) // self.per_page
        
        return {
            "page": self.page,
            "per_page": self.per_page,
            "total": total,
            "total_pages": total_pages,
            "has_next": self.page < total_pages,
            "has_prev": self.page > 1,
        }


class RateLimiter:
    """
    Simple rate limiter implementation.
    """

    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in the window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # key -> list of timestamps
    
    def is_allowed(self, key: str) -> bool:
        """
        Check if a request is allowed.
        
        Args:
            key: Identifier for the client
            
        Returns:
            bool: True if allowed, False if rate limited
        """
        now = datetime.utcnow().timestamp()
        
        # Clean up old entries
        if key in self.requests:
            self.requests[key] = [
                t for t in self.requests[key]
                if t > now - self.window_seconds
            ]
        else:
            self.requests[key] = []
        
        # Check limit
        if len(self.requests[key]) >= self.max_requests:
            return False
        
        # Add request
        self.requests[key].append(now)
        return True
    
    def get_remaining(self, key: str) -> int:
        """
        Get remaining requests allowed.
        
        Args:
            key: Identifier for the client
            
        Returns:
            int: Remaining requests
        """
        now = datetime.utcnow().timestamp()
        
        if key in self.requests:
            active = [
                t for t in self.requests[key]
                if t > now - self.window_seconds
            ]
            return max(0, self.max_requests - len(active))
        
        return self.max_requests