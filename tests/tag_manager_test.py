import unittest
from src.tag_manager import TagManager

class TestTagManager(unittest.TestCase):
    def setUp(self):
        self.manager = TagManager()

    def test_add_tag(self):
        self.manager.add_start(1.0)
        self.manager.add_end(3.0)
        self.assertEqual(len(self.manager.get_tags()), 1)
        self.assertEqual(self.manager.get_tags()[0]['start'], 1.0)
        self.assertEqual(self.manager.get_tags()[0]['end'], 3.0)

    def test_remove_tag(self):
        self.manager.add_start(2.0)
        self.manager.add_end(4.0)
        self.manager.remove_tag(0)
        self.assertEqual(len(self.manager.get_tags()), 0)

    def test_pre_start_offset(self):
        self.manager.set_offset(1.0)
        self.manager.add_start(5.0)
        self.assertEqual(self.manager.get_tags()[0]['start'], 4.0)

if __name__ == '__main__':
    unittest.main()
