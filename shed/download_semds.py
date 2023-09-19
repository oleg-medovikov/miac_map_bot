from sqlalchemy import false, and_
from aiogram import md

from models import Meddoc, Log
from conf import settings
from disp import bot
from func import start_download_semd


async def download_semds_automatic():
    DOCS = await Meddoc.query.where(
        and_(Meddoc.processed == false(), Meddoc.error == false())
    ).gino.all()

    MESS = f"Всего не загруженных семдов на данный момент: {len(DOCS)}"

    await Log.create(u_id=int(settings.MASTER), action=12, result=MESS)
    await bot.send_message(
        settings.MASTER,
        md.quote(MESS),
        disable_notification=True,
        parse_mode="MarkdownV2",
    )
    await start_download_semd(DOCS)
