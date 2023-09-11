from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from .dispatcher import dp
from clas import User


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    try:
        USER = await User.get(message.from_user.id)
    except ValueError:
        mess = "Вы неизвестный пользователь!"
        return await message.answer(mess)

    mess = f"Приветствую, {USER.fio}!"
    return await message.answer(mess, disable_notification=True, parse_mode="html")
