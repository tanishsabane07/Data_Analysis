"""
Chart Widget using Matplotlib for the Desktop App.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ChartWidget(QWidget):
    def __init__(self, title="Chart", chart_type="pie"):
        super().__init__()
        self.title = title
        self.chart_type = chart_type
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create matplotlib figure with dark theme
        self.figure = Figure(figsize=(5, 4), dpi=100, facecolor='#1e293b')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #1e293b; border-radius: 8px;")
        
        layout.addWidget(self.canvas)
    
    def set_data(self, data):
        """Set data for pie chart (type distribution)."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        
        if not data:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', 
                   color='#94a3b8', fontsize=14)
            self.canvas.draw()
            return
        
        labels = list(data.keys())
        values = list(data.values())
        
        colors = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899', '#22c55e']
        
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors[:len(values)],
            textprops={'color': '#f1f5f9', 'fontsize': 10},
            wedgeprops={'edgecolor': '#1e293b', 'linewidth': 2}
        )
        
        for autotext in autotexts:
            autotext.set_color('#f1f5f9')
            autotext.set_fontsize(9)
        
        ax.set_title(self.title, color='#f1f5f9', fontsize=12, fontweight='bold', pad=10)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def set_bar_data(self, data):
        """Set data for bar chart (averages)."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        
        if not data:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', 
                   color='#94a3b8', fontsize=14)
            self.canvas.draw()
            return
        
        labels = list(data.keys())
        values = list(data.values())
        colors = ['#3b82f6', '#10b981', '#f59e0b']
        
        bars = ax.bar(labels, values, color=colors, edgecolor='#0f172a', linewidth=1)
        
        # Add value labels on bars
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.annotate(f'{val:.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       color='#f1f5f9', fontsize=10)
        
        ax.set_title(self.title, color='#f1f5f9', fontsize=12, fontweight='bold', pad=10)
        ax.tick_params(colors='#94a3b8')
        ax.spines['bottom'].set_color('#475569')
        ax.spines['left'].set_color('#475569')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Grid
        ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#475569')
        ax.set_axisbelow(True)
        
        self.figure.tight_layout()
        self.canvas.draw()


class LineChartWidget(QWidget):
    """Line chart for parameter trends."""
    
    def __init__(self, title="Parameter Trends"):
        super().__init__()
        self.title = title
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.figure = Figure(figsize=(8, 4), dpi=100, facecolor='#1e293b')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #1e293b; border-radius: 8px;")
        
        layout.addWidget(self.canvas)
    
    def set_data(self, records):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e293b')
        
        if not records:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', 
                   color='#94a3b8', fontsize=14)
            self.canvas.draw()
            return
        
        # Limit to first 15 records for readability
        records = records[:15]
        
        names = [r.get('equipment_name', '')[:10] for r in records]
        flowrates = [r.get('flowrate', 0) for r in records]
        pressures = [r.get('pressure', 0) for r in records]
        temperatures = [r.get('temperature', 0) for r in records]
        
        x = range(len(names))
        
        ax.plot(x, flowrates, 'o-', label='Flowrate', color='#3b82f6', linewidth=2, markersize=6)
        ax.plot(x, pressures, 's-', label='Pressure', color='#10b981', linewidth=2, markersize=6)
        ax.plot(x, temperatures, '^-', label='Temperature', color='#f59e0b', linewidth=2, markersize=6)
        
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right')
        
        ax.set_title(self.title, color='#f1f5f9', fontsize=12, fontweight='bold', pad=10)
        ax.tick_params(colors='#94a3b8')
        ax.spines['bottom'].set_color('#475569')
        ax.spines['left'].set_color('#475569')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        ax.legend(facecolor='#334155', edgecolor='#475569', labelcolor='#f1f5f9')
        ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#475569')
        ax.set_axisbelow(True)
        
        self.figure.tight_layout()
        self.canvas.draw()
