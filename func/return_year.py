from datetime import timedelta, date


def return_year() -> tuple["date", "date"]:
    "Получение дат начала и конца в виде строк"
    return date.today() - timedelta(days=31), date.today()
