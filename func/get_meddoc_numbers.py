import requests
from uuid import UUID
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import and_
from datetime import date


from conf import settings
from models import Org, Meddoc, Patient
from .parse_date import parse_date


async def get_meddoc_numbers(START: date, STOP: date) -> str:
    "выгружаем номера историй болезней и номера документов"

    START_ = START.strftime("%Y-%m-%d")
    STOP_ = STOP.strftime("%Y-%m-%d")
    URL = (
        settings.REGIZ_URL
        + f"?id=1270&args={START_},{STOP_}"
        + f"&auth={settings.REGIZ_TOKEN}"
    )

    req = requests.get(URL)
    if req.status_code != 200:
        return "проблемы с подключением"

    DICT = {"all": 0, "good": 0, "bad": 0, "org": 0}
    for _ in req.json():
        DICT["all"] += 1
        # первым делом нужно получить id организации
        org = await Org.query.where(
            Org.case_level1_key == UUID(_.get("case_organization_level1_key"))
        ).gino.first()
        if org is None:
            org = await Org.create(
                case_level1_key=UUID(_.get("case_organization_level1_key")),
                short_name=_.get("case_organization_level1_short_name"),
            )
            DICT["org"] += 1
        # теперь формируем пациента
        patient = await Patient.query.where(
            and_(
                Patient.global_id == UUID(_.get("case_patient_global_key")),
                Patient.birthdate_baby == _.get("birthcertificate_birthdate"),
            )
        ).gino.first()
        if patient is None:
            patient = await Patient.create(
                global_id=UUID(_.get("case_patient_global_key")),
                sex=True if _.get("case_patient_gender") == "male" else False,
                birthdate=parse_date(_.get("case_patient_birthdate")),
                birthdate_baby=parse_date(_.get("birthcertificate_birthdate")),
            )

        # теперь пробуем создать меддок
        try:
            await Meddoc.create(
                meddoc_biz_key=int(_.get("meddoc_biz_key")),
                org_id=org.id,
                p_id=patient.id,
                history_number=_.get("case_history_number"),
                creation_date=parse_date(_.get("md_date")),
                success_date=parse_date(_.get("success_date")),
                doc_type_code=int(_.get("meddoc_meddocumenttype_code")),
            )
        except UniqueViolationError:
            # уже существует такой бизкей
            DICT["bad"] += 1
        else:
            DICT["good"] += 1

    return f"""Всего обработано номеров: {DICT['all']}
    из них новых: {DICT['good']}
    из них уже были в базе: {DICT['bad']}

    Новых организаций: {DICT['org']}
    """
