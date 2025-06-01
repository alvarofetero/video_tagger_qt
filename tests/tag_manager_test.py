import unittest
from src.tag_manager import TagManager
import pytest
from PyQt5.QtWidgets import QApplication

@pytest.mark.usefixtures("qapp", "cleanup_qt")
class TestTagManager(unittest.TestCase):
    def setUp(self):
        """Initialize test environment"""
        self.manager = TagManager()
        QApplication.processEvents()  # Process any pending events

    def test_add_tag(self):
        """Test adding a tag with proper event loop handling"""
        # Process any pending events before test
        QApplication.processEvents()
        
        # Test adding a tag
        self.manager.add_start(1.0)
        self.manager.add_end(3.0)
        
        # Process events after modifications
        QApplication.processEvents()
        
        # Verify results
        tags = self.manager.get_tags()
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0]['start'], 1.0)
        self.assertEqual(tags[0]['end'], 3.0)

    def test_remove_tag(self):
        """Test removing a tag with proper event loop handling"""
        QApplication.processEvents()
        
        # Add and then remove a tag
        self.manager.add_start(2.0)
        self.manager.add_end(4.0)
        self.manager.remove_tag(0)
        
        QApplication.processEvents()
        
        self.assertEqual(len(self.manager.get_tags()), 0)

    def test_pre_start_offset(self):
        """Test pre-start offset with proper event loop handling"""
        QApplication.processEvents()
        
        self.manager.set_offset(1.0)
        self.manager.add_start(5.0)
        
        QApplication.processEvents()
        
        self.assertEqual(self.manager.get_tags()[0]['start'], 4.0)

    def tearDown(self):
        """Clean up test environment"""
        QApplication.processEvents()  # Process any pending events before cleanup


if __name__ == '__main__':
    unittest.main()
