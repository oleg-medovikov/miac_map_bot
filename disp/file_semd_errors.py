from logging import error
from aiogram.types import Message
from aiogram.filters import Command
from pandas import DataFrame
from aiogram.types.input_file import BufferedInputFile
from sqlalchemy.util import KeyedTuple

from .dispetcher import dp
from base import db
from models import UserLog, Meddoc, Org, MeddocError, Error
from func import check_user, write_excel_any_sheets


@dp.message(Command("file_semd_errors"))
async def file_semd_errors(message: Message):
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
                Error.name,
            ]
        )
        .select_from(MeddocError.join(Meddoc.outerjoin(Org)).outerjoin(Error))
        # .where(Meddoc.history_number != "")
        .order_by(Org.short_name)
        .gino.all()
    )

    COLUMNS = [
        "Организация",
        "дата отправки",
        "meddoc_biz_key",
        "номер истории",
        "ошибка",
    ]

    df = DataFrame(data=DATA, columns=COLUMNS)

    # === Делаем сводный отчет ===
    sv = df.pivot_table(
        index=["Организация"],
        columns=["ошибка"],
        values=["meddoc_biz_key"],
        aggfunc="count",
    ).stack(0)
    sv = sv.reset_index()
    try:
        del sv["level_1"]
    except KeyError:
        pass

    DICT = {
        "свод": sv,
        "список": df,
    }

    FILEPATH = "/tmp/Ошибки отправки СЕМД.xlsx"
    FILENAME = "Ошибки отправки СЕМД.xlsx"

    write_excel_any_sheets(FILEPATH, DICT)

    file = BufferedInputFile(open(FILEPATH, "rb").read(), FILENAME)
    return await message.answer_document(file)
