import requests
from base64 import b64decode
from bs4 import BeautifulSoup
from sqlalchemy import and_, true, false
from datetime import date

from models import Meddoc, Doctor, Work, Case, Adress, Diagnoz, CaseContent
from conf import settings
from .geocoder import geocoder
from .analis_cda import analis_cda
from exept import NetricaError, NoCDAfiles, NoFindMKB, NoFindReg


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
    KEYS = DICT.keys()
    cont = await CaseContent.query.where(
        and_(
            CaseContent.doc_fio == true() if "doc_fio" in KEYS else false(),
            CaseContent.doc_telefon == true() if "doc_telefon" in KEYS else false(),
            CaseContent.doc_spec == true() if "doc_spec" in KEYS else false(),
            CaseContent.doc_snils == true() if "doc_snils" in KEYS else false(),
            CaseContent.adress_reg == true() if "adress_reg" in KEYS else false(),
            CaseContent.adress_reg_fias == true()
            if "adress_reg_fias" in KEYS
            else false(),
            CaseContent.date_sickness == true()
            if isinstance(DICT.get("date_sickness"), date)
            else false(),
            CaseContent.date_first_req == true()
            if isinstance(DICT.get("date_first_req"), date)
            else false(),
            CaseContent.primary_anti_epidemic_measures == true()
            if DICT.get("primary_anti_epidemic_measures") is not None
            else false(),
            CaseContent.time_SES == true()
            if isinstance(DICT.get("time_SES"), date)
            else false(),
            CaseContent.work_adress == true()
            if DICT.get("work_adress") is not None
            else false(),
            CaseContent.work_adress_fias == true()
            if DICT.get("work_adress_fias") is not None
            else false(),
            CaseContent.work_name == true()
            if DICT.get("work_name") is not None
            else false(),
            CaseContent.work_last_date == true()
            if isinstance(DICT.get("work_last_date"), date)
            else false(),
            CaseContent.date_diagnoz == true()
            if isinstance(DICT.get("date_diagnoz"), date)
            else false(),
            CaseContent.diagnoz == true()
            if DICT.get("diagnoz") is not None
            else false(),
            CaseContent.MKB == true() if DICT.get("MKB") is not None else false(),
            CaseContent.lab_confirm == true()
            if DICT.get("lab_confirm") is not None
            else false(),
        )
    ).gino.first()
    if cont is None:
        cont = await CaseContent.create(
            doc_fio=DICT.get("doc_fio") is not None,
            doc_telefon=DICT.get("doc_telefon") is not None,
            doc_spec=DICT.get("doc_spec") is not None,
            doc_snils=DICT.get("doc_snils") is not None,
            adress_reg=DICT.get("adress_reg") is not None,
            adress_reg_fias=DICT.get("adress_reg_fias") is not None,
            date_sickness=isinstance(DICT.get("date_sickness"), date),
            date_first_req=isinstance(DICT.get("date_first_req"), date),
            hospitalization_type=DICT.get("hospitalization_type") is not None,
            primary_anti_epidemic_measures=DICT.get("primary_anti_epidemic_measures")
            is not None,
            time_SES=isinstance(DICT.get("time_SES"), date),
            work_adress=DICT.get("work_adress") is not None,
            work_adress_fias=DICT.get("work_adress_fias") is not None,
            work_name=DICT.get("work_name") is not None,
            work_last_date=isinstance(DICT.get("work_last_date"), date),
            date_diagnoz=isinstance(DICT.get("date_diagnoz"), date),
            diagnoz=DICT.get("diagnoz") is not None,
            MKB=DICT.get("MKB") is not None,
            lab_confirm=DICT.get("lab_confirm") is not None,
        )
    # добавляем в док анализ контента

    await doc.update(cc_id=cont.id).apply()

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
        raise NoFindReg("не найден адрес регистрации!")
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
    if DICT.get("MKB") in (None, ""):
        raise NoFindMKB("Нет диагноза!")
    diag = await Diagnoz.query.where(
        and_(
            Diagnoz.MKB == DICT.get("MKB"),
            Diagnoz.diagnoz == DICT.get("diagnoz"),
        )
    ).gino.first()

    if diag is None:
        diag = await Diagnoz.create(MKB=DICT.get("MKB"), diagnoz=DICT.get("diagnoz"))

    # === наконец-то пробуем создать сам случай извещения ===
    case = await Case.create(
        d_id=doctor.id,
        a_id=adr.id,
        w_id=None if work is None else work.id,
        di_id=diag.id,
        date_sicness=DICT.get("date_sickness")
        if isinstance(DICT.get("date_sickness"), date)
        else None,
        date_first_req=DICT["date_first_req"]
        if isinstance(DICT.get("date_first_req"), date)
        else None,
        time_SES=None
        if isinstance(DICT.get("time_SES"), str)
        else DICT.get("time_SES"),
        date_diagnoz=DICT["date_diagnoz"]
        if isinstance(DICT["date_diagnoz"], date)
        else None,
        hospitalization=int(DICT.get("hospitalization_type", 1))
        if DICT.get("hospitalization_type", "").isdigit()
        else None,
        anti_epidemic_measures=DICT.get("primary_anti_epidemic_measures"),
        lab_confirm=DICT.get("lab_confirm") is True,
    )
    return case
