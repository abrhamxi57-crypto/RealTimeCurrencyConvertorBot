from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils import get_rates, save_json, load_json

HISTORY_FILE = "history.json"
FEEDBACK_FILE = "feedback.json" 

user_history = load_json(HISTORY_FILE)
user_feedback = load_json(FEEDBACK_FILE)

def main_menu():
    return ReplyKeyboardMarkup([
        ["▶️ Start", "ℹ️ Help"],
        ["💱 Rates", "🔄 Convert"],
        ["📜 History", "🧹 Clear History"],
        ["✍ Feedback"]
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "👋 Welcome to Currency Converter Bot!\n"
        "This bot provides real-time exchange rates.\n\n"
        "What our bot can do?\n\n"
        "- Shows real-time exchange rates.\n"
        "- Converts money between currencies.\n"
        "- Saves user's conversion history."
    )
    await update.message.reply_text(welcome_msg, reply_markup=main_menu())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Always respond correctly whether called by button or command
    msg = (
        
        "Buttons:\n"
        "▶️ Start - Start bot\n"
        "ℹ️ Help - Show this message\n"
        "💱 Rates - Show exchange rates\n"
        "🔄 Convert - Convert currencies\n"
        "📜 History - Show conversion history\n"
        "🧹 Clear History - Clear your history\n"
        "✍ Feedback - Send feedback"
    )
    await update.message.reply_text(msg, reply_markup=main_menu())

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /convert USD ETB 100")
        return

    f, t = context.args[0].upper(), context.args[1].upper()
    try:
        amount = float(context.args[2])
    except:
        await update.message.reply_text("Invalid amount")
        return

    data = get_rates(f)
    if not data or data.get("result") != "success":
        await update.message.reply_text("Rate error")
        return

    rate = data["conversion_rates"].get(t)
    if not rate:
        await update.message.reply_text("Currency not found")
        return

    result = amount * rate
    msg = f"{amount} {f} = {result:.4f} {t}\nRate: {rate:.4f}"
    await update.message.reply_text(msg)

    uid = str(update.message.from_user.id)
    user_history.setdefault(uid, []).append(msg)
    user_history[uid] = user_history[uid][-50:]
    save_json(HISTORY_FILE, user_history)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = str(update.message.from_user.id)

    if text == "▶️ Start":
        await start(update, context)
    elif text == "ℹ️ Help":
        await help_command(update, context)
    elif text == "💱 Rates":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("USD", callback_data="rate_USD"),
             InlineKeyboardButton("EUR", callback_data="rate_EUR"),
             InlineKeyboardButton("ETB", callback_data="rate_ETB")]
        ])
        await update.message.reply_text("Choose base currency:", reply_markup=kb)
    elif text == "🔄 Convert":
        await update.message.reply_text("Use /convert like this: /convert USD ETB 100")
    elif text == "📜 History":
        history = user_history.get(uid, [])
        if not history:
            history = ["No history yet"]
        await update.message.reply_text("\n".join(history))
    elif text == "🧹 Clear History":
        user_history[uid] = []
        save_json(HISTORY_FILE, user_history)
        await update.message.reply_text("History cleared")
    elif text == "✍ Feedback":
        context.user_data["await_feedback"] = True
        await update.message.reply_text("Send your feedback message:")
    elif context.user_data.get("await_feedback"):
        # Save feedback
        feedback_text = text.strip()
        if feedback_text:  # ignore empty messages
            user_feedback.setdefault(uid, []).append(feedback_text)
            save_json(FEEDBACK_FILE, user_feedback)
        context.user_data["await_feedback"] = False
        await update.message.reply_text("Thanks for your feedback!")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    base = query.data.replace("rate_", "")
    data = get_rates(base)
    if not data or data.get("result") != "success":
        await query.edit_message_text("Error fetching rates")
        return

    rates = data["conversion_rates"]
    msg = f"📊 Exchange Rates for {base}\n\n"
    msg += "\n".join([f"{k}: {v}" for k, v in list(rates.items())[:165]])
    await query.edit_message_text(msg)
