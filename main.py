from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers import start, help_command, convert, button_handler, callback_handler

TELEGRAM_TOKEN = "8522836537:AAFBrkNfi0jjZDnghIAegFTIDjCDRXIfY38"


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
