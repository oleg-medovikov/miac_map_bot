from aiogram.filters import Command

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)


from .dispetcher import dp
from models import UserLog
from func import check_user


@dp.message(Command("return_map_events"))
async def return_map_events(message: Message):
    check, user = await check_user(message, "user")
    if not check:
        return

    await UserLog.create(u_id=user.id, a_id=40)

    await message.answer(
        "Карта по категории Пневмония, нажмите, чтобы открыть",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Открыть карту",
                        web_app=WebAppInfo(url="https://medovikov.fun:8000/map_events"),
                    )
                ]
            ]
        ),
    )
