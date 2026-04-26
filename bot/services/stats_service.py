import json
from datetime import datetime

from bot.config import STATS_FILE


def log_message_stats(update):
    today = datetime.now().strftime("%Y-%m-%d")
    user_id = str(update.effective_user.id)
    text = update.message.text

    try:
        with open(STATS_FILE, "r", encoding="utf-8") as file:
            stats = json.load(file)
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
        day_stats["new_users"].append(user_id)

    if text in day_stats["button_clicks"]:
        day_stats["button_clicks"][text] += 1
    else:
        day_stats["button_clicks"][text] = 1

    with open(STATS_FILE, "w", encoding="utf-8") as file:
        json.dump(stats, file, ensure_ascii=False, indent=2)


def build_stats_report():
    with open(STATS_FILE, "r", encoding="utf-8") as file:
        stats = json.load(file)

    if not stats:
        return "Файл stats.json пуст."

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

        for btn, count in day.get("button_clicks", {}).items():
            button_totals[btn] = button_totals.get(btn, 0) + count

    top_buttons = sorted(button_totals.items(), key=lambda x: x[1], reverse=True)[:10]
    report_lines.append("🔝 Топ-10 кнопок")
    for btn, count in top_buttons:
        report_lines.append(f"- {btn}: {count}")

    return "\n".join(report_lines)
