#!/usr/bin/env python3
"""Quick test of video loading functionality"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QTimer

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.player import VideoPlayer
from src.utils.logger import AppLogger

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = AppLogger.get_logger()
        self.logger.info("TestWindow: Initializing")
        
        self.setWindowTitle("Video Player Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create video player
        self.logger.info("TestWindow: Creating VideoPlayer")
        self.video_player = VideoPlayer(self)
        layout.addWidget(self.video_player)
        
        # Create test button
        test_button = QPushButton("Load Test Video")
        test_button.clicked.connect(self.load_test_video)
        layout.addWidget(test_button)
        
        self.logger.info("TestWindow: Setup complete")
    
    def load_test_video(self):
        test_video = "D:/videos/Horta_B_2025_2026/J28_2026_05_03_PIFERRER/S4100004.MP4"
        
        if os.path.exists(test_video):
            self.logger.info(f"TestWindow: Loading video: {test_video}")
            self.video_player.load_video(test_video)
            self.logger.info("TestWindow: Video load request sent")
        else:
            self.logger.error(f"TestWindow: Video not found: {test_video}")
            print(f"Video file not found: {test_video}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    # Load video after window is shown
    QTimer.singleShot(1000, window.load_test_video)
    
    sys.exit(app.exec())
