"""
History Widget for the Desktop App.
"""

import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QListWidgetItem, QMessageBox,
    QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal


class HistoryWidget(QWidget):
    dataset_selected = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.token = None
        self.datasets = []
        self.init_ui()
    
    def set_token(self, token):
        self.token = token
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📁 Upload History")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("secondaryBtn")
        refresh_btn.clicked.connect(self.refresh)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # List
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        # Info
        info = QLabel("💡 The system keeps the last 5 uploaded datasets. Double-click to view dashboard.")
        info.setStyleSheet("color: #64748b; font-size: 12px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
    
    def refresh(self):
        try:
            headers = {}
            if self.token:
                headers['Authorization'] = f'Token {self.token}'
            
            response = requests.get(
                'http://localhost:8000/api/history/',
                headers=headers
            )
            
            if response.status_code == 200:
                self.datasets = response.json()
                self.update_list()
        except requests.exceptions.ConnectionError:
            QMessageBox.warning(
                self, 
                "Connection Error", 
                "Cannot connect to the server. Make sure the backend is running."
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def update_list(self):
        self.list_widget.clear()
        
        if not self.datasets:
            item = QListWidgetItem("No uploads yet. Upload a CSV file to get started!")
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self.list_widget.addItem(item)
            return
        
        for i, dataset in enumerate(self.datasets):
            # Create formatted text
            filename = dataset.get('filename', 'Unknown')
            uploaded_at = dataset.get('uploaded_at', '')[:19].replace('T', ' ')
            total_count = dataset.get('total_count', 0)
            avg_flow = dataset.get('avg_flowrate', 0)
            
            text = f"{'⭐ ' if i == 0 else ''}{filename}\n"
            text += f"Uploaded: {uploaded_at} • {total_count} records\n"
            text += f"Avg Flowrate: {avg_flow:.1f} L/min"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, dataset)
            self.list_widget.addItem(item)
    
    def on_item_double_clicked(self, item):
        dataset_summary = item.data(Qt.UserRole)
        if not dataset_summary:
            return
        
        # Fetch full dataset data
        try:
            headers = {}
            if self.token:
                headers['Authorization'] = f'Token {self.token}'
            
            dataset_id = dataset_summary.get('id')
            response = requests.get(
                f'http://localhost:8000/api/data/{dataset_id}/',
                headers=headers
            )
            
            if response.status_code == 200:
                dataset = response.json()
                self.dataset_selected.emit(dataset)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
