from aiogram.types import Message
from aiogram.filters import CommandStart

from .dispetcher import dp
from models import UserLog
from func import check_user


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=0)
    mess = "Приветствую!"
    return await message.answer(mess, disable_notification=True, parse_mode="html")
