from sqlalchemy import and_
from typing import Optional

from models import Case, Doctor, Adress, Work, Diagnoz


async def get_case(
    DICT: dict,
    doctor: "Doctor",
    adress: "Adress",
    work: Optional["Work"],
    diagnoz: "Diagnoz",
) -> "Case":
    "сравнить с существующими и создать уникальный"

    TEST = {
        "d_id": doctor.id,
        "a_id": adress.id,
        "w_id": None if work is None else work.id,
        "di_id": diagnoz.id,
        "date_sickness": DICT.get("date_sickness"),
        "date_first_req": DICT.get("date_first_req"),
        "time_SES": DICT.get("time_SES"),
        "date_diagnoz": DICT.get("date_diagnoz"),
        "hospitalization": DICT.get("hospitalization_type", 1),
        "measures": DICT.get("primary_anti_epidemic_measures"),
        "lab_confirm": DICT.get("lab_confirm"),
    }
    case = await Case.query.where(
        and_(*[getattr(Case, key) == value for key, value in TEST.items()])
    ).gino.first()
    if case is None:
        case = await Case.create(**TEST)

    return case
