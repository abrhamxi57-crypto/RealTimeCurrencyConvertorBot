import logging
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
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

class RailwayHealthHandler(BaseHTTPRequestHandler):
    """Answers Railway's HTTP health checks so the deployment stays active."""
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK: Currency Converter Bot is running!")

    def log_message(self, format, *args):
        pass  # Suppress repetitive HTTP health check logs

def start_health_check_server():
    """Starts a minimal background HTTP server if Railway sets a PORT environment variable."""
    port_str = os.getenv("PORT")
    if port_str:
        try:
            port = int(port_str)
            server = HTTPServer(("0.0.0.0", port), RailwayHealthHandler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            logger.info(f"Railway HTTP health-check server running on port {port}")
        except Exception as e:
            logger.warning(f"Failed to start health check server: {e}")

def main():
    token = config.TELEGRAM_TOKEN
    if not token or token == "your_telegram_bot_token_here":
        logger.error("TELEGRAM_TOKEN is missing or not configured in .env file!")
        print("\n[ERROR] TELEGRAM_TOKEN is not set in .env! Please set it before running.\n")
        sys.exit(1)

    # Start health check server for Railway if PORT is provided
    start_health_check_server()

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
