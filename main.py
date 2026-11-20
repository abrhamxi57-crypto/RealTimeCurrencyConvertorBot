import logging
import sys
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
import config
from handlers.commands import start, help_command, convert_command, rates_command
from handlers.favorites import favorites_command
from handlers.messages import button_handler
from handlers.callbacks import callback_handler

# Configure structured logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("CurrencyBot")

def main():
    token = config.TELEGRAM_TOKEN
    if not token or token == "your_telegram_bot_token_here":
        logger.error("TELEGRAM_TOKEN is missing or not configured in .env file!")
        print("\n[ERROR] TELEGRAM_TOKEN is not set in .env! Please set it before running.\n")
        sys.exit(1)

    logger.info("Initializing Currency Converter Bot...")
    app = ApplicationBuilder().token(token).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("convert", convert_command))
    app.add_handler(CommandHandler("rates", rates_command))
    app.add_handler(CommandHandler("favorites", favorites_command))
    app.add_handler(CommandHandler("favorite", favorites_command))

    # Message & Callback Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("Bot is ready and polling for updates...")
    print("🚀 Currency Converter Bot is running! Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
