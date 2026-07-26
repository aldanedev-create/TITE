
---

## `docs/development.md`

```markdown
# Development Guide

## Setup

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment (recommended)

### Getting Started

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


---

## `docs/development.md`

```markdown
# Development Guide

## Setup

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment (recommended)

### Getting Started

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

Running Tests
bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/tite --cov-report=html

# Run specific test
pytest tests/test_core/test_bootstrap.py -v

# Run with debug output
pytest -v --tb=short
Debugging
Logging
python
from tite.utils.logger import setup_logger

logger = setup_logger(level="DEBUG")
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
Interactive Debugging
python
# Set breakpoint
breakpoint()

# Use IPython debugger
import ipdb; ipdb.set_trace()
Verbose Output
bash
# Run with verbose output
tite --verbose new my-project

# Set environment variable
export TITE_VERBOSE=1
tite new my-project
Performance
Profiling
bash
# Run with profiler
python -m cProfile -o output.prof src/tite/cli/app.py new my-project

# Analyze profile
python -m pstats output.prof
Memory Profiling
bash
# Install memory profiler
pip install memory-profiler

# Run with memory profiling
python -m memory_profiler src/tite/cli/app.py new my-project
Release Process
1. Update Version
bash
# Update __init__.py
# Update pyproject.toml
2. Update Changelog
bash
# Update CHANGELOG.md
3. Build Package
bash
python scripts/build.py
4. Run Tests
bash
pytest
5. Create Release
bash
python scripts/release.py
Contributing Guidelines
Fork the repository

Create a feature branch

Write tests for your changes

Update documentation

Submit a pull request

See CONTRIBUTING.md for detailed guidelines.