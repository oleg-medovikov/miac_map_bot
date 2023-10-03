from aiogram.types import Message
from aiogram.filters import Command
from pandas import DataFrame
from aiogram.types.input_file import BufferedInputFile

from .dispetcher import dp
from models import UserLog, Category
from func import check_user, write_styling_excel


@dp.message(Command("file_category"))
async def file_category(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=15)
    categoryes = await Category.query.gino.all()

    df = DataFrame(data=[_.to_dict() for _ in categoryes])
    df = df[["id", "name", "short", "color", "mkb", "demaind", "active"]]

    FILEPATH = "/tmp/Category.xlsx"
    FILENAME = FILEPATH.rsplit("/", 1)[-1]
    SHETNAME = "def"
    write_styling_excel(FILEPATH, df, SHETNAME)

    file = BufferedInputFile(open(FILEPATH, "rb").read(), FILENAME)
    return await message.answer_document(file)
