import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer, pyqtSignal
from src.utils.logger import AppLogger

# Class: VideoPlayer
# Description: A video player widget that uses VLC for playback.
# It supports loading videos, playback control, speed adjustment, and time tracking.
# Dependencies: PyQt5, VLC (or mock for testing)
class VideoPlayer(QWidget):
    time_changed = pyqtSignal(float)  # Signal for current video time
    speed_changed = pyqtSignal(float)  # Signal for speed changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = AppLogger.get_logger()
        
        # Use mock VLC in test environments or when VLC is not available
        use_mock = ('pytest' in sys.modules) or os.environ.get('CI') == 'true'
        
        if use_mock:
            from tests.utils.vlc_mock import MockVLCInstance
            self.instance = MockVLCInstance()
        else:
            try:
                import vlc
                self.instance = vlc.Instance()
            except (ImportError, OSError) as e:
                self.logger.warning(f"Failed to initialize VLC, falling back to mock: {e}")
                from tests.utils.vlc_mock import MockVLCInstance
                self.instance = MockVLCInstance()
            
        self.mediaplayer = self.instance.media_player_new()
        self.setup_ui()
        self.setup_timer()

    def setup_ui(self):
        """Setup the UI components"""
        self.video_frame = QWidget(self)
        self.video_frame.setStyleSheet("background-color: black;")
        self.video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_frame.setMouseTracking(True)
        self.drawing_controls = None
        self.annotations = []

        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def set_drawing_controls(self, drawing_controls):
        """Set the drawing controls instance"""
        self.drawing_controls = drawing_controls

    def paintEvent(self, event):
        """Handle paint events"""
        from PyQt5.QtGui import QPainter, QPen, QBrush
        from PyQt5.QtCore import Qt
        painter = QPainter(self)
        for annotation in self.annotations:
            if annotation["tool"] == "circle":
                painter.setPen(QPen(annotation["color"], annotation["size"], Qt.SolidLine))
                painter.setBrush(QBrush(annotation["color"], Qt.SolidPattern))
                painter.drawEllipse(annotation["position"], annotation["size"], annotation["size"])
        painter.end()

    def set_drawing_controls(self, drawing_controls):
        """Set the drawing controls instance"""
        self.drawing_controls = drawing_controls

    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if self.drawing_controls:
            if self.drawing_controls.selected_tool == "circle":
                from PyQt5.QtGui import QPainter, QPen, QBrush
                from PyQt5.QtCore import Qt
                annotation = {
                    "tool": "circle",
                    "position": event.pos(),
                    "color": self.drawing_controls.selected_color,
                    "size": self.drawing_controls.drawing_size
                }
                self.annotations.append(annotation)
                self.update() # Trigger paintEvent
            print(f"Drawing tool: {self.drawing_controls.selected_tool}")
            print(f"Drawing color: {self.drawing_controls.selected_color.name()}")
            print(f"Drawing size: {self.drawing_controls.drawing_size}")

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
        
        # # parse the metadata of the file
        # self.media.parse()
        # # set the title of the track as window title
                
        # Extract video metadata
        media.parse_with_options(0, 2000)  # Parse metadata
        file_name = os.path.basename(path)
        # fps = media.get_fps()
        # width, height = media.get_tracks()[0].video.width, media.get_tracks()[0].video.height

        # Display metadata in the UI
        # self.logger.info(f"Loaded video: {file_name}, FPS: {fps}, Resolution: {width}x{height}")
        # self.setWindowTitle(f"{file_name} - {fps:.2f} FPS, {width}x{height}")
        media.parse()
        
        self.logger.info(f"Loaded video: {media.get_meta(0)}")
        self.logger.info(f"Video duration: {media.get_duration() / 1000.0:.2f} seconds")
        self.logger.info(f"Video tracks: {media.get_meta(1)}")  # 1 is for video track
        self.setWindowTitle(media.get_meta(0))

        
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
