# Tite Plugins

## Overview

Tite supports a plugin system that allows you to extend its functionality. Plugins can add new commands, modes, templates, and hooks.

## Plugin Architecture

┌─────────────────────────────────────────────────────┐
│ Tite Core │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ Command │ │ Mode │ │ Template │ │
│ │ Registry │ │ Registry │ │ Registry │ │
│ └──────────┘ └──────────┘ └──────────┘ │
└──────────────────────┬──────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ Plugin API │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ Hooks │ │ Events │ │ Context │ │
│ └──────────┘ └──────────┘ └──────────┘ │
└──────────────────────┬──────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ Plugins │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ Plugin 1 │ │ Plugin 2 │ │ Plugin 3 │ │
│ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────┘

text

## Creating a Plugin

### Plugin Structure
my-tite-plugin/
├── src/
│ └── my_tite_plugin/
│ ├── init.py
│ ├── plugin.py
│ ├── commands/
│ ├── modes/
│ └── templates/
├── pyproject.toml
├── README.md
└── LICENSE

text

### Plugin Manifest

```toml
# pyproject.toml
[project]
name = "my-tite-plugin"
version = "0.1.0"
description = "My Tite plugin"

[tool.tite.plugin]
name = "my-plugin"
version = "0.1.0"
description = "My Tite plugin"
commands = ["my-command"]
modes = ["my-mode"]
hooks = ["pre-create", "post-create"]
Plugin Implementation
python
# src/my_tite_plugin/plugin.py
from typing import Any, Dict

from tite.plugin import Plugin, hook, command


class MyPlugin(Plugin):
    """My Tite plugin."""

    name = "my-plugin"
    version = "0.1.0"
    description = "My Tite plugin"

    @hook("pre-create")
    def pre_create(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Hook called before project creation."""
        print("Pre-create hook")
        return context

    @hook("post-create")
    def post_create(self, context: Dict[str, Any]) -> None:
        """Hook called after project creation."""
        print("Post-create hook")

    @command("my-command")
    def my_command(self, args: Dict[str, Any]) -> int:
        """My custom command."""
        print("My command executed")
        return 0


def get_plugin():
    """Return plugin instance."""
    return MyPlugin()
Installing a Plugin
bash
# Install from PyPI
pip install my-tite-plugin

# Install from local
pip install /path/to/my-tite-plugin

# Install from GitHub
pip install git+https://github.com/user/my-tite-plugin.git
Plugin Types
Commands
Plugins can add new commands:

python
@command("my-command")
def my_command(args: Dict[str, Any]) -> int:
    """My custom command."""
    print("My command executed")
    return 0
Modes
Plugins can add new modes:

python
@mode("my-mode")
def get_mode() -> Dict[str, Any]:
    """Get mode configuration."""
    return {
        "name": "My Mode",
        "description": "My custom mode",
        "template": "my-template",
        "packages": ["package1", "package2"],
        "structure": {
            "directories": ["src", "tests"],
            "files": ["README.md"],
        },
    }
Templates
Plugins can add new templates:

python
@template("my-template")
def get_template() -> Dict[str, Any]:
    """Get template definition."""
    return {
        "name": "My Template",
        "description": "My custom template",
        "files": {
            "README.md": "# My Project\n",
            "src/main.py": "def main(): pass\n",
        },
    }
Hooks
Plugins can hook into lifecycle events:

Hook	Description
pre-create	Before project creation
post-create	After project creation
pre-dev	Before development server starts
post-dev	After development server stops
pre-clean	Before cleaning
post-clean	After cleaning
pre-doctor	Before health checks
post-doctor	After health checks
Plugin API Reference
Plugin Class
python
class Plugin:
    """Base plugin class."""

    name: str = "plugin"
    version: str = "0.1.0"
    description: str = ""

    def initialize(self, context: Dict[str, Any]) -> None:
        """Initialize the plugin."""
        pass

    def shutdown(self) -> None:
        """Shutdown the plugin."""
        pass
Hook Decorator
python
@hook("hook-name")
def my_hook(context: Dict[str, Any]) -> Dict[str, Any]:
    """Hook implementation."""
    return context
Command Decorator
python
@command("command-name")
def my_command(args: Dict[str, Any]) -> int:
    """Command implementation."""
    return 0
Mode Decorator
python
@mode("mode-name")
def get_mode() -> Dict[str, Any]:
    """Mode implementation."""
    return {
        "name": "My Mode",
        "description": "My custom mode",
    }
Template Decorator
python
@template("template-name")
def get_template() -> Dict[str, Any]:
    """Template implementation."""
    return {
        "name": "My Template",
        "description": "My custom template",
    }
Plugin Discovery
Tite discovers plugins in the following locations:

Installed Packages: Packages with tite-plugin entry point

Plugin Directory: ~/.tite/plugins/

Project Plugins: .tite/plugins/

Entry Point Discovery
toml
# pyproject.toml
[project.entry-points."tite.plugins"]
my-plugin = "my_tite_plugin.plugin:get_plugin"
Plugin Directory
text
~/.tite/plugins/
├── my-plugin/
│   ├── __init__.py
│   ├── plugin.py
│   └── pyproject.toml
└── another-plugin/
    ├── __init__.py
    └── plugin.py
Plugin Best Practices
1. Namespace
Use descriptive names: my-plugin not plugin

Prefix commands: my-plugin:command

Prefix modes: my-plugin:mode

2. Versioning
Follow semantic versioning

Check Tite version compatibility

Document breaking changes

3. Documentation
Document all commands

Document all hooks

Provide usage examples

4. Testing
Test with Tite

Test with different Python versions

Test on different platforms

5. Performance
Lazy load modules

Cache expensive operations

Avoid blocking operations

Example Plugin
Structure
text
tite-awesome-plugin/
├── src/
│   └── tite_awesome_plugin/
│       ├── __init__.py
│       ├── plugin.py
│       ├── commands/
│       │   ├── __init__.py
│       │   └── awesome.py
│       └── templates/
│           ├── __init__.py
│           └── awesome/
│               └── README.md
├── pyproject.toml
├── README.md
└── LICENSE
Code
python
# src/tite_awesome_plugin/plugin.py
from typing import Any, Dict

from tite.plugin import Plugin, hook, command, mode


class AwesomePlugin(Plugin):
    name = "awesome-plugin"
    version = "0.1.0"
    description = "Add awesome features to Tite"

    @hook("post-create")
    def post_create(self, context: Dict[str, Any]) -> None:
        print("🎉 Project created with awesome plugin!")

    @command("awesome")
    def awesome_command(self, args: Dict[str, Any]) -> int:
        print("✨ Awesome command executed!")
        return 0

    @mode("awesome")
    def get_awesome_mode(self) -> Dict[str, Any]:
        return {
            "name": "Awesome Mode",
            "description": "Create awesome projects",
            "template": "awesome",
            "packages": ["requests", "click"],
        }


def get_plugin():
    return AwesomePlugin()
Usage
bash
# Install plugin
pip install tite-awesome-plugin

# Use plugin command
tite awesome

# Use plugin mode
tite mode awesome my-project
Troubleshooting
Plugin Not Found
Check if plugin is installed: pip list

Check entry point: pip show tite-awesome-plugin

Check plugin directory: ~/.tite/plugins/

Plugin Not Loading
Check Python path: sys.path

Check for import errors

Check for syntax errors

Plugin Conflicts
Check for duplicate hooks

Check for duplicate commands

Check for duplicate modes

Future Development
Planned Features
□ Plugin Marketplace: Discover and install plugins
□ Plugin Manager: tite plugin install, tite plugin remove
□ Plugin Sandbox: Isolated plugin execution
□ Plugin Versioning: Compatibility checking
□ Plugin Updates: Auto-update plugins
Community Plugins
tite-django-plugin: Django support

tite-fastapi-plugin: FastAPI support

tite-flask-plugin: Flask support

tite-docker-plugin: Docker integration

tite-aws-plugin: AWS deployment

tite-azure-plugin: Azure deployment

tite-gcp-plugin: Google Cloud deployment