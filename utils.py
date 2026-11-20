"""Backward compatibility layer for legacy imports of utils.py."""

import config
from services.storage_service import StorageService
from services.currency_service import CurrencyService

EXCHANGE_API_KEY = config.EXCHANGE_API_KEY
BASE_URL = config.PRIMARY_API_BASE

def load_json(path):
    return StorageService.load_json(path, {})

def save_json(path, data):
    return StorageService.save_json(path, data)

def get_rates(base):
    return CurrencyService.get_rates(base)
