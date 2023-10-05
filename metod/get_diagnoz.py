from sqlalchemy import and_
from re import fullmatch

from models import Diagnoz
from exept import NoFindMKB, NoCorrectMKB


async def get_diagnoz(DICT: dict) -> "Diagnoz":
    if DICT.get("MKB") in (None, ""):
        raise NoFindMKB("Нет диагноза!")

    if not (
        bool(fullmatch(r"\w\d{2}\.\d+", DICT["MKB"]))
        or bool(fullmatch(r"\w\d{2}", DICT["MKB"]))
    ):
        raise NoCorrectMKB("Нет корректного диагноза!")

    diagnoz = await Diagnoz.query.where(
        and_(
            Diagnoz.mkb == DICT.get("MKB"),
            Diagnoz.diagnoz == DICT.get("diagnoz"),
        )
    ).gino.first()

    if diagnoz is None:
        diagnoz = await Diagnoz.create(
            mkb=DICT["MKB"].upper(),
            mkb3=DICT["MKB"][0:3].upper(),
            diagnoz=DICT.get("diagnoz"),
        )

    return diagnoz
