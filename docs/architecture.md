# Tite Architecture

## Overview

Tite is a zero-configuration Python project bootstrapper designed to automate project initialization while remaining technology-neutral. This document describes the architecture, design decisions, and internal workings of Tite.

## Core Philosophy

> "Tite has one job: Prepare the project so the developer can immediately start coding."

Tite is built on several key principles:

- **Convention over Configuration** - Sensible defaults for all projects
- **Framework Agnostic** - Works with any Python framework or library
- **Zero Prompts** - No unnecessary user interaction
- **Production Ready** - Creates professional, standardized project structures
- **Fast Execution** - Projects ready in seconds

## Architecture Diagram

┌─────────────────────────────────────────────────────────────────────────────┐
│ USER / CLI │
│ tite <command> [args] │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ CLI LAYER │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ parser │ │ output │ │ terminal│ │ progress│ │ help │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ COMMAND LAYER │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │
│ │ new │ │ dev │ │doctor│ │clean│ │ info│ │config│ │ env │ │mode │ │
│ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ CORE LAYER │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │bootstrap │ │ project │ │filesystem│ │ templates│ │ config │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ validator│ │ detector │ │installer │ │environment│ │ git │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ process │ │ workflow │ │ blueprint│ │
│ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ SERVICE LAYER │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ venv │ │ python │ │ packages │ │interpreter│ │ git │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ health │ │ doctor │ │ server │ │ watcher │ │ reload │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ UTILITY LAYER │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │
│ │ logger │ │ paths │ │ io │ │ system │ │archive │ │terminal│ │
│ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │
│ ┌────────┐ ┌────────┐ │
│ │download│ │platform│ │
│ └────────┘ └────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Module Descriptions

### CLI Layer (`src/tite/cli/`)

The CLI layer handles user interaction, command parsing, and output formatting.

| Module | Purpose |
|--------|---------|
| `app.py` | Main CLI entry point, command routing |
| `parser.py` | Argument parsing with argparse |
| `output.py` | Rich console output, tables, panels |
| `terminal.py` | Terminal utilities, color support |
| `progress.py` | Progress bars and spinners |
| `help.py` | Help message generation |

### Command Layer (`src/tite/cli/commands/`)

Each command is implemented as a separate module.

| Command | Purpose |
|---------|---------|
| `new.py` | Create new Python project |
| `dev.py` | Start development server |
| `doctor.py` | Run health checks |
| `clean.py` | Clean build artifacts |
| `info.py` | Show project information |
| `config.py` | View/modify configuration |
| `env.py` | Show environment details |
| `mode.py` | Work with project modes |
| `init.py` | Initialize existing project |
| `update.py` | Update dependencies |
| `version.py` | Show version information |

### Core Layer (`src/tite/core/`)

The core layer contains the main business logic.

| Module | Purpose |
|--------|---------|
| `bootstrap.py` | Project creation orchestration |
| `project.py` | Project metadata management |
| `filesystem.py` | File operations |
| `templates.py` | Template rendering |
| `config.py` | Configuration management |
| `validator.py` | Validation utilities |
| `detector.py` | Project detection |
| `installer.py` | Package installation |
| `environment.py` | Virtual environment management |
| `git.py` | Git operations |
| `process.py` | Process management |
| `workflow.py` | Workflow execution |

### Blueprint Layer (`src/tite/blueprint/`)

The blueprint layer handles reusable project templates.

| Module | Purpose |
|--------|---------|
| `parser.py` | Parse blueprint definitions |
| `builder.py` | Build projects from blueprints |
| `validator.py` | Validate blueprints |
| `schema.py` | Blueprint schema |
| `templates.py` | Template engine |

### Service Layer (`src/tite/` submodules)

Service modules provide specific functionality.

| Module | Purpose |
|--------|---------|
| `environment/` | Python environment management |
| `git/` | Git operations |
| `diagnostics/` | Health checking |
| `dev/` | Development server |
| `modes/` | Project modes |
| `config/` | Configuration management |

### Utility Layer (`src/tite/utils/`)

Utility modules provide shared functionality.

| Module | Purpose |
|--------|---------|
| `logger.py` | Logging configuration |
| `paths.py` | Path manipulation |
| `io.py` | File I/O operations |
| `system.py` | System information |
| `archive.py` | Archive operations |
| `terminal.py` | Terminal utilities |
| `download.py` | File downloading |
| `platform.py` | Platform detection |

## Data Flow

### Project Creation Flow
User: tite new my-project
│
▼
CLI: parse arguments → route to new command
│
▼
Command: validate project name → create BootstrapManager
│
▼
BootstrapManager:
├── create_structure() → FileSystemManager
├── generate_files() → TemplateRenderer
├── create_venv() → EnvironmentManager
├── init_git() → GitManager
├── install_dependencies() → PackageInstaller
└── run_post_hooks()
│
▼
Output: "Project created successfully!"

text

### Development Server Flow
User: tite dev
│
▼
CLI: parse arguments → route to dev command
│
▼
DevServer:
├── load_config() → ConfigManager
├── start_process() → ProcessRunner
├── start_watcher() → FileWatcher
└── open_browser() → BrowserLauncher
│
▼
File change detected:
├── stop_process()
├── start_process()
└── log: "Reloading..."

text

## Design Patterns

### Factory Pattern
- `BootstrapManager` creates and configures all project components
- `ConfigManager` creates configuration from multiple sources

### Strategy Pattern
- Different mode implementations (Data, AI, Automation)
- Different template renderers

### Observer Pattern
- File watcher observes file system changes
- Event handlers respond to changes

### Builder Pattern
- `BlueprintBuilder` constructs projects from blueprints
- `BootstrapManager` constructs projects step by step

### Adapter Pattern
- `EnvironmentManager` adapts `VenvManager`
- `GitManager` adapts `GitRepository`
- `ConfigManager` adapts `BaseConfigManager`

### Command Pattern
- Each CLI command is a separate module
- Commands can be composed and chained

### Singleton Pattern
- `ModeRegistry` maintains single registry of modes
- `ConfigManager` manages single configuration instance

## Error Handling

Tite uses a hierarchical exception system:
TiteError
├── ProjectExistsError
├── InvalidProjectNameError
├── TemplateNotFoundError
├── ModeNotFoundError
├── EnvironmentError
├── ConfigurationError
├── DependencyError
├── FileOperationError
├── GitError
├── NetworkError
├── PermissionError
├── CommandNotFoundError
├── ValidationError
├── TemplateRenderError
└── StateError

text

## Configuration

Tite uses a layered configuration approach:

1. **Defaults** - Built-in default values
2. **Project Config** - `.tite/tite.toml` in the project
3. **Global Config** - `~/.tite/config.toml`
4. **Environment Variables** - `TITE_*` prefixed
5. **Command-line Arguments** - Highest precedence

## Extensibility

Tite is designed to be extensible through:

1. **Modes** - Domain-specific project templates
2. **Blueprints** - Reusable project definitions
3. **Plugins** - External extensions (planned)
4. **Templates** - Custom project templates

## Performance Considerations

- **Lazy Loading** - Modules loaded only when needed
- **Caching** - Configuration and template caching
- **Async Support** - For I/O operations
- **Parallel Processing** - For workflow steps

## Security

- **Input Validation** - All user inputs validated
- **Path Traversal Prevention** - Paths resolved safely
- **No Code Execution** - Templates don't execute code
- **Safe Defaults** - Sensible security defaults