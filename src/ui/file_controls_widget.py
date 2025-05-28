from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QProgressBar, QHBoxLayout, 
                             QLabel,QGroupBox, QLineEdit, QComboBox, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from .base_component import UIComponent
from exporter import ExporterThread
from src.utils.logger import AppLogger

class FileControls(UIComponent):
    def __init__(self, parent=None, video_player=None, tags=None):
        super().__init__(parent)
        if video_player is None:
            raise ValueError("video_player must be provided")
        self.video_player = video_player
        self.tags = tags if tags is not None else []
        self.output_directory = None
        self.logger = AppLogger.get_logger()
        
        
    def setup_ui(self, layout):
        # Create main group box for file controls
        file_group = QGroupBox("File Controls")
        file_layout = QVBoxLayout(file_group)

         # File name input for exports
        self.filename_input = QLineEdit()  # Changed to match the name used in export_clips
        self.filename_input.setPlaceholderText("Enter base name for clips")
        file_layout.addWidget(QLabel("Export Filename:"))
        file_layout.addWidget(self.filename_input)

        # File type selection
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["MP4", "AVI", "MKV"])
        file_layout.addWidget(self.file_type_combo)

        # File size display
        self.file_size_label = QLabel("File Size: 0 MB")
        file_layout.addWidget(self.file_size_label)

        # Progress bar for exports
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        file_layout.addWidget(self.progress_bar)

        # Add the group box to the main layout
        layout.addWidget(file_group)

    # Cargar video desde el disco
    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "Seleccionar Video")
        # If a file was selected, update the video path and load the video
        if file_path:
            self.video_path = file_path
            self.video_player.load_video(file_path)

     ## Exportar los clips de video según los tags
    def export_clips(self):
        self.logger.info("[FileControls] Exporting clips...")
        self.logger.info("[FileControls] Tags to be exported : %s", self.tags)
        if not self.tags or any(tag["end"] is None for tag in self.tags):
            print("⚠️ Algunos tags no tienen fin definido.")
            return

        if not self.output_directory:
            self.output_directory = QFileDialog.getExistingDirectory(self.parent, "Selecciona la carpeta de salida")
            

        if self.output_directory:
            filename_base = self.filename_input.text().strip() or "clip"
            self.progress_bar.setMaximum(len(self.tags))
            self.progress_bar.setValue(0)
            #self.export_clip_button.setEnabled(False)

            self.export_thread = ExporterThread(
                self.tags, self.video_path, self.output_directory, filename_base
            )
            self.export_thread.progress.connect(self.progress_bar.setValue)
            self.export_thread.finished.connect(self.on_export_finished)
            self.export_thread.start()

    def on_export_finished(self):
        """Handler for when export thread finishes"""
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        #self.export_clip_button.setEnabled(True)
        
        # Show success message
        QMessageBox.information(
            self.parent,
            "Export Complete",
            f"All clips have been exported to:\n{self.output_directory}"
        )
        self.logger.info(f"Clips exported successfully to {self.output_directory}")

