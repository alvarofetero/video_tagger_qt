from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QInputDialog,
    QMessageBox, QListWidget, QSpinBox, QLineEdit, QComboBox,
      QGroupBox, QMainWindow, QSplitter, QMenuBar, QAction, QMenu, QStyle)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from src.ui.base_component import UIComponent
from src.player import VideoPlayer
from src.ui.video_player_controls_widget import PlayerControls
from src.ui.tag_widget import TagControls
from src.ui.file_controls_widget import FileControls
from src.utils.logger import AppLogger
from src.tag_manager import TagManager

## Main application window for Video Tagger
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
        
         # Pass video_player to FileControls
        self.file_controls = FileControls(self, video_player=self.video_player, tags=self.tag_manager.get_tags())

        self.player_controls.set_video_player(self.video_player)  # Set the video player
        self.tag_controls.set_video_player(self.video_player)

        
        self.setup_ui()
        self.setup_menu()
        self.setup_connections()

    def setup_menu(self):
        """Setup the application menu bar"""
        menubar = self.menuBar()
        
        # Archivo menu
        archivo_menu = menubar.addMenu('Archivo')
        
        #Open video action
        open_action = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), 'Abrir Video', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.file_controls.load_video) # Connect to load_video method
        archivo_menu.addAction(open_action)
        
        archivo_menu.addSeparator()

        # Save tags action
        save_action = QAction(self.style().standardIcon(QStyle.SP_CommandLink), 'Guardar Tags', self)
        save_action.setShortcut('Ctrl+S')
        #save_action.triggered.connect(self.save_tags)
        #save_action.triggered.connect(self.file_controls.save_tags)
        archivo_menu.addAction(save_action)


        load_action = QAction('Cargar Tags', self)
        #load_action.triggered.connect(self.file_controls.load_tags) 
        archivo_menu.addAction(load_action)
        export_action = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton),'Exportar Clip', self)
        export_action.triggered.connect(self.file_controls.export_clips)
        archivo_menu.addAction(export_action)
        archivo_menu.addSeparator()

        
        # Configuración menu
        config_menu = menubar.addMenu('Configuración')
        categories_action = QAction('Categorías', self)
        categories_action.triggered.connect(self.edit_categories)
        config_menu.addAction(categories_action)

        time_settings_action = QAction('Ajustes de Tiempo', self)
        time_settings_action.triggered.connect(self.edit_time_settings)
        config_menu.addAction(time_settings_action)
        
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
        self.player_controls.setup_ui(control_layout) ## call setup_ui on player_controls
        self.tag_controls.setup_ui(control_layout)  ## call setup_ui on tag_controls
        self.file_controls.setup_ui(control_layout) ## call setup_ui on file_controls
        
        # self.file_controls.set_video_player(self.video_player)
        # self.tag_controls.set_video_player(self.video_player)
        # self.player_controls.set_video_player(self.video_player)
        
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

    def edit_time_settings(self):
        """Open a dialog to edit time adjustment settings"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Time Adjustment Settings")
        layout = QVBoxLayout(dialog)

        # Create spinboxes for time adjustments
        pre_layout = QHBoxLayout()
        pre_label = QLabel("Pre-tag duration (seconds):")
        pre_spin = QSpinBox()
        pre_spin.setRange(0, 10)
        pre_spin.setValue(self.tag_controls.pre_spin.value())
        pre_layout.addWidget(pre_label)
        pre_layout.addWidget(pre_spin)
        layout.addLayout(pre_layout)

        post_layout = QHBoxLayout()
        post_label = QLabel("Post-tag duration (seconds):")
        post_spin = QSpinBox()
        post_spin.setRange(0, 10)
        post_spin.setValue(self.tag_controls.post_spin.value())
        post_layout.addWidget(post_label)
        post_layout.addWidget(post_spin)
        layout.addLayout(post_layout)

        # OK/Cancel buttons
        button_box = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        def on_accept():
            self.tag_controls.pre_spin.setValue(pre_spin.value())
            self.tag_controls.post_spin.setValue(post_spin.value())
            dialog.accept()
            
        ok_button.clicked.connect(on_accept)
        cancel_button.clicked.connect(dialog.reject)
        
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)
        layout.addLayout(button_box)

        dialog.exec_()