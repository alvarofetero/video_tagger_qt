from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QLabel,QGroupBox, QLineEdit, QComboBox, QFileDialog)
from PyQt5.QtCore import Qt
from .base_component import UIComponent

class FileControls(UIComponent):
    def __init__(self, parent=None, video_player=None):
        super().__init__(parent)
        if video_player is None:
            raise ValueError("video_player must be provided")
        self.video_player = video_player
        
    def setup_ui(self, layout):
        # Create main group box for file controls
        file_group = QGroupBox("File Controls")
        file_layout = QVBoxLayout(file_group)

        # File name input
        self.file_name_input = QLineEdit()
        self.file_name_input.setPlaceholderText("Enter file name")
        file_layout.addWidget(self.file_name_input)

        # File type selection
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["MP4", "AVI", "MKV"])
        file_layout.addWidget(self.file_type_combo)

        # File size display
        self.file_size_label = QLabel("File Size: 0 MB")
        file_layout.addWidget(self.file_size_label)

        # Add the group box to the main layout
        layout.addWidget(file_group)

    # Cargar video desde el disco
    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "Seleccionar Video")
        # If a file was selected, update the video path and load the video
        if file_path:
            self.video_path = file_path
            self.video_player.load_video(file_path)
