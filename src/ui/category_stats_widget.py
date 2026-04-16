from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QGroupBox
)
from PyQt5.QtCore import Qt
from src.services.storage import CategoryClickTracker


class CategoryStatsWidget(QWidget):
    """Widget to display category click statistics."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.click_tracker = CategoryClickTracker()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the stats UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("📊 Category Click Statistics")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        
        # Stats table
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Category", "Click Count"])
        self.stats_table.horizontalHeader().setStretchLastSection(True)
        self.stats_table.setMaximumHeight(250)
        layout.addWidget(self.stats_table)
        
        # Button layout for controls
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_stats)
        button_layout.addWidget(refresh_btn)
        
        reset_all_btn = QPushButton("🔴 Reset All")
        reset_all_btn.setStyleSheet("background-color: #d9534f;")
        reset_all_btn.clicked.connect(self.reset_all_stats)
        button_layout.addWidget(reset_all_btn)
        
        layout.addLayout(button_layout)
        
        # Initial refresh
        self.refresh_stats()
    
    def refresh_stats(self):
        """Refresh the statistics display."""
        counts = self.click_tracker.get_all_counts()
        
        # Clear and rebuild table
        self.stats_table.setRowCount(0)
        
        # Sort by count descending, then by category name
        sorted_counts = sorted(
            counts.items(),
            key=lambda x: (-x[1], x[0])
        )
        
        for row, (category, count) in enumerate(sorted_counts):
            self.stats_table.insertRow(row)
            
            # Category name
            cat_item = QTableWidgetItem(str(category))
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemIsEditable)
            self.stats_table.setItem(row, 0, cat_item)
            
            # Click count
            count_item = QTableWidgetItem(str(count))
            count_item.setFlags(count_item.flags() & ~Qt.ItemIsEditable)
            count_item.setTextAlignment(Qt.AlignCenter)
            self.stats_table.setItem(row, 1, count_item)
        
        # Show total
        total = sum(counts.values())
        if total == 0:
            self.stats_table.insertRow(0)
            no_data = QTableWidgetItem("No clicks yet")
            no_data.setFlags(no_data.flags() & ~Qt.ItemIsEditable)
            self.stats_table.setItem(0, 0, no_data)
    
    def reset_all_stats(self):
        """Reset all category click counts."""
        self.click_tracker.reset_all()
        self.refresh_stats()
