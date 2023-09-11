from pydantic import BaseModel
from datetime import date
from typing import Optional

from base import database, t_meddocs


class Meddoc(BaseModel):
    meddoc_biz_key: int
    creation_date: date
    success_date: date
    birthdate: date
    org_id: int
    history_number: str
    doc_type_code: int
    processed: Optional[bool]
    error: Optional[bool]

    async def add(self) -> None:
        "Добавляем новый документ, если его нет в базе"
        query = t_meddocs.select(t_meddocs.c.meddoc_biz_key == self.meddoc_biz_key)
        res = await database.fetch_one(query)
        if res is None:
            query = t_meddocs.insert().values(**self.model_dump())
            await database.execute(query)
