import requests
from datetime import datetime, date, timedelta


from conf import settings
from metod import get_org, get_patient, parsing_date
from models import Meddoc


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
        meddoc = await Meddoc.query.where(
            Meddoc.meddoc_biz_key == int(_.get("meddoc_biz_key"))
        ).gino.first()
        if meddoc is not None:
            # уже существует такой бизкей
            DICT["bad"] += 1
            continue

        # первым делом нужно получить id организации
        org = await get_org(_)
        # теперь формируем пациента
        patient = await get_patient(_)
        # теперь пробуем создать меддок

        creation_date = parsing_date(_.get("md_date"))

        await Meddoc.create(
            meddoc_biz_key=int(_.get("meddoc_biz_key")),
            org_id=org.id,
            p_id=patient.id,
            history_number=_.get("case_history_number"),
            creation_date=creation_date,
            success_date=parsing_date(_.get("success_date")),
            doc_type_code=int(_.get("meddoc_meddocumenttype_code")),
            age=(
                (
                    datetime.combine(creation_date, datetime.min.time())
                    - datetime.combine(patient.birthdate, datetime.min.time())
                )
                // timedelta(days=365.2425)
            ),
        )
        DICT["good"] += 1

    return f"""Всего обработано номеров: {DICT['all']}
    из них новых: {DICT['good']}
    из них уже были в базе: {DICT['bad']}
    """
