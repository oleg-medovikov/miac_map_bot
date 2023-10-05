from aiogram.types import Message
from aiogram.filters import Command

from .dispetcher import dp
from models import UserLog
from func import check_user


MESS = """*Доступные команды для редактирования базы*
    *Файлы таблиц*
    /file_users
    /file_category

    *Выгрузка данных из нетрики*
    скопом выгрузить номера мед документов на 365 дней назад
    /get_cases_year
    проставить позраст, если есть пустые
    /put_down_the_age
    
    *посмотреть пример случая*
    /get_one_case

    *начать выгрузку и обработку документов*
    /download_all_semd

    *сортировать по категориям*
    /sort_category

    """.replace(
    "_", "\\_"
)


@dp.message(Command("admin_panel"))
async def admin_panel(message: Message):
    check, user = await check_user(message, "admin")
    if not check:
        return
    await UserLog.create(u_id=user.id, a_id=10)
    return await message.answer(MESS, disable_notification=True, parse_mode="Markdown")
