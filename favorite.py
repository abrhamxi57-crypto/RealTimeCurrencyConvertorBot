"""Favorites management utility and re-export module."""

from services.storage_service import StorageService
from services.currency_service import CurrencyService

def get_favorites(user_id: str):
    return StorageService.get_favorites(user_id)

def add_favorite(user_id: str, base: str, target: str):
    return StorageService.add_favorite(user_id, base, target)

def remove_favorite(user_id: str, base: str, target: str):
    return StorageService.remove_favorite(user_id, base, target)
