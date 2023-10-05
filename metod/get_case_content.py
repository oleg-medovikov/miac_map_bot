from sqlalchemy import and_
from datetime import date

from models import CaseContent


async def get_case_content(DICT: dict) -> "CaseContent":
    "сравнить с существующими и создать уникальный"
    KEYS = DICT.keys()

    TEST = {
        "doc_fio": "doc_fio" in KEYS,
        "doc_telefon": "doc_telefon" in KEYS,
        "doc_spec": "doc_spec" in KEYS,
        "doc_snils": "doc_snils" in KEYS,
        "adress_reg": "adress_reg" in KEYS,
        "adress_reg_fias": "adress_reg_fias" in KEYS,
        "date_sickness": isinstance(DICT.get("date_sickness"), date),
        "date_first_req": isinstance(DICT.get("date_first_req"), date),
        "hospitalization": "hospitalization_type" in KEYS,
        "measures": "primary_anti_epidemic_measures" in KEYS,
        "time_SES": isinstance(DICT.get("time_SES"), date),
        "work_adress": "work_adress" in KEYS,
        "work_adress_fias": "work_adress_fias" in KEYS,
        "work_name": "work_name" in KEYS,
        "work_last_date": isinstance(DICT.get("work_last_date"), date),
        "date_diagnoz": isinstance(DICT.get("date_diagnoz"), date),
        "diagnoz": "diagnoz" in KEYS,
        "MKB": "MKB" in KEYS,
        "lab_confirm": "lab_confirm" in KEYS,
    }
    content = await CaseContent.query.where(
        and_(*[getattr(CaseContent, key) == value for key, value in TEST.items()])
    ).gino.first()
    if content is None:
        content = await CaseContent.create(**TEST)

    return content
