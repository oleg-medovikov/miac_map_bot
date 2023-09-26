from aiogram.types import Message
from aiogram.filters import Command

from .dispetcher import dp
from models import UserLog
from func import check_user


MESS = """*Доступные команды для редактирования базы*

    /get_users

    *Выгрузка данных из нетрики*
    скопом выгрузить номера мед документов на 365 дней назад
    /get_cases_year
    
    *посмотреть пример случая*
    /get_one_case

    *начать выгрузку и обработку документов*
    /download_all_semd

    """.replace(
    "_", "\\_"
)


@dp.message(Command("admin_panel"))
async def admin_panel(message: Message):
    if not await check_user(message, "admin"):
        return
    await UserLog.create(u_id=message.chat.id, action=10)
    return await message.answer(MESS, disable_notification=True, parse_mode="Markdown")
