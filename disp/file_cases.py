from aiogram.types import Message
from aiogram.filters import Command
from pandas import DataFrame
from aiogram.types.input_file import BufferedInputFile

from .dispetcher import dp
from base import db
from models import UserLog, Meddoc, Patient, Org, Case, Adress, Doctor, Diagnoz
from func import check_user


@dp.message(Command("file_cases"))
async def file_cases(message: Message):
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
                Patient.sex,
                Patient.birthdate,
                Patient.birthdate_baby,
                Doctor.fio,
                Doctor.spec,
                Doctor.telefon,
                Case.date_sickness,
                Case.date_first_req,
                Case.date_diagnoz,
                Case.time_SES,
                Diagnoz.MKB,
                Diagnoz.diagnoz,
                Adress.text,
                Adress.point,
            ]
        )
        .select_from(
            Meddoc.outerjoin(Patient)
            .outerjoin(Org)
            .join(Case.outerjoin(Doctor).outerjoin(Adress).outerjoin(Diagnoz))
        )
        .gino.all()
    )

    COLUMNS = [
        "Организация",
        "номер истории",
        "дата отправки",
        "Пол",
        "Дата рождения",
        "Дата рождения ребенка",
        "ФИО врача",
        "Специальность",
        "Телефон",
        "Дата заболевания",
        "Дата первого обращения",
        "Дата диагноза",
        "Дата отправки в СЕС",
        "МКБ",
        "Диагноз",
        "Адрес регистрации",
        "координаты",
    ]

    df = DataFrame(data=DATA, columns=COLUMNS)

    FILEPATH = "/tmp/Экстренные извещения.xlsx"
    FILENAME = "Экстренные извещения.xlsx"
    # SHETNAME = "def"
    # write_styling_excel(FILENAME, df, SHETNAME)
    df.to_excel(FILEPATH, index=False)

    file = BufferedInputFile(open(FILEPATH, "rb").read(), FILENAME)
    return await message.answer_document(file)
