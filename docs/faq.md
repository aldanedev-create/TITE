
---

## `docs/faq.md`

```markdown
# Frequently Asked Questions

## General

### What is Tite?

Tite is a zero-configuration Python project bootstrapper. It automates project initialization, creating a production-ready development environment in seconds, regardless of the libraries or frameworks you choose.

### Why was Tite created?

Python developers often perform repetitive configuration tasks before starting a new project. Unlike JavaScript's Vite, Python lacks a unified tool that focuses exclusively on minimizing configuration while remaining framework-independent. Tite fills this gap.

### Is Tite a framework?

No. Tite is not a framework. It doesn't dictate how you build your application. It simply prepares a clean, professional Python workspace so you can start building immediately.

### What's the difference between Tite and Poetry/Pipenv?

- **Poetry/Pipenv**: Dependency management and packaging
- **Tite**: Project initialization and development workflow

Tite works alongside Poetry or Pipenv, not as a replacement.

## Installation

### How do I install Tite?

```bash
pip install tite

What Python versions are supported?
Tite supports Python 3.9 and above.

Can I install Tite globally?
Yes, you can install Tite globally using pip. However, we recommend using a virtual environment to avoid conflicts.

Does Tite work on Windows/Mac/Linux?
Yes, Tite is cross-platform and works on Windows, macOS, and Linux.

Usage
How do I create a new project?
bash
tite new my-project
How do I start the development server?
bash
cd my-project
tite dev
How do I check project health?
bash
tite doctor
What modes are available?
data - Data science projects

ai - AI/ML projects

automation - Automation projects

web - Web applications

api - REST APIs

library - Python libraries

cli - Command-line tools

How do I use a mode?
bash
tite mode data sales-analysis
Can I customize the project structure?
Yes, you can customize the project structure using templates or the blueprint system.

Configuration
Where is the configuration file?
Project configuration is in .tite/tite.toml in the project root.

How do I change the default Python version?
toml
[project]
python_version = ">=3.10"
How do I change the development port?
toml
[dev]
port = 5000
Can I use environment variables?
Yes, Tite supports .env files and environment variables with the APP_ prefix.

Templates
What templates are available?
default - Standard Python project

web - Web application

api - REST API

library - Python library

cli - Command-line tool

Can I create custom templates?
Yes, you can create custom templates using the blueprint system or by placing templates in ~/.tite/templates/.

How do I use a template?
bash
tite new my-project --template web
Modes
What are modes?
Modes are pre-configured project setups for specific use cases (data science, AI, automation, etc.).

Can I create custom modes?
Yes, you can create custom modes using the plugin system or by defining modes in configuration.

How do I list available modes?
bash
tite mode list
Development
How does hot reload work?
Tite watches your source files for changes. When a change is detected, the development server automatically restarts, providing instant feedback.

Can I disable hot reload?
Yes, use the --no-reload flag:

bash
tite dev --no-reload
Can I use a different command for dev?
Yes, use the --command flag or configure it in tite.toml:

bash
tite dev --command "uvicorn src.main:app --reload"
Troubleshooting
"Command not found" error
Make sure Tite is installed and in your PATH:

bash
which tite
"Project already exists" error
Use --force to overwrite:

bash
tite new my-project --force
"Virtual environment not found" error
Create a virtual environment:

bash
python -m venv .venv
"Git not found" error
Make sure Git is installed and in your PATH.

"Python version not supported" error
Tite requires Python 3.9 or higher. Check your Python version:

bash
python --version
Performance
Is Tite fast?
Yes, Tite is designed to be fast. Project creation typically takes 1-2 seconds.

Does Tite cache anything?
Yes, Tite caches configuration and template data to improve performance.

How much memory does Tite use?
Tite uses approximately 50-100 MB of memory during normal operation.

Security
Is Tite secure?
Tite follows security best practices:

All inputs are validated

No remote code execution

Safe default configurations

No telemetry by default

Does Tite collect telemetry?
No, Tite does not collect any telemetry by default. You can opt-in to anonymous usage statistics.

Are my secrets safe?
Tite does not store or transmit any sensitive information. Environment variables are stored locally in .env files.

Integration
Can I use Tite with Docker?
Yes, Tite can generate Dockerfiles and Docker Compose configurations.

Can I use Tite with CI/CD?
Yes, Tite works with GitHub Actions, GitLab CI, Jenkins, and other CI/CD systems.

Can I use Tite with VS Code?
Yes, Tite generates .vscode settings for better integration.

Can I use Tite with PyCharm?
Yes, Tite generates .idea settings for better integration.

Contributing
How can I contribute?
Report bugs

Suggest features

Fix issues

Improve documentation

Write tests

How do I set up development?
bash
git clone https://github.com/yourusername/tite.git
cd tite
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
What's the code style?
Tite follows PEP 8 with Black formatting (88-character line length).

Future
What's planned for Tite?
See the roadmap for detailed plans.

Will Tite support other languages?
Tite is focused on Python. However, the architecture is flexible enough to support other languages in the future.

When is the next release?
Check the milestones for release dates.

Support
Where can I get help?
Documentation: tite.readthedocs.io

Issues: GitHub Issues

Discussions: GitHub Discussions

Is commercial support available?
Yes, commercial support is available for enterprise customers. Contact us for details.

Can I sponsor the project?
Yes, sponsorship is welcome! See the GitHub Sponsors page.

Still have questions? Open a discussion on GitHub.