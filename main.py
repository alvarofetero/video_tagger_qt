import sys
import vlc
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QLabel, QSplitter, QListWidget, QLineEdit
from PyQt5.QtCore import Qt
import subprocess
import os

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

        # Botones de tags
        self.add_start_tag_button = QPushButton("Agregar Start Tag", self)
        self.add_start_tag_button.clicked.connect(self.add_start_tag)

        self.add_end_tag_button = QPushButton("Agregar End Tag", self)
        self.add_end_tag_button.clicked.connect(self.add_end_tag)

        self.export_clip_button = QPushButton("Exportar Clips", self)
        self.export_clip_button.clicked.connect(self.export_clips)

        # Cuadro de texto para el nombre del archivo exportado
        self.filename_input = QLineEdit(self)
        self.filename_input.setPlaceholderText("Nombre base para los archivos exportados")
        self.filename_input.setText("clip")  # Nombre base por defecto

        # Lista de tags
        self.tag_list = QListWidget(self)

        # Layout de los controles (izquierda)
        control_layout = QVBoxLayout()
        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.volume_label)
        control_layout.addWidget(self.volume_slider)
        control_layout.addWidget(self.add_start_tag_button)
        control_layout.addWidget(self.add_end_tag_button)
        control_layout.addWidget(self.filename_input)
        control_layout.addWidget(self.export_clip_button)
        control_layout.addWidget(self.tag_list)

        # Layout principal (dividido entre video y controles)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.video_widget)
        control_widget = QWidget(self)
        control_widget.setLayout(control_layout)
        splitter.addWidget(control_widget)

        self.setCentralWidget(splitter)

        self.video_path = None
        self.tags = []  # Lista para almacenar los momentos de los tags
        self.current_time = 0  # El tiempo actual del video
        self.is_start_tag = True  # Para controlar si estamos añadiendo el tag de inicio o fin
        self.output_directory = None  # Ruta para guardar el archivo

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

    def add_start_tag(self):
        """Agrega un tag de inicio en el momento actual del video."""
        self.current_time = self.player.get_time() / 1000  # Obtener el tiempo en segundos
        if self.is_start_tag:
            self.tags.append({"start": self.current_time, "end": None})  # Agregamos el tag de inicio
            self.tag_list.addItem(f"Start Tag en {self.current_time:.2f} segundos")
            self.is_start_tag = False  # Ahora esperamos el tag de fin
        else:
            print("Ya has agregado un tag de inicio. Ahora agrega un tag de fin.")

    def add_end_tag(self):
        """Agrega un tag de fin en el momento actual del video."""
        self.current_time = self.player.get_time() / 1000  # Obtener el tiempo en segundos
        if not self.is_start_tag:
            if len(self.tags) > 0 and self.tags[-1]["end"] is None:
                self.tags[-1]["end"] = self.current_time  # Asignamos el fin al último tag
                self.tag_list.addItem(f"End Tag en {self.current_time:.2f} segundos")
                self.is_start_tag = True  # Ahora esperamos el siguiente tag de inicio
            else:
                print("No hay un tag de inicio disponible para asociar un tag de fin.")
        else:
            print("Primero agrega un tag de inicio.")

    def export_clips(self):
        """Exporta todos los clips entre los pares de tags (start, end)."""
        if len(self.tags) == 0 or any(tag["end"] is None for tag in self.tags):
            print("No hay un par de tags completo para exportar.")
            return

        # Pedimos al usuario que seleccione la ubicación de guardado
        if not self.output_directory:
            self.output_directory = QFileDialog.getExistingDirectory(self, "Selecciona la carpeta para guardar los clips")
        
        if self.output_directory:
            # Usamos un nombre base para los archivos exportados
            filename_base = self.filename_input.text().strip()
            if not filename_base:
                filename_base = "clip"  # Si no se ha especificado un nombre, usamos el nombre base por defecto
            
            # Exportar cada clip
            for i, tag in enumerate(self.tags):
                if tag["end"]:
                    start_time = tag["start"]
                    end_time = tag["end"]
                    output_filename = f"{filename_base}_{i+1}.mp4"
                    output_path = os.path.join(self.output_directory, output_filename)

                    print(f"Exportando clip {i+1} desde {start_time:.2f} segundos hasta {end_time:.2f} segundos a {output_path}.")

                    # Usamos ffmpeg para cortar el video
                    command = [
                        "ffmpeg", "-i", self.video_path, 
                        "-ss", str(start_time), 
                        "-to", str(end_time), 
                        "-c:v", "libx264", "-c:a", "aac", 
                        "-strict", "experimental", output_path
                    ]
                    subprocess.run(command)
                    print(f"Clip {i+1} exportado como {output_path}.")
        else:
            print("No se seleccionó una carpeta para guardar los clips.")

def main():
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
