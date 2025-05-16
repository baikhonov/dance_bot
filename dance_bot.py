from telegram.helpers import escape_markdown
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto, InputMediaVideo
import logging

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


TOKEN = "7759262339:AAEd_szhH3dPBvrs7KrWJOOwqxhzEmRxKeg"

# Главное меню
main_menu_buttons = [["💃🕺 Танцы в паре", "👠 Женский стиль"], [
    "🧑‍🏫 Индивидуальные занятия"]]
main_menu_markup = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard=True)

# Подменю
submenu_buttons = [
    ["💸 Цены", "📅 Расписание"],
    ["📍 Как добраться", "❓ FAQ"],
    ["⬅️ Назад"]
]
submenu_markup = ReplyKeyboardMarkup(submenu_buttons, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Выберите направление:", reply_markup=main_menu_markup)


async def send_location_info(update: Update):
    await update.message.reply_text(
        "📍 *Как добраться:*\n\n"
        "🗺 Адрес: *Новотроицкое шоссе, 10* (2 этаж)\n\n"
        "🔗 Карты:\n"
        "• [Яндекс Карты](https://yandex.ru/maps/-/CHrLEEO7)\n"
        "• [Google Карты](https://maps.app.goo.gl/gAY7vvHBx5CbuKbB7)\n"
        "• [2ГИС](https://go.2gis.com/p3kDs)\n\n"
        "🚖 *Маршруты общественного транспорта:*\n"
        "1️⃣ Автобусы: *16, 16А, 24, 25, 26, 26А, 37, 38, 41, 55* — ост. *Тагильская*, вверх по Новотроицкому шоссе\n"
        "2️⃣ Маршрут *16А Новосибирская* — ост. *Баня*, далее вверх по Новотроицкому шоссе\n"
        "Ориентир: маг. *Трансдеталь*, напротив заправки *Башнефть*\n\n"
        "🚪 Вход с *обратной стороны здания*. Поднимайтесь на второй этаж.",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

    media = [
        InputMediaPhoto(
            media="AgACAgIAAxkBAAICrGggKvUpLL-bc9e8d46S2fsYTNf7AAL-8TEbCEkAAUnKnJXb1hfUYQEAAwIAA3gAAzYE", caption="Фото здания спереди"),
        InputMediaPhoto(
            media="AgACAgIAAxkBAAICs2ggK4fpSXoUpP1WTWQQxOJ3Q75GAAL_8TEbCEkAAUl2lhNGB2y5ogEAAwIAA3kAAzYE", caption="Фото парковки"),
        InputMediaVideo(
            media="BAACAgIAAxkBAAICtWggK7nKjKiCN3WAATvuBuJNrg6CAALCcgACCEkAAUn-A2e8HBdrNTYE", caption="Видео маршрута")
    ]

    await update.message.reply_media_group(media)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    direction = context.user_data.get("direction")

    if text in ["💃🕺 Танцы в паре", "👠 Женский стиль"]:
        context.user_data["direction"] = text
        await update.message.reply_text(f"Вы выбрали: {text}. Что вас интересует?", reply_markup=submenu_markup)

    elif text == "🧑‍🏫 Индивидуальные занятия":
        context.user_data.clear()
        await update.message.reply_text(
            "🧑‍🏫 *Индивидуальные занятия:*\n\n"
            "👥 Пары — до 2 человек\n"
            "👣 Соло — до 4 человек\n\n"
            "⏱ *Продолжительность*: 55 минут\n"
            "💵 Цена:\n"
            "— 1300₽ — один преподаватель\n"
            "— 1500₽ — два преподавателя\n\n"
            "📝 *Запись*: осуществляется по предоплате 500₽\n"
            "🚫 *Отмена*: не позднее чем за 3 часа до начала\n"
            "❌ При более поздней отмене — предоплата не возвращается",
            parse_mode="Markdown",
            reply_markup=main_menu_markup
        )

    elif text == "⬅️ Назад":
        context.user_data.clear()
        await update.message.reply_text("Вы вернулись в главное меню. Выберите направление:", reply_markup=main_menu_markup)

    elif text == "💸 Цены":
        if direction == "💃🕺 Танцы в паре":
            await update.message.reply_text(
                "💃🕺 Цены — Танцы в паре:\n\n"
                "✅ Пробное – 300р\n"
                "✅ Пробное в паре (М+Ж) – 250/500р\n"
                "✅ Разовое занятие – 400р\n"
                "☑️ Абонемент 4 занятия – 1400р\n"
                "☑️ Абонемент 8 занятий – 2400р\n\n"
                "🎁 Акция – приведи друга (М) впервые на танцы — не платите за это занятие оба (при условии, что вы оба приходите и друг ни разу не был у нас)\n"
                "🎉 Вечеринка — по цене абонемента или 400р разово\n\n"
                "📅 Абонемент действует 1 мес (30 календарных дней)\n"
                "❌ Деньги за купленные абонементы не возвращаются\n"
                "📌 Неиспользованные занятия списываются по старым условиям\n\n"
                "✅ Второе занятие для парней — бесплатно\n"
                "✅ Парни могут посещать любой поток\n\n"
                "📞 89011127646 — Татьяна Юрьевна (Сбер)"
            )
        elif direction == "👠 Женский стиль":
            await update.message.reply_text(
                "👠 Цены — Женский стиль:\n\n"
                "✅ Разовое занятие — 400 рублей\n"
                "📞 89011127646 — Татьяна Юрьевна (Сбер)"
            )
        else:
            await update.message.reply_text("Сначала выберите направление:", reply_markup=main_menu_markup)

    elif text == "📅 Расписание":
        if direction == "💃🕺 Танцы в паре":
            await update.message.reply_text(
                "📅 Расписание — Танцы в паре:\n\n"
                "🟢 Понедельник, Среда:\n"
                "   — 19:30-20:30 (Продолжающая группа)\n"
                "   — 20:30-21:30 (Продолжающая группа)\n\n"
                "🟡 Вторник, Четверг:\n"
                "   — 19:30-20:30 (Общее хорео)\n"
                "   — 20:30-21:30 (Начинающая группа)\n\n"
                "🔵 Суббота:\n"
                "   — 19:00-20:00 (Начинающая группа)\n"
                "   — 20:00-23:00 🎉Вечеринка🎉"
            )
        elif direction == "👠 Женский стиль":
            await update.message.reply_text(
                "📅 Расписание — Женский стиль:\n\n"
                "🟣 Пятница:\n"
                "   — 18:30-19:30 Lady Style (начинающие)\n"
                "   — 19:30-20:30 Lady Style (старшие)\n\n"
                "🟣 Воскресенье:\n"
                "   — 14:00-15:00 Lady Style (начинающие)\n"
                "   — 15:00-16:00 Lady Style (старшие)"
            )
        else:
            await update.message.reply_text("Сначала выберите направление:", reply_markup=main_menu_markup)

    elif text == "📍 Как добраться":
        await send_location_info(update)

    elif text == "❓ FAQ":
        if direction == "💃🕺 Танцы в паре":
            await update.message.reply_text("❓ FAQ — Танцы в паре:\n\n1. Без партнёра? — Нет!\n2. Сменка? — Обязательно.")
        elif direction == "👠 Женский стиль":
            await update.message.reply_text("❓ FAQ — Женский стиль:\n\n1. Без каблуков можно? — Да!\n2. Форма? — Удобная одежда.")
        else:
            await update.message.reply_text("Сначала выберите направление:", reply_markup=main_menu_markup)

    else:
        await update.message.reply_text("Пожалуйста, выберите один из пунктов меню ниже 👇", reply_markup=main_menu_markup)


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        application.run_polling(
            poll_interval=3,  # Интервал опроса сервера
            timeout=30,       # Таймаут запросов
            drop_pending_updates=True  # Игнорировать старые сообщения при перезапуске
        )
    except Exception as e:
        logger.error(f"Бот остановлен: {e}")
        raise  # Передаём ошибку в обёртку


if __name__ == "__main__":
    main()
