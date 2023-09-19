from bs4 import BeautifulSoup
from datetime import datetime


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
    DICT = {}

    # ===== пробуем вытащить поле пациент ==========
    patient = soup.find("patient")
    if patient is not None:
        for _ in patient.find_all():
            code = _.get("code")
            codeSystem = _.get("codeSystem")
            displayName = _.get("displayName")

            if codeSystem == "1.2.643.5.1.13.13.11.1005":
                DICT["MKB"] = code
                DICT["diagnoz"] = displayName

    # ===== поиск адреса регистрации ========
    for addr in soup.find_all("addr"):
        print(addr)
        print("+++++++++++++")
        if return_attr(
            addr.find("address:Type"), "codeSystem"
        ) == "1.2.643.5.1.13.13.11.1504" and return_attr(
            addr.find("address:Type"), "code"
        ) in (
            "1",
            "2",
            "3",
        ):
            DICT["adress_reg"] = return_attr(addr.find("streetAddressLine"), "text")
            DICT["adress_reg_fias"] = return_attr(addr.find("fias:HOUSEGUID"), "text")
        # 4 код по этому справочнику  - место работы
        if (
            return_attr(addr.find("address:Type"), "codeSystem")
            == "1.2.643.5.1.13.13.11.1504"
            and return_attr(addr.find("address:Type"), "code") == "4"
        ):
            DICT["work_adress"] = return_attr(addr.find("streetAddressLine"), "text")
            DICT["work_adress_fias"] = return_attr(addr.find("fias:HOUSEGUID"), "text")

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

    # ==== разбираем даты ==========
    # отдельный способ разбирать даты
    for date in soup.find_all("effectiveTime"):
        parents = date.find_previous_siblings()
        print(date)
        for parent in parents:
            codeSystem = parent.get("codeSystem")
            code = parent.get("code")
            # ====== Дата заболевания ==========
            if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12144":
                DICT["date_sickness"] = return_attr(date, "value")
                continue
            # ==== Дата первичного обращения (выявления) ===
            if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12145":
                DICT["date_first_req"] = return_attr(date, "value")
                continue
            # Дата и час первичной сигнализации в СЭС
            if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "12149":
                DICT["time_SES"] = return_attr(date, "value")
                continue
            # Диагноз
            if codeSystem == "1.2.643.5.1.13.13.99.2.166" and code == "838":
                DICT["date_diagnoz"] = return_attr(date, "value")
                print(DICT["date_diagnoz"], "diagnoz")
                continue

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
                if DICT["diagnoz"] == "":
                    DICT["diagnoz"] = obs.value.get("displayName")
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
