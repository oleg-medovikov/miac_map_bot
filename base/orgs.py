from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

t_orgs = Table(
    "orgs",
    metadata,
    Column("m_id", SmallInteger, primary_key=True),  # порядковый номер организации
    Column("case_level1_key", UUID),  # guid организации
    Column("short_name", String),  # короткое название организации
    Column("date_update", DateTime),  # дата добавления, изменения
)
