"""
Main entry point for the desktop application.

This module provides the entry point for the desktop application
using PySide6, PyQt6, or Tkinter.
"""

import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/desktop.log", mode="a", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)

# Try to import PySide6 first, fallback to PyQt6, then Tkinter
try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    FRAMEWORK = "pyside6"
    HAS_QT = True
except ImportError:
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        FRAMEWORK = "pyqt6"
        HAS_QT = True
    except ImportError:
        import tkinter as tk
        FRAMEWORK = "tkinter"
        HAS_QT = False

from src.app import Application
from src.ui.window import MainWindow


def main() -> int:
    """
    Main entry point for the desktop application.
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    logger.info(f"Starting {{ project_name }} desktop application...")
    logger.info(f"Framework: {FRAMEWORK}")
    
    try:
        if HAS_QT:
            return run_qt_app()
        else:
            return run_tkinter_app()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        return 1


def run_qt_app() -> int:
    """Run the Qt application."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("{{ project_name }}")
    app.setOrganizationName("{{ author_name }}")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    return app.exec()


def run_tkinter_app() -> int:
    """Run the Tkinter application."""
    # Create root window
    root = tk.Tk()
    root.title("{{ project_name }}")
    root.geometry("800x600")
    
    # Create application
    app = Application(root)
    
    # Run application
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())