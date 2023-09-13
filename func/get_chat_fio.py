from aiogram.types import Message

LIST = ["username", "first_name", "last_name"]


def get_chat_fio(mess: Message) -> str:
    return " ".join([mess.chat.__dict__[_] for _ in LIST])
