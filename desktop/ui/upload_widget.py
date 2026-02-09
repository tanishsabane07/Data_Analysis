"""
CSV Upload Widget for the Desktop App.
"""

import os
import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QGroupBox, QMessageBox,
    QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSignal


class UploadWidget(QWidget):
    upload_success = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.token = None
        self.init_ui()
    
    def set_token(self, token):
        self.token = token
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Upload area
        upload_group = QGroupBox("📤 Upload CSV File")
        upload_layout = QVBoxLayout(upload_group)
        upload_layout.setSpacing(16)
        upload_layout.setAlignment(Qt.AlignCenter)
        
        # Drop zone visual
        drop_zone = QWidget()
        drop_zone.setStyleSheet("""
            QWidget {
                border: 2px dashed #475569;
                border-radius: 12px;
                background-color: rgba(59, 130, 246, 0.02);
                padding: 40px;
            }
        """)
        drop_layout = QVBoxLayout(drop_zone)
        drop_layout.setAlignment(Qt.AlignCenter)
        
        # Icon
        icon = QLabel("📁")
        icon.setStyleSheet("font-size: 64px;")
        icon.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(icon)
        
        # Text
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("font-size: 16px; color: #94a3b8;")
        self.file_label.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(self.file_label)
        
        hint = QLabel("Click 'Browse' to select a CSV file")
        hint.setStyleSheet("font-size: 12px; color: #64748b;")
        hint.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(hint)
        
        upload_layout.addWidget(drop_zone)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self.browse_btn = QPushButton("📂 Browse")
        self.browse_btn.setObjectName("secondaryBtn")
        self.browse_btn.clicked.connect(self.browse_file)
        btn_layout.addWidget(self.browse_btn)
        
        self.upload_btn = QPushButton("🚀 Upload & Analyze")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        btn_layout.addWidget(self.upload_btn)
        
        upload_layout.addLayout(btn_layout)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #334155;
                height: 8px;
            }
            QProgressBar::chunk {
                background-color: #3b82f6;
                border-radius: 4px;
            }
        """)
        upload_layout.addWidget(self.progress)
        
        layout.addWidget(upload_group)
        
        # Format info
        info_group = QGroupBox("📋 Expected CSV Format")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel(
            "Your CSV file should contain the following columns:\n\n"
            "Equipment Name, Type, Flowrate, Pressure, Temperature"
        )
        info_text.setStyleSheet("color: #94a3b8; font-size: 14px;")
        info_layout.addWidget(info_text)
        
        example = QLabel("Example: Pump-1, Pump, 120, 5.2, 110")
        example.setStyleSheet("""
            background-color: #334155;
            padding: 12px;
            border-radius: 6px;
            color: #06b6d4;
            font-family: monospace;
        """)
        info_layout.addWidget(example)
        
        layout.addWidget(info_group)
        
        # Spacer
        layout.addStretch()
    
    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.setText(f"Selected: {os.path.basename(filename)}")
            self.file_label.setStyleSheet("font-size: 16px; color: #10b981; font-weight: bold;")
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        if not self.selected_file:
            return
        
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.upload_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        
        try:
            headers = {}
            if self.token:
                headers['Authorization'] = f'Token {self.token}'
            
            with open(self.selected_file, 'rb') as f:
                files = {'file': (os.path.basename(self.selected_file), f, 'text/csv')}
                
                self.progress.setValue(30)
                
                response = requests.post(
                    'http://localhost:8000/api/upload/',
                    files=files,
                    headers=headers
                )
                
                self.progress.setValue(80)
                
                if response.status_code == 201:
                    self.progress.setValue(100)
                    data = response.json()
                    
                    QMessageBox.information(
                        self, 
                        "Success", 
                        f"Successfully uploaded!\nFound {data.get('total_count', 0)} equipment records."
                    )
                    
                    # Reset UI
                    self.selected_file = None
                    self.file_label.setText("No file selected")
                    self.file_label.setStyleSheet("font-size: 16px; color: #94a3b8;")
                    
                    # Emit signal with data
                    self.upload_success.emit(data)
                else:
                    error_msg = response.json().get('error', 'Upload failed')
                    QMessageBox.warning(self, "Error", error_msg)
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self, 
                "Connection Error", 
                "Cannot connect to the server.\nMake sure the Django backend is running on http://localhost:8000"
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        
        finally:
            self.progress.setVisible(False)
            self.upload_btn.setEnabled(bool(self.selected_file))
            self.browse_btn.setEnabled(True)
