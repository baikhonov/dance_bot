import os
import json
import re
import logging
from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto, InputMediaVideo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Единая база данных бота
BOT_DATA = {
    "prices": {
        "couple": {
            "title": "💃🕺 Танцы в паре",
            "items": [
                "✅ Пробное – 300р",
                "✅ Пробное в паре (М+Ж) – 500р",
                "✅ Разовое занятие – 400р",
                "💃🕺 Абонемент 4 занятия – 1400р",
                "💃🕺 Абонемент 8 занятий – 2400р *",
                "💃🕺 Абонемент 10 занятий – 3000р **",
                "* - с возможностью бесплатно ходить в среднюю группу (для парней, обучающих очно в учебных заведениях)",
                "** - с возможностью бесплатно ходить в среднюю группу (для всех парней)",
                "Абонементы действуют 30 календарных дней с момента первого посещения. Возврату и обмену не подлежат."
            ],
            "keywords": ["парные", "бачата", "партнер", "партнерша", "пара", "сколько", "абонемент", "цена", "стоимость"]
        },
        "solo": {
            "title": "👠 Женский стиль",
            "items": [
                "✅ Разовое занятие — 300 рублей",
                "🙅‍♀️ Абонементов на это направление нет"
            ],
            "keywords": ["соло", "женск", "девуш", "леди", "сколько", "абонемент", "цена", "стоимость"]
        },
        "individual": {
            "title": "🧑‍🏫 Индивидуальные занятия",
            "items": [
                "— 1300₽ — один преподаватель",
                "— 1500₽ — два преподавателя",
                "⏱ Продолжительность: 55 минут",
                "👥 В паре — до 2 человек",
                "💃 Сольно — до 4 человек",
                "📝 Запись: осуществляется по предоплате 500₽",
                "🚫 Отмена: не позднее чем за 3 часа до начала",
                "❌ При более поздней отмене — предоплата не возвращается"
            ],
            "keywords": ["индивид", "персон", "частн", "сколько", "цена", "стоимость"]
        }
    },
    "schedule": {
        "couple": {
            "title": "💃🕺 Танцы в паре",
            "items": [
                "🟢 Понедельник, Среда:",
                "   — 19:30-20:30 (Старшая группа)",
                "   — 20:30-21:30 (Старшая группа)\n\n",
                "🟡 Вторник:",
                "   — 19:30-20:30 (общее хорео соло - занятие для парней и девушек, отработка навыков сольного танца)",
                "   — 20:30-21:30 (Бачата 24ч курс)\n\n",
                "🔴 Четверг:",
                "   — 19:30-20:30 (общее хорео соло - занятие для парней и девушек, отработка навыков сольного танца)",
                "   — 20:30-21:30 (Средняя группа)\n\n",
                "🔵 Суббота:",
                "   — 19:00-20:00 (Средняя группа)",
                "   — 20:00-23:00 Тематическая вечеринка (без алкоголя)\n\n",
                "🟤 Воскресенье:",
                "   — 18:00-19:00 (Бачата 24ч курс)",
            ],
            "keywords": ["парные", "бачата", "партнер", "партнерша", "пара", "расписание", "когда", "дни"]
        },
        "solo": {
            "title": "👠 Женский стиль",
            "items": [
                "🟡 Вторник, Четверг:",
                "   — 19:30-20:30 (общее хорео соло - занятие для парней и девушек, отработка навыков сольного танца)\n\n",
                "🟣 Воскресенье (только леди):",
                "   — 16:00-17:00 общий уровень",
                "   — 15:00-16:00 начинающие"
            ],
            "keywords": ["соло", "женск", "девуш", "леди", "расписание", "когда", "дни"]
        },
        "individual": {
            "title": "🧑‍🏫 Индивидуальные занятия",
            "items": [
                '⏱️ Дата и время подбираются индивидуально с <a href="https://t.me/tanya_tlegenova">Татьяной</a> и <a href="https://t.me/Keulemzhay_Tlegenov">Кеулемжаем</a>'
            ],
            "keywords": ["индивид", "персон", "частн", "расписание", "когда", "дни"]
        }
    },
    "address": {
        "text": "🗺 Адрес: <b>Новотроицкое шоссе, 10</b> (2 этаж)\n🚪 Вход с <b>обратной стороны здания</b>. Поднимайтесь на второй этаж.\n\n"
                "🔗 Карты:\n"
                "• <a href='https://yandex.ru/maps/-/CHrLEEO7'>Яндекс Карты</a>\n"
                "• <a href='https://maps.app.goo.gl/gAY7vvHBx5CbuKbB7'>Google Карты</a>\n"
                "• <a href='https://go.2gis.com/p3kDs'>2ГИС</a>\n\n"
                "🚖 <b>Маршруты общественного транспорта:</b>\n"
                "1️⃣ Автобусы: <b>3, 4, 6, 30</b>\n"
                "Маршрутки: <b>16, 16А, 23А, 24, 25, 25Б, 26, 26А, 37, 38, 44, 55</b>\n"
                "Трамваи: <b>1, 3, 5А, 7, 8</b>\n"
                "— ост. <b>Тагильская</b>, вверх по Новотроицкому шоссе\n"
                "2️⃣ Маршрут <b>16А Новосибирская</b> — ост. <b>Баня</b>, далее вверх по Новотроицкому шоссе\n"
                "Ориентир: маг. <b>Трансдеталь</b>, напротив заправки <b>Башнефть</b>",
        "keywords": ["адрес", "где", "метро", "доехать", "местоположение", "город"],
        "media": [
            {
                "type": "photo",
                "media": "AgACAgIAAxkBAAICrGggKvUpLL-bc9e8d46S2fsYTNf7AAL-8TEbCEkAAUnKnJXb1hfUYQEAAwIAA3gAAzYE",
                "caption": "Фото здания спереди"
            },
            {
                "type": "photo",
                "media": "AgACAgIAAxkBAAICs2ggK4fpSXoUpP1WTWQQxOJ3Q75GAAL_8TEbCEkAAUl2lhNGB2y5ogEAAwIAA3kAAzYE",
                "caption": "Фото парковки"
            },
            {
                "type": "video",
                "media": "BAACAgIAAxkBAAICtWggK7nKjKiCN3WAATvuBuJNrg6CAALCcgACCEkAAUn-A2e8HBdrNTYE",
                "caption": "Видео маршрута"
            }
        ]
    },
    "faq": {
        "items": [
            {
                "question": "Вы находитесь в Орске?",
                "answer": "Да! Мы находимся в Орске по адресу Новотроицкое шоссе, 10 (от Новотроицка тоже недалеко).",
                "group": 1,
                "keywords": ["местоположение", "где вы", "адрес", "орск", "новотроицк"]
            },
            {
                "question": "А можно без партнёра на парные?",
                "answer": 'Да, можно, но лучше уточнить у  <a href="https://t.me/tanya_tlegenova">Татьяны</a>.',
                "group": 1,
                "keywords": ["без партнёра", "нет партнёра", "одному", "парные", "одна", "один"]
            },
            {
                "question": "Что нужно брать с собой на занятие?",
                "answer": "Сменную обувь (кроссовки, если есть, то туфли, любую обувь с гнущейся подошвой).",
                "group": 1,
                "keywords": ["что взять", "одежда", "обувь", "с собой", "форма"]
            },
            {
                "question": "А занятия сколько длятся по времени?",
                "answer": "Групповое - 60 минут, индивидуальное — 55 минут ⏱️",
                "group": 1,
                "keywords": ["длительность", "время", "сколько длится", "продолжительность"]
            },
            {
                "question": "Мне 38 лет, берёте?",
                "answer": "Да. Нашим ученикам от 18 до 60+.",
                "group": 1,
                "keywords": ["возраст", "мне лет", "берёте ли", "старше", "подхожу ли"]
            },
            {
                "question": "А я деревянный…",
                "answer": "Это поправимо! У нас как раз всё для тех, кто начинает с нуля 😊",
                "group": 1,
                "keywords": ["деревянный", "неловкий", "начинающий", "с нуля", "не умею танцевать"]
            },
            {
                "question": "Я хочу на парные танцы, но мне, наверное, сначала надо соло?",
                "answer": "Не обязательно.",
                "group": 1,
                "keywords": ["соло перед парными", "нужно ли соло", "сначала соло", "парные"]
            },
            {
                "question": "Можно просто прийти посмотреть?",
                "answer": "Можно, но лучше прийти и попробовать.",
                "group": 1,
                "keywords": ["прийти посмотреть", "можно глянуть", "без участия", "ознакомиться"]
            },
            {
                "question": "Чем занимается ваша школа? Как проходят занятия?",
                "answer": "На парных занятиях мы учим <b>импровизировать</b> — чувствовать музыку и партнёра без заученных движений. А на соло (женском стиле) ставим красивые, выразительные хореографии, которые развивают пластику, осанку и уверенность.",
                "group": 1,
                "keywords": ["чем занимаетесь", "как проходят", "чему учите", "о школе", "занятия"]
            },
            {
                "question": "Нужна ли специальная обувь для занятий?",
                "answer": "Нет.",
                "group": 1,
                "keywords": ["специальная обувь", "нужна ли обувь", "обувь", "танцы"]
            },
            {
                "question": "У вас такое расписание, а я работаю посменно, я не смогу ходить часто. Есть ли смысл ходить?",
                "answer": "Конечно. Даже 1–2 занятия в неделю дают результат. Можно чередовать дни и выбирать удобные. А ещё есть индивидуальные занятия.",
                "group": 2,
                "keywords": ["посменно", "редко", "не часто", "заниматься редко", "график"]
            },
            {
                "question": "Вы танцуете только бачату?",
                "answer": "Да! В бачате столько нюансов, что в неё легко влюбиться и изучать годами ✨.",
                "group": 2,
                "keywords": ["бачата", "только бачата", "вид танцев", "что танцуете"]
            },
            {
                "question": "А что такое соло?",
                "answer": "Соло — это занятия без партнёра/партнёрши. Вы учитесь красиво танцевать, развиваете пластику и координацию.",
                "group": 2,
                "keywords": ["соло", "женский стиль", "без партнёра", "одиночные"]
            },
            {
                "question": "Как проходят вечеринки?",
                "answer": "Вечеринки с дресс-кодом/тематические (в определённом стиле или цвете, например, всё чёрное, яркое или в пижамах 😊). Танцуем три часа без алкоголя. С собой приносим вкусняшки на стол. Часто проводим конкурсы, игры, квесты. Каждая суббота по-своему особенная. 😊",
                "group": 2,
                "keywords": ["вечеринки", "танцы вечером", "мероприятия", "суббота", "вечер"]
            },
            {
                "question": "Какая активность есть вне студии?",
                "answer": "Мы организуем выезды в другие города, на природу.",
                "group": 2,
                "keywords": ["вне студии", "поездки", "выезды", "на природу", "поездка"]
            },
            {
                "question": "Проводите ли вы мастер-класс или программу на праздники и мероприятия?",
                "answer": "Да, проводим. Условия обговариваются индивидуально.",
                "group": 2,
                "keywords": ["мастер-класс", "праздники", "мероприятия", "выступление", "программа"]
            },
            {
                "question": "А свадебные танцы ставите?",
                "answer": "Да.",
                "group": 2,
                "keywords": ["свадьба", "свадебный танец", "первый танец", "свадебные", "постановка"]
            }
        ]
    },
    "promotions": {
        "text": "🆕 Новый набор с 1 октября 2025 года, первое пробное занятие 27 сентября\n"
                "🎁 Акция – приведи друга (М) впервые на танцы — не платите за это занятие оба (при условии, что вы оба приходите и друг ни разу не был у нас)\n"
                "✅ Второе по счету парное занятие для парней в понедельник и среду — бесплатно\n",
        "keywords": ["акция", "скидка", "промо", "набор"]
    },
    "contacts": {
        "text": "👩‍💼 <b>Татьяна Тлегенова</b>\n"
                "📞 Телефон: +7 (901) 112-76-46\n"
                "📘 <a href='https://vk.com/tanya_tlegenova'>ВКонтакте</a>\n"
                "📩 <a href='https://t.me/tanya_tlegenova'>Telegram</a>\n"
                "💬 <a href='https://wa.me/79011127646'>WhatsApp</a>\n\n"
                "👨‍💼 <b>Кеулемжай Тлегенов</b>\n"
                "📞 Телефон: +7 (953) 455-21-75\n"
                "📘 <a href='https://vk.com/ktlegenov'>ВКонтакте</a>\n"
                "📩 <a href='https://t.me/Keulemzhay_Tlegenov'>Telegram</a>\n"
                "💬 <a href='https://wa.me/79534552175'>WhatsApp</a>\n\n"
                "<b>Аккаунты студии BachataManía</b>\n"
                "<a href='https://t.me/bachata_orsk'>Мы в Telegram</a>\n"
                "<a href='https://vk.com/bachatamania_56'>Мы в ВК</a>\n"
                "<a href='https://t.me/+wQ6vcAPYPRVlNTYy'>Женское соло</a>\n"
                "Подпишись! 😉",
        "keywords": ["контакты", "связь", "телефон", "преподаватель"]
    }
}

