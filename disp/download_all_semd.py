from aiogram.types import Message
from aiogram.filters import Command
from aiogram import md
from sqlalchemy import null


from .dispetcher import dp
from models import UserLog, Meddoc
from func import check_user, start_download_semd


@dp.message(Command("download_all_semd"))
async def download_all_semd(message: Message):
    check, user = await check_user(message, "admin")
    if not check:
        return

    DOCS = await Meddoc.query.where(Meddoc.c_id == null()).gino.all()

    MESS = f"Всего не загруженных семдов на данный момент: {len(DOCS)}"

    await UserLog.create(u_id=user.id, a_id=13)
    await message.answer(
        md.quote(MESS), disable_notification=True, parse_mode="MarkdownV2"
    )
    await start_download_semd(DOCS)
