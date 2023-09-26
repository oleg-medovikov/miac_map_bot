from aiogram.types import Message
from aiogram.filters import Command

from .dispetcher import dp
from models import UserLog
from func import check_user, get_one_meddoc


@dp.message(Command("get_one_case"))
async def get_one_case(message: Message):
    if not await check_user(message, "user"):
        return

    MESS = "Делаю выгрузку одного меддока: "

    MESS += "\n\n"
    MESS += " ``` \n"
    MESS += get_one_meddoc()
    MESS += "\n ``` "

    await UserLog.create(u_id=message.chat.id, action=11, result=MESS)
    return await message.answer(
        MESS, disable_notification=True, parse_mode="MarkdownV2"
    )
