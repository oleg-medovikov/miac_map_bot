from aiogram.types import Message
from aiogram.filters import CommandStart

from .dispetcher import dp
from models import User, Log


LIST = ["username", "first_name", "last_name"]


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    USER = await User.query.where(User.u_id == message.chat.id).gino.first()
    result = " ".join([message.chat.__dict__[_] for _ in LIST])
    if USER is None:
        await Log.create(u_id=message.chat.id, action=2, result=result)
        mess = "Вы неизвестный пользователь!"
        return await message.answer(mess)

    await Log.create(u_id=message.chat.id, action=1, result=result)
    mess = f"Приветствую, {USER.fio}!"
    return await message.answer(mess, disable_notification=True, parse_mode="html")
