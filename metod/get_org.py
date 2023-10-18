from sqlalchemy import and_
from uuid import UUID

from models import Org


async def get_org(DICT: dict) -> "Org":
    "сравнить с существующими и создать уникальный"

    TEST = {
        "case_level1_key": UUID(DICT.get("case_organization_level1_key")),
        "short_name": DICT.get("case_organization_level1_short_name"),
    }
    org = await Org.query.where(
        and_(*[getattr(Org, key) == value for key, value in TEST.items()])
    ).gino.first()
    if org is None:
        org = await Org.create(**TEST)

    return org
