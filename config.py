import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the repository
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()

# Currency API Configuration
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY", "").strip()
PRIMARY_API_BASE = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}" if EXCHANGE_API_KEY else ""
BACKUP_API_BASE = "https://open.er-api.com/v6"

# Cache TTL (in seconds, default 1 hour)
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

# Storage paths
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_FILE = DATA_DIR / "history.json"
FEEDBACK_FILE = DATA_DIR / "feedback.json"
FAVORITES_FILE = DATA_DIR / "favorites.json"
RATES_CACHE_FILE = DATA_DIR / "rates_cache.json"

# Popular currencies to display in summary
POPULAR_CURRENCIES = [
    "USD", "EUR", "GBP", "ETB", "CAD", "JPY", "CHF", "AUD", 
    "CNY", "INR", "AED", "SAR", "KES", "TRY", "ZAR"
]

CURRENCY_FLAGS = {
    "USD": "🇺🇸", "EUR": "🇪🇺", "GBP": "🇬🇧", "ETB": "🇪🇹", "CAD": "🇨🇦",
    "JPY": "🇯🇵", "CHF": "🇨🇭", "AUD": "🇦🇺", "CNY": "🇨🇳", "INR": "🇮🇳",
    "AED": "🇦🇪", "SAR": "🇸🇦", "KES": "🇰🇪", "TRY": "🇹🇷", "ZAR": "🇿🇦"
}
