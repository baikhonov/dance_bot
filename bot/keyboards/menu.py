from telegram import InlineKeyboardButton, InlineKeyboardMarkup


DIRECTION_LABELS = {
    "couple": "💃🕺 Танцы в паре",
    "solo": "👠 Женский стиль",
    "individual": "🧑‍🏫 Индивидуальные занятия",
}

MENU_TO_CATEGORY = {
    "prices": "prices",
    "schedule": "schedule",
    "address": "address",
    "faq": "faq",
    "promo": "promotions",
    "contacts": "contacts",
}


def get_main_menu_markup():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💸 Цены", callback_data="menu:prices"),
                InlineKeyboardButton("📍 Адрес", callback_data="menu:address"),
            ],
            [
                InlineKeyboardButton("📅 Расписание", callback_data="menu:schedule"),
                InlineKeyboardButton("❓ Частые вопросы", callback_data="menu:faq:1"),
            ],
            [
                InlineKeyboardButton("Новый набор и акции", callback_data="menu:promo"),
                InlineKeyboardButton("Cвязь с нами", callback_data="menu:contacts"),
            ],
        ]
    )


def get_direction_markup(menu_type):
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(DIRECTION_LABELS["couple"], callback_data=f"dir:{menu_type}:couple")],
            [InlineKeyboardButton(DIRECTION_LABELS["solo"], callback_data=f"dir:{menu_type}:solo")],
            [InlineKeyboardButton(DIRECTION_LABELS["individual"], callback_data=f"dir:{menu_type}:individual")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="nav:main")],
        ]
    )


def get_back_to_main_markup():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Назад в меню", callback_data="nav:main")]]
    )


def get_faq_markup(current_group, groups):
    row = []
    idx = groups.index(current_group) if current_group in groups else 0

    if idx > 0:
        prev_group = groups[idx - 1]
        row.append(InlineKeyboardButton("⬅️ Предыдущий", callback_data=f"menu:faq:{prev_group}"))
    if idx < len(groups) - 1:
        next_group = groups[idx + 1]
        row.append(InlineKeyboardButton("Следующий ➡️", callback_data=f"menu:faq:{next_group}"))

    rows = [row] if row else []
    rows.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="nav:main")])
    return InlineKeyboardMarkup(rows)
