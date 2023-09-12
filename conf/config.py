from os import getenv
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(dotenv_path=".conf")


@dataclass
class Settings:
    BOT_API: str
    DATABASE_URL: str
    REGIZ_AUTH: str
    REGIZ_URL: str
    REGIZ_TOKEN: str
    MASTER: str
    PROXY_URL: str


settings = Settings(
    BOT_API=getenv("BOT_API", default=""),
    DATABASE_URL=getenv("DATABASE_URL", default=""),
    REGIZ_AUTH=getenv("REGIZ_AUTH", default=""),
    REGIZ_URL=getenv("REGIZ_URL", default=""),
    REGIZ_TOKEN=getenv("REGIZ_TOKEN", default=""),
    MASTER=getenv("MASTER", default=""),
    PROXY_URL=getenv("PROXY_URL", default=""),
)
