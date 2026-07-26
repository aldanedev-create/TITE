"""
Tests for the web application.

This module contains unit tests for the web application endpoints
and functionality.
"""

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


class TestWebApplication:
    """Test suite for web application."""

    def test_home_page(self, client):
        """Test that home page loads successfully."""
        response = client.get("/")
        
        if HAS_FASTAPI:
            assert response.status_code == 200
            assert "text/html" in response.headers["content-type"]
        else:
            assert response.status_code == 200
        
        # Check for content
        content = response.text if hasattr(response, 'text') else response.data.decode()
        assert "{{ project_name }}" in content.lower() or "{{ project_name }}" in content

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        if HAS_FASTAPI:
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
            assert "framework" in response.json()
        else:
            assert response.status_code == 200
            data = response.json if hasattr(response, 'json') else response.get_json()
            assert data["status"] == "healthy"
            assert "framework" in data

    def test_static_files(self, client):
        """Test static files are served."""
        # Test CSS
        response = client.get("/static/css/style.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

    def test_static_js(self, client):
        """Test JavaScript static file."""
        response = client.get("/static/js/main.js")
        assert response.status_code == 200
        assert "javascript" in response.headers.get("content-type", "")

    def test_not_found(self, client):
        """Test 404 handling."""
        response = client.get("/non-existent-route")
        assert response.status_code == 404

    def test_config_loading(self):
        """Test configuration loading."""
        from src import config
        
        # Test default config
        assert hasattr(config, "AppConfig")
        assert hasattr(config, "config")
        assert hasattr(config.config, "debug")
        assert hasattr(config.config, "port")
        assert hasattr(config.config, "host")

    def test_config_validation(self, monkeypatch):
        """Test configuration validation."""
        from src.config import AppConfig
        
        # Valid config
        config = AppConfig()
        assert config.validate() is True
        
        # Invalid config - port out of range
        with monkeypatch.context() as m:
            m.setenv("PORT", "99999")
            config = AppConfig()
            with pytest.raises(ValueError):
                config.validate()
        
        # Invalid config - empty host
        with monkeypatch.context() as m:
            m.setenv("HOST", "")
            config = AppConfig()
            with pytest.raises(ValueError):
                config.validate()

    def test_config_from_env(self, monkeypatch):
        """Test loading config from environment variables."""
        from src.config import load_config, AppConfig
        
        with monkeypatch.context() as m:
            m.setenv("APP_DEBUG", "true")
            m.setenv("APP_PORT", "9000")
            m.setenv("APP_HOST", "0.0.0.0")
            
            # Since AppConfig loads from env at import, we need to reload
            import importlib
            import sys
            
            if "src.config" in sys.modules:
                importlib.reload(sys.modules["src.config"])
            
            from src.config import config as reloaded_config
            
            # Check that values were loaded
            assert reloaded_config.port == 9000
            assert reloaded_config.host == "0.0.0.0"

    def test_config_file_loading(self, tmp_path):
        """Test loading config from file."""
        import json
        
        from src.config import load_config
        
        # Create a test config file
        config_data = {
            "debug": True,
            "port": 5000,
            "host": "0.0.0.0",
            "secret_key": "test-secret-key",
        }
        
        config_path = tmp_path / "config.json"
        with open(config_path, "w") as f:
            json.dump(config_data, f)
        
        # Load config
        loaded_config = load_config(config_path, env_prefix="")
        
        assert loaded_config.debug is True
        assert loaded_config.port == 5000
        assert loaded_config.host == "0.0.0.0"
        assert loaded_config.secret_key == "test-secret-key"

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        from src.config import AppConfig
        
        config = AppConfig()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "debug" in config_dict
        assert "port" in config_dict
        assert "host" in config_dict
        assert "secret_key" in config_dict
        assert config_dict["secret_key"] == "***"  # Should be masked
        assert "allowed_hosts" in config_dict
        assert "cors_origins" in config_dict


class TestMainModule:
    """Test suite for main module."""

    def test_create_app(self):
        """Test app creation."""
        from src.main import create_app
        
        app = create_app()
        assert app is not None

    def test_main_imports(self):
        """Test that main module imports correctly."""
        import src.main
        assert hasattr(src.main, "create_app")
        assert hasattr(src.main, "main")
        assert hasattr(src.main, "FRAMEWORK")

    def test_logging_setup(self):
        """Test logging configuration."""
        import src.main
        assert hasattr(src.main, "logger")
        
        # Check that logger is configured
        logger = src.main.logger
        assert logger is not None
        assert logger.name == "src.main"


# Skip tests if no web framework is installed
pytestmark = pytest.mark.skipif(
    not (HAS_FASTAPI or HAS_FLASK),
    reason="No web framework available for testing"
)