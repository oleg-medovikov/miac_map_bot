from func import set_default_commands
from base import database


async def on_startup(dp, bot):
    # запустим подключение к базе
    await database.connect()
    # это команды меню в телеграм боте
    await set_default_commands(bot)
    # Начинаем работу бота
    await dp.start_polling(bot)
