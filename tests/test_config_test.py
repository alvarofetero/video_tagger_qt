import os
import json
import unittest
from unittest.mock import mock_open, patch
import tempfile
import pytest
from PyQt5.QtWidgets import QApplication
from src.config import load_categories

@pytest.mark.usefixtures("qapp", "cleanup_qt")
class TestLoadCategories(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        QApplication.processEvents()

    def test_load_categories_with_valid_file(self):
        mock_data = json.dumps(["Category1", "Category2"])
        with patch("builtins.open", mock_open(read_data=mock_data)):
            with patch("os.path.join", return_value=os.path.join(self.temp_dir, "mocked_path")):
                QApplication.processEvents()
                categories = load_categories("mocked_path")
                QApplication.processEvents()
                self.assertEqual(categories, ["Category1", "Category2"])

    def test_load_categories_with_missing_file(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch("os.path.join", return_value=os.path.join(self.temp_dir, "mocked_path")):
                QApplication.processEvents()
                categories = load_categories("mocked_path")
                QApplication.processEvents()
                self.assertEqual(categories, ["General"])

    def test_load_categories_with_invalid_json(self):
        mock_data = "invalid json"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            with patch("os.path.join", return_value=os.path.join(self.temp_dir, "mocked_path")):
                QApplication.processEvents()
                categories = load_categories("mocked_path")
                QApplication.processEvents()
                self.assertEqual(categories, ["General"])

    def test_load_categories_with_default_path(self):
        mock_data = json.dumps(["DefaultCategory"])
        default_path = os.path.join(os.path.dirname(__file__), "..", "src", "categories.json")
        with patch("builtins.open", mock_open(read_data=mock_data)):
            with patch("os.path.join", return_value=default_path):
                QApplication.processEvents()
                categories = load_categories()
                QApplication.processEvents()
                self.assertEqual(categories, ["DefaultCategory"])

    def tearDown(self):
        """Clean up test environment"""
        QApplication.processEvents()
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass  # Ignore cleanup errors
        QApplication.processEvents()