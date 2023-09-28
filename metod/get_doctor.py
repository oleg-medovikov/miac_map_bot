from sqlalchemy import and_

from models import Doctor


async def get_doctor(DICT: dict) -> "Doctor":
    "сравнить с существующими и создать уникальный"

    TEST = {
        "org": DICT.get("org"),
        "fio": DICT.get("doc_fio"),
        "telefon": DICT.get("doc_telefon"),
        "spec": DICT.get("doc_spec"),
        "snils": DICT.get("doc_snils"),
    }
    doctor = await Doctor.query.where(
        and_(*[getattr(Doctor, key) == value for key, value in TEST.items()])
    ).gino.first()
    if doctor is None:
        doctor = await Doctor.create(**TEST)

    return doctor
