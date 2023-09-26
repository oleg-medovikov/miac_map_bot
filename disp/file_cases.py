from aiogram.types import Message
from aiogram.filters import Command
from pandas import DataFrame
from aiogram.types.input_file import BufferedInputFile

from .dispetcher import dp
from models import UserLog, Case, Adress
from func import check_user


@dp.message(Command("file_cases"))
async def file_cases(message: Message):
    if not await check_user(message, "user"):
        return

    await UserLog.create(u_id=message.chat.id, action=10)

    # === Джойним вещи и вытаскиваем ===
    results = await Case.join(Adress).select().gino.all()

    df = DataFrame([_.to_dict() for _ in results])

    FILEPATH = "/tmp/Экстренные извещения.xlsx"
    FILENAME = "Экстренные извещения.xlsx"
    # SHETNAME = "def"
    # write_styling_excel(FILENAME, df, SHETNAME)
    df.to_excel(FILEPATH, index=False)

    file = BufferedInputFile(open(FILEPATH, "rb").read(), FILENAME)
    return await message.answer_document(file)
