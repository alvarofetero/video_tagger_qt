from PyQt5.QtCore import QObject

### Base class for all UI components in the application
class UIComponent(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)  # Initialize QObject
        self.parent = parent

    def setup_ui(self, layout):
        raise NotImplementedError("Each UI component must implement setup_ui")