"""
Этот бот написан для выгрузки 
экстренных извещений об инфекционных заболеваний.
Передача формы №058/у СЭМДами от МО
для последущей обработки и создания тепловых карт
Автор: Медовиков Олег
2023
"""

import warnings
import asyncio

from disp import dp, bot, on_startup
from shed import scheduler

warnings.filterwarnings("ignore")


async def main():
    await asyncio.gather(
        on_startup(dp, bot),
        scheduler(),
    )


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            break
