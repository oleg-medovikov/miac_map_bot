from aiogram.types import Message
from aiogram.filters import Command
from aiogram import md
from sqlalchemy import false


from .dispetcher import dp
from models import User, Log, Meddoc
from func import get_chat_fio, delete_message


@dp.message(Command("download_all_semd"))
async def download_all_semd(message: Message):
    # === проверка на админа
    USER = await User.query.where(User.u_id == message.chat.id).gino.first()
    result = get_chat_fio(message)
    await delete_message(message)
    if USER is None or USER.role not in ("admin"):
        await Log.create(u_id=message.chat.id, action=3, result=result)
        mess = "У Вас недостаточно прав для этого действия!"
        return await message.answer(mess)
    # ===============================
    DOCS = await Meddoc.query.where(Meddoc.processed == false()).gino.all()

    MESS = f"Всего не загруженных семдов на данный момент: {len(DOCS)}"

    await Log.create(u_id=message.chat.id, action=12, result=MESS)
    return await message.answer(
        md.quote(MESS), disable_notification=True, parse_mode="MarkdownV2"
    )
