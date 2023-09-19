from aiogram import md

from models import Token
from conf import settings
from disp import bot


async def refresh_tokens():
    await Token.update.values(active=True).gino.status()
    MESS = "активировал ключи"
    return await bot.send_message(
        settings.MASTER,
        md.quote(MESS),
        disable_notification=True,
        parse_mode="MarkdownV2",
    )
