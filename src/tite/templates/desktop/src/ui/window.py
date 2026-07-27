"""
Main window for the desktop application.

This module provides the main window UI for the application
using PySide6, PyQt6, or Tkinter.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import Qt first
try:
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QMenuBar, QMenu, QStatusBar,
        QToolBar, QMessageBox
    )
    from PySide6.QtCore import Qt, QSize
    from PySide6.QtGui import QAction, QIcon, QFont
    HAS_QT = True
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QLabel, QPushButton, QMenuBar, QMenu, QStatusBar,
            QToolBar, QMessageBox
        )
        from PyQt6.QtCore import Qt, QSize
        from PyQt6.QtGui import QAction, QIcon, QFont
        HAS_QT = True
    except ImportError:
        import tkinter as tk
        from tkinter import ttk, messagebox
        HAS_QT = False


if HAS_QT:
    class MainWindow(QMainWindow):
        """
        Main window for the Qt application.
        """
        
        def __init__(self):
            """
            Initialize the main window.
            """
            super().__init__()
            
            # Set window properties
            self.setWindowTitle("{{ project_name }}")
            self.setMinimumSize(800, 600)
            
            # Setup UI
            self._setup_menu()
            self._setup_toolbar()
            self._setup_central_widget()
            self._setup_status_bar()
            
            # Apply theme
            self._apply_theme()
            
            logger.info("Main window initialized")
        
        def _setup_menu(self) -> None:
            """Setup the menu bar."""
            menubar = self.menuBar()
            
            # File menu
            file_menu = menubar.addMenu("&File")
            
            new_action = QAction("&New", self)
            new_action.setShortcut("Ctrl+N")
            new_action.triggered.connect(self._on_new)
            file_menu.addAction(new_action)
            
            open_action = QAction("&Open...", self)
            open_action.setShortcut("Ctrl+O")
            open_action.triggered.connect(self._on_open)
            file_menu.addAction(open_action)
            
            file_menu.addSeparator()
            
            exit_action = QAction("E&xit", self)
            exit_action.setShortcut("Ctrl+Q")
            exit_action.triggered.connect(self.close)
            file_menu.addAction(exit_action)
            
            # Edit menu
            edit_menu = menubar.addMenu("&Edit")
            
            preferences_action = QAction("&Preferences", self)
            preferences_action.triggered.connect(self._on_preferences)
            edit_menu.addAction(preferences_action)
            
            # Help menu
            help_menu = menubar.addMenu("&Help")
            
            about_action = QAction("&About", self)
            about_action.triggered.connect(self._on_about)
            help_menu.addAction(about_action)
        
        def _setup_toolbar(self) -> None:
            """Setup the toolbar."""
            toolbar = QToolBar()
            toolbar.setMovable(False)
            self.addToolBar(toolbar)
            
            # Add actions to toolbar
            new_action = QAction("New", self)
            new_action.triggered.connect(self._on_new)
            toolbar.addAction(new_action)
            
            open_action = QAction("Open", self)
            open_action.triggered.connect(self._on_open)
            toolbar.addAction(open_action)
        
        def _setup_central_widget(self) -> None:
            """Setup the central widget."""
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            layout = QVBoxLayout(central_widget)
            layout.setSpacing(10)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Header
            header_label = QLabel("Welcome to {{ project_name }}!")
            header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_font = QFont()
            header_font.setPointSize(24)
            header_font.setBold(True)
            header_label.setFont(header_font)
            layout.addWidget(header_label)
            
            # Description
            desc_label = QLabel("{{ project_description }}")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
            
            layout.addStretch()
            
            # Buttons
            button_layout = QHBoxLayout()
            button_layout.setSpacing(10)
            
            action_btn = QPushButton("Action")
            action_btn.clicked.connect(self._on_action)
            button_layout.addWidget(action_btn)
            
            quit_btn = QPushButton("Quit")
            quit_btn.clicked.connect(self.close)
            button_layout.addWidget(quit_btn)
            
            button_layout.addStretch()
            layout.addLayout(button_layout)
        
        def _setup_status_bar(self) -> None:
            """Setup the status bar."""
            status_bar = QStatusBar()
            self.setStatusBar(status_bar)
            status_bar.showMessage("Ready")
        
        def _apply_theme(self) -> None:
            """Apply the application theme."""
            # Dark theme
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1a1a2e;
                }
                QWidget {
                    background-color: #1a1a2e;
                    color: #e2e8f0;
                }
                QPushButton {
                    background-color: #6366f1;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4f46e5;
                }
                QPushButton:pressed {
                    background-color: #4338ca;
                }
                QLabel {
                    color: #e2e8f0;
                }
                QMenuBar {
                    background-color: #1a1a2e;
                    color: #e2e8f0;
                }
                QMenuBar::item:selected {
                    background-color: #2d2d5e;
                }
                QMenu {
                    background-color: #1a1a2e;
                    color: #e2e8f0;
                    border: 1px solid #2d2d5e;
                }
                QMenu::item:selected {
                    background-color: #2d2d5e;
                }
                QToolBar {
                    background-color: #1a1a2e;
                    border: none;
                    spacing: 5px;
                }
                QStatusBar {
                    background-color: #1a1a2e;
                    color: #94a3b8;
                }
            """)
        
        def _on_new(self) -> None:
            """Handle New action."""
            QMessageBox.information(self, "New", "New action triggered!")
        
        def _on_open(self) -> None:
            """Handle Open action."""
            QMessageBox.information(self, "Open", "Open action triggered!")
        
        def _on_preferences(self) -> None:
            """Handle Preferences action."""
            QMessageBox.information(self, "Preferences", "Preferences dialog would open here.")
        
        def _on_about(self) -> None:
            """Handle About action."""
            QMessageBox.about(
                self,
                "About {{ project_name }}",
                f"""
                <h2>{{ project_name }}</h2>
                <p>{{ project_description }}</p>
                <p>Version: 0.1.0</p>
                <p>Framework: PySide6</p>
                <p>Built with ❤️ using Tite</p>
                """
            )
        
        def _on_action(self) -> None:
            """Handle Action button click."""
            QMessageBox.information(self, "Action", "Action triggered!")

