from sqlalchemy import and_

from models import Doctor


async def get_doctor(DICT: dict) -> "Doctor":
    "сравнить с существующими и создать уникальный"

    TEST = {
        "doc_fio": DICT.get("doc_fio"),
        "doc_telefon": DICT.get("doc_telefon"),
        "doc_spec": DICT.get("doc_spec"),
        "doc_snils": DICT.get("doc_snils"),
    }
    doctor = await Doctor.query.where(
        and_(*[getattr(Doctor, key) == value for key, value in TEST.items()])
    ).gino.first()
    if doctor is None:
        doctor = await Doctor.create(**TEST)

    return doctor
