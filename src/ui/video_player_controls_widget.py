from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PyQt5.QtCore import Qt
from .base_component import UIComponent

class PlayerControls(UIComponent):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_player = None

    def setup_ui(self, layout):
        # Create a group box for player controls
        player_group = QGroupBox("Player Controls")
        player_layout = QVBoxLayout(player_group)

        # Play button section
        self.play_button = QPushButton("▶️ Play / Pause")
        self.play_button.setMinimumHeight(40)
        self.play_button.setStyleSheet("font-size: 16px;")
        player_layout.addWidget(self.play_button)

        # Seek controls section
        seek_layout = QHBoxLayout()
        self.rewind_button = QPushButton("⏪ -5s")
        self.forward_button = QPushButton("⏩ +5s")
        seek_layout.addWidget(self.rewind_button)
        seek_layout.addWidget(self.forward_button)
        player_layout.addLayout(seek_layout)

        # Speed controls section in its own group
        speed_group = QGroupBox("Playback Speed")
        speed_layout = QHBoxLayout(speed_group)
        self.speed_down_button = QPushButton("⏪ -")
        self.speed_up_button = QPushButton("⏩ +")
        self.speed_label = QLabel("🔁 1.00x")
        speed_layout.addWidget(self.speed_down_button)
        speed_layout.addWidget(self.speed_label)
        speed_layout.addWidget(self.speed_up_button)
        
        player_layout.addWidget(speed_group)
        layout.addWidget(player_group)

    def set_video_player(self, video_player):
        self.video_player = video_player
        # Connect the speed changed signal
        self.video_player.speed_changed.connect(self.update_speed_label)

    def update_speed_label(self, new_rate):
        self.speed_label.setText(f"🔁 {new_rate:.2f}x")    