from aiogram.types import Message
from aiogram.filters import Command

from .dispetcher import dp
from models import UserLog
from func import check_user


MESS = """*Доступные команды для анализа данных*
    *Выгрузить существующие данные*
    что на данный момент хранится в баззе по меддокам
    \file_cases

    """.replace(
    "_", "\\_"
)


@dp.message(Command("analitic_panel"))
async def analitic_panel(message: Message):
    if not await check_user(message, "user"):
        return
    await UserLog.create(u_id=message.chat.id, action=10)
    return await message.answer(MESS, disable_notification=True, parse_mode="Markdown")
