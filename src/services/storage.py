import os
import json
from typing import Dict


class CategoryClickTracker:
    """Tracks and persists the number of times each category is clicked."""

    def __init__(self, base_path: str = None):
        """
        Initialize the tracker with a path to store click counts.
        
        Args:
            base_path: base directory path. If None, uses src/ directory.
        """
        if base_path:
            root = base_path
        else:
            root = os.path.dirname(os.path.dirname(__file__))
        
        self.clicks_path = os.path.join(root, "category_clicks.json")
        self._clicks: Dict[str, int] = {}
        self.load()

    def load(self) -> Dict[str, int]:
        """Load click counts from file."""
        try:
            if os.path.exists(self.clicks_path):
                with open(self.clicks_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    # Ensure all values are integers
                    self._clicks = {str(k): int(v) for k, v in data.items()}
                else:
                    self._clicks = {}
            else:
                self._clicks = {}
        except Exception:
            self._clicks = {}
        return self._clicks

    def save(self) -> bool:
        """Save click counts to file."""
        try:
            with open(self.clicks_path, 'w', encoding='utf-8') as f:
                json.dump(self._clicks, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def increment(self, category: str) -> int:
        """
        Increment the click count for a category.
        
        Args:
            category: Category name
            
        Returns:
            The updated click count
        """
        category = str(category).strip()
        if not category:
            return 0
        
        self._clicks[category] = self._clicks.get(category, 0) + 1
        self.save()
        return self._clicks[category]

    def get_count(self, category: str) -> int:
        """Get the current click count for a category."""
        return self._clicks.get(str(category), 0)

    def get_all_counts(self) -> Dict[str, int]:
        """Get all click counts."""
        return dict(self._clicks)

    def reset(self, category: str = None) -> bool:
        """
        Reset click count for a category or all categories if category is None.
        
        Args:
            category: Category to reset, or None to reset all
            
        Returns:
            True if successful
        """
        try:
            if category is None:
                self._clicks = {}
            else:
                category = str(category)
                if category in self._clicks:
                    del self._clicks[category]
            return self.save()
        except Exception:
            return False

    def reset_all(self) -> bool:
        """Reset all click counts."""
        return self.reset(None)
