from aiogram.filters import BaseFilter
from aiogram.types import Message

from .dispetcher import dp
from models import UserLog, Meddoc, Org, Doctor, Case, Diagnoz, Patient
from func import check_user, meddoc_message


class NumbersOnlyFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return isinstance(message.text, str) and message.text.isdigit()


@dp.message(NumbersOnlyFilter())
async def processing_biz_key(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=33)

    # пробуем найти меддок с таким бизкеем
    if not isinstance(message.text, str):
        return
    doc = (
        await Meddoc.load(org=Org, patient=Patient)
        .query.where(Meddoc.meddoc_biz_key == int(message.text))
        .gino.first()
    )
    if doc is None:
        mess = "У меня нет документа с таким biz_key!"
        return await message.answer(mess, disable_notification=True, parse_mode="html")
    case = (
        await Case.load(doctor=Doctor, diagnoz=Diagnoz)
        .query.where(Case.id == doc.c_id)
        .gino.first()
    )

    mess = await meddoc_message(doc, case)
    return await message.answer(mess, disable_notification=True, parse_mode="Markdown")
