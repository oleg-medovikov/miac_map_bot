from typing import Optional
from sqlalchemy import and_

from models import Work
from .get_adress import get_adress


async def get_work(DICT: dict) -> Optional["Work"]:
    if DICT.get("work_adress") is None:
        return None

    # сначала нужно получить a_id
    DICT_ = {
        "adress_reg": DICT["work_adress"],
        "adress_reg_fias": DICT.get("work_adress_fias"),
    }
    work_adr = await get_adress(DICT_)
    # ищем работу с таким же адресом и названием
    work = await Work.query.where(
        and_(Work.a_id == work_adr.id, Work.name == DICT.get("work_name"))
    ).gino.first()
    if work is None:
        work = await Work.create(name=DICT["work_name"], a_id=work_adr.id)

    return work
