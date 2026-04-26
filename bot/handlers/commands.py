from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.config import ADMIN_ID
from bot.keyboards.menu import get_main_menu_markup
from bot.services.stats_service import build_stats_report


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Обновляю меню...", reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text("Выберите пункт меню:", reply_markup=get_main_menu_markup())


async def send_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Доступ запрещён.")
        return

    try:
        await update.message.reply_text(build_stats_report())
    except Exception as error:
        await update.message.reply_text(f"Ошибка чтения stats.json: {error}")
