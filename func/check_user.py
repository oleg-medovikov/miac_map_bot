from aiogram.types import Message

from models import User, UserLog
from func import get_chat_fio, delete_message


async def check_user(message: Message, role: str) -> tuple[bool, "User"]:
    "проверка пользователя на соответсвие роли"

    USER = await User.query.where(User.chat_id == message.chat.id).gino.first()
    result = get_chat_fio(message)
    await delete_message(message)
    if USER is None:
        USER = await User.create(chat_id=message.chat.id, fio=result, role="new human")
        await UserLog.create(u_id=USER.id, a_id=2)
        mess = "Вы неизвестный пользователь!"
        await message.answer(mess)
        return False, USER

    demand = {"admin": ["admin"], "user": ["user", "admin"]}.get(role, [])

    if USER.role not in demand:
        await UserLog.create(u_id=USER.id, a_id=1)
        mess = "У вас недостаточно прав!"
        await message.answer(mess)
        return False, USER
    else:
        return True, USER
