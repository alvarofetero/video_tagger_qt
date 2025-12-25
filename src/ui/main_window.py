from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QInputDialog,
    QMessageBox, QListWidget, QSpinBox, QLineEdit, QComboBox,
      QGroupBox, QMainWindow, QSplitter, QMenuBar, QAction, QMenu, QStyle)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# from src.ui.base_component import UIComponent

from src.ui.video_player_controls_widget import PlayerControls
from src.ui.tag_widget import TagControls
from src.ui.file_controls_widget import FileControls
from src.ui.drawing_controls_widget import DrawingControls

from src.player import VideoPlayer
from src.utils.logger import AppLogger
from src.tag_manager import TagManager
from src.ui.main_window_helpers import setup_menu as build_menu, edit_categories as helper_edit_categories, edit_time_settings as helper_edit_time_settings

## Main application window for Video Tagger
## This class initializes the main window, sets up the UI components, and manages the application flow.
class VideoTaggerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = AppLogger.get_logger()
        self.logger.info("Starting Video Tagger application")
        self.setWindowTitle("Video Tagger")
        self.setMinimumSize(1000, 600)
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Initialize tag manager
        self.tag_manager = TagManager()

        # Initialize video player first
        self.video_player = VideoPlayer(self)
  
        # Initialize components
        self.player_controls = PlayerControls(self)
        self.tag_controls = TagControls(self)
        self.drawing_controls = DrawingControls(self)
        
         # Pass video_player to FileControls
        self.file_controls = FileControls(self, video_player=self.video_player, tags=self.tag_manager.get_tags())

        self.player_controls.set_video_player(self.video_player)  # Set the video player
        self.tag_controls.set_video_player(self.video_player)
        self.video_player.set_drawing_controls(self.drawing_controls)

        
        self.setup_ui()
        # build_menu extracted to helpers
        build_menu(self)
        self.setup_connections()
        
    # menu building moved to src/ui/main_window_helpers.py

    def setup_ui(self):
         # Main layout for central widget
        main_layout = QVBoxLayout(self.central_widget)

        # Main splitter
        splitter = QSplitter(Qt.Horizontal, self)
        
        # Left panel
        controls_panel = QWidget()
        control_layout = QVBoxLayout(controls_panel)

        self.addToolBar(Qt.TopToolBarArea, self.drawing_controls)
        self.drawing_controls.setAllowedAreas(Qt.AllToolBarAreas)
        
        # Add components
        self.player_controls.setup_ui(control_layout) ## call setup_ui on player_controls
        self.tag_controls.setup_ui(control_layout)  ## call setup_ui on tag_controls
        self.file_controls.setup_ui(control_layout) ## call setup_ui on file_controls
        # self.drawing_controls.setup_ui()
        
        # self.file_controls.set_video_player(self.video_player)
        # self.tag_controls.set_video_player(self.video_player)
        # self.player_controls.set_video_player(self.video_player)
        
        splitter.addWidget(controls_panel)
        splitter.addWidget(self.video_player)
        splitter.setSizes([200, 800])

        # Main layout
        main_layout.addWidget(splitter)

    def setup_connections(self):
        """
        Sets up signal-slot connections for the main window's UI components.

        This method connects various UI controls to their respective event handlers:
        - Connects the play button to toggle playback functionality.
        - Connects the rewind button to seek backward by a fixed duration.
        - Connects the forward button to seek forward by a fixed duration.
        """
        # Player controls
        self.player_controls.play_button.clicked.connect(self.video_player.toggle_playback)
        self.player_controls.rewind_button.clicked.connect(lambda: self.video_player.seek_relative(-5))
        self.player_controls.forward_button.clicked.connect(lambda: self.video_player.seek_relative(5))
        self.player_controls.speed_down_button.clicked.connect(lambda: self.video_player.change_speed(-0.25))
        self.player_controls.speed_up_button.clicked.connect(lambda: self.video_player.change_speed(0.25))
        
        # Tag controls
        self.tag_controls.tag_started.connect(self.on_tag_started)
        self.tag_controls.tag_ended.connect(self.on_tag_ended)

        # Update file controls when tags change
        self.tag_controls.tag_started.connect(lambda *args: self.file_controls.set_tags(self.tag_manager.get_tags()))
        self.tag_controls.tag_ended.connect(lambda *args: self.file_controls.set_tags(self.tag_manager.get_tags()))

    def on_tag_started(self, category, start_time):
        self.tag_manager.add_start(start_time, category)
        self.tag_controls.update_tag_list(self.tag_manager.get_tags())
        self.logger.info(f"[VideoTaggerApp] Started tag for {category} at {start_time:.2f}s")

    def on_tag_ended(self, category, end_time):
        self.tag_manager.add_end(end_time)
        self.tag_controls.update_tag_list(self.tag_manager.get_tags())
        self.logger.info(f"[VideoTaggerApp] Ended tag for {category} at {end_time:.2f}s")

    def edit_categories(self):
        """Wrapper that delegates to common helper (keeps call sites intact)."""
        helper_edit_categories(self)

    def _save_categories_to_file(self):
        """Save current categories back to the JSON file"""
        import os
        import json
        categories_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "categories.json")
        try:
            with open(categories_path, 'w', encoding='utf-8') as f:
                json.dump(self.tag_controls.categories, f, indent=4, ensure_ascii=False)
            self.logger.info("Categories saved successfully to categories.json")
        except Exception as e:
            self.logger.error(f"Error saving categories: {e}")
            QMessageBox.warning(self, "Error", "Failed to save categories to file.")
  
    def edit_time_settings(self):
        """Wrapper that delegates to common helper (keeps call sites intact)."""
        helper_edit_time_settings(self)
