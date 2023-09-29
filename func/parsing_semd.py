from base64 import b64decode
from bs4 import BeautifulSoup

from models import Meddoc, Case
from exept import CDAisEmpty, NoCDAfiles
from metod import (
    get_case,
    get_case_content,
    get_doctor,
    get_adress,
    get_work,
    get_diagnoz,
    get_request,
)

from .analis_cda import analis_cda


async def parsing_semd(doc: "Meddoc") -> "Case":
    "скачиваем и записваем в базу результат анализа"

    JSON = await get_request(doc)
    DICT = {}
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

    if len(DICT) == 0:
        raise NoCDAfiles("не удалось проанализировать файлы")
    if len(DICT) < 8:
        raise CDAisEmpty("Пустой файл")

    # === анализируем, что удалось вытащить из файла
    cont = await get_case_content(DICT)
    # добавляем в док анализ контента
    await doc.update(cc_id=cont.id).apply()
    # ==== сначала пробуем получить доктора =====
    doctor = await get_doctor(DICT)
    # ==== теперь получаем адрес регистрации ====
    adress = await get_adress(DICT)
    # ==== получаем сведения о работе ====
    work = await get_work(DICT)
    # ==== получаем диагноз =====
    diagnoz = await get_diagnoz(DICT)
    # === наконец-то пробуем создать сам случай извещения ===
    case = await get_case(DICT, doctor, adress, work, diagnoz)
    return case
