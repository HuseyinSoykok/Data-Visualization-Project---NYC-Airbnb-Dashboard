"""
NYC Airbnb Dashboard - Modern PySide6 Application
Professional Desktop UI with Modern Design Patterns
"""

import sys
import os

# Add qt_app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import QFont, QFontDatabase, QIcon

from core.main_window import MainWindow
from core.theme_manager import ThemeManager


def load_fonts():
    """Load custom fonts for the application"""
    font_paths = [
        ":/fonts/Inter-Regular.ttf",
        ":/fonts/Inter-Medium.ttf",
        ":/fonts/Inter-Bold.ttf",
    ]
    for path in font_paths:
        QFontDatabase.addApplicationFont(path)


def main():
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("NYC Airbnb Dashboard")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Data Visualization Project")
    
    # Set default font
    font = QFont("Segoe UI", 10)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)
    
    # Initialize theme manager
    theme_manager = ThemeManager()
    
    # Load and apply stylesheet
    theme_manager.apply_theme(app, "dark")
    
    # Create and show main window
    window = MainWindow(theme_manager)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
