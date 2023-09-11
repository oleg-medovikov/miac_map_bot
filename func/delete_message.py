from aiogram.exceptions import TelegramNotFound


async def delete_message(message):
    "удаление сообщения с обработкой исключения"

    try:
        await message.delete()
    except TelegramNotFound:
        pass
