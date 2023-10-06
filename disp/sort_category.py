from aiogram.types import Message
from aiogram.filters import Command

from .dispetcher import dp
from models import UserLog
from func import check_user, sort_category


@dp.message(Command("sort_category"))
async def sort_category(message: Message):
    check, user = await check_user(message, "admin")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=16)

    mess = await sort_category()

    return await message.answer(mess, disable_notification=True, parse_mode="html")
