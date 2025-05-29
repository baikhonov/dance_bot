import os
import time
import traceback
import logging
from telegram.helpers import escape_markdown
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto, InputMediaVideo
from dotenv import load_dotenv

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()  # Загружает переменные из .env

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Главное меню
main_menu_buttons = [
    ["💸 Цены", "📍 Адрес"],
    ["📅 Расписание", "❓ Частые вопросы"],
    ["Новый набор и акции", "Cвязь с нами"]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard=True)

# Подменю направлений
direction_buttons = [
    ["💃🕺 Танцы в паре", "👠 Женский стиль"],
    ["🧑‍🏫 Индивидуальные занятия"],
    ["⬅️ Назад"]
]
direction_markup = ReplyKeyboardMarkup(direction_buttons, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Выберите пункт меню:", reply_markup=main_menu_markup)


async def send_location_info(update: Update):
    await update.message.reply_text(
        "🗺 Адрес: *Новотроицкое шоссе, 10* (2 этаж)\n"
        "🚪 Вход с *обратной стороны здания*. Поднимайтесь на второй этаж.\n\n"
        "🔗 Карты:\n"
        "• [Яндекс Карты](https://yandex.ru/maps/-/CHrLEEO7)\n"
        "• [Google Карты](https://maps.app.goo.gl/gAY7vvHBx5CbuKbB7)\n"
        "• [2ГИС](https://go.2gis.com/p3kDs)\n\n"
        "🚖 *Маршруты общественного транспорта:*\n"
        "1️⃣ Автобусы: *16, 16А, 24, 25, 26, 26А, 37, 38, 41, 55* — ост. *Тагильская*, вверх по Новотроицкому шоссе\n"
        "2️⃣ Маршрут *16А Новосибирская* — ост. *Баня*, далее вверх по Новотроицкому шоссе\n"
        "Ориентир: маг. *Трансдеталь*, напротив заправки *Башнефть*",
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

    if text in ["💸 Цены", "📅 Расписание"]:
        context.user_data["menu"] = text
        await update.message.reply_text("Выберите направление:", reply_markup=direction_markup)

    elif text == "❓ Частые вопросы":
        await update.message.reply_text(
            "<b>Вы находитесь в Орске?</b>\n"
            "Да! Мы находимся в Орске по адресу Новотроицкое шоссе, 10 (от Новотроицка тоже недалеко).\n\n"

            "<b>А можно без партнёра на парные?</b>\n"
            "Да, можно, но лучше уточнить у @tanya_tlegenova (Татьяны)\n\n"

            "<b>Что нужно брать с собой на занятие?</b>\n"
            "Сменную обувь (кроссовки, если есть, то туфли, любую обувь с гнущейся подошвой).\n\n"

            "<b>А занятия сколько длятся по времени?</b>\n"
            "Групповое - 60 минут, индивидуальное —  55 минут ⏱️\n\n"

            "<b>Мне 38 лет, берёте?</b>\n"
            "Да. Нашим ученикам от 18 до 60+.\n\n"

            "<b>А я деревянный…</b>\n"
            "Это поправимо! У нас как раз всё для тех, кто начинает с нуля 😊\n\n"

            "<b>Я хочу на парные танцы, но мне, наверное, сначала надо соло?</b>\n"
            "Не обязательно.\n\n"

            "<b>Можно просто прийти посмотреть?</b>\n"
            "Можно, но лучше прийти и попробовать.\n\n"
            
            "<b>Чем занимается ваша школа? Как проходят занятия?</b>\n"
            "На парных занятиях мы учим <b>импровизировать</b> — чувствовать музыку и партнёра без заученных движений. "
            "А на соло (женском стиле) ставим красивые, выразительные хореографии, которые развивают пластику, осанку и уверенность.\n\n"

            "<b>Нужна ли специальная обувь для занятий?</b>\n"
            "Нет."
            ,
            parse_mode="HTML"
        )


        await update.message.reply_text(
            "<b>У вас такое расписание, а я работаю посменно, я не смогу ходить часто. Есть ли смысл ходить?</b>\n"
            "Конечно. Даже 1–2 занятия в неделю дают результат. Можно чередовать дни и выбирать удобные. "
            "А ещё есть индивидуальные занятия.\n\n"

            "<b>Вы танцуете только бачату?</b>\n"
            "Да! В бачате столько нюансов, что в неё легко влюбиться и изучать годами ✨.\n\n"
            
            "<b>А что такое соло?</b>\n"
            "Соло — это занятия без партнёра/партнёрши. Вы учитесь красиво танцевать, развиваете пластику и координацию.\n\n"
            
            "<b>Как проходят вечеринки?</b>\n"
            "Вечеринки с дресс-кодом/тематические (в определённом стиле или цвете, например, всё чёрное, яркое или в пижамах 😊). "
            "Танцуем три часа без алкоголя."
            "С собой приносим вкусняшки на стол. Часто проводим конкурсы, игры, квесты. "
            "Каждая суббота по-своему особенная. 😊\n\n"

            "<b>Какая активность есть вне студии?</b>\n"
            "Мы организуем выезды в другие города, на природу.\n\n"

            "<b>Проводите ли вы мастер-класс или программу на праздники и мероприятия?</b>\n"
            "Да, проводим. Условия обговариваются индивидуально.\n\n"

            "<b>А свадебные танцы ставите?</b>\n"
            "Да.\n\n"
            ,
            parse_mode="HTML"
        )

        return


    elif text == "📍 Адрес":
        await send_location_info(update)

    elif text == "Новый набор и акции":
        await update.message.reply_text(
            "🎁 Акция – приведи друга (М) впервые на танцы — не платите за это занятие оба (при условии, что вы оба приходите и друг ни разу не был у нас)\n"
            "✅ Второе по счету парное занятие для парней в понедельник и среду — бесплатно",
            parse_mode="Markdown"
        )

    elif text in ["💃🕺 Танцы в паре", "👠 Женский стиль", "🧑‍🏫 Индивидуальные занятия"]:
        context.user_data["direction"] = text
        menu = context.user_data.get("menu")

        if menu == "💸 Цены":
            if text == "💃🕺 Танцы в паре":
                await update.message.reply_text(
                    "✅ Пробное – 300р\n"
                    "✅ Пробное в паре (М+Ж) – 500р\n"
                    "✅ Разовое занятие – 400р\n"
                    "💃🕺 Абонемент 4 занятия – 1400р\n"
                    "💃🕺 Абонемент 8 занятий – 2400р\n"
                    "Абонемент действует 30 календарных дней с момента первого посещения. Возврату и обмену не подлежит"
                )
            elif text == "👠 Женский стиль":
                await update.message.reply_text(
                    "✅ Разовое занятие — 300 рублей\n"
                    "🙅‍♀️ Абонементов на это направление нет"
                )
            elif text == "🧑‍🏫 Индивидуальные занятия":
                await update.message.reply_text(
                    "— 1300₽ — один преподаватель\n"
                    "— 1500₽ — два преподавателя\n"
                    "⏱ *Продолжительность*: 55 минут\n\n"
                    "👥 В паре — до 2 человек\n"
                    "💃 Сольно — до 4 человек\n\n"
                    "📝 *Запись*: осуществляется по предоплате 500₽\n"
                    "🚫 *Отмена*: не позднее чем за 3 часа до начала\n"
                    "❌ При более поздней отмене — предоплата не возвращается",
                    parse_mode="Markdown"
                )

        elif menu == "📅 Расписание":
            if text == "💃🕺 Танцы в паре":
                await update.message.reply_text(
                    "🟢 Понедельник, Среда:\n"
                    "   — 19:30-20:30 (Продолжающая группа)\n"
                    "   — 20:30-21:30 (Продолжающая группа)\n\n"
                    "🟡 Вторник, Четверг:\n"
                    "   — 19:30-20:30 (занятие для парней и девушек, отработка навыков сольного танца)\n"
                    "   — 20:30-21:30 (Начинающая группа)\n\n"
                    "🔵 Суббота:\n"
                    "   — 19:00-20:00 (Начинающая группа)\n"
                    "   — 20:00-23:00 Тематическая вечеринка (без алкоголя)\n\n"
                    "🟣 Воскресенье:\n"
                    "   — 19:00-22:00 Танцы на улице (бесплатно, проводятся мастер-классы)"
                )
            elif text == "👠 Женский стиль":
                await update.message.reply_text(
                    "🟡 Вторник, Четверг:\n"
                    "   — 19:30-20:30 (занятие для парней и девушек, отработка навыков сольного танца)\n\n"
                    "🟣 Пятница (только леди):\n"
                    "   — 18:30-19:30 начинающие\n"
                    "   — 19:30-20:30 старшие\n\n"
                    "🟣 Воскресенье (только леди):\n"
                    "   — 14:00-15:00 начинающие\n"
                    "   — 15:00-16:00 старшие"
                )
            elif text == "🧑‍🏫 Индивидуальные занятия":
                await update.message.reply_text(
                    "⏱️ Дата и время подбираются индивидуально с  @tanya_tlegenova (Татьяной) и @Keulemzhay_Tlegenov (Кеулемжаем)"
                )


        elif menu == "❓ Частые вопросы":
            if text == "💃🕺 Танцы в паре":
                await update.message.reply_text(
                    "❓ FAQ — Танцы в паре:\n\n"
                    "1. Без партнёра? — Нет!\n"
                    "2. Сменка? — Обязательно."
                )
            elif text == "👠 Женский стиль":
                await update.message.reply_text(
                    "❓ FAQ — Женский стиль:\n\n"
                    "1. Без каблуков можно? — Да!\n"
                    "2. Форма? — Удобная одежда."
                )
            elif text == "🧑‍🏫 Индивидуальные занятия":
                await update.message.reply_text(
                    "❓ FAQ — Индивидуальные занятия:\n\n"
                    "1. Когда можно записаться? — В любой день по договорённости\n"
                    "2. Сколько человек в группе? — До 4 (сольно) / до 2 (в паре)"
                )

    elif text == "⬅️ Назад":
        context.user_data.clear()
        await update.message.reply_text("Вы вернулись в главное меню. Выберите пункт:", reply_markup=main_menu_markup)

    elif text == "Cвязь с нами":
        await update.message.reply_text(
            "👩‍💼 <b>Татьяна Тлегенова</b>\n"
            "📞 Телефон: +7 (901) 112-76-46\n"
            "📘 <a href='https://vk.com/tanya_tlegenova'>ВКонтакте</a>\n"
            "📩 <a href='https://t.me/tanya_tlegenova'>Telegram</a>\n"
            "💬 <a href='https://wa.me/79011127646'>WhatsApp</a>\n\n"
            "👨‍💼 <b>Кеулемжай Тлегенов</b>\n"
            "📞 Телефон: +7 (953) 455-21-75\n"
            "📘 <a href='https://vk.com/ktlegenov'>ВКонтакте</a>\n"
            "📩 <a href='https://t.me/Keulemzhay_Tlegenov'>Telegram</a>\n"
            "💬 <a href='https://wa.me/79534552175'>WhatsApp</a>\n\n"
            "Вы можете написать или позвонить любому из преподавателей.\n\n"

            "<b>Аккаунты студии BachataManía</b>\n"
            "<a href='https://t.me/bachata_orsk'>Мы в Telegram</a>\n"
            "<a href='https://vk.com/bachatamania_56'>Мы в ВК</a>\n"
            "<a href='https://t.me/+wQ6vcAPYPRVlNTYy'>Женское соло</a>\n"
            "Подпишись! 😉"
            
            ,
            parse_mode="HTML",
            disable_web_page_preview=True
        )



    else:
        await update.message.reply_text("Пожалуйста, выберите один из пунктов меню ниже 👇", reply_markup=main_menu_markup)


def create_application():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application


def main():
    try:
        application = create_application()
        logger.info("Запуск бота...")

        application.run_polling(
            poll_interval=3,
            timeout=30,
            drop_pending_updates=True
        )

    except KeyboardInterrupt:
        logger.info("Бот остановлен вручную")

    except Exception:
        error_msg = traceback.format_exc()
        logger.error(f"Ошибка бота:\n{error_msg}")
        print(f"Ошибка бота:\n{error_msg}")
        # Без sleep — пусть systemd решает, когда перезапускать
        raise  # Важно! Исключение поднимается наверх → systemd увидит сбой


if __name__ == "__main__":
    main()
