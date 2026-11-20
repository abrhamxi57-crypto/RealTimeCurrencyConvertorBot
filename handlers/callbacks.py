from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import config
from services.currency_service import CurrencyService
from services.storage_service import StorageService
from handlers.keyboards import rates_keyboard, favorites_keyboard

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all inline keyboard button interactions."""
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = str(update.effective_user.id)

    # 1. Base rate selection (e.g. rate_USD, rate_EUR, rate_ETB)
    if data.startswith("rate_"):
        base = data.replace("rate_", "").upper()
        popular = CurrencyService.get_popular_rates(base)

        if not popular:
            await query.edit_message_text(f"❌ Could not retrieve rates for {base}.")
            return

        base_flag = config.CURRENCY_FLAGS.get(base, "🌐")
        lines = [f"{base_flag} **Live Exchange Rates for 1 {base}:**\n"]
        for curr, rate in popular.items():
            flag = config.CURRENCY_FLAGS.get(curr, "•")
            lines.append(f"{flag} **{curr}**: `{rate:,.4f}`")

        msg = "\n".join(lines)
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=rates_keyboard())

    # 2. Quick convert from favorite pair (e.g. favconv_USD_ETB)
    elif data.startswith("favconv_"):
        parts = data.split("_")
        if len(parts) >= 3:
            b, t = parts[1], parts[2]
            res = CurrencyService.convert(b, t, 100.0)
            if res.get("success"):
                b_flag = config.CURRENCY_FLAGS.get(b, "🪙")
                t_flag = config.CURRENCY_FLAGS.get(t, "🪙")
                text = (
                    f"⚡ **Quick Conversion:**\n\n"
                    f"{b_flag} **100 {b}** = {t_flag} **{res['result']:,.4f} {t}**\n"
                    f"📊 Rate: 1 {b} = {res['rate']:.4f} {t}"
                )
                favs = StorageService.get_favorites(uid)
                await query.edit_message_text(text, parse_mode="Markdown", reply_markup=favorites_keyboard(favs))

    # 3. Add prompt
    elif data == "fav_prompt_add":
        context.user_data["await_favorite_add"] = True
        await query.message.reply_text(
            "➕ Send the currency pair you want to add (e.g., `USD ETB` or `EUR GBP`):",
            parse_mode="Markdown"
        )

    # 4. Manage / Delete list
    elif data == "fav_manage":
        favs = StorageService.get_favorites(uid)
        if not favs:
            await query.edit_message_text("No favorites to manage.")
            return

        del_buttons = []
        for pair in favs:
            del_buttons.append([
                InlineKeyboardButton(f"🗑 Remove {pair[0]}/{pair[1]}", callback_data=f"favdel_{pair[0]}_{pair[1]}")
            ])
        del_buttons.append([InlineKeyboardButton("🔙 Back", callback_data="fav_back")])
        await query.edit_message_text(
            "Select a pair to remove from favorites:",
            reply_markup=InlineKeyboardMarkup(del_buttons)
        )

    # 5. Delete specific pair
    elif data.startswith("favdel_"):
        parts = data.split("_")
        if len(parts) >= 3:
            b, t = parts[1], parts[2]
            StorageService.remove_favorite(uid, b, t)
            favs = StorageService.get_favorites(uid)
            await query.edit_message_text(
                f"✅ Removed {b}/{t}.",
                reply_markup=favorites_keyboard(favs)
            )

    # 6. Back to favorites view
    elif data == "fav_back":
        favs = StorageService.get_favorites(uid)
        await query.edit_message_text(
            "⭐ **Your Favorite Currency Pairs:**",
            parse_mode="Markdown",
            reply_markup=favorites_keyboard(favs)
        )
