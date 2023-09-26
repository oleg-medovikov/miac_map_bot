import requests
from datetime import datetime, timedelta


from conf import settings


def get_one_meddoc() -> str:
    "выгружаем одну историю болезни для примера"

    START = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    STOP = datetime.today().strftime("%Y-%m-%d")
    URL = (
        settings.REGIZ_URL
        + f"?id=1270&args={START},{STOP}"
        + f"&auth={settings.REGIZ_TOKEN}"
    )

    req = requests.get(URL)
    if req.status_code != 200:
        return "проблемы с подключением"

    return str(req.json()[0])
