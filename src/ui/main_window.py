from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QInputDialog,
    QMessageBox, QListWidget, QSpinBox, QLineEdit, QComboBox,
      QGroupBox, QMainWindow, QSplitter, QMenuBar, QAction, QMenu)

from PyQt5.QtCore import Qt
from .base_component import UIComponent

from src.player import VideoPlayer
from ui.video_player_controls_widget import PlayerControls
from src.ui.tag_widget import TagControls
from src.ui.file_controls_widget import FileControls
from src.utils.logger import AppLogger

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

        # Initialize video player first
        self.video_player = VideoPlayer(self)
  
        # Initialize components
        self.player_controls = PlayerControls(self)
        self.tag_controls = TagControls(self)
        self.video_player = VideoPlayer(self)
         # Pass video_player to FileControls
        self.file_controls = FileControls(self, video_player=self.video_player)

        self.player_controls.set_video_player(self.video_player)  # Set the video player
        
        self.setup_ui()
        self.setup_menu()
        self.setup_connections()

    def setup_menu(self):
        """Setup the application menu bar"""
        menubar = self.menuBar()
        
        # Archivo menu
        archivo_menu = menubar.addMenu('Archivo')
        open_action = QAction('Abrir Video', self)
        open_action.triggered.connect(self.file_controls.load_video)
        archivo_menu.addAction(open_action)
        
        # Configuración menu
        config_menu = menubar.addMenu('Configuración')
        categories_action = QAction('Categorías', self)
        categories_action.triggered.connect(self.edit_categories)
        config_menu.addAction(categories_action)
        
        # Salir action
        salir_action = QAction('Salir', self)
        salir_action.triggered.connect(self.close)
        archivo_menu.addSeparator()
        archivo_menu.addAction(salir_action)


    def setup_ui(self):
         # Main layout for central widget
        main_layout = QVBoxLayout(self.central_widget)

        # Main splitter
        splitter = QSplitter(Qt.Horizontal, self)
        
        # Left panel
        controls_panel = QWidget()
        control_layout = QVBoxLayout(controls_panel)
        
        # Add components
        self.player_controls.setup_ui(control_layout)
        self.tag_controls.setup_ui(control_layout)
        self.file_controls.setup_ui(control_layout)
        
        splitter.addWidget(controls_panel)
        splitter.addWidget(self.video_player)
        splitter.setSizes([300, 700])

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
        # ...more connections...

    def edit_categories(self):
        """Open a dialog to edit tag categories"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Categories")
        layout = QVBoxLayout(dialog)

        # Create list widget for categories
        category_list = QListWidget()
        category_list.addItems(self.tag_controls.categories)
        layout.addWidget(category_list)

        # Add category button
        add_button = QPushButton("Add Category")
        def add_category():
            text, ok = QInputDialog.getText(dialog, "Add Category", "Category name:")
            if ok and text:
                if text not in self.tag_controls.categories:
                    self.tag_controls.categories.append(text)
                    category_list.addItem(text)
                else:
                    QMessageBox.warning(dialog, "Warning", "Category already exists!")

        add_button.clicked.connect(add_category)
        layout.addWidget(add_button)

        # Remove category button
        remove_button = QPushButton("Remove Category")
        def remove_category():
            current = category_list.currentItem()
            if current:
                idx = category_list.row(current)
                category = self.tag_controls.categories[idx]
                self.tag_controls.categories.remove(category)
                category_list.takeItem(idx)

        remove_button.clicked.connect(remove_category)
        layout.addWidget(remove_button)

        # Show dialog
        dialog.exec_()
        
        # Update tag controls after dialog closes
        self.tag_controls.update_category_buttons()