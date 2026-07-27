"""
Unit tests for the {{ project_name }} core module.

This module contains tests for the core functionality of the
{{ project_name }} library.
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest

from {{ package_name }} import core
from {{ package_name }}.core import {{ project_name|title|replace('-', '') }}, main_function


class Test{{ project_name|title|replace('-', '') }}:
    """Test suite for the {{ project_name|title|replace('-', '') }} class."""

    def test_init_default(self):
        """Test initialization with default parameters."""
        instance = {{ project_name|title|replace('-', '') }}()
        assert instance.config == {}
        assert instance.verbose is False

    def test_init_with_config(self):
        """Test initialization with custom configuration."""
        config = {"key": "value", "debug": True}
        instance = {{ project_name|title|replace('-', '') }}(config=config)
        assert instance.config == config
        assert instance.verbose is False

    def test_init_with_verbose(self):
        """Test initialization with verbose flag."""
        instance = {{ project_name|title|replace('-', '') }}(verbose=True)
        assert instance.config == {}
        assert instance.verbose is True

    def test_process_string(self):
        """Test processing string input."""
        instance = {{ project_name|title|replace('-', '') }}()
        result = instance.process("Hello, World!")
        
        assert result["type"] == "string"
        assert result["length"] == 13
        assert result["content"] == "Hello, World!"

    def test_process_string_as_path(self):
        """Test processing a string that is a valid path."""
        instance = {{ project_name|title|replace('-', '') }}()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Test content")
            temp_path = f.name
        
        try:
            result = instance.process(temp_path)
            assert result["type"] == "file"
            assert Path(result["path"]).exists()
            assert result["content"] == "Test content"
            assert result["size"] > 0
        finally:
            Path(temp_path).unlink()

    def test_process_file(self):
        """Test processing file input."""
        instance = {{ project_name|title|replace('-', '') }}()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("File content for testing")
            temp_path = Path(f.name)
        
        try:
            result = instance.process(temp_path)
            assert result["type"] == "file"
            assert result["path"] == str(temp_path)
            assert result["content"] == "File content for testing"
            assert result["size"] == temp_path.stat().st_size
        finally:
            temp_path.unlink()

    def test_process_file_not_found(self):
        """Test processing non-existent file."""
        instance = {{ project_name|title|replace('-', '') }}()
        non_existent = Path("/non/existent/file.txt")
        
        with pytest.raises(FileNotFoundError):
            instance.process(non_existent)

    def test_process_dict(self):
        """Test processing dictionary input."""
        instance = {{ project_name|title|replace('-', '') }}()
        input_dict = {"key1": "value1", "key2": 42, "key3": [1, 2, 3]}
        
        result = instance.process(input_dict)
        
        assert result["type"] == "dict"
        assert result["keys"] == ["key1", "key2", "key3"]
        assert result["content"] == input_dict

    def test_process_unsupported_type(self):
        """Test processing unsupported input type."""
        instance = {{ project_name|title|replace('-', '') }}()
        
        with pytest.raises(ValueError):
            instance.process(123)  # type: ignore

    def test_validate(self):
        """Test data validation."""
        instance = {{ project_name|title|replace('-', '') }}()
        
        # Valid data
        assert instance.validate("test") is True
        assert instance.validate({"key": "value"}) is True
        
        # Invalid data
        assert instance.validate(None) is False

    def test_get_info(self):
        """Test getting instance information."""
        instance = {{ project_name|title|replace('-', '') }}(config={"test": True}, verbose=True)
        info = instance.get_info()
        
        assert info["name"] == "{{ project_name }}"
        assert "version" in info
        assert info["verbose"] is True
        assert info["config"] == {"test": True}


class TestMainFunction:
    """Test suite for the main_function convenience wrapper."""

    def test_main_function_string(self):
        """Test main_function with string input."""
        result = main_function("Hello, World!")
        
        assert result["type"] == "string"
        assert result["length"] == 13
        assert result["content"] == "Hello, World!"

    def test_main_function_dict(self):
        """Test main_function with dictionary input."""
        input_dict = {"test": "data"}
        result = main_function(input_dict)
        
        assert result["type"] == "dict"
        assert result["content"] == input_dict

    def test_main_function_with_config(self):
        """Test main_function with custom configuration."""
        config = {"custom": True}
        result = main_function("test", config=config)
        
        assert result["type"] == "string"
        assert result["content"] == "test"

    def test_main_function_verbose(self):
        """Test main_function with verbose flag."""
        result = main_function("test", verbose=True)
        assert result["type"] == "string"


class TestUtilityFunctions:
    """Test suite for utility functions."""

    def test_load_config_none(self):
        """Test loading config with no path."""
        config = core.load_config()
        assert config == {}

    def test_load_config_missing(self):
        """Test loading config from missing file."""
        config = core.load_config(Path("/missing/config.json"))
        assert config == {}

    def test_load_config_json(self, tmp_path):
        """Test loading JSON config."""
        config_data = {"key": "value", "number": 42}
        config_path = tmp_path / "config.json"
        
        with open(config_path, "w") as f:
            json.dump(config_data, f)
        
        loaded = core.load_config(config_path)
        assert loaded == config_data

    def test_load_config_toml(self, tmp_path):
        """Test loading TOML config."""
        config_data = {"key": "value", "number": 42}
        config_path = tmp_path / "config.toml"
        
        with open(config_path, "w") as f:
            f.write('key = "value"\nnumber = 42\n')
        
        loaded = core.load_config(config_path)
        assert loaded["key"] == "value"
        assert loaded["number"] == 42

    def test_load_config_unsupported(self, tmp_path):
        """Test loading unsupported config format."""
        config_path = tmp_path / "config.unsupported"
        
        with open(config_path, "w") as f:
            f.write("test")
        
        with pytest.raises(ValueError):
            core.load_config(config_path)


@pytest.fixture
def sample_instance():
    """Fixture providing a configured instance for testing."""
    return {{ project_name|title|replace('-', '') }}(config={"test_mode": True}, verbose=True)


def test_fixture_usage(sample_instance):
    """Test using the fixture."""
    info = sample_instance.get_info()
    assert info["config"]["test_mode"] is True
    assert info["verbose"] is True