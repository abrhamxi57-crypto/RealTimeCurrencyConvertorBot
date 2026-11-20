"""Backward compatibility layer for legacy imports of handlers.py."""

from handlers import (
    start,
    help_command,
    convert_command as convert,
    button_handler,
    callback_handler,
    rates_command,
    favorites_command
)
from handlers.keyboards import main_menu

__all__ = [
    "start",
    "help_command",
    "convert",
    "button_handler",
    "callback_handler",
    "rates_command",
    "favorites_command",
    "main_menu"
]
