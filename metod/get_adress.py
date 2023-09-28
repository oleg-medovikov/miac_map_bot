from models import Adress
from .geocoder import geocoder

from exept import NoFindReg


async def get_adress(DICT: dict) -> "Adress":
    "сравнить с существующими и создать уникальный"

    if DICT.get("adress_reg") is None:
        raise NoFindReg("не найден адрес регистрации!")

    adress = await Adress.query.where(Adress.line == DICT["adress_reg"]).gino.first()

    if adress is None:
        ADR = await geocoder(DICT["adress_reg"])
        adress = await Adress.create(
            line=DICT["adress_reg"],
            fias=DICT.get("adress_reg_fias"),
            point=ADR["point"],
            text=ADR["text"],
            street=ADR["street"],
            house=ADR["house"],
        )

    return adress
