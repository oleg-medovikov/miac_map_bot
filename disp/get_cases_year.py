from aiogram.types import Message
from aiogram.filters import Command
from aiogram import md


from .dispetcher import dp
from models import User, Log
from func import get_chat_fio, delete_message, return_year, get_meddoc_numbers


@dp.message(Command("get_cases_year"))
async def get_cases_year(message: Message):
    # === проверка на админа
    USER = await User.query.where(User.u_id == message.chat.id).gino.first()
    result = get_chat_fio(message)
    await delete_message(message)
    if USER is None or USER.role not in ("admin"):
        await Log.create(u_id=message.chat.id, action=3, result=result)
        mess = "У Вас недостаточно прав для этого действия!"
        return await message.answer(mess)
    # ===============================

    START, STOP = return_year()
    MESS = "Делаю выгрузку номеров меддокументов с " + str(START) + " по " + str(STOP)

    MESS += "\n\n"
    MESS += await get_meddoc_numbers(START, STOP)

    await Log.create(u_id=message.chat.id, action=11, result=MESS)
    return await message.answer(
        md.quote(MESS), disable_notification=True, parse_mode="MarkdownV2"
    )
