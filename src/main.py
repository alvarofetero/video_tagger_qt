import sys
import os

# Add conditional import for Windows
if os.name == 'nt':  # Only on Windows
    import pythoncom
    pythoncom.CoInitialize() # Initialize COM for PyQt5

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from PyQt5.QtWidgets import QApplication
#from ui import VideoTaggerApp

import qdarkstyle
from src.ui.main_window import VideoTaggerApp


### Main function to run the application
# It initializes the QApplication, sets the style, creates an instance of VideoTaggerApp, and starts the event loop.
if __name__ == "__main__":
    
    app = QApplication(sys.argv) # Inicializa la aplicación

    # Apply dark theme
    app.setStyle("Fusion") # Estilo de la aplicación
    ##app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # Estilo oscuro de la aplicación
    style = qdarkstyle.load_stylesheet_pyqt5()
    # style += """
    #         QGroupBox {
    #             border: 2px solid #666;
    #             border-radius: 5px;
    #             margin-top: 1em;
    #             padding-top: 10px;
    #         }
    #         QGroupBox::title {
    #             subcontrol-origin: margin;
    #             left: 10px;
    #             padding: 0 3px;
    #             background-color: #444;
    #         }
    # """
    
    app.setStyleSheet(style)

    # Create and show the main window
    window = VideoTaggerApp() # Instancia de la aplicación
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

    if __name__ == "__main__":
        main()
