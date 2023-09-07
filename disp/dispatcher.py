from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from conf import TELEGRAM_TOKEN

import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("schedule").propagate = False
logging.getLogger("schedule").addHandler(logging.NullHandler())

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
