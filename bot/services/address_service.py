import logging

from telegram import InputMediaPhoto, InputMediaVideo
from telegram.error import BadRequest

from bot.data.repository import get_content
from bot.keyboards.menu import get_back_to_main_markup


logger = logging.getLogger(__name__)


async def send_location_info_from_query(query):
    address = get_content()["address"]

    media_group = []
    for media in address["media"]:
        if media["type"] == "photo":
            media_group.append(InputMediaPhoto(media=media["media"], caption=media.get("caption", "")))
        elif media["type"] == "video":
            media_group.append(InputMediaVideo(media=media["media"], caption=media.get("caption", "")))

    failed_media = []
    try:
        if media_group:
            await query.message.reply_media_group(media=media_group)
    except BadRequest as error:
        logger.warning("Не удалось отправить media-group для адреса: %s", error)
        failed_media = [item.get("caption", "Без подписи") for item in address["media"]]

    if failed_media:
        await query.message.reply_text(
            "Часть медиа не удалось отправить:\n- " + "\n- ".join(failed_media),
            reply_markup=get_back_to_main_markup(),
        )
        return

    await query.message.reply_text(
        address["text"],
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=get_back_to_main_markup(),
    )
