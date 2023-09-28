import requests
from base64 import b64decode
from bs4 import BeautifulSoup
from sqlalchemy import and_

from models import Meddoc, Work, Case, Adress, Diagnoz
from exept import NetricaError, NoCDAfiles, NoFindMKB, NoFindReg
from conf import settings

from .geocoder import geocoder
from .analis_cda import analis_cda
from .get_case_content import get_case_content
from .get_doctor import get_doctor
from .get_case import get_case


async def parsing_semd(doc: "Meddoc") -> "Case":
    "скачиваем и записваем в базу результат анализа"
    URL = (
        settings.REGIZ_URL_2
        + str(doc.meddoc_biz_key)
        + "?mimeTypeOriginal=true&_format=json&IsIgnoreFHIRcode=true"
    )
    HEADER = dict(Authorization=settings.REGIZ_AUTH)

    req = requests.get(URL, headers=HEADER)
    if req.status_code != 200:
        raise NetricaError("проблема с подключением\n" + URL)

    try:
        req.json()["entry"][0]["resource"]["content"]
    except KeyError:
        raise NoCDAfiles("Нет прикрепленных файлов!")

    DICT = {}
    # разбираем прикрепленные файлы и ищем cda
    for file in req.json()["entry"][0]["resource"]["content"]:
        if file["attachment"]["contentType"] != "text/xml":
            continue

        data = file["attachment"]["data"]

        soup = BeautifulSoup(b64decode(data), "xml")
        try:
            DICT = analis_cda(soup)
        except Exception as e:
            print(str(e))
            continue

    if DICT == {}:
        raise NoCDAfiles("не удалось проанализировать файлы")
    # === анализируем, что удалось вытащить из файла
    cont = await get_case_content(DICT)
    # добавляем в док анализ контента
    await doc.update(cc_id=cont.id).apply()
    # ==== сначала пробуем получить доктора =====
    doctor = await get_doctor(DICT)
    # ==== теперь получаем адрес регистрации ====
    if DICT.get("adress_reg") in (None, ""):
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
    # ==== получаем сведения о работе ====
    if DICT.get("work_adress") not in (None, ""):
        # сначала нужно получить a_id
        work_adr = await Adress.query.where(
            Adress.line == DICT["work_adress"]
        ).gino.first()
        if work_adr is None:
            WORK_ADR = await geocoder(DICT["work_adress"])
            work_adr = await Adress.create(
                line=DICT["work_adress"],
                fias=DICT.get("work_adress_fias"),
                point=WORK_ADR["point"],
                text=WORK_ADR["text"],
                street=WORK_ADR["street"],
                house=WORK_ADR["house"],
            )
        # ищем работу с таким же адресом и названием
        work = await Work.query.where(
            and_(Work.a_id == work_adr.a_id, Work.name == DICT.get("work_name"))
        ).gino.first()
        if work is None:
            work = await Work.create(name=DICT["work_name"], a_id=work_adr.a_id)
    else:
        work = None
    # ==== получаем диагноз =====
    if DICT.get("MKB") in (None, ""):
        raise NoFindMKB("Нет диагноза!")
    diagnoz = await Diagnoz.query.where(
        and_(
            Diagnoz.MKB == DICT.get("MKB"),
            Diagnoz.diagnoz == DICT.get("diagnoz"),
        )
    ).gino.first()

    if diagnoz is None:
        diagnoz = await Diagnoz.create(MKB=DICT.get("MKB"), diagnoz=DICT.get("diagnoz"))

    # === наконец-то пробуем создать сам случай извещения ===
    case = await get_case(DICT, doctor, adress, work, diagnoz)
    return case
