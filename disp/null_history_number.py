from aiogram.types import Message
from aiogram.filters import Command
from pandas import DataFrame
from aiogram.types.input_file import BufferedInputFile
from sqlalchemy import null

from .dispetcher import dp
from base import db
from models import UserLog, Meddoc, Org
from func import check_user, write_excel_any_sheets


@dp.message(Command("null_history_number"))
async def null_history_number(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=31)

    # === Джойним вещи и вытаскиваем список ===

    DATA = (
        await db.select(
            [
                Org.short_name,
                Meddoc.creation_date,
                Meddoc.meddoc_biz_key,
                Meddoc.history_number,
            ]
        )
        .select_from(Meddoc.outerjoin(Org))
        .where(Meddoc.history_number == "")
        .order_by(Org.short_name)
        .gino.all()
    )

    COLUMNS = [
        "Организация",
        "дата отправки",
        "meddoc_biz_key",
        "номер истории",
    ]

    df = DataFrame(data=DATA, columns=COLUMNS)

    # === Делаем сводный отчет ===
    DATA = (
        await db.select(
            [
                Org.short_name,
                db.func.count(Meddoc.meddoc_biz_key),
            ]
        )
        .select_from(Meddoc.outerjoin(Org))
        .where(Meddoc.history_number == "")
        .group_by(Org.short_name)
        .order_by(Org.short_name)
        .gino.all()
    )
    COLUMNS = [
        "Организация",
        "количество",
    ]

    sv = DataFrame(data=DATA, columns=COLUMNS)

    FILEPATH = "/tmp/Нет номера истории болезни.xlsx"
    FILENAME = "Нет номера истории болезни.xlsx"
    DICT = {
        "свод": sv,
        "список": df,
    }

    write_excel_any_sheets(FILEPATH, DICT)

    file = BufferedInputFile(open(FILEPATH, "rb").read(), FILENAME)
    return await message.answer_document(file)
