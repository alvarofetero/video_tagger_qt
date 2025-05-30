from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QSpinBox, QLabel, QHBoxLayout, QGroupBox, QListWidget,
    QShortcut
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeySequence
from .base_component import UIComponent

class TagControls(UIComponent):
    tag_started = pyqtSignal(str, float) # Emits (category, start_time)
    tag_ended = pyqtSignal(str, float)   # Emits (category, end_time)
    tag_removed = pyqtSignal(int)        # Emits index of removed tag

    def __init__(self, parent=None):
         # Call parent class __init__ with parent
        super(TagControls, self).__init__(parent)
       
        self.active_category = None
        self.video_player = None
        self.categories = ["Ataque", "Transición", "ABP", "Presión", "Defensa", "Ocasión", "Otros"]
        self.category_buttons = {}

        # Initialize time adjustment values (not shown in UI)
        self.pre_spin = QSpinBox()
        self.pre_spin.setRange(0, 10)
        self.pre_spin.setValue(1)
        
        self.post_spin = QSpinBox()
        self.post_spin.setRange(0, 10)
        self.post_spin.setValue(1)

    def set_video_player(self, video_player):
        self.video_player = video_player

    def setup_ui(self, layout):
        
        # Create main group box for tags
        tag_group = QGroupBox("Video Tags")
        tag_layout = QVBoxLayout(tag_group)

        tag_section = QWidget(self.parent)
        tag_layout = QVBoxLayout(tag_section)

        # Category buttons with shortcuts
        self.categories = ["Ataque", "Transición", "ABP", "Presión", "Defensa", "Ocasión", "Otros"]
        self.category_buttons = {}
        
        for i, category in enumerate(self.categories):
            btn = QPushButton(f"{i+1}. {category}")
            btn.setMinimumHeight(40)
            btn.setStyleSheet("font-size: 16px;")
            tag_layout.addWidget(btn)
            self.category_buttons[category] = btn
            self.category_buttons[category].clicked.connect(self.on_category_button_clicked)
            self.category_buttons[category].setProperty("category", category)
            self.category_buttons[category].setProperty("index", i+1)
            
            # Add number shortcut (1-9)
            if i < 9:  # Only add shortcuts for first 9 categories
                shortcut = QShortcut(QKeySequence(str(i + 1)), tag_section)
                shortcut.activated.connect(lambda c=category: self.on_category_shortcut(c))

        ## Lista de tags
        self.tag_list = QListWidget()
        tag_layout.addWidget(QLabel("📝 Tags creados:"))
        self.apply_format_to_taglist(self.tag_list)
        tag_layout.addWidget(self.tag_list)

        layout.addWidget(tag_section)

    def on_category_button_clicked(self):
        """Handle category button clicks for tag creation"""
        if not self.video_player:
            return

        button = self.sender()
        category = button.property("category")
        current_time = self.video_player.get_time()

        if self.active_category == category:
            # End tag for this category
            adjusted_end = current_time + self.post_spin.value()
            self.tag_ended.emit(category, adjusted_end)
            button.setStyleSheet("font-size: 16px;")  # Reset style
            self.active_category = None
        else:
            # Start new tag
            adjusted_start = max(0, current_time - self.pre_spin.value())
            self.tag_started.emit(category, adjusted_start)
            
            # Reset previous active button if exists
            if self.active_category and self.active_category in self.category_buttons:
                self.category_buttons[self.active_category].setStyleSheet("font-size: 16px;")
            
            # Highlight active button
            button.setStyleSheet("background-color: yellow; font-size: 16px;")
            self.active_category = category

    def on_category_shortcut(self, category):
        """Handle category shortcut keys"""
        if category in self.category_buttons:
            button = self.category_buttons[category]
            button.click()  # Simulate button click

    def update_tag_list(self, tags):
        """Update the tag list with current tags"""
        self.tag_list.clear()
        for i, tag in enumerate(tags):
            if tag["start"] is not None:
                start_time = f"{tag['start']:.1f}"
                end_time = f"{tag['end']:.1f}" if tag["end"] is not None else "..."
                category = tag["category"]
                self.tag_list.addItem(f"{i+1}. {category} ({start_time}s - {end_time}s)")

    def clear_tags(self):
        """Clear the tag list and reset active category"""
        self.tag_list.clear()
        if self.active_category:
            self.category_buttons[self.active_category].setStyleSheet("font-size: 16px;")
        self.active_category = None

    def apply_format_to_taglist(self, tag_list):
        """Apply custom formatting to the tag list"""
        tag_list.setStyleSheet("""
        QListWidget {
            background-color: #2b2b2b;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            padding: 5px;
        }
        QListWidget::item {
            color: #ffffff;
            padding: 5px;
            margin: 2px 0px;
        }
        QListWidget::item:selected {
            background-color: #3d3d3d;
        }
    """)