from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from base import database, t_orgs
from uuid import UUID


class Org(BaseModel):
    mo_id: int
    case_level1_key: UUID
    short_name: str
    date_update: Optional[datetime]

    @staticmethod
    async def get_id(KEY: str, NAME: str) -> int:
        "получить порядковый номер организации из справочника"
        query = t_orgs.select(t_orgs.c.case_level1_key == UUID(KEY))
        res = await database.fetch_one(query)
        if res is not None:
            return res["mo_id"]

        query = t_orgs.insert().values(
            **{
                "case_level1_key": KEY,
                "short_name": NAME,
                "date_update": datetime.now(),
            }
        )
        await database.execute(query)
        query = t_orgs.select(t_orgs.c.case_level1_key == UUID(KEY))
        res = await database.fetch_one(query)
        if res is not None:
            return res["mo_id"]
        else:
            return 0
