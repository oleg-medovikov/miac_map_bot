from aiogram.types import Message
from aiogram.filters import Command
from pandas import DataFrame
from aiogram.types.input_file import BufferedInputFile

from .dispetcher import dp
from base import db
from models import UserLog, Meddoc, Org, MeddocError, Error
from func import check_user, write_excel_any_sheets


@dp.message(Command("file_semd_errors"))
async def file_semd_errors(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=32)

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
    # для сводного отчета вытаскиваем все обработанные семды
    DATA = (
        await db.select(
            [
                Org.case_level1_key,
                Org.short_name,
                db.func.count(Meddoc.meddoc_biz_key),
                db.func.count(MeddocError.m_id),
                db.func.min(Meddoc.creation_date),
            ]
        )
        .select_from(Meddoc.outerjoin(Org).outerjoin(MeddocError))
        .group_by(Org.case_level1_key, Org.short_name)
        .order_by(Org.short_name)
        .gino.all()
    )
    COLUMNS = [
        "GUID" "Организация",
        "Организация",
        "всего передано",
        "ошибка при прочтении СЭМДа",
        "начиная с даты",
    ]
    count = DataFrame(data=DATA, columns=COLUMNS)

    sv = count.merge(sv, how="left", on="Организация")

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
