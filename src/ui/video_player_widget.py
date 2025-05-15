from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer, pyqtSignal
import vlc

class VideoPlayer(QWidget):
    time_changed = pyqtSignal(float)  # Signal for current video time in seconds

    def __init__(self, parent=None):
        super().__init__(parent)

        # VLC instance
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()

        # Timer for updates
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)

        # Video frame widget
        self.video_frame = QWidget(self)
        self.video_frame.setStyleSheet("background-color: black;")
        self.video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


    def load_video(self, path):
        """Load a video file into the player"""
        media = self.instance.media_new(path)
        self.mediaplayer.set_media(media)
        
        # Set the window ID where to render VLC's video output
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.video_frame.winId())
        elif sys.platform == "win32":  # for Windows
            self.mediaplayer.set_hwnd(self.video_frame.winId())
        elif sys.platform == "darwin":  # for macOS
            self.mediaplayer.set_nsobject(int(self.video_frame.winId()))

        self.timer.start()

    # # 🎞️ Reproductor de video a la derecha
    #     self.video_player = VideoPlayer(self)
    #     splitter.addWidget(self.video_player) # Añadir reproductor de video al splitter


    def toggle_playback(self):
        """Toggle between play and pause"""
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
        else:
            self.mediaplayer.play()

    def update_ui(self):
        """Update UI elements based on current playback state"""
        if self.mediaplayer.is_playing():
            current_time = self.mediaplayer.get_time() / 1000.0
            self.time_changed.emit(current_time)

    def get_time(self):
        """Get current playback time in seconds"""
        return self.mediaplayer.get_time() / 1000.0

    def set_time(self, seconds):
        """Set playback position to specified time in seconds"""
        self.mediaplayer.set_time(int(seconds * 1000))

    def change_speed(self, delta):
        """Change playback speed by delta"""
        current_rate = self.mediaplayer.get_rate()
        new_rate = max(0.25, min(4.0, current_rate + delta))
        self.mediaplayer.set_rate(new_rate)
        return new_rate