from aiogram.types import Message
from aiogram.filters import Command
from aiogram import md

from .dispetcher import dp
from models import User, Log
from func import get_chat_fio, delete_message


MESS = """*Доступные команды для редактирования базы*

    /get_users

    *Выгрузка данных из нетрики*
    скопом выгрузить номера мед документов на 365 дней назад
    /get_cases_year
    * начать выгрузку и обработку документов
    /download_all_semd

    """


@dp.message(Command("admin_panel"))
async def admin_panel(message: Message):
    # === проверка на админа
    USER = await User.query.where(User.u_id == message.chat.id).gino.first()
    result = get_chat_fio(message)
    await delete_message(message)
    if USER is None or USER.role not in ("admin"):
        await Log.create(u_id=message.chat.id, action=3, result=result)
        mess = "У Вас недостаточно прав для этого действия!"
        return await message.answer(mess)
    # ===============================
    await Log.create(u_id=message.chat.id, action=10)
    return await message.answer(
        md.quote(MESS), disable_notification=True, parse_mode="MarkdownV2"
    )
