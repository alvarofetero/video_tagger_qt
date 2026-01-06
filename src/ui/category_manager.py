import os
import json
from typing import List

class CategoryManager:
    """Load/save category list from categories.json and provide simple helpers."""

    def __init__(self, base_path: str = None):
        # base_path should be the src/ui directory or None to auto-resolve
        if base_path:
            root = base_path
        else:
            root = os.path.dirname(os.path.dirname(__file__))
        self.categories_path = os.path.join(root, "categories.json")
        self._categories: List[str] = []
        self.load()

    def load(self) -> List[str]:
        try:
            with open(self.categories_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                self._categories = [str(x) for x in data]
            else:
                self._categories = []
        except Exception:
            # fallback default
            self._categories = ["General"]
        return self._categories

    def save(self, categories: List[str]) -> bool:
        try:
            with open(self.categories_path, 'w', encoding='utf-8') as f:
                json.dump(categories, f, indent=4, ensure_ascii=False)
            self._categories = list(categories)
            return True
        except Exception:
            return False

    def get(self) -> List[str]:
        return list(self._categories)

    def add(self, name: str) -> bool:
        name = name.strip()
        if not name or name in self._categories:
            return False
        self._categories.append(name)
        return self.save(self._categories)

    def remove(self, name: str) -> bool:
        if name not in self._categories:
            return False
        self._categories.remove(name)
        return self.save(self._categories)