# Клавиатуры
main_menu_buttons = [
    ["💸 Цены", "📍 Адрес"],
    ["📅 Расписание", "❓ Частые вопросы"],
    ["Новый набор и акции", "Cвязь с нами"]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard=True)

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
    address = BOT_DATA["address"]
    await update.message.reply_text(address["text"], parse_mode="HTML", disable_web_page_preview=True)

    media_group = []
    for media in address["media"]:
        if media["type"] == "photo":
            media_group.append(InputMediaPhoto(
                media["media"], caption=media["caption"]))
        else:
            media_group.append(InputMediaVideo(
                media["media"], caption=media["caption"]))

    await update.message.reply_media_group(media_group)


async def process_free_text(text):
    text = text.lower()
    responses = []

    # Собираем все возможные ответы из всех категорий
    for category, category_data in BOT_DATA.items():
        # Обработка цен и расписания
        if category in ["prices", "schedule"]:
            for direction, direction_data in category_data.items():
                # Проверяем все ключевые слова для этого направления
                for keyword in direction_data["keywords"]:
                    if re.search(rf'\b{re.escape(keyword)}', text):
                        response = f"{direction_data['title']}:\n\n" + \
                            "\n".join(direction_data["items"])
                        if response not in responses:  # Избегаем дубликатов
                            responses.append(response)
                        break  # Прерываем после первого совпадения в этом направлении

        # Обработка адреса, акций и контактов
        elif category in ["address", "promotions", "contacts"]:
            for keyword in category_data["keywords"]:
                if re.search(rf'\b{re.escape(keyword)}', text):
                    if category_data["text"] not in responses:
                        responses.append(category_data["text"])
                    break

        # Обработка FAQ
        elif category == "faq":
            for item in category_data["items"]:
                for keyword in item["keywords"]:
                    if re.search(rf'\b{re.escape(keyword)}', text):
                        faq_response = f"<b>{item['question']}</b>\n{item['answer']}"
                        if faq_response not in responses:
                            responses.append(faq_response)
                        break

    # Формируем итоговый ответ
    if not responses:
        return "Пожалуйста, выберите один из пунктов меню ниже 👇"

    if len(responses) == 1:
        return responses[0]

    # Для нескольких ответов добавляем заголовок и разделители
    header = "🔍 Вот что я нашел по вашему запросу:\n\n"
    separator = "\n\n――――――\n\n"
    return header + separator.join(responses[:3])  # Ограничиваем 3 ответами


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime
    import json

    def log_stats(update: Update):
        stats_file = "stats.json"
        today = datetime.now().strftime("%Y-%m-%d")
        user_id = str(update.effective_user.id)
        text = update.message.text

        try:
            with open(stats_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            stats = {}

        if today not in stats:
            stats[today] = {
                "new_users": [],
                "active_users": [],
                "button_clicks": {},
            }

        day_stats = stats[today]

        if user_id not in day_stats["active_users"]:
            day_stats["active_users"].append(user_id)

        if user_id not in day_stats["new_users"]:
            # Новый пользователь за день
            # Можно уточнить регистрацию более точно, если нужно
            day_stats["new_users"].append(user_id)

        if text in day_stats["button_clicks"]:
            day_stats["button_clicks"][text] += 1
        else:
            day_stats["button_clicks"][text] = 1

        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    log_stats(update)

    text = update.message.text
    user_data = context.user_data

    # Обработка кнопок главного меню
    if text in ["💸 Цены", "📅 Расписание"]:
        user_data["menu"] = text
        await update.message.reply_text("Выберите направление:", reply_markup=direction_markup)
        return

    # Обработка кнопок направлений
    if text in ["💃🕺 Танцы в паре", "👠 Женский стиль", "🧑‍🏫 Индивидуальные занятия"]:
        user_data["direction"] = text
        menu = user_data.get("menu")

        if menu == "💸 Цены":
            direction_key = "couple" if text == "💃🕺 Танцы в паре" else "solo" if text == "👠 Женский стиль" else "individual"
            data = BOT_DATA["prices"][direction_key]
            await update.message.reply_text("\n".join(data["items"]))
        elif menu == "📅 Расписание":
            direction_key = "couple" if text == "💃🕺 Танцы в паре" else "solo" if text == "👠 Женский стиль" else "individual"
            if direction_key in BOT_DATA["schedule"]:
                data = BOT_DATA["schedule"][direction_key]
                await update.message.reply_text("\n".join(data["items"]),
                                                parse_mode='HTML',
                                                disable_web_page_preview=True)
        return

    # Обработка других кнопок
    if text == "📍 Адрес":
        await send_location_info(update)
        return

    if text == "❓ Частые вопросы":
        groups = {}
        for item in BOT_DATA["faq"]["items"]:
            group = item.get("group", 1)
            if group not in groups:
                groups[group] = []
            groups[group].append(item)

        for group_num, items in groups.items():
            message = "\n\n".join(
                f"<b>{q['question']}</b>\n{q['answer']}" for q in items)
            await update.message.reply_text(message, parse_mode="HTML", disable_web_page_preview=True)
        return

    if text == "Новый набор и акции":
        await update.message.reply_text(BOT_DATA["promotions"]["text"], parse_mode="HTML")
        return

    if text == "Cвязь с нами":
        await update.message.reply_text(BOT_DATA["contacts"]["text"], parse_mode="HTML", disable_web_page_preview=True)
        return

    if text == "⬅️ Назад":
        await start(update, context)
        return

    # Обработка произвольного текста
    response = await process_free_text(text)
    await update.message.reply_text(response, reply_markup=main_menu_markup, parse_mode="HTML", disable_web_page_preview=True)

async def send_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = 1888074242  #  Telegram ID админа

    if update.effective_user.id != admin_id:
        await update.message.reply_text("⛔ Доступ запрещён.")
        return

    try:
        with open("stats.json", "r", encoding="utf-8") as f:
            stats = json.load(f)
    except Exception as e:
        await update.message.reply_text(f"Ошибка чтения stats.json: {e}")
        return

    if not stats:
        await update.message.reply_text("Файл stats.json пуст.")
        return

    dates = sorted(stats.keys(), reverse=True)[:7]
    report_lines = ["📊 Статистика за последние 7 дней\n"]

    button_totals = {}

    for date in dates:
        day = stats[date]
        new = len(day.get("new_users", []))
        active = len(day.get("active_users", []))
        total_clicks = sum(day.get("button_clicks", {}).values())

        report_lines.append(
            f"📅 {date}\n"
            f"👥 Новые пользователи: {new}\n"
            f"🔄 Активные пользователи: {active}\n"
            f"🖱 Нажатий кнопок: {total_clicks}\n"
        )

        # Суммируем по всем дням
        for btn, count in day.get("button_clicks", {}).items():
            button_totals[btn] = button_totals.get(btn, 0) + count

    # Топ кнопок
    top_buttons = sorted(button_totals.items(), key=lambda x: x[1], reverse=True)[:10]
    report_lines.append("🔝 Топ-10 кнопок")
    for btn, count in top_buttons:
        report_lines.append(f"- {btn}: {count}")

    await update.message.reply_text("\n".join(report_lines))


def create_application():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("stats", send_stats))
    return application


def main():
    application = create_application()
    logger.info("Запуск бота...")
    application.run_polling()


if __name__ == "__main__":
    main()
