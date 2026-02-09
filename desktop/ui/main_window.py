"""
Main Window for the Chemical Equipment Visualizer Desktop App.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QStatusBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .upload_widget import UploadWidget
from .chart_widget import ChartWidget
from .table_widget import TableWidget
from .auth_dialog import AuthDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_dataset = None
        self.token = None
        self.user = None
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("⚗️ Chemical Equipment Visualizer")
        self.setMinimumSize(1200, 800)
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        layout.addWidget(self.tabs)
        
        # Create tabs
        self.upload_widget = UploadWidget()
        self.upload_widget.upload_success.connect(self.on_upload_success)
        
        self.dashboard_widget = self.create_dashboard_placeholder()
        self.history_widget = self.create_history_widget()
        
        self.tabs.addTab(self.upload_widget, "📤 Upload")
        self.tabs.addTab(self.dashboard_widget, "📊 Dashboard")
        self.tabs.addTab(self.history_widget, "📁 History")
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready - Upload a CSV file to begin")
    
    def create_header(self):
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 41, 59, 0.8);
                border-radius: 16px;
                padding: 16px;
            }
        """)
        layout = QVBoxLayout(header)
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title = QLabel("⚗️ Chemical Equipment Visualizer")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #60a5fa, stop:0.5 #06b6d4, stop:1 #8b5cf6);
        """)
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Analyze and visualize your chemical equipment parameters with ease")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Auth button
        auth_layout = QHBoxLayout()
        auth_layout.setAlignment(Qt.AlignCenter)
        
        self.auth_btn = QPushButton("🔐 Login")
        self.auth_btn.setObjectName("secondaryBtn")
        self.auth_btn.clicked.connect(self.show_auth_dialog)
        auth_layout.addWidget(self.auth_btn)
        
        self.user_label = QLabel("")
        self.user_label.setStyleSheet("color: #94a3b8; margin-left: 10px;")
        self.user_label.hide()
        auth_layout.addWidget(self.user_label)
        
        layout.addLayout(auth_layout)
        
        return header
    
    def create_dashboard_placeholder(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        icon = QLabel("📊")
        icon.setStyleSheet("font-size: 64px; opacity: 0.5;")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)
        
        label = QLabel("No dataset selected. Upload a CSV file or select from history.")
        label.setStyleSheet("color: #94a3b8; font-size: 16px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        self.dashboard_placeholder = widget
        return widget
    
    def create_history_widget(self):
        from .history_widget import HistoryWidget
        widget = HistoryWidget()
        widget.dataset_selected.connect(self.on_dataset_selected)
        return widget
    
    def show_auth_dialog(self):
        dialog = AuthDialog(self)
        if dialog.exec_():
            self.user = dialog.user
            self.token = dialog.token
            self.update_auth_display()
            self.upload_widget.set_token(self.token)
            self.history_widget.set_token(self.token)
            self.history_widget.refresh()
    
    def update_auth_display(self):
        if self.user:
            self.auth_btn.setText("🚪 Logout")
            self.user_label.setText(f"Welcome, {self.user['username']}!")
            self.user_label.show()
            self.auth_btn.clicked.disconnect()
            self.auth_btn.clicked.connect(self.logout)
        else:
            self.auth_btn.setText("🔐 Login")
            self.user_label.hide()
            self.auth_btn.clicked.disconnect()
            self.auth_btn.clicked.connect(self.show_auth_dialog)
    
    def logout(self):
        self.user = None
        self.token = None
        self.upload_widget.set_token(None)
        self.history_widget.set_token(None)
        self.update_auth_display()
        self.statusBar.showMessage("Logged out successfully")
    
    def on_upload_success(self, dataset):
        self.current_dataset = dataset
        self.update_dashboard(dataset)
        self.tabs.setCurrentIndex(1)  # Switch to dashboard
        self.history_widget.refresh()
        self.statusBar.showMessage(f"Successfully uploaded! Found {dataset.get('total_count', 0)} equipment records.")
    
    def on_dataset_selected(self, dataset):
        self.current_dataset = dataset
        self.update_dashboard(dataset)
        self.tabs.setCurrentIndex(1)  # Switch to dashboard
    
    def update_dashboard(self, dataset):
        # Remove placeholder and create actual dashboard
        self.tabs.removeTab(1)
        
        dashboard = QWidget()
        layout = QVBoxLayout(dashboard)
        layout.setSpacing(16)
        
        # Stats section
        stats_widget = self.create_stats_widget(dataset)
        layout.addWidget(stats_widget)
        
        # Charts section
        charts_layout = QHBoxLayout()
        
        # Pie chart
        pie_chart = ChartWidget("Equipment Type Distribution", "pie")
        pie_chart.set_data(dataset.get('type_distribution', {}))
        charts_layout.addWidget(pie_chart)
        
        # Bar chart
        bar_chart = ChartWidget("Average Parameter Values", "bar")
        bar_chart.set_bar_data({
            'Flowrate': dataset.get('avg_flowrate', 0),
            'Pressure': dataset.get('avg_pressure', 0),
            'Temperature': dataset.get('avg_temperature', 0)
        })
        charts_layout.addWidget(bar_chart)
        
        layout.addLayout(charts_layout)
        
        # Table section
        table_widget = TableWidget()
        table_widget.set_data(dataset.get('records', []))
        layout.addWidget(table_widget)
        
        # PDF button
        pdf_btn = QPushButton("📄 Download PDF Report")
        pdf_btn.setObjectName("successBtn")
        pdf_btn.clicked.connect(lambda: self.download_pdf(dataset.get('id')))
        layout.addWidget(pdf_btn)
        
        self.tabs.insertTab(1, dashboard, "📊 Dashboard")
        self.tabs.setCurrentIndex(1)
    
    def create_stats_widget(self, dataset):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        layout = QHBoxLayout(widget)
        
        stats = [
            ("Total Equipment", str(dataset.get('total_count', 0)), "#3b82f6"),
            ("Avg Flowrate", f"{dataset.get('avg_flowrate', 0):.1f} L/min", "#10b981"),
            ("Avg Pressure", f"{dataset.get('avg_pressure', 0):.1f} bar", "#8b5cf6"),
            ("Avg Temperature", f"{dataset.get('avg_temperature', 0):.1f} °C", "#f59e0b"),
        ]
        
        for label, value, color in stats:
            stat_card = self.create_stat_card(label, value, color)
            layout.addWidget(stat_card)
        
        return widget
    
    def create_stat_card(self, label, value, color):
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: #334155;
                border-radius: 8px;
                padding: 16px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: #94a3b8; font-size: 12px;")
        label_widget.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_widget)
        
        return card
    
    def download_pdf(self, dataset_id):
        if not dataset_id:
            return
        
        import requests
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        
        try:
            headers = {}
            if self.token:
                headers['Authorization'] = f'Token {self.token}'
            
            response = requests.get(
                f'http://localhost:8000/api/report/{dataset_id}/',
                headers=headers
            )
            
            if response.status_code == 200:
                # Save file
                filename, _ = QFileDialog.getSaveFileName(
                    self, "Save PDF Report", 
                    f"equipment_report_{dataset_id}.pdf",
                    "PDF Files (*.pdf)"
                )
                
                if filename:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    
                    QMessageBox.information(self, "Success", f"Report saved to {filename}")
                    self.statusBar.showMessage(f"PDF report saved successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to generate PDF report")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error: {str(e)}")
