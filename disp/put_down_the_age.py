from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import null
from datetime import timedelta

from .dispetcher import dp

from models import UserLog, Meddoc, Patient
from func import check_user


@dp.message(Command("put_down_the_age"))
async def put_down_the_age(message: Message):
    check, user = await check_user(message, "admin")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=17)

    DOCS = (
        await Meddoc.load(patient=Patient).query.where(Meddoc.age == null()).gino.all()
    )

    mess = f"Всего меддоков без возрастов: {len(DOCS)}"
    await message.answer(mess, disable_notification=True, parse_mode="html")

    for doc in DOCS:
        age = (doc.creation_date - doc.patient.birthdate) // timedelta(days=365.2425)

        await doc.update(age=age).apply()

    mess = "Все возраста проставлены!"
    return await message.answer(mess, disable_notification=True, parse_mode="html")
