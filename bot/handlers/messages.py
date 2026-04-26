from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.menu import get_main_menu_markup
from bot.services.content_service import process_free_text
from bot.services.stats_service import log_message_stats


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_message_stats(update)

    text = update.message.text
    response = await process_free_text(text)
    await update.message.reply_text(
        response,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=get_main_menu_markup(),
    )
