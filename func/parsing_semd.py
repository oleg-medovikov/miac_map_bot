import requests
from base64 import b64decode
from bs4 import BeautifulSoup
from sqlalchemy import and_

from models import Meddoc, Doctor, Work, Case, Adress, Diagnoz, CaseContent
from conf import settings
from .geocoder import geocoder
from .analis_cda import analis_cda


class error(Exception):
    pass


async def parsing_semd(doc: Meddoc):
    "скачиваем и записваем в базу результат анализа"
    URL = (
        settings.REGIZ_URL_2
        + str(doc.meddoc_biz_key)
        + "?mimeTypeOriginal=true&_format=json&IsIgnoreFHIRcode=true"
    )
    HEADER = dict(Authorization=settings.REGIZ_AUTH)

    req = requests.get(URL, headers=HEADER)
    if req.status_code != 200:
        raise error("проблема с подключением\n" + URL)

    try:
        req.json()["entry"][0]["resource"]["content"]
    except KeyError:
        raise error("Нет прикрепленных файлов!")

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
        raise error("не удалось проанализировать файлы")
    # === анализируем, что удалось вытащить из файла
    content = await CaseContent.query.where(
        CaseContent.meddoc_biz_key == doc.meddoc_biz_key
    ).gino.first()
    if content is not None:
        await content.delete()
    await CaseContent.create(
        meddoc_biz_key=doc.meddoc_biz_key,
        org_id=doc.org_id,
        doc_fio=DICT.get("doc_fio") not in (None, ""),
        doc_telefon=DICT.get("doc_telefon") not in (None, ""),
        doc_spec=DICT.get("doc_spec") not in (None, ""),
        doc_snils=DICT.get("doc_snils") not in (None, ""),
        adress_reg=DICT.get("adress_reg") not in (None, ""),
        adress_reg_fias=DICT.get("adress_reg_fias") not in (None, ""),
        date_sickness=DICT.get("date_sickness") not in (None, ""),
        date_first_req=DICT.get("date_first_req") not in (None, ""),
        hospitalization_type=DICT.get("hospitalization_type") not in (None, ""),
        primary_anti_epidemic_measures=DICT.get("primary_anti_epidemic_measures")
        not in (None, ""),
        time_SES=not isinstance(DICT.get("time_SES"), str)
        and DICT.get("time_SES") is not None,
        work_adress=DICT.get("work_adress") not in (None, ""),
        work_adress_fias=DICT.get("work_adress_fias") not in (None, ""),
        work_name=DICT.get("work_name") not in (None, ""),
        work_last_date=DICT.get("work_last_date") not in (None, ""),
        date_diagnoz=DICT.get("") not in (None, ""),
        diagnoz=DICT.get("") not in (None, ""),
        MKB=DICT.get("") not in (None, ""),
        lab_confirm=DICT.get("") not in (None, ""),
    )

    # ==== сначала пробуем получить доктора =====
    doctor = await Doctor.query.where(
        and_(
            Doctor.org == DICT.get("org"),
            Doctor.fio == DICT.get("doc_fio"),
            Doctor.telefon == DICT.get("doc_telefon"),
            Doctor.spec == DICT.get("doc_spec"),
        )
    ).gino.first()

    if doctor is None:
        doctor = await Doctor.create(
            org=DICT.get("org"),
            fio=DICT.get("doc_fio"),
            telefon=DICT.get("doc_telefon"),
            spec=DICT.get("doc_spec"),
        )
    # ==== теперь получаем адрес регистрации ====
    if DICT.get("adress_reg") in (None, ""):
        raise error("не найден адрес регистрации!")
    adr = await Adress.query.where(Adress.line == DICT["adress_reg"]).gino.first()
    if adr is None:
        ADR = await geocoder(DICT["adress_reg"])
        adr = await Adress.create(
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
    diag = (
        await Diagnoz.query.where(Diagnoz.MKB == DICT["MKB"])
        .where(Diagnoz.diagnoz == DICT["diagnoz"])
        .gino.first()
    )
    if diag is None:
        diag = await Diagnoz.create(MKB=DICT["MKB"], diagnoz=DICT["diagnoz"])

    # === наконец-то пробуем сосздать сам случай извещения ===
    case = await Case.query.where(
        Case.meddoc_biz_key == doc.meddoc_biz_key
    ).gino.first()
    if case is not None:
        await case.delete()

    await Case.create(
        meddoc_biz_key=doc.meddoc_biz_key,
        d_id=doctor.d_id,
        a_id=adr.a_id,
        date_sicness=DICT["date_sickness"],
        date_first_req=DICT["date_first_req"],
        hospitalization_type=int(DICT["hospitalization_type"])
        if DICT["hospitalization_type"] is not None
        else None,
        primary_anti_epidemic_measures=DICT["primary_anti_epidemic_measures"],
        time_SES=None
        if isinstance(DICT.get("time_SES"), str)
        else DICT.get("time_SES"),
        w_id=work.w_id if work is not None else None,
        date_diagnoz=DICT["date_diagnoz"],
        di_id=diag.di_id,
        lab_confirm=DICT.get("lab_confirm") is True,
    )
