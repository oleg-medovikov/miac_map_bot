from aiogram.exceptions import TelegramNotFound
from aiogram.types import Message


async def delete_message(message: Message):
    "удаление сообщения с обработкой исключения"

    try:
        await message.delete()
    except TelegramNotFound:
        pass
