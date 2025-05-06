from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog,
    QLineEdit, QProgressBar, QListWidget, QListWidgetItem, QSplitter, QLabel, QComboBox
)
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMenuBar, QToolBar, QStatusBar
from PyQt5.QtCore import Qt

import json

from PyQt5.QtWidgets import QInputDialog, QMessageBox

from player import VideoPlayer
from exporter import ExporterThread
from config import load_categories
from timeline import TimelineWidget
from tag_manager import TagManager

class VideoTaggerApp(QWidget):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Tagger")
        self.setMinimumSize(1000, 600)

        # Inicializar variables
        self.video_path = None
        self.output_directory = ""
        self.tags = [] #eliminar, se usará el tag_manager 
        self.tag_manager = TagManager()

        # Llama al método que agrega la barra de menú
        self._create_menu_bar()
        
        self.setup_ui()

    def setup_ui(self):
        # Splitter principal: izquierda controles, derecha video
        splitter = QSplitter(Qt.Horizontal, self)

        # 🎛️ Controles a la izquierda
        controls_panel = QWidget()
        control_layout = QVBoxLayout(controls_panel)

        ## Botones de control
        self.load_button = QPushButton("📁 Cargar Video")
        self.load_button.clicked.connect(self.load_video)
        
        ## Añadir botones al layout
        control_layout.addWidget(self.load_button)

        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Nombre base del archivo")
        control_layout.addWidget(self.filename_input)

        self.export_clip_button = QPushButton("💾 Exportar Clips")
        self.export_clip_button.clicked.connect(self.export_clips)
        control_layout.addWidget(self.export_clip_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        control_layout.addWidget(self.progress_bar)

        splitter.addWidget(controls_panel) # Añadir panel de controles al splitter

        # 🎞️ Reproductor de video a la derecha
        self.video_player = VideoPlayer(self)
        splitter.addWidget(self.video_player) # Añadir reproductor de video al splitter
       
        

        splitter.setSizes([300, 700])  # Anchos iniciales (izquierda, derecha)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(splitter) # Añadir splitter al layout principal

        self.add_UI_PlayerControlsSection(control_layout) # Añadir sección de controles al layout de controles
        self.add_UI_TagSection(control_layout) # Añadir sección de tags al layout de controles

        

    def add_UI_PlayerControlsSection(self, layout):
        # Añadir la sección de controles al layout principal
        player_controls = QWidget()
        player_layout = QVBoxLayout(player_controls)

        # Añadir los botones de control al layout
        player_layout.addWidget(QLabel("🎮 Controles de Reproducción:"))
        self.play_button = QPushButton("▶️ Play / Pause")
        self.play_button.clicked.connect(self.toggle_playback)
        player_layout.addWidget(self.play_button)

        # Botones de velocidad de reproducción
        speed_layout = QHBoxLayout()
        self.speed_down_button = QPushButton("⏪ -")
        self.speed_down_button.clicked.connect(lambda: self.change_speed(-0.25))

        self.speed_up_button = QPushButton("⏩ +")
        self.speed_up_button.clicked.connect(lambda: self.change_speed(0.25))
        
        speed_layout.addWidget(self.speed_down_button)
        speed_layout.addWidget(self.speed_up_button)

        # Mostrar velocidad actual
        self.speed_label = QLabel("🔁 Velocidad: 1.00x")
        self.speed_label.setAlignment(Qt.AlignCenter)
        speed_layout.addWidget(self.speed_label)

        # Añadir el panel de controles al layout principal
        layout.addWidget(player_controls)

        # Añadir el layout de velocidad al layout de controles
        layout.addLayout(speed_layout)

    ## Método para añadir la sección de tags al layout de controles
    ## Se encarga de crear la sección de tags en la UI
    ## y añadir los botones y controles necesarios para manejar los tags
    def add_UI_TagSection(self, layout):
        # Añadir la sección de tags al layout principal
        tag_section = QWidget()
        tag_layout = QVBoxLayout(tag_section)

        tag_layout.addWidget(QLabel("🛠️ Herramientas de Tag:"))

        self.category_box = QComboBox()
        self.category_box.addItems(load_categories())
        tag_layout.addWidget(QLabel("Categoría:"))
        tag_layout.addWidget(self.category_box)

        self.start_tag_button = QPushButton("🔖 Marcar Inicio")
        self.start_tag_button.clicked.connect(self.mark_start)

        self.end_tag_button = QPushButton("🏁 Marcar Fin")
        self.end_tag_button.clicked.connect(self.mark_end)

        tag_layout.addWidget(self.start_tag_button)
        tag_layout.addWidget(self.end_tag_button)

        ## Lista de tags
        self.tag_list = QListWidget()
        tag_layout.addWidget(QLabel("📝 Tags creados:"))
        tag_layout.addWidget(self.tag_list)

        # Botones de manejo de tags
        tag_controls_layout = QHBoxLayout()

        self.delete_tag_button = QPushButton("🗑️ Eliminar Tag")
        self.delete_tag_button.clicked.connect(self.delete_selected_tag)
        tag_controls_layout.addWidget(self.delete_tag_button)

        self.save_tags_button = QPushButton("💾 Guardar Tags")
        self.save_tags_button.clicked.connect(self.save_tags)
        tag_controls_layout.addWidget(self.save_tags_button)

        self.load_tags_button = QPushButton("📂 Cargar Tags")
        self.load_tags_button.clicked.connect(self.load_tags)
        tag_controls_layout.addWidget(self.load_tags_button)

        tag_layout.addLayout(tag_controls_layout)

        self.timeline = TimelineWidget(
        get_duration=lambda: self.video_player.mediaplayer.get_length() / 1000.0,
        get_tags=lambda: self.tags
        )
        self.timeline.tag_clicked.connect(self.seek_to_tag)
        
        self.video_player.time_changed.connect(self.timeline.set_current_time)
        
        layout.addWidget(QLabel("📊 Línea de tiempo de tags:"))
        layout.addWidget(self.timeline)

        # Añadir la sección de tags al layout principal
        layout.addWidget(tag_section)


    def _create_menu_bar(self):

        menubar = QMenuBar(self)

        # Menú Archivo
        file_menu = menubar.addMenu("Archivo")

        # Acción: Cargar Video
        load_action = QAction("Cargar Video", self)
        load_action.triggered.connect(self.load_video)
        file_menu.addAction(load_action)

        # Acción: Exportar Clips
        export_action = QAction("Exportar Clips", self)
        export_action.triggered.connect(self.export_clips)
        file_menu.addAction(export_action)

        # Acción: Guardar Tags
        save_tags_action = QAction("Guardar Tags", self)
        save_tags_action.triggered.connect(self.save_tags)
        file_menu.addAction(save_tags_action)

        # Acción: Cargar Tags
        load_tags_action = QAction("Cargar Tags", self)
        load_tags_action.triggered.connect(self.load_tags)
        file_menu.addAction(load_tags_action)


    def add_splitter_to_layout(self, layout):
        # Añadir el splitter al layout principal
        layout.addWidget(self.splitter)
            

    ## Método para buscar un tag específico en la línea de tiempo
    ## y reproducir el video desde ese punto
    def seek_to_tag(self, time_seconds):
        self.video_player.set_time(time_seconds)
        self.video_player.mediaplayer.play()
        print(f"🎯 Saltando a tag en {time_seconds:.2f}s")


    # Cargar video desde el disco
    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Video")
        if file_path:
            self.video_path = file_path
            self.video_player.load_video(file_path)

    ## Reproducir / Pausar el video
    def toggle_playback(self):
        if self.video_player.mediaplayer.is_playing():
            self.video_player.mediaplayer.pause()
        else:
            self.video_player.mediaplayer.play()

    # Marcar el inicio y fin de un tag
    def mark_start(self):
        if self.video_path:
            category = self.category_box.currentText()
            if not category:
                QMessageBox.warning(self, "Error", "Selecciona una categoría.")
                return
            # Ajustar el tiempo de inicio al segundo anterior
            current_time = self.video_player.get_time()
            adjusted_time = max(0, current_time - 1.0)  # Resta 1 segundo, sin ir a negativo
            self.tags.append({"start": adjusted_time, "end": None})
            self.update_tag_list()
            self.timeline.update()
            self.tag_manager.add_start(adjusted_time, category)
            
    def mark_end(self):
        if self.tags and self.tags[-1]["end"] is None:
            current_time = self.video_player.get_time()
            self.tags[-1]["end"] = current_time
            self.update_tag_list()
            print(f"[TAG] Fin en {current_time:.2f}s")
            self.timeline.update()

    # Actualizar la lista de tags en la UI
    def update_tag_list(self):
        self.tag_list.clear()
        for i, tag in enumerate(self.tags):
            start = f"{tag['start']:.2f}" if tag["start"] is not None else "?"
            end = f"{tag['end']:.2f}" if tag["end"] is not None else "?"
            self.tag_list.addItem(QListWidgetItem(f"{i+1}. Inicio: {start} | Fin: {end}"))

    # for i, tag in enumerate(self.tag_manager.get_tags()):
    # self.table.setItem(i, 0, QTableWidgetItem(f"{tag['start']:.2f}"))
    # self.table.setItem(i, 1, QTableWidgetItem(f"{tag['end']:.2f}" if tag["end"] else ""))
    # self.table.setItem(i, 2, QTableWidgetItem(tag["category"]))
        

    ## Eliminar el tag seleccionado
    def delete_selected_tag(self):
        current_row = self.tag_list.currentRow()
        if current_row >= 0:
            del self.tags[current_row]
            self.update_tag_list()
            self.timeline.update()

    ## Guardar los tags en un archivo JSON
    def save_tags(self):
        if not self.tags:
            QMessageBox.information(self, "Info", "No hay tags para guardar.")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Tags", filter="JSON Files (*.json)")
        if file_path:
            with open(file_path, "w") as f:
                json.dump(self.tags, f, indent=2)
            QMessageBox.information(self, "Guardado", "Tags guardados correctamente.")
            self.timeline.update()

    ## Cargar los tags desde un archivo JSON
    def load_tags(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar Tags", filter="JSON Files (*.json)")
        if file_path:
            with open(file_path, "r") as f:
                self.tags = json.load(f)
            self.update_tag_list()
            QMessageBox.information(self, "Cargado", "Tags cargados correctamente.")
            self.timeline.update()

    ## Cambiar la velocidad de reproducción
    def change_speed(self, delta):
        current = self.video_player.mediaplayer.get_rate()
        new_rate = max(0.25, min(4.0, current + delta))
        self.video_player.mediaplayer.set_rate(new_rate)
        self.speed_label.setText(f"🔁 Velocidad: {new_rate:.2f}x")
        print(f"🎚️ Velocidad: {new_rate:.2f}x")

            
    ## Exportar los clips de video según los tags
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

    ## Callback cuando la exportación termina
    def on_export_finished(self):
        self.export_clip_button.setEnabled(True)
        print("✅ Exportación finalizada.")
