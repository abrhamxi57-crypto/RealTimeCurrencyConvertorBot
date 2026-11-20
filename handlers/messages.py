import re
from telegram import Update
from telegram.ext import ContextTypes
import config
from services.storage_service import StorageService
from services.currency_service import CurrencyService
from handlers.keyboards import main_menu, rates_keyboard
from handlers.commands import start, help_command, parse_convert_args
from handlers.favorites import favorites_command

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles text messages from reply keyboard buttons and conversational states."""
    text = (update.message.text or "").strip()
    uid = str(update.effective_user.id)

    # 1. Feedback State
    if context.user_data.get("await_feedback"):
        context.user_data["await_feedback"] = False
        if text:
            StorageService.add_feedback(uid, text)
            await update.message.reply_text(
                "🙏 Thank you for your feedback! It helps improve the bot.",
                reply_markup=main_menu()
            )
        else:
            await update.message.reply_text("Feedback cancelled.", reply_markup=main_menu())
        return

    # 2. Add Favorite Pair State
    if context.user_data.get("await_favorite_add"):
        context.user_data["await_favorite_add"] = False
        parts = [p.upper() for p in re.split(r"[\s/,-]+", text) if p]
        if len(parts) >= 2:
            base, target = parts[0], parts[1]
            added = StorageService.add_favorite(uid, base, target)
            if added:
                await update.message.reply_text(f"✅ Added **{base}/{target}** to your favorites!", parse_mode="Markdown")
            else:
                await update.message.reply_text(f"ℹ️ **{base}/{target}** is already in your favorites.", parse_mode="Markdown")
        else:
            await update.message.reply_text("⚠️ Invalid pair format. Please use two currency codes, e.g. `USD ETB`.", parse_mode="Markdown")
        return

    # 3. Main Menu Buttons
    if text == "▶️ Start":
        await start(update, context)
        return

    if text == "ℹ️ Help":
        await help_command(update, context)
        return

    if text == "💱 Rates":
        await update.message.reply_text(
            "📊 **Live Exchange Rates**\nSelect a base currency to view rates:",
            parse_mode="Markdown",
            reply_markup=rates_keyboard()
        )
        return

    if text == "🔄 Convert":
        await update.message.reply_text(
            "💡 **How to convert:**\n\n"
            "Simply send a message or command like:\n"
            "• `/convert 100 USD to EUR`\n"
            "• `/convert 50 GBP to ETB`\n"
            "• Or just type: `100 USD to ETB` directly!",
            parse_mode="Markdown"
        )
        return

    if text == "⭐ Favorites":
        await favorites_command(update, context)
        return

    if text == "📜 History":
        history = StorageService.get_history(uid)
        if not history:
            await update.message.reply_text("📜 You have no conversion history yet.", reply_markup=main_menu())
        else:
            recent = history[-15:]
            msg = "📜 **Your Recent Conversions:**\n\n" + "\n".join([f"• {item}" for item in recent])
            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=main_menu())
        return

    if text == "🧹 Clear History":
        StorageService.clear_history(uid)
        await update.message.reply_text("🧹 Your conversion history has been cleared.", reply_markup=main_menu())
        return

    if text == "✍ Feedback":
        context.user_data["await_feedback"] = True
        await update.message.reply_text(
            "✍ Please type your feedback or suggestions below:",
            reply_markup=main_menu()
        )
        return

    # 4. Natural text conversion support (e.g. user just types "100 USD to EUR" or "50 EUR ETB")
    try:
        tokens = text.split()
        if len(tokens) >= 3:
            amount, from_curr, to_curr = parse_convert_args(tokens)
            result = CurrencyService.convert(from_curr, to_curr, amount)
            if result.get("success"):
                from_flag = config.CURRENCY_FLAGS.get(from_curr, "🪙")
                to_flag = config.CURRENCY_FLAGS.get(to_curr, "🪙")
                rate = result['rate']
                res_val = result['result']

                source_tag = ""
                if result.get("is_stale"):
                    source_tag = "\n⚠️ _Note: Cached offline rate_"
                elif result.get("is_cached"):
                    source_tag = "\n⚡ _Source: Cached Rate_"

                response_text = (
                    f"{from_flag} **{amount:,.2f} {from_curr}** = {to_flag} **{res_val:,.4f} {to_curr}**\n\n"
                    f"📊 Rate: 1 {from_curr} = {rate:.4f} {to_curr}"
                    f"{source_tag}"
                )
                await update.message.reply_text(response_text, parse_mode="Markdown", reply_markup=main_menu())

                # Save history
                history_entry = f"{amount:,.2f} {from_curr} ➔ {res_val:,.2f} {to_curr} (Rate: {rate:.4f})"
                StorageService.add_history(uid, history_entry)
                return
    except Exception:
        pass

    # Fallback response for unhandled text
    await update.message.reply_text(
        "I didn't recognize that command. Use the buttons below or type `/help` for assistance.",
        reply_markup=main_menu()
    )
