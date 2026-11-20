from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
import config

def main_menu() -> ReplyKeyboardMarkup:
    """Returns the main persistent reply keyboard markup."""
    return ReplyKeyboardMarkup([
        ["▶️ Start", "ℹ️ Help"],
        ["💱 Rates", "🔄 Convert"],
        ["⭐ Favorites", "📜 History"],
        ["🧹 Clear History", "✍ Feedback"]
    ], resize_keyboard=True, is_persistent=True)

def rates_keyboard() -> InlineKeyboardMarkup:
    """Returns an inline keyboard with common base currencies."""
    buttons = [
        [
            InlineKeyboardButton("🇺🇸 USD", callback_data="rate_USD"),
            InlineKeyboardButton("🇪🇺 EUR", callback_data="rate_EUR"),
            InlineKeyboardButton("🇬🇧 GBP", callback_data="rate_GBP")
        ],
        [
            InlineKeyboardButton("🇪🇹 ETB", callback_data="rate_ETB"),
            InlineKeyboardButton("🇨🇦 CAD", callback_data="rate_CAD"),
            InlineKeyboardButton("🇦🇪 AED", callback_data="rate_AED")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def favorites_keyboard(favorites: List[List[str]]) -> InlineKeyboardMarkup:
    """Returns an inline keyboard for quick-converting favorite currency pairs."""
    keyboard = []
    row = []
    for pair in favorites:
        base, target = pair[0], pair[1]
        text = f"{base} ➔ {target}"
        callback = f"favconv_{base}_{target}"
        row.append(InlineKeyboardButton(text, callback_data=callback))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Management row
    keyboard.append([
        InlineKeyboardButton("➕ Add Favorite", callback_data="fav_prompt_add"),
        InlineKeyboardButton("🗑 Manage Favorites", callback_data="fav_manage")
    ])
    return InlineKeyboardMarkup(keyboard)
