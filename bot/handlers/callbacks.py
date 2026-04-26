from telegram import Update
from telegram.ext import ContextTypes

from bot.data.repository import get_content
from bot.keyboards.menu import (
    DIRECTION_LABELS,
    get_back_to_main_markup,
    get_direction_markup,
    get_faq_markup,
    get_main_menu_markup,
)
from bot.services.address_service import send_location_info_from_query
from bot.services.content_service import build_faq_text, get_faq_groups, render_direction_response


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    callback_data = query.data
    bot_data = get_content()

    if callback_data == "nav:main":
        context.user_data.clear()
        await query.message.reply_text("Выберите пункт меню:", reply_markup=get_main_menu_markup())
        return

    if callback_data in ("menu:prices", "menu:schedule"):
        menu_type = callback_data.split(":")[1]
        context.user_data["menu_type"] = menu_type
        await query.message.reply_text("Выберите направление:", reply_markup=get_direction_markup(menu_type))
        return

    if callback_data.startswith("dir:"):
        parts = callback_data.split(":")
        if len(parts) != 3:
            await query.message.reply_text(
                "Эта кнопка устарела. Откройте меню заново.",
                reply_markup=get_back_to_main_markup(),
            )
            return

        _, menu_type, direction_key = parts
        if menu_type not in ("prices", "schedule") or direction_key not in DIRECTION_LABELS:
            await query.message.reply_text(
                "Эта кнопка устарела. Откройте меню заново.",
                reply_markup=get_back_to_main_markup(),
            )
            return

        response_text = render_direction_response(menu_type, direction_key)
        await query.message.reply_text(
            response_text,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=get_direction_markup(menu_type),
        )
        return

    if callback_data == "menu:address":
        await send_location_info_from_query(query)
        return

    if callback_data.startswith("menu:faq"):
        parts = callback_data.split(":")
        current_group = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 1
        await query.message.reply_text(
            build_faq_text(current_group),
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=get_faq_markup(current_group, get_faq_groups(current_group)),
        )
        return

    if callback_data == "menu:promo":
        await query.message.reply_text(
            bot_data["promotions"]["text"],
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=get_back_to_main_markup(),
        )
        return

    if callback_data == "menu:contacts":
        await query.message.reply_text(
            bot_data["contacts"]["text"],
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=get_back_to_main_markup(),
        )
        return

    await query.message.reply_text(
        "Неизвестная команда меню. Откройте меню заново.",
        reply_markup=get_back_to_main_markup(),
    )
