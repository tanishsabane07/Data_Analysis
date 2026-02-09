"""
Authentication Dialog for the Desktop App.
"""

import requests
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTabWidget, QWidget,
    QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt


class AuthDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user = None
        self.token = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("🔐 Authentication")
        self.setMinimumSize(400, 350)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("🔐 Login / Register")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f1f5f9;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tab widget for Login/Register
        self.tabs = QTabWidget()
        
        # Login tab
        login_widget = QWidget()
        login_layout = QFormLayout(login_widget)
        login_layout.setSpacing(12)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter username")
        login_layout.addRow("Username:", self.login_username)
        
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText("Enter password")
        login_layout.addRow("Password:", self.login_password)
        
        login_btn = QPushButton("🚀 Login")
        login_btn.clicked.connect(self.do_login)
        login_layout.addRow("", login_btn)
        
        self.tabs.addTab(login_widget, "Login")
        
        # Register tab
        register_widget = QWidget()
        register_layout = QFormLayout(register_widget)
        register_layout.setSpacing(12)
        
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Choose username")
        register_layout.addRow("Username:", self.reg_username)
        
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Enter email (optional)")
        register_layout.addRow("Email:", self.reg_email)
        
        self.reg_password = QLineEdit()
        self.reg_password.setEchoMode(QLineEdit.Password)
        self.reg_password.setPlaceholderText("Choose password (min 6 chars)")
        register_layout.addRow("Password:", self.reg_password)
        
        register_btn = QPushButton("✨ Create Account")
        register_btn.clicked.connect(self.do_register)
        register_layout.addRow("", register_btn)
        
        self.tabs.addTab(register_widget, "Register")
        
        layout.addWidget(self.tabs)
        
        # Info
        info = QLabel("💡 Login is optional. Without login, your history is shared with anonymous users.")
        info.setStyleSheet("color: #64748b; font-size: 11px;")
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondaryBtn")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
    
    def do_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        try:
            response = requests.post(
                'http://localhost:8000/api/auth/login/',
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.user = data.get('user')
                self.token = data.get('token')
                QMessageBox.information(self, "Success", f"Welcome back, {username}!")
                self.accept()
            else:
                error = response.json().get('error', 'Login failed')
                QMessageBox.warning(self, "Error", error)
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Error", "Cannot connect to server")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def do_register(self):
        username = self.reg_username.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return
        
        try:
            response = requests.post(
                'http://localhost:8000/api/auth/register/',
                json={'username': username, 'email': email, 'password': password}
            )
            
            if response.status_code == 201:
                data = response.json()
                self.user = data.get('user')
                self.token = data.get('token')
                QMessageBox.information(self, "Success", f"Account created! Welcome, {username}!")
                self.accept()
            else:
                errors = response.json()
                error_msg = errors.get('username', [errors.get('error', ['Registration failed'])])[0]
                QMessageBox.warning(self, "Error", str(error_msg))
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Error", "Cannot connect to server")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
