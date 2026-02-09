"""
Chemical Equipment Parameter Visualizer - Desktop Application
Main entry point for the PyQt5 desktop application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from ui.main_window import MainWindow


def set_dark_theme(app):
    """Apply a dark theme to the application."""
    palette = QPalette()
    
    # Dark colors
    palette.setColor(QPalette.Window, QColor(15, 23, 42))
    palette.setColor(QPalette.WindowText, QColor(241, 245, 249))
    palette.setColor(QPalette.Base, QColor(30, 41, 59))
    palette.setColor(QPalette.AlternateBase, QColor(51, 65, 85))
    palette.setColor(QPalette.ToolTipBase, QColor(30, 41, 59))
    palette.setColor(QPalette.ToolTipText, QColor(241, 245, 249))
    palette.setColor(QPalette.Text, QColor(241, 245, 249))
    palette.setColor(QPalette.Button, QColor(30, 41, 59))
    palette.setColor(QPalette.ButtonText, QColor(241, 245, 249))
    palette.setColor(QPalette.BrightText, QColor(59, 130, 246))
    palette.setColor(QPalette.Link, QColor(59, 130, 246))
    palette.setColor(QPalette.Highlight, QColor(59, 130, 246))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    # Set stylesheet for more detailed styling
    app.setStyleSheet("""
        QMainWindow {
            background-color: #0f172a;
        }
        QTabWidget::pane {
            border: 1px solid #334155;
            border-radius: 8px;
            background-color: #1e293b;
        }
        QTabBar::tab {
            background-color: #1e293b;
            color: #94a3b8;
            padding: 12px 24px;
            margin-right: 4px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        QTabBar::tab:selected {
            background-color: #3b82f6;
            color: white;
        }
        QTabBar::tab:hover:!selected {
            background-color: #334155;
        }
        QPushButton {
            background-color: #3b82f6;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2563eb;
        }
        QPushButton:disabled {
            background-color: #475569;
            color: #94a3b8;
        }
        QPushButton#secondaryBtn {
            background-color: #334155;
            border: 1px solid #475569;
        }
        QPushButton#secondaryBtn:hover {
            background-color: #475569;
        }
        QPushButton#successBtn {
            background-color: #10b981;
        }
        QPushButton#successBtn:hover {
            background-color: #059669;
        }
        QLineEdit {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 10px;
            color: #f1f5f9;
        }
        QLineEdit:focus {
            border-color: #3b82f6;
        }
        QTableWidget {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            gridline-color: #334155;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QTableWidget::item:selected {
            background-color: #3b82f6;
        }
        QHeaderView::section {
            background-color: #334155;
            color: #f1f5f9;
            padding: 10px;
            border: none;
            font-weight: bold;
        }
        QLabel {
            color: #f1f5f9;
        }
        QLabel#subtitle {
            color: #94a3b8;
        }
        QLabel#statValue {
            font-size: 24px;
            font-weight: bold;
            color: #3b82f6;
        }
        QLabel#statLabel {
            color: #94a3b8;
            font-size: 12px;
        }
        QGroupBox {
            border: 1px solid #334155;
            border-radius: 8px;
            margin-top: 16px;
            padding: 16px;
            background-color: #1e293b;
        }
        QGroupBox::title {
            color: #f1f5f9;
            font-weight: bold;
            subcontrol-origin: margin;
            left: 16px;
            padding: 0 8px;
        }
        QListWidget {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
        }
        QListWidget::item {
            padding: 12px;
            border-bottom: 1px solid #334155;
        }
        QListWidget::item:selected {
            background-color: #3b82f6;
        }
        QListWidget::item:hover:!selected {
            background-color: #334155;
        }
        QScrollBar:vertical {
            background-color: #1e293b;
            width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background-color: #475569;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #64748b;
        }
    """)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setApplicationDisplayName("Chemical Equipment Visualizer")
    
    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Apply dark theme
    set_dark_theme(app)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
