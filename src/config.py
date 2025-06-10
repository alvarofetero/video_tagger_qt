
# This module provides functions to load and save categories from a JSON file.
# It includes error handling to ensure that the application can still run even if the categories file is missing or corrupted.
# It also provides a default category if the file cannot be loaded.
import json
import os
from src.utils.logger import AppLogger

logger = AppLogger.get_logger()

DEFAULT_CONFIG = {
    "categories": [
        "Nico",
        "Gol",
        "Portero",
        "Salida de balón",
        "Recuperación",
        "Defensa",
        "Presión tras pérdida",
        "ABP",
        "Ataque posicional"
    ],
    "tag_duration": {
        "pre_tag": 3,
        "post_tag": 2
    }
}

def load_config():
    """Load configuration from JSON file"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default config file if it doesn't exist
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    except json.JSONDecodeError:
        logger.error("Invalid config.json file")
        return DEFAULT_CONFIG
    
def save_config(config):
    """Save configuration to JSON file"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving config: {e}")



def get_tag_duration_config():
    """Load tag duration configuration"""
    config = load_config()
    durations = config.get("tag_duration", {"pre_tag": 1, "post_tag": 1})
    return durations.get("pre_tag", 1), durations.get("post_tag", 1)

def load_categories():
    """Load categories from config"""
    config = load_config()
    return config.get("categories", ["General"])

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