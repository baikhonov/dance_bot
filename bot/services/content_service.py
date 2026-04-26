import re

from bot.data.repository import get_content
from bot.keyboards.menu import MENU_TO_CATEGORY


def get_faq_group_items(group_number):
    grouped = {}
    for item in get_content()["faq"]["items"]:
        group = item.get("group", 1)
        grouped.setdefault(group, []).append(item)
    return grouped, grouped.get(group_number, [])


def build_faq_text(group_number):
    grouped, group_items = get_faq_group_items(group_number)
    if not group_items:
        return "Раздел FAQ пока пуст."

    message = "\n\n".join(f"<b>{q['question']}</b>\n{q['answer']}" for q in group_items)
    return f"❓ Частые вопросы (блок {group_number}/{len(grouped)})\n\n{message}"


def get_faq_groups(current_group):
    grouped, _ = get_faq_group_items(current_group)
    return sorted(grouped.keys())


def render_direction_response(menu_type, direction_key):
    data = get_content()[MENU_TO_CATEGORY[menu_type]][direction_key]
    return f"{data['title']}:\n\n" + "\n".join(data["items"])


async def process_free_text(text):
    text = text.lower()
    responses = []
    bot_data = get_content()

    for category, category_data in bot_data.items():
        if category in ["prices", "schedule"]:
            for _, direction_data in category_data.items():
                for keyword in direction_data["keywords"]:
                    if re.search(rf"\b{re.escape(keyword)}", text):
                        response = f"{direction_data['title']}:\n\n" + "\n".join(direction_data["items"])
                        if response not in responses:
                            responses.append(response)
                        break
        elif category in ["address", "promotions", "contacts"]:
            for keyword in category_data["keywords"]:
                if re.search(rf"\b{re.escape(keyword)}", text):
                    if category_data["text"] not in responses:
                        responses.append(category_data["text"])
                    break
        elif category == "faq":
            for item in category_data["items"]:
                for keyword in item["keywords"]:
                    if re.search(rf"\b{re.escape(keyword)}", text):
                        faq_response = f"<b>{item['question']}</b>\n{item['answer']}"
                        if faq_response not in responses:
                            responses.append(faq_response)
                        break

    if not responses:
        return "Пожалуйста, выберите один из пунктов меню ниже 👇"

    if len(responses) == 1:
        return responses[0]

    header = "🔍 Вот что я нашел по вашему запросу:\n\n"
    separator = "\n\n――――――\n\n"
    return header + separator.join(responses[:3])
