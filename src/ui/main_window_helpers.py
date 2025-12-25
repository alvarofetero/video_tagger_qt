from PyQt5.QtWidgets import (
    QDialog, QInputDialog, QMessageBox, QListWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
)
from PyQt5.QtWidgets import QAction, QStyle
from PyQt5.QtCore import Qt
import os
import json

def setup_menu(window):
    """Create application menu and connect actions to window methods / controls."""
    menubar = window.menuBar()

    archivo_menu = menubar.addMenu('Archivo')

    open_action = QAction(window.style().standardIcon(QStyle.SP_DialogOpenButton), 'Abrir Video', window)
    open_action.setShortcut('Ctrl+O')
    open_action.triggered.connect(window.file_controls.load_video)
    archivo_menu.addAction(open_action)

    archivo_menu.addSeparator()

    save_action = QAction(window.style().standardIcon(QStyle.SP_CommandLink), 'Guardar Tags', window)
    save_action.setShortcut('Ctrl+S')
    save_action.triggered.connect(window.file_controls.save_tags)
    archivo_menu.addAction(save_action)

    load_action = QAction('Cargar Tags', window)
    load_action.triggered.connect(window.file_controls.load_tags)
    archivo_menu.addAction(load_action)

    export_action = QAction(window.style().standardIcon(QStyle.SP_DialogSaveButton), 'Exportar Clip', window)
    export_action.triggered.connect(window.file_controls.export_clips)
    archivo_menu.addAction(export_action)
    archivo_menu.addSeparator()

    config_menu = menubar.addMenu('Configuración')
    categories_action = QAction('Categorías', window)
    categories_action.triggered.connect(lambda: edit_categories(window))
    config_menu.addAction(categories_action)

    time_settings_action = QAction('Ajustes de Tiempo', window)
    time_settings_action.triggered.connect(lambda: edit_time_settings(window))
    config_menu.addAction(time_settings_action)

    salir_action = QAction('Salir', window)
    salir_action.triggered.connect(window.close)
    archivo_menu.addSeparator()
    archivo_menu.addAction(salir_action)


def edit_categories(window):
    """Dialog to add/remove categories. Uses window.tag_controls and window._save_categories_to_file()."""
    dialog = QDialog(window)
    dialog.setWindowTitle("Edit Categories")
    layout = QVBoxLayout(dialog)

    category_list = QListWidget()
    category_list.addItems(window.tag_controls.categories)
    layout.addWidget(category_list)

    add_button = QPushButton("Add Category")
    def add_category():
        text, ok = QInputDialog.getText(dialog, "Add Category", "Category name:")
        if ok and text:
            name = text.strip()
            if not name:
                QMessageBox.warning(dialog, "Warning", "Category name cannot be empty")
                return
            if name not in window.tag_controls.categories:
                window.tag_controls.categories.append(name)
                category_list.addItem(name)
                window.tag_controls.update_category_buttons()
                # Save changes to categories.json via main window helper
                window._save_categories_to_file()
            else:
                QMessageBox.warning(dialog, "Warning", "Category already exists!")
    add_button.clicked.connect(add_category)
    layout.addWidget(add_button)

    remove_button = QPushButton("Remove Category")
    def remove_category():
        current = category_list.currentItem()
        if not current:
            return
        idx = category_list.row(current)
        category = window.tag_controls.categories[idx]
        if category == getattr(window.tag_controls, "active_category", None):
            QMessageBox.warning(dialog, "Warning", "Cannot remove an active category")
            return
        window.tag_controls.categories.remove(category)
        category_list.takeItem(idx)
        window.tag_controls.update_category_buttons()
        window._save_categories_to_file()
    remove_button.clicked.connect(remove_category)
    layout.addWidget(remove_button)

    dialog.exec_()
    # ensure UI reflects any changes
    window.tag_controls.update_category_buttons()


def edit_time_settings(window):
    """Dialog to edit pre/post time settings stored in tag_controls."""
    dialog = QDialog(window)
    dialog.setWindowTitle("Time Adjustment Settings")
    layout = QVBoxLayout(dialog)

    pre_layout = QHBoxLayout()
    pre_label = QLabel("Pre-tag duration (seconds):")
    pre_spin = QSpinBox()
    pre_spin.setRange(0, 10)
    pre_spin.setValue(window.tag_controls.pre_spin.value())
    pre_layout.addWidget(pre_label)
    pre_layout.addWidget(pre_spin)
    layout.addLayout(pre_layout)

    post_layout = QHBoxLayout()
    post_label = QLabel("Post-tag duration (seconds):")
    post_spin = QSpinBox()
    post_spin.setRange(0, 10)
    post_spin.setValue(window.tag_controls.post_spin.value())
    post_layout.addWidget(post_label)
    post_layout.addWidget(post_spin)
    layout.addLayout(post_layout)

    button_box = QHBoxLayout()
    ok_button = QPushButton("OK")
    cancel_button = QPushButton("Cancel")

    def on_accept():
        window.tag_controls.pre_spin.setValue(pre_spin.value())
        window.tag_controls.post_spin.setValue(post_spin.value())
        dialog.accept()

    ok_button.clicked.connect(on_accept)
    cancel_button.clicked.connect(dialog.reject)

    button_box.addWidget(ok_button)
    button_box.addWidget(cancel_button)
    layout.addLayout(button_box)

    dialog.exec_()