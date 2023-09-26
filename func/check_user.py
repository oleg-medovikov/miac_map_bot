from aiogram.types import Message

from models import User, UserLog
from func import get_chat_fio, delete_message


async def check_user(message: Message, role: str) -> bool:
    "проверка пользователя на соответсвие роли"

    USER = await User.query.where(User.u_id == message.chat.id).gino.first()
    result = get_chat_fio(message)
    await delete_message(message)
    if USER is None:
        await User.create(chat_id=message.chat.id, fio=result, role="new human")
        await UserLog.create(u_id=message.chat.id, a_id=2)
        mess = "Вы неизвестный пользователь!"
        await message.answer(mess)
        return False

    demand = {"admin": ["admin"], "user": ["user", "admin"]}.get(role, [])

    if USER.role not in demand:
        await UserLog.create(u_id=message.chat.id, a_id=1)
        mess = "У вас недостаточно прав!"
        await message.answer(mess)
        return False
    else:
        return True
