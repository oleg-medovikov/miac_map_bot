from aiogram.types import Message
from aiogram.filters import CommandStart

from .dispetcher import dp
from models import User


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    USER = await User.query.where(User.u_id == message.chat.id).gino.one()
    if USER is None:
        mess = "Вы неизвестный пользователь!"
        return await message.answer(mess)

    mess = f"Приветствую, {USER.fio}!"
    return await message.answer(mess, disable_notification=True, parse_mode="html")