else:
    class MainWindow:
        """
        Main window for the Tkinter application.
        """
        
        def __init__(self, root):
            """
            Initialize the main window.
            
            Args:
                root: Tkinter root window
            """
            self.root = root
            
            # Setup UI
            self._setup_menu()
            self._setup_ui()
            
            logger.info("Main window initialized")
        
        def _setup_menu(self) -> None:
            """Setup the menu bar."""
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)
            
            # File menu
            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="New", command=self._on_new)
            file_menu.add_command(label="Open", command=self._on_open)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.root.quit)
            
            # Help menu
            help_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Help", menu=help_menu)
            help_menu.add_command(label="About", command=self._on_about)
        
        def _setup_ui(self) -> None:
            """Setup the user interface."""
            # Main frame
            main_frame = ttk.Frame(self.root, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Header
            header_label = ttk.Label(
                main_frame,
                text="Welcome to {{ project_name }}!",
                font=("Arial", 24, "bold")
            )
            header_label.pack(pady=10)
            
            # Description
            desc_label = ttk.Label(
                main_frame,
                text="{{ project_description }}",
                wraplength=500,
                justify=tk.CENTER
            )
            desc_label.pack(pady=10)
            
            # Button frame
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(pady=20)
            
            action_btn = ttk.Button(
                button_frame,
                text="Action",
                command=self._on_action
            )
            action_btn.pack(side=tk.LEFT, padx=5)
            
            quit_btn = ttk.Button(
                button_frame,
                text="Quit",
                command=self.root.quit
            )
            quit_btn.pack(side=tk.LEFT, padx=5)
            
            # Status bar
            status_bar = ttk.Label(
                self.root,
                text="Ready",
                relief=tk.SUNKEN,
                anchor=tk.W
            )
            status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        def _on_new(self) -> None:
            """Handle New action."""
            messagebox.showinfo("New", "New action triggered!")
        
        def _on_open(self) -> None:
            """Handle Open action."""
            messagebox.showinfo("Open", "Open action triggered!")
        
        def _on_about(self) -> None:
            """Handle About action."""
            messagebox.showinfo(
                "About {{ project_name }}",
                f"{{ project_name }}\n\n"
                f"{{ project_description }}\n\n"
                f"Version: 0.1.0\n"
                f"Framework: Tkinter\n"
                f"Built with ❤️ using Tite"
            )
        
        def _on_action(self) -> None:
            """Handle Action button click."""
            messagebox.showinfo("Action", "Action triggered!")