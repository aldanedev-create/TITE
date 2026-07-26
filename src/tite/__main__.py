"""
Main entry point for Tite when run as a module.

This allows Tite to be run using:
    python -m tite
"""

import sys

from tite.cli.app import main

if __name__ == "__main__":
    sys.exit(main())