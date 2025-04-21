import sys
import vlc
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QLabel, QSplitter
from PyQt5.QtCore import Qt

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Reproductor de Video VLC")
        self.setGeometry(100, 100, 800, 600)

        # Crear una instancia de VLC
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Crear el widget de video (usamos QWidget como contenedor)
        self.video_widget = QWidget(self)
        self.player.set_hwnd(self.video_widget.winId())  # Vinculamos el widget al reproductor VLC

        # Crear los controles de la parte izquierda
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.toggle_play_pause)

        self.load_button = QPushButton("Cargar Video", self)
        self.load_button.clicked.connect(self.load_video)

        self.volume_label = QLabel("Volumen: 50", self)
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setValue(50)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Layout de los controles (izquierda)
        control_layout = QVBoxLayout()
        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.volume_label)
        control_layout.addWidget(self.volume_slider)

        # Layout principal (dividido entre video y controles)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.video_widget)
        control_widget = QWidget(self)
        control_widget.setLayout(control_layout)
        splitter.addWidget(control_widget)

        self.setCentralWidget(splitter)

        self.video_path = None

    def load_video(self):
        """Permite seleccionar un archivo de video y cargarlo en el reproductor."""
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Selecciona un video", "", "Videos (*.mp4 *.avi *.mov *.mkv)")
        
        if file_path:
            self.video_path = file_path
            self.load_and_play_video(file_path)

    def load_and_play_video(self, file_path):
        """Carga y reproduce el video desde el archivo seleccionado."""
        media = self.instance.media_new(file_path)
        self.player.set_media(media)
        self.player.play()

    def toggle_play_pause(self):
        """Alterna entre reproducir y pausar el video."""
        if self.player.is_playing():
            self.player.pause()
            self.play_button.setText("Play")
        else:
            if self.video_path:
                self.player.play()
                self.play_button.setText("Pause")

    def set_volume(self, value):
        """Ajusta el volumen del reproductor."""
        self.player.audio_set_volume(value)
        self.volume_label.setText(f"Volumen: {value}")

def main():
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
