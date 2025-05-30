from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QProgressBar, QHBoxLayout, 
                             QLabel, QGroupBox, QLineEdit, QComboBox, QFileDialog, QMessageBox)
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
        self.export_threads = []

    def setup_ui(self, layout):
        # Create main group box for file controls
        file_group = QGroupBox("Export Controls")
        file_layout = QVBoxLayout(file_group)

        # Export button
        self.export_button = QPushButton("📤 Export Clips")
        self.export_button.clicked.connect(self.export_clips)
        file_layout.addWidget(self.export_button)

        # Progress section with better layout
        progress_group = QGroupBox("Export Progress")
        progress_layout = QVBoxLayout(progress_group)

        # Status message
        self.status_label = QLabel("")
        progress_layout.addWidget(self.status_label)

        # Overall progress
        overall_header = QHBoxLayout()
        self.progress_label = QLabel("Overall Progress:")
        overall_header.addWidget(self.progress_label)
        self.progress_percentage = QLabel("0%")
        overall_header.addWidget(self.progress_percentage)
        progress_layout.addLayout(overall_header)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        # Current clip section
        self.current_clip_label = QLabel("Processing:")
        progress_layout.addWidget(self.current_clip_label)
        
        clip_progress_layout = QHBoxLayout()
        
        # Clip name and progress in same row
        self.clip_name_label = QLabel("")
        clip_progress_layout.addWidget(self.clip_name_label, stretch=1)
        
        self.clip_progress_bar = QProgressBar()
        self.clip_progress_bar.setVisible(False)
        self.clip_progress_bar.setFixedWidth(100)  # Fixed width for the progress bar
        clip_progress_layout.addWidget(self.clip_progress_bar)
        
        self.clip_percentage = QLabel("0%")
        self.clip_percentage.setFixedWidth(40)  # Fixed width for percentage
        clip_progress_layout.addWidget(self.clip_percentage)
        
        progress_layout.addLayout(clip_progress_layout)

        file_layout.addWidget(progress_group)

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
        self.logger.info("[FileControls] Starting export process...")
        if not self.tags or any(tag["end"] is None for tag in self.tags):
            QMessageBox.warning(self.parent, "Warning", "⚠️ Some tags don't have an end time defined.")
            return

        if not self.video_path:
            self.logger.warning("No video loaded")
            QMessageBox.warning(self.parent, "Warning", "Please load a video first")
            return

        if not self.output_directory:
            self.output_directory = QFileDialog.getExistingDirectory(
                self.parent, 
                "Select Output Directory"
            )

        if self.output_directory:
            # Initialize progress UI
            self.status_label.setText("Export started... This may take a few minutes.")
            self.status_label.setStyleSheet("color: blue;")
            self.status_label.setVisible(True)
            
            self.progress_bar.setMaximum(100)
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            
            self.clip_progress_bar.setMaximum(100)
            self.clip_progress_bar.setValue(0)
            self.clip_progress_bar.setVisible(True)
            
            self.progress_label.setVisible(True)
            self.current_clip_label.setVisible(True)  # Fixed: using correct label reference
            self.clip_name_label.setVisible(True)
            self.clip_percentage.setVisible(True)
            self.progress_percentage.setVisible(True)
            
            self.export_button.setEnabled(False)
            
            # Clear any existing threads
            self.export_threads.clear()
            
            # Create export thread
            thread = ExporterThread(
                self.tags,
                self.video_path, 
                self.output_directory, 
                "clip"
            )
            
            thread.progress.connect(self.update_overall_progress)
            thread.clip_progress.connect(self.update_clip_progress)
            thread.finished.connect(lambda t=thread: self.on_thread_finished(t))
            
            self.export_threads.append(thread)
            thread.start()
            self.logger.info(f"Started export thread")

    def update_overall_progress(self, value):
        """Update the overall progress bar"""
        self.progress_bar.setValue(value)
        self.progress_percentage.setText(f"{value}%")
        # Force immediate update
        self.progress_bar.repaint()
        self.progress_percentage.repaint()

    def update_clip_progress(self, clip_index, value):
        """Update the current clip progress"""
        if clip_index < len(self.tags):
            clip = self.tags[clip_index]
            self.clip_name_label.setText(f"Processing: {clip['category']}_{clip_index + 1}")
            self.clip_name_label.repaint()
            
        self.clip_progress_bar.setValue(value)
        self.clip_percentage.setText(f"{value}%")
        # Force immediate update
        self.clip_progress_bar.repaint()
        self.clip_percentage.repaint()

    def on_thread_finished(self, thread):
        """Handle completion of export thread"""
        if thread in self.export_threads:
            self.export_threads.remove(thread)
            thread.deleteLater()
            
        if not self.export_threads:
            self.on_export_finished()

    def on_export_finished(self):
        """Handler for when all exports are finished"""
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.progress_percentage.setText("0%")
        
        self.clip_progress_bar.setVisible(False)
        self.clip_progress_bar.setValue(0)
        self.clip_percentage.setText("0%")
        self.clip_name_label.setText("")
        
        self.progress_label.setVisible(False)
        self.current_clip_label.setVisible(False)
        self.clip_name_label.setVisible(False)
        self.status_label.setVisible(False)
        
        self.export_button.setEnabled(True)
        
        QMessageBox.information(
            self.parent,
            "Export Complete",
            f"All clips have been exported to:\n{self.output_directory}"
        )
        self.logger.info(f"All clips exported successfully to {self.output_directory}")

    def set_tags(self, tags):
        """Update the tags list"""
        self.tags = tags
        self.export_button.setEnabled(bool(tags))

