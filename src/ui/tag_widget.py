from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QSpinBox, QLabel, QHBoxLayout, QGroupBox, QListWidget
)
from .base_component import UIComponent

class TagControls(UIComponent):
    def setup_ui(self, layout):
        
        # Create main group box for tags
        tag_group = QGroupBox("Video Tags")
        tag_layout = QVBoxLayout(tag_group)

        tag_section = QWidget(self.parent)
        tag_layout = QVBoxLayout(tag_section)

        # Category buttons
        self.categories = ["Ataque", "Transición", "ABP", "Presión", "Defensa", "Ocasión", "Otros"]
        self.category_buttons = {}
        
        for i, category in enumerate(self.categories):
            btn = QPushButton(f"{i+1}. {category}")
            btn.setMinimumHeight(40)
            btn.setStyleSheet("font-size: 16px;")
            tag_layout.addWidget(btn)
            self.category_buttons[category] = btn

        ## Lista de tags
        self.tag_list = QListWidget()
        tag_layout.addWidget(QLabel("📝 Tags creados:"))
        tag_layout.addWidget(self.tag_list)

         # Time adjustments section
        time_group = QGroupBox("Time Adjustments")
        time_layout = QVBoxLayout(time_group)

        self.pre_spin = QSpinBox()
        self.pre_spin.setRange(0, 10)
        self.pre_spin.setValue(1)
        self.pre_spin.setPrefix("Inicio -")
        time_layout.addWidget(self.pre_spin)

        self.post_spin = QSpinBox()
        self.post_spin.setRange(0, 10)
        self.post_spin.setValue(1)
        self.post_spin.setPrefix("Fin +")
        time_layout.addWidget(self.post_spin)

        tag_layout.addWidget(time_group)
        layout.addWidget(tag_section)