# Tite Commands

## Overview

Tite provides a comprehensive set of commands for project creation, development, and maintenance. All commands follow a consistent pattern and support common options.

## Global Options

| Option | Description |
|--------|-------------|
| `--help, -h` | Show help message |
| `--version, -v` | Show version information |
| `--verbose` | Enable verbose output |
| `--no-color` | Disable colored output |

## Core Commands

### `tite new`

Create a new Python project.

```bash
tite new <project-name> [options]

Options:

Option	Description
--template, -t	Template to use (default: default)
--mode, -m	Mode to use (data, ai, automation, web, api, library, cli)
--path, -p	Path to create the project in
--force, -f	Force creation even if directory exists
--no-git	Skip Git initialization
--no-venv	Skip virtual environment creation
Examples:

bash
# Create a default project
tite new my-app

# Create with a specific mode
tite new sales-analysis --mode data

# Create with a specific template
tite new my-library --template library

# Create with custom path
tite new my-app --path ~/projects/

# Force creation
tite new my-app --force
tite dev
Start the development server with hot reload.

bash
tite dev [options]
Options:

Option	Description
--host	Host to bind to (default: 127.0.0.1)
--port, -p	Port to bind to (default: 8000)
--no-reload	Disable automatic reload
--command	Command to run (overrides config)
Examples:

bash
# Start development server
tite dev

# Start on specific port
tite dev --port 5000

# Start with custom command
tite dev --command "uvicorn src.main:app --reload"

# Disable auto-reload
tite dev --no-reload
tite doctor
Run health checks on the project.

bash
tite doctor [options]
Options:

Option	Description
--fix	Attempt to fix issues automatically
--check	Run a specific check only
--verbose, -v	Show detailed information
Checks:

Check	Description
python	Python version check
env	Virtual environment check
git	Git repository check
files	Project files check
deps	Dependencies check
config	Configuration check
Examples:

bash
# Run all checks
tite doctor

# Run specific check
tite doctor --check python

# Fix issues automatically
tite doctor --fix

# Verbose output
tite doctor --verbose
tite clean
Clean build artifacts and cache files.

bash
tite clean [options]
Options:

Option	Description
--dry-run	Show what would be cleaned
--all	Clean everything including venv
--type	Type of files to clean (cache, build, logs, all)
Examples:

bash
# Clean all
tite clean

# Dry run
tite clean --dry-run

# Clean only cache
tite clean --type cache

# Clean everything including venv
tite clean --all
tite info
Show project information.

bash
tite info [options]
Options:

Option	Description
--json	Output in JSON format
--section	Show a specific section
Sections:

Section	Description
project	Project metadata
env	Environment information
deps	Dependencies
git	Git status
config	Configuration
Examples:

bash
# Show all info
tite info

# Show specific section
tite info --section project

# JSON output
tite info --json
tite config
View or modify configuration.

bash
tite config [options]
Options:

Option	Description
--get	Get a configuration value
--set	Set a configuration value
--list	List all configuration
--reset	Reset to default
Examples:

bash
# List all config
tite config --list

# Get specific value
tite config --get project.name

# Set specific value
tite config --set dev.port 9000

# Reset to default
tite config --reset dev.port
tite env
Show environment details.

bash
tite env [options]
Options:

Option	Description
--json	Output in JSON format
--show-packages	Show installed packages
--show-vars	Show environment variables
Examples:

bash
# Show environment
tite env

# Show packages
tite env --show-packages

# Show all details
tite env --show-packages --show-vars

# JSON output
tite env --json
tite mode
Work with project modes.

bash
tite mode <mode> <project-name> [options]
Options:

Option	Description
--list	List available modes
--path, -p	Path to create the project in
--force, -f	Force creation
Available Modes:

Mode	Description
data	Data science project
ai	AI/ML project
automation	Automation project
web	Web application
api	REST API
library	Python library
cli	Command-line tool
Examples:

bash
# List modes
tite mode list

# Create data science project
tite mode data sales-analysis

# Create AI project
tite mode ai chatbot

# Create automation project
tite mode automation backup-tool

# Create web project
tite mode web my-website

# Create API project
tite mode api my-api
tite init
Initialize Tite in an existing project.

bash
tite init [options]
Options:

Option	Description
--path, -p	Path to the existing project
--force, -f	Force initialization
Examples:

bash
# Initialize current directory
tite init

# Initialize specific path
tite init --path ~/projects/my-project

# Force reinitialization
tite init --force
tite update
Update project dependencies.

bash
tite update [options]
Options:

Option	Description
--package, -p	Update a specific package
--major	Allow major version updates
--dry-run	Show what would be updated
Examples:

bash
# Update all dependencies
tite update

# Update specific package
tite update --package requests

# Allow major updates
tite update --major

# Dry run
tite update --dry-run
tite version
Show version information.

bash
tite version [options]
Options:

Option	Description
--short	Show only the version number
Examples:

bash
# Show full version info
tite version

# Show only version number
tite version --short
Command Aliases
Some commands have shorter aliases:

Command	Alias
tite new	tite n
tite dev	tite d
tite doctor	tite dr
tite info	tite i
tite config	tite c
tite env	tite e
tite version	tite v
Exit Codes
Code	Description
0	Success
1	General error
2	Invalid command
3	Invalid project name
4	Project exists
5	Template not found
6	Mode not found
7	Environment error
8	Configuration error
9	Dependency error
10	File operation error
11	Git error
12	Network error
13	Permission error