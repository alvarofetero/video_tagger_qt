import os
import json
import unittest
from unittest.mock import mock_open, patch
from src.config import load_categories

class TestLoadCategories(unittest.TestCase):
    def test_load_categories_with_valid_file(self):
        mock_data = json.dumps(["Category1", "Category2"])
        with patch("builtins.open", mock_open(read_data=mock_data)):
            with patch("os.path.join", return_value="mocked_path"):
                categories = load_categories("mocked_path")
                self.assertEqual(categories, ["Category1", "Category2"])

    def test_load_categories_with_missing_file(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch("os.path.join", return_value="mocked_path"):
                categories = load_categories("mocked_path")
                self.assertEqual(categories, ["General"])

    def test_load_categories_with_invalid_json(self):
        mock_data = "invalid json"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            with patch("os.path.join", return_value="mocked_path"):
                categories = load_categories("mocked_path")
                self.assertEqual(categories, ["General"])

    def test_load_categories_with_default_path(self):
        mock_data = json.dumps(["DefaultCategory"])
        default_path = os.path.join(os.path.dirname(__file__), "categories.json")
        with patch("builtins.open", mock_open(read_data=mock_data)):
            with patch("os.path.join", return_value=default_path):
                categories = load_categories()
                self.assertEqual(categories, ["DefaultCategory"])

if __name__ == "__main__":
    unittest.main()