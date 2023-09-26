from aiogram.types import Message
from aiogram.filters import Command
from aiogram import md
from sqlalchemy import false, and_


from .dispetcher import dp
from models import UserLog, Meddoc
from func import check_user, start_download_semd


@dp.message(Command("download_all_semd"))
async def download_all_semd(message: Message):
    if not await check_user(message, "admin"):
        return

    DOCS = await Meddoc.query.where(
        and_(Meddoc.processed == false(), Meddoc.error == false())
    ).gino.all()

    MESS = f"Всего не загруженных семдов на данный момент: {len(DOCS)}"

    await UserLog.create(u_id=message.chat.id, action=12)
    await message.answer(
        md.quote(MESS), disable_notification=True, parse_mode="MarkdownV2"
    )
    await start_download_semd(DOCS)
