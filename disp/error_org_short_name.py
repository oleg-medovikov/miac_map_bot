from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import null, and_

from .dispetcher import dp
from models import UserLog, Meddoc, Org
from func import check_user


@dp.message(Command("error_org_short_name"))
async def error_org_short_name(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=18)

    DOCS = await Meddoc.load(org=Org).query.where(Org.short_name == null()).gino.all()

    errors = 0
    for doc in DOCS:
        new_org = await Org.query.where(
            and_(
                Org.case_level1_key == doc.org.case_level1_key, Org.short_name != null()
            )
        ).gino.first()
        if new_org is None:
            errors += 1
            continue
        await doc.update(org_id=new_org.id).apply()

    mess = f"Закончил исправлять организации, ошибок {errors}"
    return await message.answer(
        mess, disable_notification=True, parse_mode="MarkdownV2"
    )
