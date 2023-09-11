from .base import metadata

from sqlalchemy import (
    Table,
    Column,
    Integer,
    DateTime,
    String,
    BigInteger,
)

t_doctors = Table(
    "doctors",
    metadata,
    Column("d_id", Integer, primary_key=True),  # порядковый номер врача
    Column("org", String),  # наименование организации из СЭМДа
    Column("fio", String),  # ФИО врача
    Column("snils", BigInteger),  # идентификатор врача
    Column("spec", String),  # специальность врача
    Column("telefon", String, nullable=True),  # контактный номер
    Column("date_update", DateTime),  # дата добавления, изменения
)
