
---

## `docs/contributing.md`

```markdown
# Contributing to Tite

Thank you for considering contributing to Tite! 🎉

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Report Bugs

- **Use the issue tracker** to report bugs
- **Include details**: steps to reproduce, expected behavior, actual behavior
- **Include environment**: OS, Python version, Tite version

### Suggest Features

- **Use the issue tracker** for feature requests
- **Describe the feature** clearly
- **Explain the use case** for the feature
- **Consider implementation** approach

### Fix Bugs

- **Look for issues** labeled `bug` or `good first issue`
- **Comment** on the issue to claim it
- **Submit** a pull request with the fix

### Improve Documentation

- **Look for issues** labeled `documentation`
- **Update** docstrings, README, or docs
- **Add examples** where helpful

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment (recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/tite.git
cd tite

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

Code Style
bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/ tests/

# Security check
bandit -r src/
Testing
bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/tite --cov-report=html

# Run specific test
pytest tests/test_core/test_bootstrap.py -v
Pull Request Process
1. Create a Branch
bash
git checkout -b feature/your-feature-name
2. Make Changes
Follow the code style

Write tests for new features

Update documentation

Keep changes focused

3. Commit Changes
bash
git add .
git commit -m "feat: add your feature description"
4. Push Changes
bash
git push origin feature/your-feature-name
5. Create Pull Request
Open a pull request on GitHub with:

Description of the changes

Related issues (if any)

Testing performed

Screenshots (if UI changes)

6. Code Review
Address review comments

Make requested changes

Respond to feedback

7. Merge
Approval required from maintainer

CI checks must pass

Squash commits if needed

Commit Message Guidelines
Format
text
<type>(<scope>): <subject>

<body>

<footer>
Types
Type	Description
feat	New feature
fix	Bug fix
docs	Documentation changes
style	Code style changes
refactor	Code refactoring
perf	Performance improvements
test	Test changes
chore	Build or dependency changes
Examples
text
feat(core): add project bootstrap manager

Add BootstrapManager class for orchestrating project creation.
Includes directory creation, file generation, and post-hooks.

Closes #42
text
fix(cli): handle empty project name in new command

Validate project name before creation and show error message.

Fixes #17
Documentation Guidelines
Docstrings
Use Google-style docstrings:

python
def example_function(param1: str, param2: int = 0) -> bool:
    """
    Example function description.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)

    Returns:
        bool: Description of return value

    Raises:
        ValueError: If param1 is empty
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    return param2 > 0
Markdown
Use ATX headings (#, ##, ###)

Use code blocks with language tags

Use lists for related items

Use tables for structured data

Community
Communication Channels
GitHub Issues: For bugs and feature requests

GitHub Discussions: For questions and discussions

Discord: For real-time chat

Maintainers
Project Lead: @yourusername

Recognition
Contributors will be recognized in:

README.md: Contributors list

CHANGELOG.md: Release notes

GitHub: All contributors visible

Thank you for contributing to Tite! 🚀