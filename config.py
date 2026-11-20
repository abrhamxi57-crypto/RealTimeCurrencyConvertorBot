import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the repository
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# Default Fallback Credentials (guarantees zero-downtime deployment)
DEFAULT_TELEGRAM_TOKEN = "9217502077:AAEXNnJEYU44plfSN3T44_JSTu-TK-Y1ha0"
DEFAULT_EXCHANGE_KEY = "687824ff6db700793b0a58a6"

# Telegram Configuration
env_token = os.getenv("TELEGRAM_TOKEN", "").strip()
if env_token and env_token != "your_telegram_bot_token_here":
    TELEGRAM_TOKEN = env_token
else:
    TELEGRAM_TOKEN = DEFAULT_TELEGRAM_TOKEN

# Currency API Configuration
env_key = os.getenv("EXCHANGE_API_KEY", "").strip()
if env_key and env_key != "your_exchangerate_api_key_here":
    EXCHANGE_API_KEY = env_key
else:
    EXCHANGE_API_KEY = DEFAULT_EXCHANGE_KEY

PRIMARY_API_BASE = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}"
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
