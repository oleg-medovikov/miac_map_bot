from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from .dispatcher import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    mess = f"Hello, {hbold(message.from_user.full_name)}!"
    return await message.answer(mess, disable_notification=True, parse_mode="html")
