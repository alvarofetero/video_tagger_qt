from PyQt5.QtWidgets import QWidget

class UIComponent:
    def __init__(self, parent=None):
        self.parent = parent

    def setup_ui(self, layout):
        raise NotImplementedError("Each UI component must implement setup_ui")