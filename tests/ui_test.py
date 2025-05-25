import unittest
from PyQt5.QtWidgets import QApplication, QSplitter
from src.ui import VideoTaggerApp

class TestVideoTaggerAppUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])  # Create a QApplication instance for testing

    def setUp(self):
        self.window = VideoTaggerApp()  # Create an instance of the VideoTaggerApp
        self.window.setup_ui()  # Call the setup_ui method

    def test_ui_elements_exist(self):
        # Test if all UI elements are created
        self.assertIsNotNone(self.window.load_button, "Load button not created")
        self.assertIsNotNone(self.window.play_button, "Play button not created")
        self.assertIsNotNone(self.window.start_tag_button, "Start tag button not created")
        self.assertIsNotNone(self.window.end_tag_button, "End tag button not created")
        self.assertIsNotNone(self.window.tag_list, "Tag list not created")
        self.assertIsNotNone(self.window.filename_input, "Filename input not created")
        self.assertIsNotNone(self.window.export_clip_button, "Export clip button not created")
        self.assertIsNotNone(self.window.progress_bar, "Progress bar not created")
        self.assertIsNotNone(self.window.video_player, "Video player not created")
        self.assertIsNotNone(self.window.timeline, "Timeline widget not created")
        self.assertIsNotNone(self.window.category_box, "Category box not created")
        self.assertIsNotNone(self.window.delete_tag_button, "Delete tag button not created")
        self.assertIsNotNone(self.window.save_tags_button, "Save tags button not created")
        self.assertIsNotNone(self.window.load_tags_button, "Load tags button not created")
        self.assertIsNotNone(self.window.speed_down_button, "Speed down button not created")
        self.assertIsNotNone(self.window.speed_up_button, "Speed up button not created")
        self.assertIsNotNone(self.window.speed_label, "Speed label not created")

    def test_ui_layout(self):
        # Test if the splitter has two widgets (controls panel and video player)
        splitter_widgets = self.window.findChildren(QSplitter)
        self.assertEqual(len(splitter_widgets), 1, "Splitter not created or incorrect number of widgets")
        splitter = splitter_widgets[0]
        self.assertEqual(splitter.count(), 2, "Splitter does not contain two widgets")

    def tearDown(self):
        self.window.close()  # Close the window after each test

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()  # Quit the QApplication instance after all tests

if __name__ == "__main__":
    unittest.main()