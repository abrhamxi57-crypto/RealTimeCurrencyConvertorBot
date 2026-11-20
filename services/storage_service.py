import json
import os
from pathlib import Path
from typing import Any, Dict, List
import config

class StorageService:
    """Manages persistent JSON data storage for history, feedback, favorites, and cache."""

    @staticmethod
    def load_json(file_path: Path, default: Any = None) -> Any:
        if default is None:
            default = {}
        if not os.path.exists(file_path):
            return default
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default

    @staticmethod
    def save_json(file_path: Path, data: Any) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving {file_path}: {e}")

    # Conversion History
    @classmethod
    def get_history(cls, user_id: str) -> List[str]:
        data = cls.load_json(config.HISTORY_FILE, {})
        return data.get(str(user_id), [])

    @classmethod
    def add_history(cls, user_id: str, entry: str, max_items: int = 50) -> None:
        data = cls.load_json(config.HISTORY_FILE, {})
        uid = str(user_id)
        entries = data.setdefault(uid, [])
        entries.append(entry)
        data[uid] = entries[-max_items:]
        cls.save_json(config.HISTORY_FILE, data)

    @classmethod
    def clear_history(cls, user_id: str) -> None:
        data = cls.load_json(config.HISTORY_FILE, {})
        data[str(user_id)] = []
        cls.save_json(config.HISTORY_FILE, data)

    # Feedback
    @classmethod
    def add_feedback(cls, user_id: str, text: str) -> None:
        data = cls.load_json(config.FEEDBACK_FILE, {})
        uid = str(user_id)
        data.setdefault(uid, []).append(text)
        cls.save_json(config.FEEDBACK_FILE, data)

    # Favorites
    @classmethod
    def get_favorites(cls, user_id: str) -> List[List[str]]:
        """Returns list of pairs like [["USD", "ETB"], ["EUR", "ETB"]]."""
        data = cls.load_json(config.FAVORITES_FILE, {})
        return data.get(str(user_id), [["USD", "ETB"], ["EUR", "ETB"]])

    @classmethod
    def add_favorite(cls, user_id: str, base: str, target: str) -> bool:
        data = cls.load_json(config.FAVORITES_FILE, {})
        uid = str(user_id)
        pair = [base.upper(), target.upper()]
        favs = data.setdefault(uid, [["USD", "ETB"], ["EUR", "ETB"]])
        if pair not in favs:
            favs.append(pair)
            cls.save_json(config.FAVORITES_FILE, data)
            return True
        return False

    @classmethod
    def remove_favorite(cls, user_id: str, base: str, target: str) -> bool:
        data = cls.load_json(config.FAVORITES_FILE, {})
        uid = str(user_id)
        pair = [base.upper(), target.upper()]
        favs = data.get(uid, [])
        if pair in favs:
            favs.remove(pair)
            data[uid] = favs
            cls.save_json(config.FAVORITES_FILE, data)
            return True
        return False
