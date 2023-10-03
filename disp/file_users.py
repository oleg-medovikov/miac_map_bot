from aiogram.types import Message
from aiogram.filters import Command
from pandas import DataFrame
from aiogram.types.input_file import BufferedInputFile

from .dispetcher import dp
from models import UserLog, User
from func import check_user, write_styling_excel


@dp.message(Command("file_users"))
async def file_users(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=14)
    users = await User.query.gino.all()

    df = DataFrame(data=[_.to_dict() for _ in users])
    df = df[["id", "fio", "role", "chat_id", "date_update"]]

    FILEPATH = "/tmp/Пользователи.xlsx"
    FILENAME = FILEPATH.rsplit("/", 1)[-1]
    SHETNAME = "def"
    write_styling_excel(FILEPATH, df, SHETNAME)

    file = BufferedInputFile(open(FILEPATH, "rb").read(), FILENAME)
    return await message.answer_document(file)
