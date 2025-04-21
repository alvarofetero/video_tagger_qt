from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog,
    QLineEdit, QProgressBar, QListWidget, QListWidgetItem, QSplitter, QLabel
)
from PyQt5.QtCore import Qt
from player import VideoPlayer
from exporter import ExporterThread

class VideoTaggerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Tagger")
        self.setMinimumSize(1000, 600)

        self.video_path = None
        self.output_directory = ""
        self.tags = []

        self.setup_ui()

    def setup_ui(self):
        # Splitter principal: izquierda controles, derecha video
        splitter = QSplitter(Qt.Horizontal, self)

        # 🎛️ Controles a la izquierda
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        self.load_button = QPushButton("📁 Cargar Video")
        self.load_button.clicked.connect(self.load_video)
        control_layout.addWidget(self.load_button)

        self.play_button = QPushButton("▶️ Play / Pause")
        self.play_button.clicked.connect(self.toggle_playback)
        control_layout.addWidget(self.play_button)

        self.start_tag_button = QPushButton("🔖 Marcar Inicio")
        self.start_tag_button.clicked.connect(self.mark_start)
        control_layout.addWidget(self.start_tag_button)

        self.end_tag_button = QPushButton("🏁 Marcar Fin")
        self.end_tag_button.clicked.connect(self.mark_end)
        control_layout.addWidget(self.end_tag_button)

        self.tag_list = QListWidget()
        control_layout.addWidget(QLabel("📝 Tags creados:"))
        control_layout.addWidget(self.tag_list)

        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Nombre base del archivo")
        control_layout.addWidget(self.filename_input)

        self.export_clip_button = QPushButton("💾 Exportar Clips")
        self.export_clip_button.clicked.connect(self.export_clips)
        control_layout.addWidget(self.export_clip_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        control_layout.addWidget(self.progress_bar)

        splitter.addWidget(control_panel)

        # 🎞️ Reproductor de video a la derecha
        self.video_player = VideoPlayer(self)
        splitter.addWidget(self.video_player)

        splitter.setSizes([300, 700])  # Anchos iniciales (izquierda, derecha)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(splitter)

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Video")
        if file_path:
            self.video_path = file_path
            self.video_player.load_video(file_path)

    def toggle_playback(self):
        if self.video_player.mediaplayer.is_playing():
            self.video_player.mediaplayer.pause()
        else:
            self.video_player.mediaplayer.play()

    def mark_start(self):
        if self.video_path:
            current_time = self.video_player.get_time()
            self.tags.append({"start": current_time, "end": None})
            self.update_tag_list()
            print(f"[TAG] Inicio en {current_time:.2f}s")

    def mark_end(self):
        if self.tags and self.tags[-1]["end"] is None:
            current_time = self.video_player.get_time()
            self.tags[-1]["end"] = current_time
            self.update_tag_list()
            print(f"[TAG] Fin en {current_time:.2f}s")

    def update_tag_list(self):
        self.tag_list.clear()
        for i, tag in enumerate(self.tags):
            start = f"{tag['start']:.2f}" if tag["start"] is not None else "?"
            end = f"{tag['end']:.2f}" if tag["end"] is not None else "?"
            self.tag_list.addItem(QListWidgetItem(f"{i+1}. Inicio: {start} | Fin: {end}"))

    def export_clips(self):
        if not self.tags or any(tag["end"] is None for tag in self.tags):
            print("⚠️ Algunos tags no tienen fin definido.")
            return

        if not self.output_directory:
            self.output_directory = QFileDialog.getExistingDirectory(self, "Selecciona la carpeta")

        if self.output_directory:
            filename_base = self.filename_input.text().strip() or "clip"
            self.progress_bar.setMaximum(len(self.tags))
            self.progress_bar.setValue(0)
            self.export_clip_button.setEnabled(False)

            self.export_thread = ExporterThread(
                self.tags, self.video_path, self.output_directory, filename_base
            )
            self.export_thread.progress.connect(self.progress_bar.setValue)
            self.export_thread.finished.connect(self.on_export_finished)
            self.export_thread.start()

    def on_export_finished(self):
        self.export_clip_button.setEnabled(True)
        print("✅ Exportación finalizada.")
