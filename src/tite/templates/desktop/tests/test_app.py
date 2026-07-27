"""
Tests for the desktop application.

This module contains unit tests for the desktop application
functionality.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def config_data():
    """Provide test configuration data."""
    return {
        "debug": True,
        "theme": "dark",
        "language": "en",
    }


@pytest.fixture
def app_instance():
    """Create an application instance for testing."""
    from src.app import Application
    return Application()


class TestApplication:
    """Test suite for the application class."""

    def test_app_initialization(self, app_instance):
        """Test application initialization."""
        assert app_instance is not None
        assert app_instance.config is not None
        assert app_instance.data is not None

    def test_app_get_set(self, app_instance):
        """Test get and set methods."""
        # Set a value
        app_instance.set("test_key", "test_value")
        
        # Get the value
        value = app_instance.get("test_key")
        assert value == "test_value"
        
        # Get default value
        default = app_instance.get("nonexistent", "default")
        assert default == "default"

    def test_app_data_get_set(self, app_instance):
        """Test data get and set methods."""
        # Set data
        app_instance.set_data("user_data", {"name": "Test User"})
        
        # Get data
        data = app_instance.get_data("user_data")
        assert data["name"] == "Test User"
        
        # Get default
        default = app_instance.get_data("nonexistent", "default")
        assert default == "default"

    def test_app_save_config(self, app_instance, tmp_path):
        """Test saving configuration."""
        with patch.object(app_instance, '_get_config_path') as mock_path:
            config_path = tmp_path / "config.json"
            mock_path.return_value = config_path
            
            app_instance.set("test", "value")
            app_instance.save_config()
            
            assert config_path.exists()
            with open(config_path, "r") as f:
                saved = json.load(f)
            assert saved["test"] == "value"

    def test_app_save_data(self, app_instance, tmp_path):
        """Test saving data."""
        with patch.object(app_instance, '_get_data_path') as mock_path:
            data_path = tmp_path / "data.json"
            mock_path.return_value = data_path
            
            app_instance.set_data("test", "value")
            app_instance.save_data()
            
            assert data_path.exists()
            with open(data_path, "r") as f:
                saved = json.load(f)
            assert saved["test"] == "value"

    def test_app_load_config(self, app_instance, tmp_path):
        """Test loading configuration from file."""
        config_data = {"test": "loaded_value"}
        config_path = tmp_path / "config.json"
        
        with open(config_path, "w") as f:
            json.dump(config_data, f)
        
        with patch.object(app_instance, '_get_config_path') as mock_path:
            mock_path.return_value = config_path
            app_instance._load_config()
            
            assert app_instance.get("test") == "loaded_value"


class TestWindow:
    """Test suite for the main window."""

    def test_window_creation_qt(self):
        """Test Qt window creation."""
        try:
            from PySide6.QtWidgets import QApplication
            from src.ui.window import MainWindow
            
            app = QApplication([])
            window = MainWindow()
            assert window is not None
            assert window.windowTitle() == "{{ project_name }}"
            app.quit()
        except ImportError:
            pytest.skip("PySide6 not installed")

    def test_window_creation_tkinter(self):
        """Test Tkinter window creation."""
        try:
            import tkinter as tk
            from src.ui.window import MainWindow as TkWindow
            
            root = tk.Tk()
            window = TkWindow(root)
            assert window is not None
            assert window.root.title() == "{{ project_name }}"
            root.quit()
        except ImportError:
            pytest.skip("Tkinter not available")

    def test_window_actions(self):
        """Test window actions."""
        try:
            from PySide6.QtWidgets import QApplication
            from PySide6.QtCore import QTimer
            from src.ui.window import MainWindow
            
            app = QApplication([])
            window = MainWindow()
            
            # Test that actions exist
            assert hasattr(window, '_on_new')
            assert hasattr(window, '_on_open')
            assert hasattr(window, '_on_about')
            assert hasattr(window, '_on_action')
            
            # Trigger actions (they should not raise exceptions)
            window._on_new()
            window._on_open()
            window._on_about()
            window._on_action()
            
            app.quit()
        except ImportError:
            pytest.skip("PySide6 not installed")


class TestMain:
    """Test suite for the main module."""

    def test_main_import(self):
        """Test that main module imports correctly."""
        import src.main
        assert hasattr(src.main, "main")
        assert hasattr(src.main, "run_qt_app")
        assert hasattr(src.main, "run_tkinter_app")

    def test_main_function(self):
        """Test the main function."""
        import src.main
        
        # Mock the application to avoid actually running it
        with patch('src.main.run_qt_app') as mock_run:
            mock_run.return_value = 0
            result = src.main.main()
            assert result == 0