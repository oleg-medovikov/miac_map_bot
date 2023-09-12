from os import getenv
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional

load_dotenv(dotenv_path='.conf')

@dataclass
class Settings:
    BOT_API: Optional[str]
    DATABASE_URL: Optional[str]
    REGIZ_AUTH: Optional[str]
    REGIZ_URL: Optional[str]
    REGIZ_TOKEN: Optional[str]
    MASTER: Optional[str]
    PROXY_URL: Optional[str]

settings = Settings(
    BOT_API=getenv('BOT_API'),
    DATABASE_URL=getenv('DATABASE_URL'),
    REGIZ_AUTH=getenv('REGIZ_AUTH'),
    REGIZ_URL=getenv('REGIZ_URL'),
    REGIZ_TOKEN=getenv('REGIZ_TOKEN'),
    MASTER=getenv('MASTER'),
    PROXY_URL=getenv('PROXY_URL'),
    )
