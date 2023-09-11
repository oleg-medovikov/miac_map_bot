from .base import metadata

from sqlalchemy import (
    Table,
    Column,
    Integer,
    BigInteger,
    SmallInteger,
    DateTime,
    Date,
    String,
    Boolean,
)

t_case_semd = Table(
    "case_semd",
    metadata,
    Column(
        "meddoc_biz_key", BigInteger, primary_key=True
    ),  # дентификатор медицинского документа
    Column("d_id", Integer),  # порядковый номер врача
    Column("adress_reg_id", Integer),  # адрес регистрации пациента
    Column("date_sickness", Date),  # Дата заболевания
    Column("date_first_req", Date),  # Дата пенрвого обращения
    Column(
        "hospitalization_type", SmallInteger
    ),  # Вид случая госпитализации или обращения (первичный, повторный)
    Column(
        "primary_anti_epidemic_measures", String
    ),  # Проведенные первичные противоэпидемические мероприятия
    Column("time_SES", DateTime),  # Дата первичной сигнализации в СЭС
    Column("work_addres_id", Integer, nullable=True),  # адрес работы пациента
    Column(
        "work_name", String, nullable=True
    ),  # работа пациента наименование организации
    Column(
        "work_last_date", DateTime, nullable=True
    ),  # дата последнего посещения работы
    Column("diagnoz", String, nullable=True),  # установленный диагноз
    Column("MKB", String),  # MKB code
    Column("date_diagnoz", Date, nullable=True),  # дата диагноза
    Column("lab_confirm", Boolean),  # лабораторное потверждение
    Column("date_update", DateTime),  # дата создания строки
)
