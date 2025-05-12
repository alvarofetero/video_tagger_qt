
# This module provides functions to load and save categories from a JSON file.
# It includes error handling to ensure that the application can still run even if the categories file is missing or corrupted.
# It also provides a default category if the file cannot be loaded.
import json
import os

def load_categories(path=None):
    if path is None:
        # Resolve the path relative to the location of this file
        path = os.path.join(os.path.dirname(__file__), "categories.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading categories: {e}")
        return ["General"]