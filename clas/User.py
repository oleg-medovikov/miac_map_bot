from pydantic import BaseModel
from datetime import datetime
from asyncpg.exceptions import DataError

from base import database, t_users


class User(BaseModel):
    u_id: int
    fio: str
    role: str
    date_update: datetime

    async def add(self):
        "Добавление пользователя в таблицу пользователей"

        query = t_users.select(t_users.c.u_id == self.u_id)
        res = await database.fetch_one(query)

        if res is not None:
            return "Есть такой юзер"
        else:
            query = t_users.insert().values(self.__dict__)
            await database.execute(query)

    @staticmethod
    async def get(U_ID: int) -> "User":
        "Вытаскиваем пользователя по id"
        query = t_users.select(t_users.c.u_id == int(U_ID))
        res = await database.fetch_one(query)

        if res is None:
            raise ValueError("Неизвестный U_ID!")

        return User(**res)

    @staticmethod
    async def get_all():
        query = t_users.select().order_by(t_users.c.u_id)
        list_ = []
        for row in await database.fetch_all(query):
            list_.append(User(**row).dict())

        if len(list_):
            return list_
        else:
            return [
                {
                    "u_id": 0,
                    "fio": "Vasea",
                    "role": "mo",
                    "date_update": datetime.now(),
                }
            ]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return "Нечего обновлять"
        string = ""
        for row in list_:
            query = t_users.select(t_users.c.u_id == row["u_id"])
            res = await database.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                row["date_update"] = datetime.now()
                query = t_users.insert().values(**row)
                try:
                    await database.execute(query)
                except DataError:
                    string += f"ошибка с {row['fio']}\n"
                else:
                    string += f"добавил {row['fio']}\n"
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != "date_update":
                    row["date_update"] = datetime.now()
                    query = (
                        t_users.update()
                        .where(t_users.c.u_id == row["u_id"])
                        .values(**row)
                    )
                    try:
                        await database.execute(query)
                    except DataError:
                        string += f"ошибка с {row['fio']}\n"
                    else:
                        string += f"обновил {row['fio']}\n"

                    break
        if string == "":
            string = "Нечего обновлять"
        return string
