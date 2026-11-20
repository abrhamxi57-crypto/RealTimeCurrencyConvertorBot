import time
import requests
from typing import Optional, Dict, Any, Tuple
import config
from services.storage_service import StorageService

class CurrencyService:
    """Handles fetching live exchange rates, primary and backup API failover,

    and offline rate caching.
    """

    @classmethod
    def _get_cache(cls) -> Dict[str, Any]:
        return StorageService.load_json(config.RATES_CACHE_FILE, {})

    @classmethod
    def _save_cache(cls, cache_data: Dict[str, Any]) -> None:
        StorageService.save_json(config.RATES_CACHE_FILE, cache_data)

    @classmethod
    def get_rates_data(cls, base: str) -> Optional[Dict[str, Any]]:
        """Fetch exchange rates for a given base currency with multi-tier failover:

        1. Fresh Cache (within TTL)
        2. Primary API (ExchangeRate-API)
        3. Backup API (Open Exchange Rates)
        4. Stale Cache (Offline Fallback)
        """
        base = base.upper().strip()
        cache = cls._get_cache()
        now = time.time()

        cached_entry = cache.get(base)

        # 1. Check if we have valid fresh cache
        if cached_entry:
            age = now - cached_entry.get("timestamp", 0)
            if age < config.CACHE_TTL_SECONDS and "rates" in cached_entry:
                return {
                    "rates": cached_entry["rates"],
                    "source": cached_entry.get("source", "Cache"),
                    "timestamp": cached_entry.get("timestamp"),
                    "is_cached": True,
                    "is_stale": False
                }

        # 2. Try Primary API (ExchangeRate-API)
        if config.PRIMARY_API_BASE:
            try:
                url = f"{config.PRIMARY_API_BASE}/latest/{base}"
                resp = requests.get(url, timeout=7)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("result") == "success" and "conversion_rates" in data:
                        rates = data["conversion_rates"]
                        cache[base] = {
                            "timestamp": now,
                            "rates": rates,
                            "source": "ExchangeRate-API"
                        }
                        cls._save_cache(cache)
                        return {
                            "rates": rates,
                            "source": "ExchangeRate-API (Live)",
                            "timestamp": now,
                            "is_cached": False,
                            "is_stale": False
                        }
            except Exception as e:
                print(f"Primary API error: {e}")

        # 3. Try Backup API (open.er-api.com)
        try:
            url = f"{config.BACKUP_API_BASE}/latest/{base}"
            resp = requests.get(url, timeout=7)
            if resp.status_code == 200:
                data = resp.json()
                if "rates" in data:
                    rates = data["rates"]
                    cache[base] = {
                        "timestamp": now,
                        "rates": rates,
                        "source": "Open-ER API (Backup)"
                    }
                    cls._save_cache(cache)
                    return {
                        "rates": rates,
                        "source": "Open-ER API (Backup)",
                        "timestamp": now,
                        "is_cached": False,
                        "is_stale": False
                    }
        except Exception as e:
            print(f"Backup API error: {e}")

        # 4. Fallback to Stale Cache if available (Offline Mode)
        if cached_entry and "rates" in cached_entry:
            return {
                "rates": cached_entry["rates"],
                "source": "Offline Cache (Stale)",
                "timestamp": cached_entry.get("timestamp"),
                "is_cached": True,
                "is_stale": True
            }

        return None

    @classmethod
    def get_rates(cls, base: str) -> Optional[Dict[str, Any]]:
        """Legacy-compatible helper returning dictionary matching exchangerate-api JSON format."""
        data = cls.get_rates_data(base)
        if not data:
            return None
        return {
            "result": "success",
            "base_code": base.upper(),
            "conversion_rates": data["rates"]
        }

    @classmethod
    def convert(cls, from_curr: str, to_curr: str, amount: float) -> Dict[str, Any]:
        """Converts an amount from one currency to another."""
        from_curr = from_curr.upper().strip()
        to_curr = to_curr.upper().strip()

        if amount <= 0:
            return {"success": False, "error": "Amount must be greater than zero."}

        data = cls.get_rates_data(from_curr)
        if not data or not data.get("rates"):
            return {
                "success": False,
                "error": f"Could not retrieve exchange rates for base currency '{from_curr}'."
            }

        rates = data["rates"]
        rate = rates.get(to_curr)
        if rate is None:
            return {
                "success": False,
                "error": f"Currency code '{to_curr}' was not found in available exchange rates."
            }

        result = amount * float(rate)
        return {
            "success": True,
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "rate": float(rate),
            "result": result,
            "source": data.get("source", "Live API"),
            "is_cached": data.get("is_cached", False),
            "is_stale": data.get("is_stale", False)
        }

    @classmethod
    def get_popular_rates(cls, base: str) -> Dict[str, float]:
        """Returns rate values for popular global and regional currencies."""
        data = cls.get_rates_data(base)
        if not data or not data.get("rates"):
            return {}

        rates = data["rates"]
        popular = {}
        for code in config.POPULAR_CURRENCIES:
            if code != base.upper() and code in rates:
                popular[code] = float(rates[code])
        return popular
