from .base import metadata

from sqlalchemy import Table, Column, ARRAY, Float, Integer, String, Boolean

t_adress = Table(
    "adress",
    metadata,
    Column("line", String, primary_key=True),
    Column("point", ARRAY(Float)),
    Column("text", String),
    Column("street", String),
    Column("house", String),
    Column("flat", String),
    Column("index", Integer),
    Column("error", Boolean),
)
