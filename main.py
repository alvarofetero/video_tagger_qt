from PyQt5.QtWidgets import QApplication
from ui import VideoTaggerApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoTaggerApp()
    window.show()
    sys.exit(app.exec())
