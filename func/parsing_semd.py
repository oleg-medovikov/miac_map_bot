import requests
from base64 import b64decode
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy import and_

from models import Meddoc, Doctor, Work, Case, Adress, Diagnoz
from conf import settings
from .geocoder import geocoder


class error(Exception):
    pass


def return_attr(some_dict, attr):
    if some_dict is None:
        return None

    if getattr(some_dict, attr) is not None:
        return getattr(some_dict, attr)
    if some_dict.get(attr) is None:
        return None

    _ = some_dict.get(attr)
    if len(_) == 8 and _.isdigit() and _[0:3] == "202":
        return datetime.strptime(_, "%Y%m%d").date()

    if "+" in _ and _[0:3] == "202":
        return datetime.strptime(_[0:12], "%Y%m%d%H%M")

    return _


def analis_cda(soup: BeautifulSoup) -> dict:
    "читаем и вытаскиваем данные"
    DICT = {
        "org": "",
        "doc_fio": "doc_fio",
        "doc_telefon": "",
        "doc_spec": "",
        "doc_snils": "",
        "adress_reg": "",
        "adress_reg_fias": "",
        "date_sickness": "",
        "date_first_req": "",
        "hospitalization_type": 1,
        "primary_anti_epidemic_measures": "",
        "time_SES": "",
        "work_adress": "",
        "work_adress_fias": "",
        "work_name": "",
        "work_last_date": "",
        "date_diagnoz": "",
        "diagnoz": "",
        "MKB": "",
        "lab_confirm": False,
    }

    # ===== поиск адреса регистрации ========
    for addr in soup.find_all("addr"):
        if (
            return_attr(addr.find("address:Type"), "codeSystem")
            == "1.2.643.5.1.13.13.11.1504"
            and return_attr(addr.find("address:Type"), "code") == "1"
        ):
            DICT["adress_reg"] = return_attr(addr.find("streetAddressLine"), "text")
            DICT["adress_reg_fias"] = return_attr(addr.find("fias:HOUSEGUID"), "text")

    # ==== Разбираем врача ===========
    for autor in soup.find_all("assignedAuthor"):
        DICT["org"] = return_attr(
            autor.find("representedOrganization").find("name"), "text"
        )
        family = (
            str(return_attr(autor.find("family"), "text"))
            if isinstance(return_attr(autor.find("family"), "text"), str)
            else ""
        )
        given = (
            str(return_attr(autor.find("given"), "text"))
            if isinstance(return_attr(autor.find("given"), "text"), str)
            else ""
        )
        patronymic = (
            str(return_attr(autor.find("identity:Patronymic"), "text"))
            if isinstance(return_attr(autor.find("identity:Patronymic"), "text"), str)
            else ""
        )

        DICT["doc_fio"] = " ".join([family, given, patronymic])

        DICT["doc_telefon"] = return_attr(autor.find("telecom"), "value")
        for _ in autor.find_all("code"):
            if _.get("codeSystem") == "1.2.643.5.1.13.13.11.1002":
                DICT["doc_spec"] = _.get("displayName")
        for _ in autor.find_all("id"):
            if _.get("root") == "1.2.643.100.3":
                STRING = _.get("extension")
                try:
                    DICT["doc_snils"] = int("".join(i for i in STRING if i.isdigit()))
                except TypeError:
                    DICT["doc_snils"] = 0
    # ====== Разбираем показатели
    for obs in soup.find_all("observation"):
        CODE = obs.find("code")
        codeSystem = CODE.get("codeSystem")
        code = CODE.get("code")
        # displayName = CODE.get("displayName")

        # ==== поиск адреса и места работы =======
        if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12159":
            D = {
                "work_adress": ("streetAddressLine", "text"),
                "work_adress_fias": ("fias:HOUSEGUID", "text"),
                "work_name": ("name", "text"),
                "work_last_date": ("effectiveTime", "value"),
            }
            for key, value in D.items():
                DICT[key] = return_attr(obs.find(value[0]), value[1])

        # ====== Дата заболевания ==========
        if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12144":
            DICT["date_sickness"] = return_attr(obs.find("effectiveTime"), "value")
            continue

        # ==== Дата первичного обращения (выявления) ===
        if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12145":
            DICT["date_first_req"] = return_attr(obs.find("effectiveTime"), "value")
            continue

        # Вид случая госпитализации или обращения (первичный, повторный)
        if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12146":
            codeSystem_ = obs.find("value").get("codeSystem")
            if codeSystem_ == "1.2.643.5.1.13.13.11.1007":
                DICT["hospitalization_type"] = obs.find("value").get("code")
            continue

        # Проведенные первичные противоэпидемические мероприятия
        # и дополнительные сведения
        if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12148":
            DICT["primary_anti_epidemic_measures"] = return_attr(
                obs.find("value"), "text"
            )
            continue

        # Дата и час первичной сигнализации в СЭС
        if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12149":
            DICT["time_SES"] = return_attr(obs.find("value"), "value")
            if DICT["time_SES"] is None:
                DICT["time_SES"] = return_attr(obs.find("effectiveTime"), "value")
            continue

        # Диагноз
        if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "838":
            DICT["date_diagnoz"] = return_attr(obs.find("effectiveTime"), "value")
            DICT["diagnoz"] = obs.text.strip()
            if obs.value.get("codeSystem") == "1.2.643.5.1.13.13.11.1005":
                DICT["MKB"] = obs.value.get("code")
            continue

        # Подтверждено лабораторно (да/нет)
        if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12160":
            DICT["lab_confirm"] = return_attr(obs.find("value"), "value")
            if DICT["lab_confirm"] in ["true", "True"]:
                DICT["lab_confirm"] = True
            else:
                DICT["lab_confirm"] = False
            continue

    return DICT


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

    # ==== сначала пробуем получить доктора =====
    doctor = (
        await Doctor.query.where(Doctor.org == DICT["org"])
        .where(Doctor.fio == DICT["doc_fio"])
        .where(Doctor.telefon == DICT["doc_telefon"])
        .where(Doctor.spec == DICT["doc_spec"])
        .gino.first()
    )
    if doctor is None:
        doctor = await Doctor.create(
            org=DICT["org"],
            fio=DICT["doc_fio"],
            telefon=DICT["doc_telefon"],
            spec=DICT["doc_spec"],
        )
    # ==== теперь получаем адрес регистрации ====
    if DICT["adress_reg"] in (None, ""):
        raise error("не найден адрес регистрации!")
    adr = await Adress.query.where(Adress.line == DICT["adress_reg"]).gino.first()
    if adr is None:
        ADR = await geocoder(DICT["adress_reg"])
        adr = await Adress.create(
            line=DICT["adress_reg"],
            fias=DICT["adress_reg_fias"],
            point=ADR["point"],
            text=ADR["text"],
            street=ADR["street"],
            house=ADR["house"],
        )
    # ==== получаем сведения о работе ====
    if DICT["work_adress"] not in (None, ""):
        work = await Work.query.where(Work.line == DICT["work_adress"]).gino.first()
        if work is None:
            WORK = await geocoder(DICT["work_adress"])
            work = await Work.create(
                line=DICT["work_adress"],
                name=DICT["work_name"],
                fias=DICT["work_adress_fias"],
                point=WORK["point"],
                text=WORK["text"],
            )
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
        time_SES=DICT["time_SES"],
        w_id=work.w_id if work is not None else None,
        date_diagnoz=DICT["date_diagnoz"],
        di_id=diag.di_id,
        lab_confirm=DICT["lab_confirm"],
    )
