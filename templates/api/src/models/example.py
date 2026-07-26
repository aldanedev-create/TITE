"""
Example data models for the API.

This module defines Pydantic models or dataclasses for
request and response validation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

# Try to import Pydantic
try:
    from pydantic import BaseModel, Field, validator
    HAS_PYDANTIC = True
except ImportError:
    from dataclasses import dataclass
    HAS_PYDANTIC = False


if HAS_PYDANTIC:
    # Pydantic models for FastAPI
    
    class ExampleItem(BaseModel):
        """Example item model."""
        
        id: int = Field(..., description="Item ID")
        name: str = Field(..., min_length=1, max_length=100, description="Item name")
        status: str = Field(default="active", description="Item status")
        created_at: Optional[datetime] = Field(None, description="Creation timestamp")
        updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
        
        @validator("status")
        def validate_status(cls, v: str) -> str:
            """Validate status value."""
            allowed = ["active", "inactive", "pending"]
            if v not in allowed:
                raise ValueError(f"Status must be one of {allowed}")
            return v
    
    class ExampleItemCreate(BaseModel):
        """Model for creating a new example item."""
        
        name: str = Field(..., min_length=1, max_length=100, description="Item name")
        status: str = Field(default="active", description="Item status")
        
        @validator("status")
        def validate_status(cls, v: str) -> str:
            """Validate status value."""
            allowed = ["active", "inactive", "pending"]
            if v not in allowed:
                raise ValueError(f"Status must be one of {allowed}")
            return v
    
    class ExampleItemUpdate(BaseModel):
        """Model for updating an example item."""
        
        name: Optional[str] = Field(None, min_length=1, max_length=100, description="Item name")
        status: Optional[str] = Field(None, description="Item status")
        
        @validator("status")
        def validate_status(cls, v: str) -> str:
            """Validate status value."""
            allowed = ["active", "inactive", "pending"]
            if v is not None and v not in allowed:
                raise ValueError(f"Status must be one of {allowed}")
            return v
    
    class ListResponse(BaseModel):
        """Generic list response model."""
        
        items: List[Any] = Field(..., description="List of items")
        total: int = Field(..., description="Total number of items")
        offset: int = Field(0, description="Offset used for pagination")
        limit: int = Field(10, description="Limit used for pagination")
    
    class ErrorResponse(BaseModel):
        """Error response model."""
        
        error: Dict[str, Any] = Field(..., description="Error details")
        
        class ErrorDetail(BaseModel):
            code: int = Field(..., description="Error code")
            message: str = Field(..., description="Error message")
            type: str = Field(..., description="Error type")
            details: Optional[List[Dict[str, Any]]] = Field(None, description="Additional details")
    
    class HealthResponse(BaseModel):
        """Health check response model."""
        
        status: str = Field(..., description="Health status")
        timestamp: str = Field(..., description="Check timestamp")
        version: str = Field(..., description="API version")
        service: str = Field(..., description="Service name")
        dependencies: Dict[str, bool] = Field(..., description="Dependency status")
        system: Dict[str, str] = Field(..., description="System information")

else:
    # Dataclass fallback for Flask
    
    from dataclasses import dataclass
    
    @dataclass
    class ExampleItem:
        """Example item dataclass."""
        
        id: int
        name: str
        status: str = "active"
        created_at: Optional[str] = None
        updated_at: Optional[str] = None
    
    @dataclass
    class ExampleItemCreate:
        """Model for creating a new example item."""
        
        name: str
        status: str = "active"
    
    @dataclass
    class ExampleItemUpdate:
        """Model for updating an example item."""
        
        name: Optional[str] = None
        status: Optional[str] = None