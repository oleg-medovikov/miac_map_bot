from .dispatcher import dp
from aiogram import types
from aiogram.filters import Command

from clas import User, Log
from func import delete_message


@dp.message(Command("get_cases_year"))
async def admin_panel(message: types.Message):
    await delete_message(message)

    try:
        await User.admin(message.chat.id)
    except ValueError:
        await Log.add(message.chat.id, 1)
        return await message.answer("вы не являетесь админом", parse_mode="html")

    return await message.answer(MESS, parse_mode="Markdown")
