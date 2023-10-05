from sqlalchemy import and_
from uuid import UUID

from models import Patient
from .parsing_date import parsing_date


async def get_patient(DICT: dict) -> "Patient":
    "сравнить с существующими и создать уникальный"

    TEST = {
        "global_id": UUID(DICT.get("case_organization_level1_key")),
        "sex": True if DICT.get("case_patient_gender") == "male" else False,
        "birthdate": parsing_date(DICT.get("case_patient_birthdate")),
        "birthdate_baby": parsing_date(DICT.get("birthcertificate_birthdate")),
    }
    patient = await Patient.query.where(
        and_(*[getattr(Patient, key) == value for key, value in TEST.items()])
    ).gino.first()
    if patient is None:
        patient = await Patient.create(**TEST)

    return patient
