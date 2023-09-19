import requests
import json
from sqlalchemy import true

from models import Token
from exept import NoTokenYandex


class error(Exception):
    pass


def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)
    return results


async def geocoder(ADR: str) -> dict:
    "Проверяем адрес с помощью геокодера яндекса"

    token = (
        await Token.query.where(Token.active == true())
        .order_by(Token.count)
        .gino.first()
    )
    if token is None:
        raise NoTokenYandex("нет токена для геокодера!")

    # ADR = "санкт-петербург " + ADR
    ADRESS = ADR.replace(" ", "+").replace("++", "")
    URL = (
        "https://geocode-maps.yandex.ru/1.x?format=json&lang=ru_RU"
        + "&kind=house&geocode="
        + ADRESS
        + "&apikey="
        + token.token
    )

    req = requests.get(URL)

    if req.status_code != 200:
        await token.update(active=False).apply()
        raise error("токен закончился\n" + req.text)

    await token.update(count=token.count + 1).apply()
    DATA = req.text

    DICT_KEYS = {
        "point": "Point",
        "CountryName": "CountryName",
        "text": "text",
        "sity": "AdministrativeAreaName",
        "street": "ThoroughfareName",
        "house": "PremiseNumber",
        "index": "PostalCodeNumber",
    }
    DICT = {}
    DICT["error"] = False
    for key, value in DICT_KEYS.items():
        try:
            DICT[key] = find_values(value, DATA)[0]
        except IndexError:
            if key == "index":
                DICT[key] = 0
            elif key == "point":
                DICT[key] = {"pos": "0 0"}
            else:
                DICT[key] = ""
            DICT["error"] = True

    if DICT["sity"] != "Санкт-Петербург":
        DICT["error"] = True
    if DICT["point"] is not None:
        DICT["point"] = [float(_) for _ in DICT["point"]["pos"].split(" ")]

    return DICT
