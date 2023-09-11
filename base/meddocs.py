from .base import metadata

from sqlalchemy import (
    Boolean,
    Table,
    Column,
    BigInteger,
    String,
    Date,
    SmallInteger,
)


t_meddocs = Table(
    "meddocs",
    metadata,
    Column(
        "meddoc_biz_key", BigInteger, primary_key=True
    ),  # дентификатор медицинского документа
    Column("creation_date", Date),  # дата создания документа
    Column("success_date", Date),  # дата успешной загрузки
    Column(
        "birthdate", Date, nullable=True
    ),  # дата рождения ребенка в ближайшем месяце
    Column("org_id", SmallInteger),  # id медицинской организации
    Column("history_number", String),  # номер истории болезни
    Column("doc_type_code", SmallInteger),  # код сэмда в системе
    Column("processed", Boolean),  # был ли обработан файл
    Column("error", Boolean),  # возникли ли ошибки при обработке
)
