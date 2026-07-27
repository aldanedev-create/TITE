"""
Tests for the CLI application.

This module contains unit tests for the CLI commands and functionality.
"""

import json
import tempfile
from pathlib import Path

import pytest

# Try to import Click
try:
    from click.testing import CliRunner
    from app.main import cli
    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False

# Try to import the app
try:
    from app.main import main
    from app.commands import hello_command, status_command, register_commands
    HAS_APP = True
except ImportError:
    HAS_APP = False


@pytest.fixture
def runner():
    """Create a Click test runner."""
    if HAS_CLICK:
        return CliRunner()
    return None


@pytest.fixture
def config_file():
    """Create a temporary config file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        config_data = {
            "name": "test-app",
            "greeting": "Hello from test!",
        }
        json.dump(config_data, f)
        f.flush()
        yield Path(f.name)
    
    # Cleanup
    Path(f.name).unlink()


class TestCLI:
    """Test suite for CLI application."""

    def test_hello_command(self):
        """Test hello command."""
        result = hello_command({"name": "Test", "config": {}, "verbose": False})
        assert result == 0

    def test_status_command(self):
        """Test status command."""
        result = status_command({"config": {"name": "test"}})
        assert result == 0

    def test_register_commands(self):
        """Test command registration."""
        commands = register_commands()
        assert "hello" in commands
        assert "status" in commands
        assert "config" in commands

    @pytest.mark.skipif(not HAS_CLICK, reason="Click not installed")
    def test_cli_hello(self, runner):
        """Test hello command via CLI."""
        result = runner.invoke(cli, ["hello", "--name", "Test"])
        assert result.exit_code == 0
        assert "Hello, Test!" in result.output

    @pytest.mark.skipif(not HAS_CLICK, reason="Click not installed")
    def test_cli_status(self, runner):
        """Test status command via CLI."""
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "Application Status" in result.output

    @pytest.mark.skipif(not HAS_CLICK, reason="Click not installed")
    def test_cli_help(self, runner):
        """Test help command."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Commands" in result.output or "Usage" in result.output

    @pytest.mark.skipif(not HAS_CLICK, reason="Click not installed")
    def test_cli_verbose(self, runner):
        """Test verbose flag."""
        result = runner.invoke(cli, ["--verbose", "hello"])
        assert result.exit_code == 0

    @pytest.mark.skipif(not HAS_CLICK, reason="Click not installed")
    def test_cli_with_config(self, runner, config_file):
        """Test with config file."""
        result = runner.invoke(cli, ["--config", str(config_file), "status"])
        assert result.exit_code == 0
        assert "Config loaded: Yes" in result.output

    def test_load_config(self, config_file):
        """Test configuration loading."""
        from app.config import load_config
        
        config = load_config(str(config_file))
        assert config.get("name") == "test-app"
        assert config.get("greeting") == "Hello from test!"

    def test_load_config_defaults(self):
        """Test default configuration."""
        from app.config import load_config
        
        config = load_config()
        assert config.get("name") == "{{ project_name }}"
        assert "version" in config.data

    def test_config_save(self):
        """Test saving configuration."""
        from app.config import Config
        
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.json"
            config = Config(data={"test": "value"}, config_path=config_path)
            config.save()
            
            assert config_path.exists()
            with open(config_path, "r") as f:
                saved = json.load(f)
            assert saved["test"] == "value"

    def test_config_get_set(self):
        """Test config get/set methods."""
        from app.config import Config
        
        config = Config(data={"existing": "value"})
        assert config.get("existing") == "value"
        assert config.get("missing", "default") == "default"
        
        config.set("new_key", "new_value")
        assert config.get("new_key") == "new_value"


class TestCommands:
    """Test suite for individual commands."""

    def test_hello_command_with_config(self):
        """Test hello command with config."""
        config = {"greeting": "Special greeting!"}
        result = hello_command({"name": "Test", "config": config, "verbose": False})
        assert result == 0

    def test_hello_command_verbose(self, capsys):
        """Test hello command with verbose flag."""
        result = hello_command({"name": "Test", "config": {}, "verbose": True})
        assert result == 0

    def test_status_command_with_config(self):
        """Test status command with config."""
        config = {"name": "test-app", "version": "1.0.0", "debug": True}
        result = status_command({"config": config})
        assert result == 0

    def test_status_command_empty_config(self):
        """Test status command with empty config."""
        result = status_command({"config": {}})
        assert result == 0

    def test_config_command_show(self):
        """Test config show command."""
        from app.commands import config_command
        
        config = {"name": "test", "version": "0.1.0"}
        result = config_command({"config": config, "action": "show"})
        assert result == 0

    def test_config_command_get(self):
        """Test config get command."""
        from app.commands import config_command
        
        config = {"name": "test", "version": "0.1.0"}
        result = config_command({"config": config, "action": "get", "key": "name"})
        assert result == 0

    def test_config_command_set(self):
        """Test config set command."""
        from app.commands import config_command
        
        config = {}
        result = config_command({"config": config, "action": "set", "key": "test", "value": "value"})
        assert result == 0