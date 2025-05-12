# Category loading and saving
import json

def load_categories(path="categories.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return ["General"]

