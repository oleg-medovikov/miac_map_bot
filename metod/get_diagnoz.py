from sqlalchemy import and_

from models import Diagnoz
from exept import NoFindMKB


async def get_diagnoz(DICT: dict) -> "Diagnoz":
    if DICT.get("MKB") in (None, ""):
        raise NoFindMKB("Нет диагноза!")

    diagnoz = await Diagnoz.query.where(
        and_(
            Diagnoz.MKB == DICT.get("MKB"),
            Diagnoz.diagnoz == DICT.get("diagnoz"),
        )
    ).gino.first()

    if diagnoz is None:
        diagnoz = await Diagnoz.create(MKB=DICT.get("MKB"), diagnoz=DICT.get("diagnoz"))

    return diagnoz
