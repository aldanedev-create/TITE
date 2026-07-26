"""
Example service module.

This module provides example service implementations for the API.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ExampleService:
    """
    Example service class.
    
    This class provides example business logic and data operations.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        logger.info("ExampleService initialized with config: %s", self.config)
    
    def get_example_items(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get example items.
        
        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            
        Returns:
            List[Dict[str, Any]]: List of example items
        """
        logger.debug(f"Getting example items with limit={limit}, offset={offset}")
        
        # Example data - replace with actual database query
        items = [
            {"id": i, "name": f"Example Item {i}", "status": "active"}
            for i in range(offset + 1, offset + limit + 1)
        ]
        
        return items
    
    def get_example_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a single example item by ID.
        
        Args:
            item_id: ID of the item to retrieve
            
        Returns:
            Optional[Dict[str, Any]]: Item data or None if not found
        """
        logger.debug(f"Getting example item with id={item_id}")
        
        # Example data - replace with actual database query
        if 1 <= item_id <= 100:
            return {"id": item_id, "name": f"Example Item {item_id}", "status": "active"}
        
        return None
    
    def create_example_item(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new example item.
        
        Args:
            data: Item data
            
        Returns:
            Dict[str, Any]: Created item
        """
        logger.info(f"Creating example item with data: {data}")
        
        # Example - replace with actual database insert
        new_item = {
            "id": 101,
            "name": data.get("name", "New Item"),
            "status": data.get("status", "active"),
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        
        return new_item
    
    def update_example_item(self, item_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing example item.
        
        Args:
            item_id: ID of the item to update
            data: Updated item data
            
        Returns:
            Optional[Dict[str, Any]]: Updated item or None if not found
        """
        logger.info(f"Updating example item {item_id} with data: {data}")
        
        # Example - replace with actual database update
        existing = self.get_example_item(item_id)
        if existing is None:
            return None
        
        updated = {
            **existing,
            **data,
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }
        
        return updated
    
    def delete_example_item(self, item_id: int) -> bool:
        """
        Delete an example item.
        
        Args:
            item_id: ID of the item to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        logger.info(f"Deleting example item {item_id}")
        
        # Example - replace with actual database delete
        existing = self.get_example_item(item_id)
        if existing is None:
            return False
        
        return True


class DataProcessor:
    """
    Data processing utility class.
    
    This class provides data processing and transformation methods.
    """

    @staticmethod
    def process_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a list of data items.
        
        Args:
            data: List of data items to process
            
        Returns:
            List[Dict[str, Any]]: Processed data
        """
        processed = []
        for item in data:
            processed.append({
                **item,
                "processed_at": datetime.utcnow().isoformat() + "Z",
                "processed": True,
            })
        return processed
    
    @staticmethod
    def validate_data(data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Validate data against required fields.
        
        Args:
            data: Data to validate
            required_fields: List of required field names
            
        Returns:
            bool: True if valid, False otherwise
        """
        for field in required_fields:
            if field not in data or data[field] is None:
                return False
        return True


def get_example_service() -> ExampleService:
    """
    Factory function for getting ExampleService instance.
    
    Returns:
        ExampleService: Configured service instance
    """
    from src.config import config
    
    return ExampleService(config=config.to_dict())