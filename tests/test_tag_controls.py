import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from src.ui.tag_widget import TagControls

def test_tag_controls_init(qtbot):
    """Test that tag controls initialize correctly"""
    controls = TagControls()
    qtbot.addWidget(controls)
    
    assert controls.active_category is None
    assert len(controls.categories) > 0
    assert controls.category_buttons == {}  # Should be empty before setup_ui

def test_category_buttons_creation(qtbot, qapp):
    """Test that category buttons are created with correct properties"""
    controls = TagControls()
    qtbot.addWidget(controls)
    
    # Create a layout for testing
    from PyQt5.QtWidgets import QVBoxLayout
    layout = QVBoxLayout()
    controls.setup_ui(layout)
    
    # Verify buttons were created for each category
    assert len(controls.category_buttons) == len(controls.categories)
    
    # Check first button properties
    first_category = controls.categories[0]
    button = controls.category_buttons[first_category]
    assert button.text() == f"1. {first_category}"
    assert button.property("category") == first_category
    assert button.property("index") == 1

def test_keyboard_shortcuts(qtbot, qapp):
    """Test that keyboard shortcuts trigger category buttons"""
    controls = TagControls()
    qtbot.addWidget(controls)
    
    # Create a layout for testing
    from PyQt5.QtWidgets import QVBoxLayout, QWidget
    container = QWidget()
    layout = QVBoxLayout(container)
    controls.setup_ui(layout)
    
    # Mock video player
    class MockVideoPlayer:
        def get_time(self):
            return 10.0  # Mock 10 seconds
    controls.video_player = MockVideoPlayer()
    
    # Track signals
    signals_received = []
    controls.tag_started.connect(lambda cat, time: signals_received.append((cat, time)))
    
    # First category should have shortcut '1'
    first_category = controls.categories[0]
    
    # Show the widget (required for shortcuts to work)
    container.show()
    qtbot.wait_for_window_shown(container)
    
    # Press the '1' key
    qtbot.keyPress(container, '1')
    qtbot.wait(100)  # Give time for event to process
    
    # Verify signal was emitted with correct category and adjusted time
    assert len(signals_received) == 1, "Tag start signal not emitted"
    category, time = signals_received[0]
    assert category == first_category
    assert time == 9.0  # 10s - 1s pre-tag duration

def test_tag_creation_flow(qtbot):
    """Test the complete flow of creating a tag"""
    controls = TagControls()
    qtbot.addWidget(controls)
    
    # Create a layout for testing
    from PyQt5.QtWidgets import QVBoxLayout
    layout = QVBoxLayout()
    controls.setup_ui(layout)
    
    # Mock video player
    class MockVideoPlayer:
        def get_time(self):
            return 10.0  # Mock 10 seconds
    controls.video_player = MockVideoPlayer()
    
    # Track signals
    start_signals = []
    end_signals = []
    
    controls.tag_started.connect(lambda cat, time: start_signals.append((cat, time)))
    controls.tag_ended.connect(lambda cat, time: end_signals.append((cat, time)))
    
    # Start tag
    first_category = controls.categories[0]
    first_button = controls.category_buttons[first_category]
    qtbot.mouseClick(first_button, Qt.LeftButton)
    
    assert len(start_signals) == 1
    assert start_signals[0][0] == first_category
    assert start_signals[0][1] == 9.0  # 10s - 1s pre-tag duration
    
    # End tag
    qtbot.mouseClick(first_button, Qt.LeftButton)
    
    assert len(end_signals) == 1
    assert end_signals[0][0] == first_category
    assert end_signals[0][1] == 11.0  # 10s + 1s post-tag duration