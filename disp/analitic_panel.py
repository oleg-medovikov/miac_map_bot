from aiogram.types import Message
from aiogram.filters import Command

from .dispetcher import dp
from models import UserLog
from func import check_user


MESS = """*Доступные команды для анализа данных*
    *Выгрузить существующие данные*
    что на данный момент хранится в баззе по меддокам
    /file_cases
    
    *Файл с меддоками у которых пуcтая история болезни*
    /null_history_number

    """.replace(
    "_", "\\_"
)


@dp.message(Command("analitic_panel"))
async def analitic_panel(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=30)
    return await message.answer(MESS, disable_notification=True, parse_mode="Markdown")
