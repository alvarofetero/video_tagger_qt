import unittest
import pytest
from PyQt5.QtWidgets import QApplication, QSplitter
from PyQt5.QtCore import Qt, QTimer

@pytest.mark.usefixtures("qapp", "cleanup_qt")
class TestVideoTaggerAppUI(unittest.TestCase):
    def setUp(self):
        from src.ui import VideoTaggerApp
        # Create window in the next event loop iteration
        QTimer.singleShot(0, self._create_window)
        QApplication.processEvents()

    def _create_window(self):
        """Create the main window in a way that's safe for the event loop"""
        self.window = VideoTaggerApp()
        self.window.setAttribute(Qt.WA_DontShowOnScreen)  # Don't actually show the window
        self.window.show()  # Still need to call show() to initialize some internals
        QApplication.processEvents()  # Process any pending events

    def test_ui_elements_exist(self):
        """Test that essential UI components exist"""
        if not hasattr(self, 'window'):
            self.skipTest("Window not properly initialized")
            
        # Process events before checking components
        QApplication.processEvents()
        
        # Test if player controls are created
        self.assertIsNotNone(self.window.player_controls, "Player controls not created")
        self.assertIsNotNone(self.window.player_controls.play_button, "Play button not created")
        self.assertIsNotNone(self.window.player_controls.rewind_button, "Rewind button not created")
        self.assertIsNotNone(self.window.player_controls.forward_button, "Forward button not created")
        
        # Test if tag controls are created
        self.assertIsNotNone(self.window.tag_controls, "Tag controls not created")
        self.assertIsNotNone(self.window.tag_controls.tag_list, "Tag list not created")
        
        # Test if video player exists
        self.assertIsNotNone(self.window.video_player, "Video player not created")
        
        # Test if file controls exist
        self.assertIsNotNone(self.window.file_controls, "File controls not created")

    def test_ui_layout(self):
        """Test the main window layout structure"""
        if not hasattr(self, 'window'):
            self.skipTest("Window not properly initialized")
            
        # Process events before checking layout
        QApplication.processEvents()
        
        # Test if the main window has a central widget
        self.assertIsNotNone(self.window.central_widget, "Central widget not created")
        
        # Test if there is exactly one splitter in the main layout
        splitter_widgets = self.window.central_widget.findChildren(QSplitter)
        self.assertEqual(len(splitter_widgets), 1, "Splitter not created or incorrect number of widgets")
        
        # Test if the splitter has exactly two widgets (controls panel and video player)
        splitter = splitter_widgets[0]
        self.assertEqual(splitter.count(), 2, "Splitter does not contain two widgets")

    def tearDown(self):
        if hasattr(self, 'window'):
            QApplication.processEvents()  # Process any pending events before cleanup
            self.window.close()
            self.window.deleteLater()
            QApplication.processEvents()  # Process the deleteLater event