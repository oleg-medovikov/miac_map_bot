from base64 import b64decode
from bs4 import BeautifulSoup

from metod import get_request
from func.analis_cda import analis_cda


async def meddoc_message(doc, case):
    "рисуем сообщение с информацией"

    mess = f"""
Идетификатор документа: {doc.meddoc_biz_key}
Организация: {doc.org.short_name}
История болезни: {doc.history_number} отправлено {doc.creation_date}
"""
    if case is not None:
        mess += f""" 
```
Экстренное извещение:
    от: {case.doctor.fio}
    {case.doctor.spec}

    global пациента: {doc.patient.global_id}
    пол:                    {'мужской' if doc.patient.sex else 'женский'}
    дата рождения:          {doc.patient.birthdate}
    диагноз: {case.diagnoz.diagnoz}
    МКБ:                    {case.diagnoz.mkb}
    дата заболевания:       {case.date_sickness}
    дата первого обращения: {case.date_first_req}
    время СЭС:              {case.time_SES}
    дата диагноза:          {case.date_diagnoz}
```
"""
    else:
        JSON = await get_request(doc)
        DICT = {}
        try:
            JSON["entry"][0]["resource"]["content"]
        except KeyError:
            mess += "нет файлов"
            mess.replace("_", "\_")
            return mess

        # разбираем прикрепленные файлы и ищем cda
        for file in JSON["entry"][0]["resource"]["content"]:
            if file["attachment"]["contentType"] != "text/xml":
                continue

            data = file["attachment"]["data"]

            soup = BeautifulSoup(b64decode(data), "xml")
            try:
                DICT = analis_cda(soup)
            except Exception:
                continue
            else:
                if len(DICT):
                    break
        # запишем в сообщение
        mess += "\n что удалось извлечь из СЭМДа:"
        TEXT = str(DICT).replace("_", " ").replace(", '", ", \n'")
        mess += f"``` {TEXT} ```"

    mess = mess.replace("_", "\_")
    return mess
