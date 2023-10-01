from sqlalchemy import and_
from re import search

from models import Diagnoz
from exept import NoFindMKB


async def get_diagnoz(DICT: dict) -> "Diagnoz":
    if DICT.get("MKB") in (None, ""):
        if DICT.get("diagnoz") is not None:
            print("пробую вытащить МКБ из строки")
            try:
                DICT["MKB"] = search(r"\w\d{2}.\d+", DICT["diagnoz"]).group(0)
            except AttributeError:
                raise NoFindMKB("Нет диагноза!")
            else:
                print("Получилось!")
        else:
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
