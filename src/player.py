import sys
import vlc
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer, pyqtSignal

from src.utils.logger import AppLogger

class VideoPlayer(QWidget):
    time_changed = pyqtSignal(float)  # Signal for current video time
    speed_changed = pyqtSignal(float)  # Signal for speed changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = AppLogger.get_logger()
        
        # Initialize VLC with silent audio output in test environments
        if 'pytest' in sys.modules:
            self.instance = vlc.Instance('--aout=dummy')
        else:
            self.instance = vlc.Instance()
            
        self.mediaplayer = self.instance.media_player_new()
        self.setup_ui()
        self.setup_timer()

    def setup_ui(self):
        """Setup the UI components"""
        self.video_frame = QWidget(self)
        self.video_frame.setStyleSheet("background-color: black;")
        self.video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def setup_timer(self):
        """Setup update timer"""
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_time)

    def update_time(self):
        """Update current time and emit signal"""
        if self.mediaplayer.is_playing():
            current_time = self.get_time()
            self.time_changed.emit(current_time)

    def load_video(self, path):
        """Load and prepare video for playback"""
        if not path:
            return
            
        media = self.instance.media_new(path)
        self.mediaplayer.set_media(media)
        
        # Set render window based on platform
        if sys.platform.startswith('linux'):
            self.mediaplayer.set_xwindow(self.video_frame.winId())
        elif sys.platform == "win32":
            self.mediaplayer.set_hwnd(self.video_frame.winId())
        elif sys.platform == "darwin":
            self.mediaplayer.set_nsobject(int(self.video_frame.winId()))

        self.timer.start()
        QTimer.singleShot(100, self.mediaplayer.play)

    def toggle_playback(self):
        """Toggle between play and pause"""
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
        else:
            self.mediaplayer.play()

    def change_speed(self, delta):
        """Change playback speed"""
        current = self.mediaplayer.get_rate()
        new_rate = max(0.25, min(4.0, current + delta))
        self.mediaplayer.set_rate(new_rate)
        self.speed_changed.emit(new_rate)

    def get_time(self):
        """Get current playback time in seconds"""
        return self.mediaplayer.get_time() / 1000.0

    def set_time(self, seconds):
        """Set playback position in seconds"""
        self.mediaplayer.set_time(int(seconds * 1000))

    def seek_relative(self, seconds):
        """
        Seek forward or backward relative to current position
        seconds: int - positive for forward, negative for backward
        """
        current_time = self.get_time()
        if not self.mediaplayer.is_playing():
            return
        new_time = max(0, current_time + seconds)
        total_time = self.mediaplayer.get_length() / 1000.0
        new_time = min(new_time, total_time)
        
        self.set_time(new_time)
        self.logger.info(f"Seeking {'forward' if seconds > 0 else 'backward'} {abs(seconds)}s to {new_time:.2f}s")

