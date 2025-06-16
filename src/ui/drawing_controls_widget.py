from PyQt5.QtWidgets import (
    QToolBar, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QColorDialog, QSpinBox
)
from PyQt5.QtGui import QColor

class DrawingControls(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Drawing Tools", parent)
        self.setFloatable(True)
        self.setMovable(True)

        self.selected_color = QColor(255, 0, 0)  # Default color: red
        self.drawing_size = 5  # Default size: 5
        self.selected_tool = None
       
        self.setup_ui()

    def setup_ui(self):
        # Drawing tool selection buttons
        self.circle_button = QPushButton("Circle")
        self.arrow_button = QPushButton("Arrow")
        self.cone_button = QPushButton("Cone")
        self.cylinder_button = QPushButton("Cylinder")

        self.circle_button.clicked.connect(self.select_circle_tool)
        self.arrow_button.clicked.connect(self.select_arrow_tool)
        self.cone_button.clicked.connect(self.select_cone_tool)
        self.cylinder_button.clicked.connect(self.select_cylinder_tool)

        def set_button_style(button):
            button.setStyleSheet("QPushButton { background-color: lightblue; }"
                                 "QPushButton:!checked { background-color: none; }")

        set_button_style(self.circle_button)
        set_button_style(self.arrow_button)
        set_button_style(self.cone_button)
        set_button_style(self.cylinder_button)

        # Add buttons to the toolbar
        self.addWidget(self.circle_button)
        self.addWidget(self.arrow_button)
        self.addWidget(self.cone_button)
        self.addWidget(self.cylinder_button)

        self.addSeparator()  # Add a separator for better organization

        # Color selection
        color_widget = QWidget()
        color_layout = QHBoxLayout(color_widget)
        color_layout.setContentsMargins(0, 0, 0, 0)
        
        color_label = QLabel("Color:")
        self.color_button = QPushButton()
        self.color_button.setFixedSize(24, 24)
        self.color_button.setStyleSheet(f"background-color: {self.selected_color.name()};")
        self.color_button.clicked.connect(self.open_color_dialog)

        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        self.addWidget(color_widget)

        self.addSeparator()

 
    def select_circle_tool(self):
        self.selected_tool = "circle"
        print("Circle tool selected")

    def select_arrow_tool(self):
        self.selected_tool = "arrow"
        print("Arrow tool selected")

    def select_cone_tool(self):
        self.selected_tool = "cone"
        print("Cone tool selected")

    def select_cylinder_tool(self):
        self.selected_tool = "cylinder"
        print("Cylinder tool selected")

        # Color selection
        color_layout = QHBoxLayout()
        color_label = QLabel("Color:")
        self.color_button = QPushButton()
        self.color_button.setStyleSheet(f"background-color: {self.selected_color.name()};")
        self.color_button.clicked.connect(self.open_color_dialog)

        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        self.layout.addLayout(color_layout)

        # Size selection
        size_layout = QHBoxLayout()
        size_label = QLabel("Size:")
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(1, 20)
        self.size_spinbox.setValue(self.drawing_size)
        self.size_spinbox.valueChanged.connect(self.set_drawing_size)

        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_spinbox)
        self.layout.addLayout(size_layout)

    def open_color_dialog(self):
        color = QColorDialog.getColor(self.selected_color, self)
        if color.isValid():
            self.selected_color = color
            self.color_button.setStyleSheet(f"background-color: {self.selected_color.name()};")

    def set_drawing_size(self, size):
        self.drawing_size = size
