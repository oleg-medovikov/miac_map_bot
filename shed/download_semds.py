from sqlalchemy import null, and_
from aiogram import md

from models import Meddoc, MeddocError
from conf import settings
from disp import bot
from func import start_download_semd


async def download_semds_automatic():
    DOCS = (
        await Meddoc.outerjoin(MeddocError)
        .select()
        .where(and_(Meddoc.c_id == null(), MeddocError.m_id == null()))
        .gino.load(Meddoc)
        .all()
    )

    MESS = f"Всего не загруженных семдов на данный момент: {len(DOCS)}"

    await bot.send_message(
        settings.MASTER,
        md.quote(MESS),
        disable_notification=True,
        parse_mode="MarkdownV2",
    )
    await start_download_semd(DOCS)
