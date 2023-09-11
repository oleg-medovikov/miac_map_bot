from aiogram.types import BotCommand

dict_ = {"start": "Приветсвие", "admin_panel": "Панель управления ботом"}


async def set_default_commands(bot):
    commands = []

    for key, value in dict_.items():
        commands.append(BotCommand(command=key, description=value))

    await bot.set_my_commands(commands)
