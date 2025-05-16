# VLC-based video player
import sys
import vlc
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer, pyqtSignal

class VideoPlayer(QWidget):
    time_changed = pyqtSignal(float)  # Señal que emite el tiempo actual del video en segundos
    speed_changed = pyqtSignal(float)  # New signal for speed changes

    def __init__(self, parent=None):
        super().__init__(parent)

        # Instancia de VLC
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()

        # Timer para futuras actualizaciones
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update)

        # Widget donde se proyecta el video
        self.video_frame = QWidget(self)
        self.video_frame.setStyleSheet("background-color: black;")

        # 🔧 Asegura que el video_frame se expanda
        self.video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)
        layout.setContentsMargins(0, 0, 0, 0)  # opcional, para eliminar márgenes
        self.setLayout(layout)

    def load_video(self, path):
        media = self.instance.media_new(path)
        self.mediaplayer.set_media(media)

        # Asigna la ventana de renderizado dependiendo del sistema operativo
        if sys.platform.startswith("linux"):
            self.mediaplayer.set_xwindow(self.video_frame.winId())
        elif sys.platform == "win32":
            self.mediaplayer.set_hwnd(self.video_frame.winId())
        elif sys.platform == "darwin":
            self.mediaplayer.set_nsobject(int(self.video_frame.winId()))

        # Inicia la reproducción ligeramente después para evitar errores
        QTimer.singleShot(100, self.mediaplayer.play)

    def get_time(self):
        return self.mediaplayer.get_time() / 1000.0  # en segundos
    
    def set_time(self, time):
        self.mediaplayer.set_time(int(time * 1000))  # en milisegundos

    def update(self):
        current_time = self.get_time()
        self.time_changed.emit(current_time)

    ## Reproducir / Pausar el video
    def toggle_playback(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
        else:
            self.mediaplayer.play()

     ## Cambiar la velocidad de reproducción
    def change_speed(self, delta):
        current = self.mediaplayer.get_rate()
        new_rate = max(0.25, min(4.0, current + delta))
        self.mediaplayer.set_rate(new_rate)
        self.speed_changed.emit(new_rate) # Emit the new speed
        print(f"🎚️ Velocidad: {new_rate:.2f}x")

