from telegram import Update
from telegram.ext import ContextTypes
import config
from services.currency_service import CurrencyService
from services.storage_service import StorageService
from handlers.keyboards import main_menu, rates_keyboard, favorites_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    user_name = update.effective_user.first_name if update.effective_user else "there"
    welcome_msg = (
        f"👋 Hello {user_name}!\n\n"
        "Welcome to the **Real-Time Currency Converter Bot** 💱\n\n"
        "✨ **What I can do:**\n"
        "• ⚡ Instant live currency conversions\n"
        "• 📊 Real-time exchange rate tables\n"
        "• ⭐ Favorite currency pairs for fast 1-tap conversion\n"
        "• 📜 Personal conversion history\n"
        "• 🛡️ Offline caching & automatic backup API fallback\n\n"
        "Try typing:\n"
        "`/convert 100 USD to ETB`\n"
        "Or use the menu buttons below! 👇"
    )
    await update.message.reply_text(welcome_msg, parse_mode="Markdown", reply_markup=main_menu())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command."""
    help_text = (
        "📖 **Currency Converter Bot Help**\n\n"
        "**Available Commands:**\n"
        "• `/convert <amount> <from> to <to>` — Convert currencies\n"
        "   _Example:_ `/convert 100 USD to EUR`\n"
        "   _Or:_ `/convert USD ETB 500`\n"
        "• `/rates [currency]` — View exchange rate table\n"
        "   _Example:_ `/rates USD` or `/rates ETB`\n"
        "• `/favorites` — View & manage your favorite currency pairs\n"
        "• `/favorite add <from> <to>` — Add a favorite pair\n"
        "   _Example:_ `/favorite add USD ETB`\n"
        "• `/history` — View your last 50 conversions\n"
        "• `/clear` — Clear your conversion history\n\n"
        "**Menu Buttons:**\n"
        "▶️ Start | ℹ️ Help | 💱 Rates | 🔄 Convert\n"
        "⭐ Favorites | 📜 History | 🧹 Clear History | ✍ Feedback"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown", reply_markup=main_menu())

def parse_convert_args(args: list) -> tuple:
    """Parses various argument formats for currency conversion.

    Supported formats:
    - ["100", "USD", "to", "EUR"]
    - ["100", "USD", "EUR"]
    - ["USD", "EUR", "100"]
    - ["USD", "to", "EUR", "100"]
    Returns (amount, from_curr, to_curr) or raises ValueError.
    """
    clean_args = [a for a in args if a.lower() not in ("to", "in", "->", "=")]
    if len(clean_args) != 3:
        raise ValueError("Invalid number of arguments")

    # Format: 100 USD EUR
    try:
        amount = float(clean_args[0])
        from_curr = clean_args[1].upper()
        to_curr = clean_args[2].upper()
        return amount, from_curr, to_curr
    except ValueError:
        pass

    # Format: USD EUR 100
    try:
        amount = float(clean_args[2])
        from_curr = clean_args[0].upper()
        to_curr = clean_args[1].upper()
        return amount, from_curr, to_curr
    except ValueError:
        pass

    raise ValueError("Could not parse amount and currency codes")

async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /convert command."""
    if not context.args:
        await update.message.reply_text(
            "💡 **How to use /convert:**\n\n"
            "• `/convert 100 USD to EUR`\n"
            "• `/convert 50 EUR to ETB`\n"
            "• `/convert USD ETB 200`\n\n"
            "Try it now!",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        return

    try:
        amount, from_curr, to_curr = parse_convert_args(context.args)
    except ValueError:
        await update.message.reply_text(
            "⚠️ **Invalid format!**\n"
            "Please use: `/convert <amount> <from> to <to>`\n"
            "Example: `/convert 100 USD to EUR`",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        return

    result = CurrencyService.convert(from_curr, to_curr, amount)
    if not result.get("success"):
        await update.message.reply_text(f"❌ {result.get('error')}", reply_markup=main_menu())
        return

    from_flag = config.CURRENCY_FLAGS.get(from_curr, "🪙")
    to_flag = config.CURRENCY_FLAGS.get(to_curr, "🪙")
    rate = result['rate']
    res_val = result['result']

    source_tag = ""
    if result.get("is_stale"):
        source_tag = "\n⚠️ _Note: Cached offline rate (network unavailable)_"
    elif result.get("is_cached"):
        source_tag = "\n⚡ _Source: Cached Rate_"

    response_text = (
        f"{from_flag} **{amount:,.2f} {from_curr}** = {to_flag} **{res_val:,.4f} {to_curr}**\n\n"
        f"📊 **Exchange Rate:** 1 {from_curr} = {rate:.4f} {to_curr}\n"
        f"🔄 **Reverse Rate:** 1 {to_curr} = {1 / rate:.4f} {from_curr}"
        f"{source_tag}"
    )
    await update.message.reply_text(response_text, parse_mode="Markdown", reply_markup=main_menu())

    # Save to history
    uid = str(update.effective_user.id)
    history_entry = f"{amount:,.2f} {from_curr} ➔ {res_val:,.2f} {to_curr} (Rate: {rate:.4f})"
    StorageService.add_history(uid, history_entry)

async def rates_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /rates command (e.g. /rates USD)."""
    base = context.args[0].upper() if context.args else "USD"
    popular = CurrencyService.get_popular_rates(base)

    if not popular:
        await update.message.reply_text(
            f"❌ Could not retrieve rates for base currency **{base}**.",
            parse_mode="Markdown"
        )
        return

    base_flag = config.CURRENCY_FLAGS.get(base, "🌐")
    lines = [f"{base_flag} **Live Exchange Rates for 1 {base}:**\n"]
    for curr, rate in popular.items():
        flag = config.CURRENCY_FLAGS.get(curr, "•")
        lines.append(f"{flag} **{curr}**: `{rate:,.4f}`")

    msg = "\n".join(lines)
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=rates_keyboard())
