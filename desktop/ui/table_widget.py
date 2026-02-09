"""
Data Table Widget for the Desktop App.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt


class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("📋 Equipment Records")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #f1f5f9;")
        header_layout.addWidget(title)
        
        self.count_label = QLabel("0 records")
        self.count_label.setStyleSheet("color: #94a3b8;")
        header_layout.addStretch()
        header_layout.addWidget(self.count_label)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate (L/min)", 
            "Pressure (bar)", "Temperature (°C)"
        ])
        
        # Table settings
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
    
    def set_data(self, records):
        self.table.setRowCount(0)
        
        if not records:
            self.count_label.setText("0 records")
            return
        
        self.count_label.setText(f"{len(records)} records")
        
        for record in records:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Equipment Name
            name_item = QTableWidgetItem(record.get('equipment_name', ''))
            name_item.setForeground(Qt.white)
            self.table.setItem(row, 0, name_item)
            
            # Type (with badge styling)
            type_item = QTableWidgetItem(record.get('equipment_type', ''))
            type_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, type_item)
            
            # Flowrate
            flowrate = record.get('flowrate', 0)
            flow_item = QTableWidgetItem(f"{flowrate:.1f}")
            flow_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, flow_item)
            
            # Pressure
            pressure = record.get('pressure', 0)
            press_item = QTableWidgetItem(f"{pressure:.1f}")
            press_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, press_item)
            
            # Temperature
            temperature = record.get('temperature', 0)
            temp_item = QTableWidgetItem(f"{temperature:.1f}")
            temp_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, temp_item)
        
        self.table.resizeRowsToContents()
