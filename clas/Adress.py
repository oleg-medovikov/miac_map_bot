from pydantic import BaseModel

from base import database, t_adress


class Adress(BaseModel):
    line: str
    point: list
    text: str
    street: str
    house: str
    flat: str
    index: int
    error: bool

    @staticmethod
    async def get(LINE: str) -> "Adress":
        query = t_adress.select(t_adress.c.line == LINE)
        res = await database.fetch_one(query)
        if res is None:
            raise ValueError("Нет такого адреса")
        return Adress(**res)

    async def add(self) -> None:
        query = t_adress.insert().values(**self.dict())
        await database.execute(query)
