import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

def pytest_configure(config):
    """Disable Qt debug messages and configure test environment"""
    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_Use96Dpi)

@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([''])
        app.setQuitOnLastWindowClosed(False)  # Prevent app from quitting when windows close
    
    yield app
    
    # Ensure proper cleanup
    if app is not None:
        app.quit()
        app.processEvents()  # Process any pending events before quitting

@pytest.fixture
def qtbot(qapp, request):
    """Create a QtBot instance with proper pytest request object."""
    from pytestqt.qtbot import QtBot
    result = QtBot(qapp)
    result._request = request  # This fixes the 'node' attribute issue
    return result

@pytest.fixture(autouse=True)
def cleanup_qt():
    """Cleanup Qt resources after each test"""
    yield
    QApplication.processEvents()  # Process any pending events