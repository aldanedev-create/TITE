
---

## `docs/configuration.md`

```markdown
# Tite Configuration

## Overview

Tite uses a layered configuration system that allows you to customize behavior at multiple levels. Configuration can be set via defaults, project files, global files, environment variables, and command-line arguments.

## Configuration Hierarchy

1. **Command-line arguments** (highest precedence)
2. **Environment variables** (`TITE_*`)
3. **Project configuration** (`.tite/tite.toml`)
4. **Global configuration** (`~/.tite/config.toml`)
5. **Default configuration** (built-in)

## Configuration Files

### Project Configuration

Location: `.tite/tite.toml` (in project root)

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A Python project"
python_version = ">=3.9"
license = "MIT"
author = "John Doe"
email = "john@example.com"

[dev]
command = "python src/main.py"
port = 8000
host = "127.0.0.1"
env_file = ".env"
env_prefix = "APP_"
reload = true
debug = false

[watcher]
paths = ["src", "tests"]
extensions = [".py", ".html", ".css", ".js"]
ignore = [".venv", "__pycache__", "*.egg-info"]
debounce = 100
restart_on_change = true

[clean]
include = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "build",
    "dist",
    "*.egg-info",
    "*.pyc",
    "*.pyo",
]
exclude = [".venv", "venv"]

[git]
init = true
branch = "main"
remote_url = "https://github.com/user/repo.git"
ignore_patterns = [
    ".venv",
    "__pycache__",
    "*.pyc",
    ".env",
    "dist",
    "build",
    "*.egg-info",
]

[testing]
runner = "pytest"
arguments = ["-v", "--cov=src", "--cov-report=html"]
test_path = "tests"
coverage_threshold = 80

[packaging]
build_backend = "hatchling"
include_package_data = true
package_name = "my_project"
package_version = "0.1.0"

[docs]
builder = "sphinx"
source_dir = "docs"
build_dir = "docs/_build"
format = "html"
theme = "sphinx_rtd_theme"

[logging]
level = "INFO"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
file = "logs/app.log"
console = true
rotation = "1 day"
retention = "30 days"
compression = "gz"

[database]
enabled = false
engine = "sqlite"
url = "sqlite:///app.db"
pool_size = 5
max_overflow = 10
echo = false

[api]
prefix = "/api/v1"
cors_enabled = true
cors_origins = ["*"]
rate_limit_enabled = false
rate_limit = "100/hour"
docs_enabled = true
docs_url = "/docs"
redoc_url = "/redoc"

[security]
csrf_protection = true
session_secure = false
rate_limit = "100/hour"
password_min_length = 8
allowed_hosts = ["localhost", "127.0.0.1"]

[deployment]
platform = "auto"
environments = ["development", "staging", "production"]
health_check_path = "/health"
metrics_enabled = true

Global Configuration
Location: ~/.tite/config.toml

toml
# Global Tite configuration

[defaults]
# Default values for new projects
license = "MIT"
python_version = ">=3.9"
git_init = true

[user]
name = "John Doe"
email = "john@example.com"
github_username = "johndoe"

[paths]
projects_dir = "~/projects"
templates_dir = "~/.tite/templates"

[telemetry]
enabled = false
anonymous = true

[updates]
check = true
auto_install = false
Environment Variables
Tite recognizes the following environment variables:

Variable	Description
TITE_DEBUG	Enable debug mode
TITE_LOG_LEVEL	Set log level (DEBUG, INFO, WARNING, ERROR)
TITE_NO_COLOR	Disable colored output
TITE_VERBOSE	Enable verbose output
TITE_PROJECTS_DIR	Default projects directory
TITE_USER_NAME	User name for projects
TITE_USER_EMAIL	User email for projects
TITE_GITHUB_USERNAME	GitHub username
TITE_TEMPLATES_DIR	Custom templates directory
TITE_NO_ANALYTICS	Disable analytics
Nested Configuration
Configuration keys can be accessed using dot notation:

bash
# Get a nested value
tite config --get project.name

# Set a nested value
tite config --set dev.port 9000
Configuration Schema
Project Section
Field	Type	Default	Description
name	string	-	Project name (required)
version	string	0.1.0	Project version
description	string	-	Project description
python_version	string	>=3.9	Python version requirement
license	string	MIT	Project license
author	string	-	Project author
email	string	-	Author email
Dev Section
Field	Type	Default	Description
command	string	python src/main.py	Development command
port	integer	8000	Development port
host	string	127.0.0.1	Development host
env_file	string	.env	Environment file
env_prefix	string	APP_	Environment prefix
reload	boolean	true	Enable auto-reload
debug	boolean	false	Enable debug mode
Watcher Section
Field	Type	Default	Description
paths	array	["src", "tests"]	Watch paths
extensions	array	[".py", ".html", ".css", ".js"]	Watch extensions
ignore	array	[".venv", "__pycache__"]	Ignore patterns
debounce	integer	100	Debounce in milliseconds
restart_on_change	boolean	true	Restart on change
Clean Section
Field	Type	Default	Description
include	array	Built-in patterns	Clean patterns
exclude	array	[".venv"]	Exclude patterns
Git Section
Field	Type	Default	Description
init	boolean	true	Initialize Git
branch	string	main	Default branch
remote_url	string	-	Remote URL
ignore_patterns	array	Built-in patterns	Git ignore patterns
Testing Section
Field	Type	Default	Description
runner	string	pytest	Test runner
arguments	array	["-v"]	Test arguments
test_path	string	tests	Test directory
coverage_threshold	integer	80	Coverage threshold
Custom Configuration
You can extend the configuration with custom sections:

toml
[custom]
my_setting = "value"
my_nested = { key = "value" }

[custom.subsection]
another = "setting"
These custom values can be accessed with:

bash
tite config --get custom.my_setting
Validation
Tite validates configuration on load. Common validation rules:

Required fields must be present

Port numbers must be valid (1-65535)

Python version must be valid

Email addresses must be valid

URLs must be valid

Example Configurations
Web Project
toml
[project]
name = "my-web-app"
description = "A web application"

[dev]
command = "uvicorn src.main:app --reload"
port = 8000

[watcher]
extensions = [".py", ".html", ".css", ".js", ".json"]

[api]
prefix = "/api/v1"
cors_enabled = true
Data Science Project
toml
[project]
name = "data-analysis"
description = "Data analysis project"

[dev]
command = "jupyter notebook"

[database]
enabled = true
engine = "sqlite"
url = "sqlite:///data.db"

[testing]
coverage_threshold = 70
API Project
toml
[project]
name = "my-api"
description = "REST API"

[dev]
command = "uvicorn src.main:app --reload --host 0.0.0.0"

[api]
prefix = "/api/v1"
rate_limit_enabled = true
rate_limit = "1000/hour"

[security]
csrf_protection = false
rate_limit = "1000/hour"
Troubleshooting
Configuration Not Loading
Check file path: .tite/tite.toml must be in project root

Check file syntax: TOML must be valid

Check permissions: File must be readable

Environment Variables Not Working
Ensure variables are prefixed with TITE_

Use double underscore for nested keys: TITE_DEV__PORT

Values are parsed: true/false become booleans

Defaults Not Applied
Check if configuration file exists

Check if values are explicitly set to different values

Command-line arguments override everything