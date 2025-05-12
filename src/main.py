from PyQt5.QtWidgets import QApplication
from ui import VideoTaggerApp
import sys
import qdarkstyle

### Main function to run the application
# It initializes the QApplication, sets the style, creates an instance of VideoTaggerApp, and starts the event loop.
if __name__ == "__main__":
    app = QApplication(sys.argv) # Inicializa la aplicación
    app.setStyle("Fusion") # Estilo de la aplicación
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # Estilo oscuro de la aplicación
    
    window = VideoTaggerApp() # Instancia de la aplicación
    window.show()
    
    sys.exit(app.exec())
