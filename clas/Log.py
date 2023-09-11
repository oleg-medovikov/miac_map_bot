from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from base import database, t_logi


class Log(BaseModel):
    time: datetime
    u_id: int
    action: int
    result: Optional[str]

    @staticmethod
    async def add(U_ID: int, ACTION: int, RESULT=None):
        "Записываем событие"
        query = t_logi.insert().values(
            {"time": datetime.now(), "u_id": U_ID, "action": ACTION, "result": RESULT}
        )
        await database.execute(query)
