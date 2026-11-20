from handlers.commands import start, help_command, convert_command, rates_command
from handlers.callbacks import callback_handler
from handlers.messages import button_handler
from handlers.favorites import favorites_command

# Backward compatibility alias
convert = convert_command

__all__ = [
    "start",
    "help_command",
    "convert_command",
    "convert",
    "rates_command",
    "callback_handler",
    "button_handler",
    "favorites_command"
]
