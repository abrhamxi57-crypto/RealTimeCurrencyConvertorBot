from telegram import Update
from telegram.ext import ContextTypes
import config
from services.storage_service import StorageService
from services.currency_service import CurrencyService
from handlers.keyboards import favorites_keyboard

async def favorites_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /favorites or /favorite command."""
    uid = str(update.effective_user.id)
    args = context.args or []

    # Format: /favorite add USD ETB
    if len(args) >= 3 and args[0].lower() in ("add", "new"):
        base = args[1].upper()
        target = args[2].upper()
        added = StorageService.add_favorite(uid, base, target)
        if added:
            await update.message.reply_text(f"✅ Added **{base}/{target}** to your favorites!", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"ℹ️ **{base}/{target}** is already in your favorites.", parse_mode="Markdown")
        return

    # Format: /favorite remove USD ETB
    if len(args) >= 3 and args[0].lower() in ("remove", "rm", "del", "delete"):
        base = args[1].upper()
        target = args[2].upper()
        removed = StorageService.remove_favorite(uid, base, target)
        if removed:
            await update.message.reply_text(f"🗑 Removed **{base}/{target}** from your favorites.", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"ℹ️ **{base}/{target}** was not found in your favorites.", parse_mode="Markdown")
        return

    # Otherwise show favorites list with quick live rates
    favs = StorageService.get_favorites(uid)
    if not favs:
        await update.message.reply_text(
            "⭐ You don't have any favorite pairs yet!\n\n"
            "Add one using:\n`/favorite add USD ETB`",
            parse_mode="Markdown"
        )
        return

    lines = ["⭐ **Your Favorite Currency Pairs:**\n"]
    for pair in favs:
        b, t = pair[0], pair[1]
        res = CurrencyService.convert(b, t, 1.0)
        if res.get("success"):
            lines.append(f"• **1 {b}** = `{res['rate']:.4f} {t}`")
        else:
            lines.append(f"• **{b}/{t}**")

    lines.append("\n_Click a pair below for quick 100-unit conversion or manage your list:_")
    msg = "\n".join(lines)
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=favorites_keyboard(favs))
