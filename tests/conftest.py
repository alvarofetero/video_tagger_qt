import pytest
from PyQt5.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def qtbot(qapp, request):
    """Create a QtBot instance with proper pytest request object."""
    from pytestqt.qtbot import QtBot
    result = QtBot(qapp)
    result._request = request  # This fixes the 'node' attribute issue
    return result