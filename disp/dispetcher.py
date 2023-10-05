import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from conf import settings

logging.basicConfig(level=logging.INFO)
logging.getLogger("schedule").propagate = False
logging.getLogger("schedule").addHandler(logging.NullHandler())
logging.getLogger("gino.engine._SAEngine").setLevel(logging.ERROR)

bot = Bot(token=settings.BOT_API)
dp = Dispatcher(storage=MemoryStorage())


async def set_default_commands(bot):
    DICT = {
        "/start": "Приветсвие",
        "/analitic_panel": "Команды для анализа базы",
        "/admin_panel": "Команды для редактирования базы",
    }
    LIST = []

    for key, value in DICT.items():
        LIST.append(BotCommand(command=key, description=value))

    await bot.set_my_commands(LIST)
