from PyQt5.QtWidgets import (
    QDialog, QInputDialog, QMessageBox, QListWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QAction, QStyle
)
from PyQt5.QtCore import Qt

class MainWindowHelpers:
    """Encapsulates menu and dialog helpers for the main window."""

    def __init__(self, window, category_manager):
        self.window = window
        self.catman = category_manager

    def setup_menu(self):
        """Create application menu and connect actions to window methods / controls."""
        menubar = self.window.menuBar()

        archivo_menu = menubar.addMenu('Archivo')

        open_action = QAction(self.window.style().standardIcon(QStyle.SP_DialogOpenButton), 'Abrir Video', self.window)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.window.file_controls.load_video)
        archivo_menu.addAction(open_action)

        archivo_menu.addSeparator()

        save_action = QAction(self.window.style().standardIcon(QStyle.SP_CommandLink), 'Guardar Tags', self.window)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.window.file_controls.save_tags)
        archivo_menu.addAction(save_action)

        load_action = QAction('Cargar Tags', self.window)
        load_action.triggered.connect(self.window.file_controls.load_tags)
        archivo_menu.addAction(load_action)

        export_action = QAction(self.window.style().standardIcon(QStyle.SP_DialogSaveButton), 'Exportar Clip', self.window)
        export_action.triggered.connect(self.window.file_controls.export_clips)
        archivo_menu.addAction(export_action)
        archivo_menu.addSeparator()

        config_menu = menubar.addMenu('Configuración')
        categories_action = QAction('Categorías', self.window)
        categories_action.triggered.connect(self.edit_categories)
        config_menu.addAction(categories_action)

        time_settings_action = QAction('Ajustes de Tiempo', self.window)
        time_settings_action.triggered.connect(self.edit_time_settings)
        config_menu.addAction(time_settings_action)

        salir_action = QAction('Salir', self.window)
        salir_action.triggered.connect(self.window.close)
        archivo_menu.addSeparator()
        archivo_menu.addAction(salir_action)

    def edit_categories(self):
        """Dialog to add/remove categories. Uses window.tag_controls and CategoryManager."""
        dialog = QDialog(self.window)
        dialog.setWindowTitle("Edit Categories")
        layout = QVBoxLayout(dialog)

        category_list = QListWidget()
        category_list.addItems(self.catman.get())
        layout.addWidget(category_list)

        add_button = QPushButton("Add Category")
        def add_category():
            text, ok = QInputDialog.getText(dialog, "Add Category", "Category name:")
            if ok and text:
                name = text.strip()
                if not name:
                    QMessageBox.warning(dialog, "Warning", "Category name cannot be empty")
                    return
                if self.catman.add(name):
                    category_list.addItem(name)
                    # update UI model in main window
                    self.window.tag_controls.categories = self.catman.get()
                    self.window.tag_controls.update_category_buttons()
                else:
                    QMessageBox.warning(dialog, "Warning", "Category already exists or failed to save!")
        add_button.clicked.connect(add_category)
        layout.addWidget(add_button)

        remove_button = QPushButton("Remove Category")
        def remove_category():
            current = category_list.currentItem()
            if not current:
                return
            idx = category_list.row(current)
            category = category_list.item(idx).text()
            if category == getattr(self.window.tag_controls, "active_category", None):
                QMessageBox.warning(dialog, "Warning", "Cannot remove an active category")
                return
            if self.catman.remove(category):
                category_list.takeItem(idx)
                self.window.tag_controls.categories = self.catman.get()
                self.window.tag_controls.update_category_buttons()
            else:
                QMessageBox.warning(dialog, "Warning", "Failed to remove category")
        remove_button.clicked.connect(remove_category)
        layout.addWidget(remove_button)

        dialog.exec_()
        # ensure UI reflects any changes
        self.window.tag_controls.categories = self.catman.get()
        self.window.tag_controls.update_category_buttons()

    def edit_time_settings(self):
        """Dialog to edit pre/post time settings stored in tag_controls."""
        dialog = QDialog(self.window)
        dialog.setWindowTitle("Time Adjustment Settings")
        layout = QVBoxLayout(dialog)

        pre_layout = QHBoxLayout()
        pre_label = QLabel("Pre-tag duration (seconds):")
        pre_spin = QSpinBox()
        pre_spin.setRange(0, 10)
        pre_spin.setValue(self.window.tag_controls.pre_spin.value())
        pre_layout.addWidget(pre_label)
        pre_layout.addWidget(pre_spin)
        layout.addLayout(pre_layout)

        post_layout = QHBoxLayout()
        post_label = QLabel("Post-tag duration (seconds):")
        post_spin = QSpinBox()
        post_spin.setRange(0, 10)
        post_spin.setValue(self.window.tag_controls.post_spin.value())
        post_layout.addWidget(post_label)
        post_layout.addWidget(post_spin)
        layout.addLayout(post_layout)

        button_box = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        def on_accept():
            self.window.tag_controls.pre_spin.setValue(pre_spin.value())
            self.window.tag_controls.post_spin.setValue(post_spin.value())
            dialog.accept()

        ok_button.clicked.connect(on_accept)
        cancel_button.clicked.connect(dialog.reject)

        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)
        layout.addLayout(button_box)

        dialog.exec_()