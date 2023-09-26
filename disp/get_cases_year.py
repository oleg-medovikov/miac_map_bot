from aiogram.types import Message
from aiogram.filters import Command
from aiogram import md


from .dispetcher import dp
from models import UserLog
from func import check_user, return_year, get_meddoc_numbers


@dp.message(Command("get_cases_year"))
async def get_cases_year(message: Message):
    check, user = await check_user(message, "admin")
    if not check:
        return

    START, STOP = return_year()
    MESS = "Делаю выгрузку номеров меддокументов с " + str(START) + " по " + str(STOP)

    MESS += "\n\n"
    MESS += await get_meddoc_numbers(START, STOP)

    await UserLog.create(u_id=user.id, a_id=11)
    return await message.answer(
        md.quote(MESS), disable_notification=True, parse_mode="MarkdownV2"
    )
