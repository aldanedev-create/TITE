"""
Tests for the API application.

This module contains unit tests for the API endpoints
and functionality.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

# Try to import FastAPI and test client
try:
    from fastapi.testclient import TestClient
    from src.main import create_fastapi_app
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

# Try to import Flask and test client
try:
    from flask.testing import FlaskClient
    from src.main import create_flask_app
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False


@pytest.fixture
def app():
    """Create a test application instance."""
    try:
        return create_fastapi_app()
    except:
        return create_flask_app()


@pytest.fixture
def client(app):
    """Create a test client."""
    if HAS_FASTAPI:
        return TestClient(app)
    elif HAS_FLASK:
        return app.test_client()
    else:
        pytest.skip("No web framework available for testing")


@pytest.fixture
def sample_item_data():
    """Provide sample item data for testing."""
    return {
        "name": "Test Item",
        "status": "active",
    }


@pytest.fixture
def sample_update_data():
    """Provide sample update data for testing."""
    return {
        "name": "Updated Item",
        "status": "inactive",
    }


class TestAPI:
    """Test suite for API application."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        
        data = response.json() if hasattr(response, 'json') else response.get_json()
        assert "status" in data
        assert "version" in data
        assert "service" in data
        assert "dependencies" in data

    def test_health_live(self, client):
        """Test liveness check endpoint."""
        response = client.get("/api/v1/health/live")
        assert response.status_code == 200

    def test_health_ready(self, client):
        """Test readiness check endpoint."""
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 200

    def test_health_dependencies(self, client):
        """Test dependencies check endpoint."""
        response = client.get("/api/v1/health/dependencies")
        assert response.status_code == 200
        
        data = response.json() if hasattr(response, 'json') else response.get_json()
        assert "dependencies" in data

    def test_ping(self, client):
        """Test ping endpoint."""
        response = client.get("/api/v1/ping")
        assert response.status_code == 200
        
        data = response.json() if hasattr(response, 'json') else response.get_json()
        assert data["ping"] == "pong"
        assert "timestamp" in data

    def test_api_prefix(self, client):
        """Test API prefix configuration."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_not_found(self, client):
        """Test 404 handling."""
        response = client.get("/api/v1/non-existent")
        assert response.status_code == 404

    def test_config_loading(self):
        """Test configuration loading."""
        from src import config
        
        assert hasattr(config, "APIConfig")
        assert hasattr(config, "config")
        assert hasattr(config.config, "debug")
        assert hasattr(config.config, "port")
        assert hasattr(config.config, "host")
        assert hasattr(config.config, "api_prefix")

    def test_config_validation(self):
        """Test configuration validation."""
        from src.config import APIConfig
        
        config = APIConfig()
        assert config.validate() is True

    def test_example_service(self):
        """Test example service."""
        from src.services.example_service import ExampleService
        
        service = ExampleService()
        
        # Test get items
        items = service.get_example_items(limit=5)
        assert len(items) == 5
        assert "id" in items[0]
        assert "name" in items[0]
        assert "status" in items[0]
        
        # Test get single item
        item = service.get_example_item(1)
        assert item is not None
        assert item["id"] == 1
        
        # Test get non-existent item
        item = service.get_example_item(999)
        assert item is None
        
        # Test create item
        new_item = service.create_example_item({"name": "New Test"})
        assert new_item["name"] == "New Test"
        assert "id" in new_item
        
        # Test update item
        updated = service.update_example_item(1, {"name": "Updated"})
        assert updated is not None
        assert updated["name"] == "Updated"
        
        # Test delete item
        result = service.delete_example_item(1)
        assert result is True
        
        # Test delete non-existent
        result = service.delete_example_item(999)
        assert result is False

    def test_data_processor(self):
        """Test data processor utilities."""
        from src.services.example_service import DataProcessor
        
        data = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
        ]
        
        processed = DataProcessor.process_data(data)
        assert len(processed) == 2
        assert processed[0]["processed"] is True
        assert "processed_at" in processed[0]
        
        # Test validation
        valid = DataProcessor.validate_data(
            {"name": "Test", "status": "active"},
            ["name", "status"]
        )
        assert valid is True
        
        invalid = DataProcessor.validate_data(
            {"name": "Test"},
            ["name", "status"]
        )
        assert invalid is False

    def test_helpers(self):
        """Test helper functions."""
        from src.utils.helpers import (
            generate_id,
            generate_timestamp,
            validate_email,
            validate_uuid,
            to_camel_case,
            to_snake_case,
            truncate_string,
        )
        
        # Test ID generation
        id1 = generate_id()
        id2 = generate_id()
        assert id1 != id2
        assert validate_uuid(id1)
        
        # Test timestamp
        ts = generate_timestamp()
        assert isinstance(ts, str)
        assert "T" in ts
        assert "Z" in ts
        
        # Test email validation
        assert validate_email("test@example.com")
        assert not validate_email("invalid-email")
        
        # Test case conversion
        assert to_camel_case("snake_case") == "snakeCase"
        assert to_snake_case("camelCase") == "camel_case"
        
        # Test truncation
        assert truncate_string("short") == "short"
        assert len(truncate_string("this is a very long string", 10)) <= 10

    def test_pagination_helper(self):
        """Test pagination helper."""
        from src.utils.helpers import PaginationHelper
        
        pagination = PaginationHelper(page=2, per_page=10)
        assert pagination.get_offset() == 10
        assert pagination.get_limit() == 10
        
        metadata = pagination.get_pagination_metadata(total=100)
        assert metadata["page"] == 2
        assert metadata["per_page"] == 10
        assert metadata["total"] == 100
        assert metadata["total_pages"] == 10
        assert metadata["has_next"] is True
        assert metadata["has_prev"] is True

    def test_rate_limiter(self):
        """Test rate limiter."""
        from src.utils.helpers import RateLimiter
        
        limiter = RateLimiter(max_requests=3, window_seconds=60)
        key = "test_client"
        
        # First 3 requests should be allowed
        assert limiter.is_allowed(key) is True
        assert limiter.is_allowed(key) is True
        assert limiter.is_allowed(key) is True
        
        # 4th request should be denied
        assert limiter.is_allowed(key) is False
        
        # Check remaining
        assert limiter.get_remaining(key) == 0

    def test_deep_merge(self):
        """Test deep merge utility."""
        from src.utils.helpers import deep_merge
        
        base = {"a": 1, "b": {"c": 2, "d": 3}}
        override = {"b": {"c": 4}, "e": 5}
        
        merged = deep_merge(base, override)
        assert merged["a"] == 1
        assert merged["b"]["c"] == 4
        assert merged["b"]["d"] == 3
        assert merged["e"] == 5


class TestModels:
    """Test suite for data models."""

    def test_example_model_import(self):
        """Test that example models import correctly."""
        try:
            from src.models.example import ExampleItem
            assert ExampleItem is not None
        except ImportError:
            from src.models.example import ExampleItem
            assert ExampleItem is not None


# Skip tests if no web framework is installed
pytestmark = pytest.mark.skipif(
    not (HAS_FASTAPI or HAS_FLASK),
    reason="No web framework available for testing"
)