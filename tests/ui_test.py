import unittest
from PyQt5.QtWidgets import QApplication, QSplitter
from src.ui import VideoTaggerApp

class TestVideoTaggerAppUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])  # Create a QApplication instance for testing

    def setUp(self):
        self.window = VideoTaggerApp()  # Create an instance of the VideoTaggerApp

    def test_ui_elements_exist(self):
        """Test that essential UI components exist"""
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
        self.assertIsNotNone(self.window.file_controls.export_button, "Export button not created")

    def test_ui_layout(self):
        """Test the main window layout structure"""
        # Test if the main window has a central widget
        self.assertIsNotNone(self.window.central_widget, "Central widget not created")
        
        # Test if there is exactly one splitter in the main layout
        splitter_widgets = self.window.central_widget.findChildren(QSplitter)
        self.assertEqual(len(splitter_widgets), 1, "Splitter not created or incorrect number of widgets")
        
        # Test if the splitter has exactly two widgets (controls panel and video player)
        splitter = splitter_widgets[0]
        self.assertEqual(splitter.count(), 2, "Splitter does not contain two widgets")

    def tearDown(self):
        self.window.close()  # Close the window after each test

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()  # Quit the QApplication instance after all tests

if __name__ == "__main__":
    unittest.main()