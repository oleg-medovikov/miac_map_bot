from aiogram.types import Message
from aiogram.filters import Command
from pandas import DataFrame
from aiogram.types.input_file import BufferedInputFile
from sqlalchemy import null

from .dispetcher import dp
from base import db
from models import UserLog, Meddoc, Org
from func import check_user


@dp.message(Command("null_history_number"))
async def null_history_number(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=31)

    # === Джойним вещи и вытаскиваем ===

    DATA = (
        await db.select(
            [
                Org.short_name,
                Meddoc.history_number,
                Meddoc.creation_date,
                Meddoc.meddoc_biz_key,
            ]
        )
        .select_from(Meddoc.outerjoin(Org))
        .where(Meddoc.history_number == "")
        .gino.all()
    )

    COLUMNS = [
        "Организация",
        "номер истории",
        "дата отправки",
        "meddoc_biz_key",
    ]

    df = DataFrame(data=DATA, columns=COLUMNS)

    FILEPATH = "/tmp/Нет номера истории болезни.xlsx"
    FILENAME = "Нет номера истории болезни.xlsx"
    # SHETNAME = "def"
    # write_styling_excel(FILENAME, df, SHETNAME)
    df.to_excel(FILEPATH, index=False)

    file = BufferedInputFile(open(FILEPATH, "rb").read(), FILENAME)
    return await message.answer_document(file)
