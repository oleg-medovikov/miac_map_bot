from .base import metadata

from sqlalchemy import Table, Column, Integer, String, Boolean, Date

t_tokens = Table(
    "tokens",
    metadata,
    Column("token", String, primary_key=True),
    Column("name", String),
    Column("end", Boolean),
    Column("end_date", Date),
    Column("count", Integer),
)
