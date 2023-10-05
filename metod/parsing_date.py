from datetime import datetime, date
from typing import Optional


def parsing_date(string: Optional[str]) -> Optional["date"]:
    if string in ("", None):
        return None

    if len(string) == 8 and string.isdigit():
        return datetime.strptime(string, "%Y%m%d").date()

    if len(string) == 10:
        return datetime.strptime(string, "%Y-%m-%d").date()

    if "+" in string and "T" in string:
        return datetime.fromisoformat(string)
