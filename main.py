"""
Этот бот написан для выгрузки 
экстренных извещений инфекционных заболеваний.
Передача формы №058/у СЭМДами от МО
для последущей обработки и создания тепловых карт
Автор: Медовиков Олег
2023
"""
import asyncio

from base import db
from disp import dp, bot, set_default_commands
from conf import settings
from shed import create_scheduler


async def on_startup():
    scheduler = create_scheduler()
    scheduler.start()
    await db.set_bind(settings.DATABASE_URL)
    await db.gino.create_all()
    await set_default_commands(bot)
    await dp.start_polling(bot)


async def on_shutdown():
    await db.pop_bind().close()


if __name__ == "__main__":
    try:
        asyncio.run(on_startup())
    except KeyboardInterrupt:
        asyncio.run(on_shutdown())
