from datetime import datetime, timedelta
from aiogram import md

from conf import settings
from disp import bot
from func import get_meddoc_numbers


async def get_meddoc_automatic():
    START = datetime.now() - timedelta(days=25)
    STOP = datetime.now() + timedelta(days=1)
    MESS = (
        "Сделал выгрузку номеров меддокументов с "
        + START.strftime("%d-%m-%Y")
        + "\nпо "
        + STOP.strftime("%d-%m-%Y")
    )

    MESS += "\n\n"
    MESS += await get_meddoc_numbers(START, STOP)

    return await bot.send_message(
        settings.MASTER,
        md.quote(MESS),
        disable_notification=True,
        parse_mode="MarkdownV2",
    )
