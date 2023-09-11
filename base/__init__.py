from .base import metadata, database, engine
from .users import t_users
from .meddocs import t_meddocs
from .adress import t_adress
from .tokens import t_tokens
from .doctors import t_doctors
from .orgs import t_orgs
from .logi import t_logi

metadata.create_all(engine)


__all__ = [
    "metadata",
    "database",
    "engine",
    "t_users",
    "t_meddocs",
    "t_doctors",
    "t_orgs",
    "t_adress",
    "t_tokens",
    "t_logi",
]
