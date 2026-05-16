import json
import os
import requests

EXCHANGE_API_KEY = "687824ff6db700793b0a58a6"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}"

def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_rates(base):
    try:
        r = requests.get(f"{BASE_URL}/latest/{base}", timeout=10)
        return r.json()
    except:
        return None
