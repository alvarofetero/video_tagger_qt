from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QSpinBox, QLabel, QHBoxLayout, QGroupBox, QListWidget,
    QShortcut, QGridLayout
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeySequence
from .base_component import UIComponent
from src.config import load_categories

class TagControls(QWidget, UIComponent):
    tag_started = pyqtSignal(str, float) # Emits (category, start_time)
    tag_ended = pyqtSignal(str, float)   # Emits (category, end_time)
    tag_removed = pyqtSignal(int)        # Emits index of removed tag

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        UIComponent.__init__(self, parent)
       
        self.active_category = None
        self.video_player = None
        # Load categories from json file instead of hardcoding
        self.categories = load_categories()
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

        # Create tag section with self as parent instead of self.parent
        self.tag_section = QWidget(self)  # Changed from self.parent to self
        self.tag_section.setFocusPolicy(Qt.StrongFocus)  # Allow keyboard focus
        self.tag_layout = QVBoxLayout(self.tag_section)

        # Create initial category buttons
        self.create_category_buttons()

        ## Lista de tags
        self.tag_list = QListWidget()
        self.tag_layout.addWidget(QLabel("📝 Tags creados:"))
        self.apply_format_to_taglist(self.tag_list)
        self.tag_layout.addWidget(self.tag_list)

        # Add the section to the layout and ensure it's visible
        layout.addWidget(self.tag_section)
        self.tag_section.show()  # Ensure widget is visible

    def create_category_button(self, category, index):
        """Create a single category button with proper setup"""
        btn = QPushButton(f"{index+1}. {category}")
        btn.setMinimumHeight(40)
        btn.setStyleSheet("font-size: 16px;")
        btn.clicked.connect(self.on_category_button_clicked)
        btn.setProperty("category", category)
        btn.setProperty("index", index+1)
        
        # Add number shortcut (1-9) if applicable
        if index < 9:  # Only add shortcuts for first 9 categories
            # Find the main window
            from PyQt5.QtWidgets import QMainWindow
            parent = self
            while parent and not isinstance(parent, QMainWindow):
                parent = parent.parentWidget()
            
            if parent:  # If we found the main window
                shortcut = QShortcut(QKeySequence(str(index + 1)), parent)
                shortcut.activated.connect(lambda c=category: self.on_category_shortcut(c))
            
        return btn

    def create_category_buttons(self):
        """Create all category buttons in a two-column layout"""
        # Clear existing buttons first
        if hasattr(self, 'category_buttons'):
            for btn in self.category_buttons.values():
                btn.deleteLater()
        self.category_buttons = {}

        # Create a grid layout for the buttons
        button_grid = QGridLayout()
        button_grid.setSpacing(10)  # Add spacing between buttons
        button_grid.setHorizontalSpacing(10)  # Add horizontal spacing between columns
        button_grid.setColumnStretch(0, 1)  # Make first column stretch
        button_grid.setColumnStretch(1, 1)  # Make second column stretch

        # Create new buttons in a grid
        for i, category in enumerate(self.categories):
            btn = self.create_category_button(category, i)
            self.category_buttons[category] = btn
            row = i // 2
            col = i % 2
            button_grid.addWidget(btn, row, col)

        # Remove existing items from tag_layout
        while self.tag_layout.count():
            item = self.tag_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add the grid layout to tag_layout
        self.tag_layout.addLayout(button_grid)

        # Re-add the tag list section
        self.tag_list = QListWidget()
        self.tag_layout.addWidget(QLabel("📝 Tags creados:"))
        self.apply_format_to_taglist(self.tag_list)
        self.tag_layout.addWidget(self.tag_list)

    def update_category_buttons(self):
        """Update the category buttons after category list changes"""
        self.create_category_buttons()

        # If there was an active category that still exists, restore its highlight
        if self.active_category and self.active_category in self.category_buttons:
            self.category_buttons[self.active_category].setStyleSheet("background-color: yellow; font-size: 16px;")

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