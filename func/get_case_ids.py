from datetime import date
import requests

from conf import REGIZ_TOKEN, REGIZ_URL
from clas import Org


class error(Exception):
    pass


def get_case_ids(START: date, END: date):
    "Вытаскиваем из базы номера документов"

    URL = (
        REGIZ_URL
        + f"?id=1270&args={START.strftime('%Y-%m-%d')}"
        + f",{END.strftime('%Y-%m-%d')}&auth={REGIZ_TOKEN}"
    )
    
    req = requests.get(URL)
    
    if req.status_code != 200:
        raise error('что-то не так с соединением')

    for _ in req.json():
